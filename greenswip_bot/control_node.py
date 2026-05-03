import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point, Twist

class ControlNode(Node):
    def __init__(self):
        super().__init__('control_node')
        self.sub = self.create_subscription(Point, '/target_data', self.control_callback, 10)
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Controller Gains (P-Controller)
        self.kp_steering = 0.005
        self.max_speed = 0.5
        self.stop_threshold = 100000.0 # Stopping area
        
        self.get_logger().info("Control Node: Ackermann Logic Active")

    def control_callback(self, data):
        cmd = Twist()
        
        if data.z == 1.0: # Target is found
            # Steering
            cmd.angular.z = self.kp_steering * data.x
            
            # Speed (Stop if close, move if far)
            if data.y > self.stop_threshold:
                cmd.linear.x = 0.0
                self.get_logger().info("Target Reached - Stopping.")
            else:
                cmd.linear.x = self.max_speed
        else:
            # Safety stop if vision loses target
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            
        self.pub.publish(cmd)

def main():
    rclpy.init()
    rclpy.spin(ControlNode())
    rclpy.shutdown()
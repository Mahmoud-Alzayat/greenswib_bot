# # import rclpy
# # from rclpy.node import Node
# # from sensor_msgs.msg import Image
# # from geometry_msgs.msg import Twist
# # from cv_bridge import CvBridge
# # import cv2
# # import numpy as np

# # class VisionNode(Node):
# #     def __init__(self):
# #         super().__init__('vision_node')
# #         # Control Parameters

# #         self.bridge = CvBridge()
        
# #         # Subscriber for the Gazebo camera topic
# #         self.subscription = self.create_subscription(
# #             Image,
# #             '/model/ackerman_robot/camera/image',
# #             self.image_callback,
# #             10)
            
# #         # Publisher for Ackermann control
# #         self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        
# #         # Control Parameters
# #         self.target_speed = 0.3  # m/s
# #         self.kp = 0.005          # Proportional gain for steering
        
# #         self.get_logger().info("Greenswip Vision Node started: Target = Box")

# #     def image_callback(self, msg):
# #         try:
# #             # Convert ROS Image to OpenCV format
# #             cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
# #             height, width, _ = cv_image.shape
# #             img_center_x = width // 2

# #             # 1. Pre-processing: Convert to Grayscale and Threshold
# #             gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
# #             blur = cv2.GaussianBlur(gray, (5, 5), 0)
            
# #             # Since shapes are black on light background, use Binary Inverse
# #             _, thresh = cv2.threshold(blur, 50, 255, cv2.THRESH_BINARY_INV)

# #             # 2. Find Contours
# #             contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
# #             target_found = False
# #             error_x = 0.0

# #             for cnt in contours:
# #                 # Filter out small noise
# #                 if cv2.contourArea(cnt) < 500:
# #                     continue

# #                 # 3. Shape Approximation
# #                 epsilon = 0.04 * cv2.arcLength(cnt, True)
# #                 approx = cv2.approxPolyDP(cnt, epsilon, True)

# #                 # Detection Logic: The Box (4 vertices + Square Aspect Ratio)
# #                 if len(approx) == 4:
# #                     x, y, w, h = cv2.boundingRect(approx)
# #                     aspect_ratio = float(w) / h
                    
# #                     # A box is roughly 1:1; capsules/cylinders are typically elongated
# #                     if 0.8 <= aspect_ratio <= 1.2:
# #                         target_found = True
# #                         box_center_x = x + (w // 2)
                        
# #                         # Calculate horizontal error
# #                         error_x = float(img_center_x - box_center_x)
                        
# #                         # Visualize detection
# #                         cv2.rectangle(cv_image, (x, y), (x + w, y + h), (0, 255, 0), 3)
# #                         cv2.circle(cv_image, (box_center_x, y + h // 2), 5, (255, 0, 0), -1)
# #                         break

# #             # 4. Control Logic
# #             self.target_speed = 0.5
# #             self.kp_steer = 1.5      # steering gain
# #             self.kp_speed = 0.8      # speed scaling
# #             self.stop_area_ratio = 0.20   # stop when box occupies 20% of image
# #             self.slow_area_ratio = 0.10   # start slowing down
# #             self.dead_zone = 0.05         # small error ignore

# #             cmd = Twist()
# #             if target_found:
# #                 # Proportional control for steering
# #                 cmd.linear.x = self.target_speed
# #                 cmd.angular.z = self.kp * error_x
# #                 self.get_logger().info(f"Targeting Box - Error: {error_x:.2f}")
# #             else:
# #                 # Stop if target is lost
# #                 cmd.linear.x = 0.0
# #                 cmd.angular.z = 0.0
# #                 self.get_logger().warn("Box not detected")

# #             self.publisher.publish(cmd)

# #             # Display the processed feed for debugging
# #             cv2.imshow("Robot Perspective", cv_image)
# #             cv2.waitKey(1)

# #         except Exception as e:
# #             self.get_logger().error(f"Vision Error: {e}")

# # def main(args=None):
# #     rclpy.init(args=args)
# #     node = VisionNode()
# #     try:
# #         rclpy.spin(node)
# #     except KeyboardInterrupt:
# #         pass
# #     finally:
# #         cv2.destroyAllWindows()
# #         node.destroy_node()
# #         rclpy.shutdown()

# # if __name__ == '__main__':
# #     main()


# # # Control Parameters
# # self.target_speed = 0.5
# # self.kp_steer = 1.5      # steering gain
# # self.kp_speed = 0.8      # speed scaling
# # self.stop_area_ratio = 0.20   # stop when box occupies 20% of image
# # self.slow_area_ratio = 0.10   # start slowing down
# # self.dead_zone = 0.05         # small error ignore

# import rclpy
# from rclpy.node import Node
# from sensor_msgs.msg import Image
# from geometry_msgs.msg import Twist
# from cv_bridge import CvBridge
# import cv2
# import numpy as np

# class VisionNode(Node):
#     def __init__(self):
#         super().__init__('vision_node')
        
#         self.bridge = CvBridge()
        
#         # Subscriber matching your corrected Gazebo topic path
#         self.subscription = self.create_subscription(
#             Image,
#             '/camera/image',
#             self.image_callback,
#             10)
            
#         self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        
#         # --- Control Parameters ---
#         self.kp_steering = 0.005   # Gain for steering
#         self.max_speed = 0.4       # m/s
        
#         # Distance Logic: We stop if the box occupies too much of the frame
#         # You may need to tune 'stop_area_threshold' based on your camera FOV
#         self.stop_area_threshold = 60000  # Pixels. Large area = robot is close.
#         self.min_area_threshold = 500     # Ignore noise
        
#         self.get_logger().info("Greenswip Vision Node Active: Tracking Square Box")

#     def image_callback(self, msg):
#         try:
#             cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
#             height, width, _ = cv_image.shape
#             img_center_x = width // 2

#             # 1. Image Processing
#             gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
#             blur = cv2.GaussianBlur(gray, (5, 5), 0)
#             _, thresh = cv2.threshold(blur, 50, 255, cv2.THRESH_BINARY_INV)

#             # 2. Contour Extraction
#             contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
#             target_found = False
#             error_x = 0.0
#             current_area = 0

#             for cnt in contours:
#                 area = cv2.contourArea(cnt)
#                 if area < self.min_area_threshold:
#                     continue

#                 # 3. Geometric Filtering (4 sides + Square Ratio)
#                 epsilon = 0.04 * cv2.arcLength(cnt, True)
#                 approx = cv2.approxPolyDP(cnt, epsilon, True)

#                 if len(approx) == 4:
#                     x, y, w, h = cv2.boundingRect(approx)
#                     aspect_ratio = float(w) / h
                    
#                     # Box detection (Square aspect ratio check)
#                     if 0.7 <= aspect_ratio <= 1.3:
#                         target_found = True
#                         current_area = area
#                         box_center_x = x + (w // 2)
                        
#                         # Error: Positive = Box is to the Right, Negative = Box is to the Left
#                         error_x = float(img_center_x - box_center_x)
                        
#                         # Visual Feedback
#                         color = (0, 255, 0) if area < self.stop_area_threshold else (0, 0, 255)
#                         cv2.rectangle(cv_image, (x, y), (x + w, y + h), color, 3)
#                         break

#             # 4. Control Command (Twist)
#             cmd = Twist()
            
#             if target_found:
#                 # Steering Logic: P-Controller
#                 # Angular Z = Kp * Error
#                 cmd.angular.z = self.kp_steering * error_x
                
#                 # Speed Logic: Move if far, Stop if close
#                 if current_area > self.stop_area_threshold:
#                     cmd.linear.x = 0.0
#                     self.get_logger().info(f"Target Reached! Area: {current_area}")
#                 else:
#                     cmd.linear.x = self.max_speed
#                     self.get_logger().info(f"Approaching - Error: {error_x:.1f}")
#             else:
#                 # Safety: Stop if we lose sight of the target
#                 cmd.linear.x = 0.0
#                 cmd.angular.z = 0.0
#                 self.get_logger().warn("Searching for Target Box...")

#             self.publisher.publish(cmd)
            
#             # Show debug window
#             cv2.imshow("Greenswip Bot View", cv_image)
#             cv2.waitKey(1)

#         except Exception as e:
#             self.get_logger().error(f"Vision Node Failure: {e}")

# def main(args=None):
#     rclpy.init(args=args)
#     node = VisionNode()
#     try:
#         rclpy.spin(node)
#     except KeyboardInterrupt:
#         pass
#     finally:
#         cv2.destroyAllWindows()
#         node.destroy_node()
#         rclpy.shutdown()

# if __name__ == '__main__':
#     main()

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point # x = error, y = area, z = 1 (found) or 0 (lost)
from cv_bridge import CvBridge
import cv2

class VisionNode(Node):
    def __init__(self):
        super().__init__('vision_node')
        self.bridge = CvBridge()
        self.sub = self.create_subscription(Image, '/camera/image', self.image_callback, 10)
        self.pub = self.create_publisher(Point, '/target_data', 10)
        self.get_logger().info("Vision Node: Feature Extraction Active")

    def image_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            height, width, _ = cv_image.shape
            img_center_x = width // 2

            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            _, thresh = cv2.threshold(blur, 50, 255, cv2.THRESH_BINARY_INV)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            target_msg = Point(x=0.0, y=0.0, z=0.0) # Default: Lost

            for cnt in contours:
                if cv2.contourArea(cnt) < 300: continue
                epsilon = 0.05 * cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, epsilon, True)

                if len(approx) == 4:
                    x, y, w, h = cv2.boundingRect(approx)
                    if 0.9 <= (float(w)/h) <= 1.8:
                        target_msg.x = float(img_center_x - (x + w // 2))
                        target_msg.y = float(cv2.contourArea(cnt))
                        target_msg.z = 1.0 # Target Found
                        cv2.rectangle(cv_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        break

            self.pub.publish(target_msg)
            cv2.imshow("Vision Processing", cv_image)
            cv2.waitKey(1)
        except Exception as e:
            self.get_logger().error(f"Vision error: {e}")

def main():
    rclpy.init()
    rclpy.spin(VisionNode())
    rclpy.shutdown()

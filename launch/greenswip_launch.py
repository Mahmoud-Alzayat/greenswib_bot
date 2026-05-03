import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('greenswip_bot')
    
    # 1. Paths to your files
    world_path = os.path.join(pkg_share, 'worlds', 'shapes.sdf')
    urdf_path = os.path.join(pkg_share, 'urdf', 'robot.urdf')

    # 2. Fix the "Missing Colors" issue 
    # This tells Gazebo where to find textures/materials inside your package
    resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=[os.path.join(pkg_share, 'worlds'), ':', os.path.join(pkg_share, 'urdf')]
    )

    # 3. Launch Gazebo Sim (Fortress/Ignition)
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]),
        launch_arguments={'gz_args': f'-r {world_path}'}.items(),
    )

    # 4. Spawn the Robot
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-file', urdf_path,
            '-name', 'ackerman_robot',
            '-x', '0', '-y', '0', '-z', '0.5'
        ],
        output='screen'
    )
    bridge = Node(
    package='ros_gz_bridge',
    executable='parameter_bridge',
    arguments=[
        # Gazebo -> ROS 2 (Camera)
        '/camera/image@sensor_msgs/msg/Image[ignition.msgs.Image',
        
        # ROS 2 -> Gazebo (Movement)
        '/cmd_vel@geometry_msgs/msg/Twist]ignition.msgs.Twist',
        
        # Gazebo -> ROS 2 (Telemetry)
        '/ackerman_robot/joint_state@sensor_msgs/msg/JointState[ignition.msgs.Model'
    ],
    output='screen'
    )
    control_node = Node(
        package='greenswip_bot',
        executable='control_node',
        output='screen'
    )
    vision_node = Node(
        package='greenswip_bot',
        executable='vision_node',
        output='screen'
    )
    return LaunchDescription([
        resource_path,
        gazebo,
        spawn_robot,
        bridge,
        control_node,
        vision_node
    ])
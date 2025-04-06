import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    package_dir = get_package_share_directory("ros2_first_test")
    urdf = os.path.join(package_dir, "urdf", "first_robot.urdf")

    return LaunchDescription([

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            arguments=[urdf]),

        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            arguments=[urdf]),
            
        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2"),
    ])
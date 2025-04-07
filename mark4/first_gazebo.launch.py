import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from launch.substitutions import LaunchConfiguration

def generate_launch_description():

    package_dir = get_package_share_directory("ros2_first_test")
    urdf = os.path.join(package_dir, "urdf" , "first_robot.urdf")
    rviz = os.path.join(package_dir, "rviz" , "first_robot.rviz")
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    return LaunchDescription([

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            arguments=[urdf],
            ),

        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            arguments=[urdf],
            ),
            
        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            arguments=["-d", rviz]
            ),
        
        # gazebo settings
        ExecuteProcess(
            cmd=[
                'gazebo',
                '--verbose',
                '/usr/share/gazebo-11/worlds/empty.world',
                '-s', 'libgazebo_ros_factory.so'
            ],
            output='screen'
        ),

        Node(
            package="gazebo_ros",
            executable="spawn_entity.py",
            name="urdf_spawner",
            parameters=[{'use_sim_time': use_sim_time}],
            arguments=["-topic", "/robot_description", "-entity", "first_robot"]),
    ])
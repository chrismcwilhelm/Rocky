from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='rocky',
            executable='gait_controller',
            name='gait_controller',
            output='screen'
        ),

        Node(
            package='rocky',
            executable='inverse_kinematics',
            name='inverse_kinematics',
            output='screen'
        ),

        Node(
            package='rocky',
            executable='angle_mapper',
            name='angle_mapper',
            output='screen'
        ),

        Node(
            package='rocky',
            executable='serial_bridge',
            name='serial_bridge',
            output='screen'
        ),
    ])
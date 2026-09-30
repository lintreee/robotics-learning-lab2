from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    timeout_argument = DeclareLaunchArgument(
        "command_timeout_sec",
        default_value="0.5",
        description="收到最后一条速度命令后，等待多少秒停车",
    )

    simulator = Node(
        package="mobile_robot_sim",
        executable="mobile_robot_simulator",
        name="mobile_robot_simulator",
        output="screen",
        parameters=[
            {
                "command_timeout_sec": ParameterValue(
                    LaunchConfiguration("command_timeout_sec"),
                    value_type=float,
                )
            }
        ],
    )

    return LaunchDescription([timeout_argument, simulator])
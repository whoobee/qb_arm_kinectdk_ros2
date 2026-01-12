from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
import os

def generate_launch_description():
    ld = LaunchDescription()

    # Path to your RViz config
    rviz_config_path = os.path.join(
        os.getenv("HOME"),
        "ros2_ws",
        "src",
        "Azure_Kinect_ROS2_Driver",
        "rviz",
        "azure_k4a.rviz"
    )

    k4a_node = Node(
        package="azure_kinect_ros2_driver",
        executable="azure_kinect_node",
        name="k4a_ros2_node",
        output="screen",
        emulate_tty=True,
        parameters=[
            {"depth_enabled": True},
            {"color_enabled": True},
            {"color_resolution": "720P"},         # Wide view mode
            {"depth_mode": "WFOV_2X2BINNED"},     # Wide Field of View (binned for performance)
            {"fps": 30},
            {"point_cloud": True},
            {"rgb_point_cloud": True},
            {"point_cloud_in_depth_frame": True}
        ]
    )

    # RViz2 launch
    rviz_node = ExecuteProcess(
        cmd=["rviz2", "-d", rviz_config_path],
        output="screen"
    )

    ld.add_action(k4a_node)
    ld.add_action(rviz_node)
    return ld

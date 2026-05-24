from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    
    # 1. Bridge for Camera (Color, Depth, and Infos)
    # Combining these into one bridge node for efficiency
    camera_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='camera_bridge',
        arguments=[
            '/world/world_demo/model/tugbot/link/camera_front/sensor/color/image@sensor_msgs/msg/Image[ignition.msgs.Image',
            '/world/world_demo/model/tugbot/link/camera_front/sensor/color/camera_info@sensor_msgs/msg/CameraInfo[ignition.msgs.CameraInfo',
            '/world/world_demo/model/tugbot/link/camera_front/sensor/depth/depth_image@sensor_msgs/msg/Image[ignition.msgs.Image',
            '/world/world_demo/model/tugbot/link/camera_front/sensor/depth/camera_info@sensor_msgs/msg/CameraInfo[ignition.msgs.CameraInfo'
        ],
        output='screen'
    )

    # 2. Bridge for IMU
    imu_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='imu_bridge',
        arguments=[
            '/world/world_demo/model/tugbot/link/imu_link/sensor/imu/imu@sensor_msgs/msg/Imu[ignition.msgs.IMU'
        ],
        output='screen'
    )

    # 3. Static TF Publisher (Base to Camera)
    # Using new-style arguments --x --y --z etc to avoid the "Deprecated" warning
    static_tf_pub = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='base_link_to_camera_bridge',
        arguments=['--x', '0.2', '--y', '0', '--z', '0.1', 
                   '--yaw', '0', '--pitch', '0', '--roll', '-1.57', 
                   '--frame-id', 'tugbot', 
                   '--child-frame-id', 'tugbot/camera_front/color'],
        output='screen'
    )

    return LaunchDescription([
        camera_bridge,
        imu_bridge,
        static_tf_pub
    ])
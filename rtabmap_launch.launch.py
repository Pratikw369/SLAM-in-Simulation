import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # Use the base link of your robot in Gazebo
    # Based on your topics, 'tugbot' is the model name
    frame_id = 'tugbot' 
    
    parameters=[{
          'frame_id': frame_id,
          'subscribe_depth': True,
          'subscribe_odom_info': True,
          'approx_sync': True, # Gazebo sensors often require approx sync
          'wait_imu_to_init': True,
          'use_sim_time': True }]

    # Updated remappings to match your Gazebo topics
    remappings=[
          ('imu', '/world/world_demo/model/tugbot/link/imu_link/sensor/imu/imu'),
          ('rgb/image', '/world/world_demo/model/tugbot/link/camera_front/sensor/color/image'),
          ('rgb/camera_info', '/world/world_demo/model/tugbot/link/camera_front/sensor/color/camera_info'),
          ('depth/image', '/world/world_demo/model/tugbot/link/camera_front/sensor/depth/depth_image')]

    return LaunchDescription([

        DeclareLaunchArgument(
            'args', default_value='',
            description='Extra arguments set to rtabmap and odometry nodes.'),
        
        DeclareLaunchArgument(
            'odom_args', default_value='',
            description='Extra arguments just for odometry node.'),

        # RGBD Odometry
        Node(
            package='rtabmap_odom', executable='rgbd_odometry', output='screen',
            parameters=parameters,
            arguments=[LaunchConfiguration("args"), LaunchConfiguration("odom_args")],
            remappings=remappings),

        # RTAB-Map SLAM Node
        Node(
            package='rtabmap_slam', executable='rtabmap', output='screen',
            parameters=parameters,
            remappings=remappings,
            arguments=['-d', LaunchConfiguration("args")]), # -d deletes database on start

        # Visualization
        Node(
            package='rtabmap_viz', executable='rtabmap_viz', output='screen',
            parameters=parameters,
            remappings=remappings),
                
        # IMU Filter (Madgwick) to process raw Gazebo IMU data
        Node(
            package='imu_filter_madgwick', executable='imu_filter_madgwick_node', output='screen',
            parameters=[{'use_mag': False, 
                         'world_frame': 'enu', 
                         'publish_tf': False,
                         'use_sim_time': True}],
            remappings=[('imu/data_raw', '/world/world_demo/model/tugbot/link/imu_link/sensor/imu/imu'),
                        ('imu/data', '/imu/data')]),
    ])

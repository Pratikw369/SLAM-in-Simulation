# SLAM in Simulation
## YouTube Video :
[![Watch the video](https://img.youtube.com/vi/VdxL7b3bdSE/maxresdefault.jpg)](https://youtu.be/VdxL7b3bdSE)
▶️ [Click here to watch the video tutorial](https://youtu.be/VdxL7b3bdSE?si=wgY4gMhp5AmbHH7J)
## 
This repository provides ROS 2 launch configurations for running Simultaneous Localization and Mapping (SLAM) with RTAB-Map in a Gazebo simulation. It includes the necessary launch files to bridge sensor data from a simulated robot to ROS 2 and execute the SLAM pipeline.

## Prerequisites
Ensure the following are installed on your system. This project has been tested on Ubuntu with ROS 2 Humble.

*   **ROS 2 Humble Hawksbill:** [Installation Guide](https://docs.ros.org/en/humble/Installation.html)
*   **Gazebo Simulator:** Ignition/Gazebo Garden is recommended.
*   **ROS 2 Gazebo Bridge:** The `ros-humble-ros-gz` package.
*   **RTAB-Map for ROS 2:** `ros-humble-rtabmap-ros`
*   **IMU Filter:** `ros-humble-imu-filter-madgwick`

## Installation

1.  **Install System Dependencies**

    Open a terminal and install the required ROS 2 packages:
    ```bash
    sudo apt update
    sudo apt install ros-humble-rtabmap-ros ros-humble-imu-filter-madgwick
    ```

2.  **Set Up ROS 2 Workspace**

    Clone this repository into the `src` directory of your ROS 2 workspace, build the package, and source the environment.
    ```bash
    # Navigate to your workspace source directory
    cd ~/ros2_ws/src
    
    # Clone the repository
    git clone https://github.com/Pratikw369/SLAM-in-Simulation.git
    
    # Go back to the workspace root, build, and source
    cd ~/ros2_ws
    colcon build --packages-select SLAM-in-Simulation
    source install/setup.bash
    ```

## Usage

These launch files are configured for a `tugbot` model in a Gazebo world. You must have a running simulation that provides the necessary sensor topics before proceeding.

1.  **Run your Gazebo Simulation**

    Start your Gazebo simulation environment with the robot model. This step is not covered by this repository and is a prerequisite.

2.  **Launch the Gazebo-ROS Bridge**

    In a new terminal, run the bridge launch file. This node translates Gazebo topic messages (Ignition Transport) into ROS 2 messages. It bridges RGB/Depth camera streams and IMU data.

    ```bash
    ros2 launch SLAM-in-Simulation bridge.launch.py
    ```

3.  **Launch RTAB-Map SLAM**

    In another terminal, start the RTAB-Map SLAM process. This will launch the odometry, mapping, and visualization nodes, which will start building a map as the robot moves in the simulation.

    ```bash
    ros2 launch SLAM-in-Simulation rtabmap_launch.launch.py
    ```
    You should now see the RTAB-Map GUI, which will display the generated map, odometry, and camera feeds.

## Launch File Descriptions

*   ### `bridge.launch.py`
    This file launches the `ros_gz_bridge` to connect Gazebo with ROS 2. It is configured to:
    *   Bridge the color image, depth image, and their corresponding camera info topics.
    *   Bridge the IMU sensor data.
    *   Publish a static transform from the robot's base frame (`tugbot`) to the camera frame (`tugbot/camera_front/color`).

*   ### `rtabmap_launch.launch.py`
    This is the primary launch file for running the SLAM system. It starts the following nodes:
    *   **`rgbd_odometry`**: Computes the robot's motion by tracking visual features between consecutive frames.
    *   **`rtabmap`**: The main SLAM node that performs loop closure detection and builds the map graph.
    *   **`rtabmap_viz`**: A visualization tool that displays the map, robot trajectory, and other debug information.
    *   **`imu_filter_madgwick_node`**: Processes raw IMU data from the simulation to provide a filtered orientation estimate.
    All nodes are configured with `use_sim_time:=True`, which is essential for working with simulation data.

*   ### `rtab_original.launch.py`
    This file is a reference launch configuration and is not intended for primary use.

## Customization
The launch files are hardcoded for a robot named `tugbot` within a `world_demo` world. If you are using a different robot or world, you will need to update the topic names and frame IDs in `bridge.launch.py` and `rtabmap_launch.launch.py` to match your simulation setup.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

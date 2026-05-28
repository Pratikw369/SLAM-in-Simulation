SLAM in Simulation
This repository provides the launch configuration for running SLAM (Simultaneous Localization and Mapping) within a Gazebo simulation environment. It bridges Gazebo simulation data to ROS 2 Humble and utilizes the RTAB-Map library to generate maps from depth and RGB image streams.

Prerequisites
Ensure you have the following installed on your system (tested on Ubuntu with ROS 2 Humble):

ROS 2 Humble Hawksbill

Gazebo (Ignition/Garden/Fortress depending on your installation)

ros_gz (for the Gazebo-ROS bridge)

RTAB-Map ROS 2 (ros-humble-rtabmap-ros)

Setup Instructions
1. Install Dependencies
Make sure you have the RTAB-Map package installed in your ROS 2 workspace:

Bash
sudo apt update
sudo apt install ros-humble-rtabmap-ros
2. Workspace Setup
Clone this repository into the src folder of your ROS 2 workspace:

Bash
cd ~/ros2_ws/src
git clone https://github.com/Pratikw369/SLAM-in-Simulation.git
cd ..
colcon build
source install/setup.bash
Usage
This project utilizes a bridge to connect Gazebo simulation topics to the ROS 2 ecosystem.

Launching the Simulation Bridge
Start the bridge to ensure Gazebo sensor data (depth images and camera streams) is published to the ROS 2 network:

Bash
ros2 launch SLAM-in-Simulation bridge.launch.py
Running RTAB-Map SLAM
Once the bridge is active and publishing data, launch the RTAB-Map node to begin mapping:

Bash
ros2 launch SLAM-in-Simulation rtabmap_launch.launch.py
Note: Ensure your simulation environment is running and that your camera topics are correctly remapped in the launch files if you are using custom sensor names.

Repository Structure
bridge.launch.py: Configures the connection between Gazebo and ROS 2.

rtabmap_launch.launch.py: Primary launch file for RTAB-Map SLAM node configuration.

rtab_original.launch.py: Reference launch configuration.

Contributing
Feel free to fork this repository and submit pull requests for improvements in mapping accuracy or bridge configuration.

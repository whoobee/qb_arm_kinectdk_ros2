# Azure Kinect ROS Driver (qb_arm fork, ROS 2 Jazzy)

Fork of Microsoft's [Azure_Kinect_ROS_Driver](https://github.com/microsoft/Azure_Kinect_ROS_Driver) `humble` branch
(upstream commit `6ffb95a`), patched to build and launch on **ROS 2 Jazzy / Ubuntu 24.04**:

- `cv_bridge/cv_bridge.h` -> `cv_bridge/cv_bridge.hpp` (the `.h` header is gone in Jazzy)
- the node is installed to `lib/azure_kinect_ros_driver/` so `ros2 launch` / `ros2 run` find it
  (upstream installed it to `bin/`, which is why `driver.launch.py` failed)

Upstream CI configs (`.github/`, `azure-pipelines.yml`) are not included.

## Installing the Sensor SDK on Ubuntu 24.04

Microsoft only ships the SDK for 18.04, but its packages work on 24.04
(based on [this guide](https://gist.github.com/jlblancoc/ae2a082b0ed5af2e71645b04b7207210)):

```bash
wget https://packages.microsoft.com/ubuntu/18.04/prod/pool/main/libk/libk4a1.4/libk4a1.4_1.4.1_amd64.deb
wget https://packages.microsoft.com/ubuntu/18.04/prod/pool/main/libk/libk4a1.4-dev/libk4a1.4-dev_1.4.1_amd64.deb
# libk4a1.4 asks you to accept Microsoft's EULA (or pre-accept it with ACCEPT_EULA=Y)
sudo apt install ./libk4a1.4_1.4.1_amd64.deb ./libk4a1.4-dev_1.4.1_amd64.deb

# udev rule so the camera works without root, then re-plug the camera
curl -sL https://raw.githubusercontent.com/microsoft/Azure-Kinect-Sensor-SDK/develop/scripts/99-k4a.rules \
  | sudo tee /etc/udev/rules.d/99-k4a.rules
sudo udevadm control --reload-rules
```

`k4a-tools` (k4aviewer) is not installable on 24.04 (needs `libsoundio1`) and isn't needed for ROS.

## Building and running

```bash
rosdep install --from-paths src --ignore-src -y --skip-keys K4A   # K4A = the SDK installed above
colcon build --packages-select azure_kinect_ros_driver
ros2 launch azure_kinect_ros_driver driver.launch.py depth_mode:=NFOV_UNBINNED fps:=30
```

Note: the launch file's default `depth_mode` (`WFOV_UNBINNED`) only supports up to 15 fps; with `fps:=30`
use `NFOV_UNBINNED` or a binned mode, or the node aborts.

---

This project is a node which publishes sensor data from the [Azure Kinect Developer Kit](https://azure.microsoft.com/en-us/services/kinect-dk/) to the [Robot Operating System (ROS)](http://www.ros.org/). Developers working with ROS can use this node to connect an Azure Kinect Developer Kit to an existing ROS installation.

This repository uses the [Azure Kinect Sensor SDK](https://github.com/microsoft/Azure-Kinect-Sensor-SDK) to communicate with the Azure Kinect DK. It supports both Linux and Windows installations of ROS.

[![Build Status](https://dev.azure.com/ms/Azure_Kinect_ROS_Driver/_apis/build/status/microsoft.Azure_Kinect_ROS_Driver?branchName=melodic)](https://dev.azure.com/ms/Azure_Kinect_ROS_Driver/_build/latest?definitionId=166&branchName=melodic)

## Features

This ROS node outputs a variety of sensor data, including:

- A PointCloud2, optionally colored using the color camera
- Raw color, depth and infrared Images, including CameraInfo messages containing calibration information
- Rectified depth Images in the color camera resolution
- Rectified color Images in the depth camera resolution
- The IMU sensor stream
- A TF2 model representing the extrinsic calibration of the camera

The camera is fully configurable using a variety of options which can be specified in ROS launch files or on the command line.

However, this node does ***not*** expose all the sensor data from the Azure Kinect Developer Kit hardware. It does not provide access to:

- Microphone array

For more information about how to use the node, please see the [usage guide](docs/usage.md).

## Status

This code is provided as a starting point for using the Azure Kinect Developer Kit with ROS. Community developed features are welcome.

For information on how to contribute, please see our [contributing guide](CONTRIBUTING.md).

## Building

The Azure Kinect ROS Driver uses colcon to build. For instructions on how to build the project please see the 
[building guide](docs/building.md).

## Join Our Developer Program

Complete your developer profile [here](https://aka.ms/iwantmr) to get connected with our Mixed Reality Developer Program. You will receive the latest on our developer tools, events, and early access offers.

## Code of Conduct

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Reporting Security Issues
Security issues and bugs should be reported privately, via email, to the
Microsoft Security Response Center (MSRC) at <[secure@microsoft.com](mailto:secure@microsoft.com)>.
You should receive a response within 24 hours. If for some reason you do not, please follow up via
email to ensure we received your original message. Further information, including the
[MSRC PGP](https://technet.microsoft.com/en-us/security/dn606155) key, can be found in the
[Security TechCenter](https://technet.microsoft.com/en-us/security/default).

## License

[MIT License](LICENSE)

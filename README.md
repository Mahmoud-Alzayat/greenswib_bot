# Greenswip Bot: Autonomous Ackermann Navigation

## 📝 Project Description
**Greenswip Bot** is an autonomous robotic system developed for real-time target detection and tracking within the **Gazebo Fortress** (Ignition) simulation environment. The project features a robot utilizing **Ackermann steering kinematics**, reflecting the mechanical design of automotive systems and high-performance racing platforms.

The core architecture follows a modular **ROS 2** design, strictly separating perception from actuation to ensure high-frequency execution and independent optimization of the vision and control loops.

---

## 🏗️ System Architecture
The system follows a modular "Sense-Think-Act" pipeline. Data flows between the Gazebo simulation and the ROS 2 environment via the `ros_gz_bridge`.

### Data Flow Diagram
1. **Perception Layer**: 
   - **Gazebo** publishes raw RGB data to `/camera/image`.
   - **vision_node** subscribes to this image, performs contour analysis, and identifies the target box.
   - **Output**: A custom telemetry signal (error offset and area) published to `/target_data`.

2. **Control Layer**:
   - **control_node** subscribes to `/target_data`.
   - It applies a Proportional (P) controller to calculate the required steering angle and linear velocity.
   - **Output**: Navigation commands published to `/cmd_vel`.

3. **Actuation Layer**:
   - The **Bridge** transfers `/cmd_vel` back to the Gazebo environment to drive the robot's wheels and steering rack.

---

## 🎥 Video Demonstrations
Check out the Greenswip Bot in action through the following trials:

*   **General Performance Trial**: [Watch the Video Here](https://drive.google.com/file/d/1poUfQ2tbjKLV87wFeZ1kKnUkUhAStV67/view?usp=sharing) - *Demonstration of basic target acquisition and following.*

---

## 🚀 Getting Started

### Prerequisites
*   **OS:** Ubuntu 22.04 LTS
*   **Middleware:** ROS 2 Humble Hawksbill
*   **Simulator:** Gazebo Fortress
*   **Key Libraries:** `cv_bridge`, `opencv-python`, `ros_gz_bridge`

### Installation
1.  **Clone the repository** into your ROS 2 workspace:
    ```bash
    cd ~/your_ws/src
    git clone [https://github.com/Mahmoud-Alzayat/greenswip_bot.git](https://github.com/Mahmoud-Alzayat/greenswip_bot.git)
    ```
2.  **Build the package**:
    ```bash
    cd ~/your_ws
    colcon build --packages-select greenswip_bot
    source install/setup.bash

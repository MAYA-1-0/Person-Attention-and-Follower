# Person Attention and Follower

Usage and Requirements:

* Built and deployed on Nvidia Jetson nano (Ubuntu 18.04 image) with Intel Realsense 
* Requires ROS melodic, Realsense SDK, Opencv, Python3.x.x, numpy.

1. Clone this repository
2. Pull Docker image for dynamixel motors control of base Refer this [Repository](https://github.com/MAYA-1-0/KInematics_And_Odometry) for detailed guide.
3. Make sure you've cloned dynamixel workbench messages to the same ROS workspace as mentioned [here](https://github.com/MAYA-1-0/KInematics_And_Odometry)
4. Once all the wheel controllers are up runnning, Run the following ROS nodes.
```
rosrun stereo_vision 
```
```
rosrun stereo_vision 
```



Agent tracking and attention model involves detection of the desired person in the cluttered environment and maintaining eye contact during the process of interaction.


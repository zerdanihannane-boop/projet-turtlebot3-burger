PROJET TURTLEBOT3 BURGER - COMMANDES DE LANCEMENT

Terminal 1 : lancer la simulation TurtleBot3

source /opt/ros/jazzy/setup.bash
cd ~/tp2_ws
source install/setup.bash

export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py


Terminal 2 : lancer le bridge ROS2-Gazebo

source /opt/ros/jazzy/setup.bash
cd ~/tp2_ws
source install/setup.bash

ros2 run ros_gz_bridge parameter_bridge /cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist /scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan


Terminal 3 : lancer le noeud d'evitement d'obstacles

source /opt/ros/jazzy/setup.bash
cd ~/tp2_ws
colcon build --packages-select mon_evitement
source install/setup.bash

ros2 run mon_evitement evitement_node


En cas de probleme :

pkill -9 gz
pkill -9 ruby
pkill -9 _ros2_node
ros2 daemon stop
ros2 daemon start

## a．
  ```
  mkdir -p ~/ramen_ws/src
  ```
  ```
  cd ~/ramen_ws/src
  ```
   
  ```
ros2 pkg create --build-type ament_python --node-name men_node men
  ```
  ```
ros2 pkg create --build-type ament_python men
  ```

  ```
colcon build && source install/setup.bash && source /opt/ros/foxy/setup.bash
  ```
  ```
ros2 run hello hello_node
  ```

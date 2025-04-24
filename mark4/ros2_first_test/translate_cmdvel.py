import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class first_robot_cmdvel(Node):
    def __init__(self):
        # wake up node name
        super().__init__("first_robot_cmdvel")
        # declare publisher
        self.publisher = self.create_publisher(Twist, "/first_robot/cmd_vel", 10)
        # period publisher
        timer_period = 1
        self.timer = self.create_timer(timer_period, self.send_cmd_vel)
        # creating a message object to fit new velocities and publish them
        self.velocity = Twist()

        self.linear_x = 0.3
        self.linear_y = 0.0
        self.linear_z = 0.0
        self.angle_x = 0.0
        self.angle_y = 0.0
        self.angle_z = 0.0

    def send_cmd_vel(self):
        # setting linear velocity
        self.velocity.linear.x = self.linear_x
        self.velocity.linear.y = self.linear_y
        self.velocity.linear.z = self.linear_z
        self.velocity.angular.x = self.angle_x
        self.velocity.angular.y = self.angle_y
        self.velocity.angular.z = self.angle_z
        self.publisher.publish(self.velocity)


def main(args=None):
    rclpy.init(args=args)
    frc = first_robot_cmdvel()
    rclpy.spin(frc)
    rclpy.shutdown()

if __name__ == "__main__":
    main()


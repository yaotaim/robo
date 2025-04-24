import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu

class get_imu(Node):
    def __init__(self):
        # wake up node name
        super().__init__("get_imu_node")
        # declare subscriber
        self.subscription = self.create_subscription(Imu, "/first_robot/imu", self.get_scan_imu, 10)
        self.subscription

    def get_scan_imu(self, scan_data):
        print(scan_data)

def main(args=None):
    rclpy.init(args=args)
    gi = get_imu()
    rclpy.spin_once(gi)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
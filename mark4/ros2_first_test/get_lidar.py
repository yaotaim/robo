import rclpy 
from rclpy.node import Node 
from sensor_msgs.msg import LaserScan

class getLidar(Node):
    def __init__(self):
        # wake up node name
        super().__init__("lidar_subscriber")
        self.subscription = self.create_subscription(LaserScan, "/scan", self.get_scan_values, 10)
        self.subscription

    def get_scan_values(self, scan_data):
        print(scan_data)

def main(args=None):
    rclpy.init(args=args)
    gl = getLidar()
    rclpy.spin_once(gl)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
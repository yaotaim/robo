import rclpy 
import cv2 
from rclpy.node import Node 
from cv_bridge import CvBridge 
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist

class getVideoFrame(Node):
    def __init__(self):
        # wake up node name
        super().__init__("video_subscriber")
        # declare subscriber
        self.subscription = self.create_subscription(Image, "/camera1/image_raw", self.get_camera_data, 10)
        self.publisher = self.create_publisher(Twist, "/first_robot/cmd_vel", 10)
        # period publisher
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.send_cmd_vel)
        # setting cv2
        self.bridge = CvBridge()
        self.velocity = Twist()

    def get_camera_data(self, data):
        # separate scan data
        frame = self.bridge.imgmsg_to_cv2(data)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        image = image[:600, :]
        image = cv2.inRange(image, 0, 100)
        # 輪郭抽出
        contours, _ = cv2.findContours(image,
                                       cv2.RETR_LIST,
                                       cv2.CHAIN_APPROX_NONE)
        if len(contours) > 0:
            contour = max(contours, key=lambda x: cv2.contourArea(x))
            self.x, self.y, _, _ = cv2.boundingRect(contour)
        else:
            contour = contours
            self.x, self.y = -1, -1
        frame = cv2.drawContours(frame, contour, -1, (0, 255, 0), 5)
        # show frame
        cv2.imshow("Gazebo-camera1", frame)
        cv2.waitKey(1)

    def send_cmd_vel(self):
        if 400 >= self.x >= 0:
            self.velocity.angular.z = -1.0
        elif 800 >= self.x >= 400:
            self.velocity.angular.z = 1.0
        else:
            self.velocity.angular.z = 0.0

        self.publisher.publish(self.velocity)

def main(args=None):
    rclpy.init(args=args)
    gVF = getVideoFrame()
    rclpy.spin(gVF)
    rclpy.shutdown()

if __name__ == "__main__":
    main()


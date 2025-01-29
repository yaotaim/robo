import math
import sys
import time
import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf_transformations import euler_from_quaternion

class HappyMove(Node):
    def __init__(self):
        super().__init__('happy_move_node')
        self.pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.sub = self.create_subscription(Odometry, 'odom', self.odom_cb, 10)
        self.timer = self.create_timer(0.01, self.timer_callback)

        self.x, self.y, self.yaw = 0.0, 0.0, 0.0  # 現在位置
        self.x0, self.y0, self.yaw0 = 0.0, 0.0, 0.0  # 初期位置
        self.vel = Twist()
        self.set_vel(0.0, 0.0)

    def get_pose(self, msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        (_, _, yaw) = euler_from_quaternion((q.x, q.y, q.z, q.w))
        return x, y, yaw

    def odom_cb(self, msg):
        self.x, self.y, self.yaw = self.get_pose(msg)

    def set_vel(self, linear, angular):
        self.vel.linear.x = linear
        self.vel.angular.z = angular

    def move_distance(self, dist):
        error = 0.01
        diff = dist - math.sqrt((self.x - self.x0) ** 2 + (self.y - self.y0) ** 2)
        if math.fabs(diff) > error:
            self.set_vel(0.20, 0.0)
            return False
        else:
            self.set_vel(0.0, 0.0)
            return True

    def rotate_angle(self, angle):
        error = 0.05
        diff = self.yaw - self.yaw0
        diff = math.atan2(math.sin(diff), math.cos(diff))  # -π ~ π に正規化
        target_angle = angle

        angle_error = abs(target_angle - diff)
        if angle_error > math.pi:
            angle_error = 2 * math.pi - angle_error

        if angle_error > error:
            self.set_vel(0.0, 0.25 if target_angle > diff else -0.25)
            return False
        else:
            self.set_vel(0.0, 0.0)
            return True

    def draw_half_circle(self, r, clockwise=True):
        linear_speed = 0.2
        angular_speed = (linear_speed / r) * (-1 if clockwise else 1)
        duration = 0.01
        steps = int((math.pi * r) / (linear_speed * duration))

        for _ in range(steps):
            self.set_vel(linear_speed, angular_speed)
            rclpy.spin_once(self)
            time.sleep(duration)

        self.set_vel(0.0, 0.0)
        rclpy.spin_once(self)
        return True

    def draw_heart(self):
        # 1. 時計回りに 45 度回転
        while not self.rotate_angle(math.pi / 4):
            rclpy.spin_once(self)
        self.yaw0 = self.yaw

        # 2. 2√2 移動
        while not self.move_distance(2.0 * math.sqrt(2)):
            rclpy.spin_once(self)
        self.x0, self.y0 = self.x, self.y

        # 3. 反時計回りに 45 度回転
        while not self.rotate_angle(-math.pi / 4):
            rclpy.spin_once(self)
        self.yaw0 = self.yaw

        # 4. 半径 1 の半円（時計回り）
        self.draw_half_circle(1, clockwise=True)
        self.yaw0 = self.yaw
        self.x0, self.y0 = self.x, self.y

        # 5. 90 度回転（反時計回り）
        while not self.rotate_angle(-math.pi / 2):
            rclpy.spin_once(self)
        self.yaw0 = self.yaw

        # 6. 90 度回転（反時計回り）
        while not self.rotate_angle(-math.pi / 2):
            rclpy.spin_once(self)
        self.yaw0 = self.yaw

        # 7. 半径 1 の半円（時計回り）
        self.draw_half_circle(1, clockwise=True)
        self.yaw0 = self.yaw
        self.x0, self.y0 = self.x, self.y

        # 8. 45 度回転（反時計回り）
        while not self.rotate_angle(-math.pi / 4):
            rclpy.spin_once(self)
        self.yaw0 = self.yaw

        # 9. 2√2 移動（ゴール）
        while not self.move_distance(2.0 * math.sqrt(2)):
            rclpy.spin_once(self)
        self.x0, self.y0 = self.x, self.y

    def timer_callback(self):
        self.pub.publish(self.vel)

def main(args=None):
    rclpy.init(args=args)
    node = HappyMove()

    try:
        print("Drawing heart...")
        node.draw_heart()
    except KeyboardInterrupt:
        print('Ctrl+C detected, shutting down...')
    except ExternalShutdownException:
        sys.exit(1)
    finally:
        rclpy.try_shutdown()

import math
import sys
import time
import rclpy
import tf_transformations
from rclpy.node import Node   
from rclpy.executors import ExternalShutdownException   
from geometry_msgs.msg import Twist  
from nav_msgs.msg import Odometry    
from tf_transformations import euler_from_quaternion 


class HappyMove(Node):  
    def __init__(self):   
        super().__init__('happy_move_node2')        
        self.pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.sub = self.create_subscription(Odometry, 'odom', self.odom_cb, 10)   
        self.timer = self.create_timer(0.01, self.timer_callback)
        self.x, self.y, self.yaw = 0.0, 0.0, 0.0
        self.x0, self.y0, self.yaw0 = 0.0, 0.0, 0.0
        self.vel = Twist()
        self.set_vel(0.0, 0.0)
        self.start_time = time.time()

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
        error = 0.05  
        diff = dist - math.sqrt((self.x-self.x0)**2 + (self.y-self.y0)**2) 
        if math.fabs(diff) > error:
            self.set_vel(0.25, 0.0)
            return False
        else:
            self.set_vel(0.0, 0.0)
            return True

    def rotate_angle(self, angle):  
        error = 0.05  
        diff = self.yaw - self.yaw0
        diff = math.atan2(math.sin(diff), math.cos(diff))  
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
     
    def move_time(self, linear_vel, angular_vel, duration):       
        self.set_vel(linear_vel, angular_vel)
        start_time = time.time()  # 移動を開始した時刻を記録
        while rclpy.ok():
            if time.time() - start_time >= duration:
                self.set_vel(0.0, 0.0)
                return True
            rclpy.spin_once(self)  # 定期的にコールバックを処理
        return False        

    def timer_callback(self):  
        self.pub.publish(self.vel)  

    def set_init_pos(self):
        self.x0 = self.x
        self.y0 = self.y

    def set_init_yaw(self):
        self.yaw0 = self.yaw

    def draw_square(self, x):
        linear_vel = 0.25
        angular_vel = 0.3
        for _ in range(4):
            rclpy.spin_once(self)
            self.set_init_pos()
            
            while not self.move_distance(x):
                rclpy.spin_once(self)
            self.set_vel(0.0, 0.0)
            rclpy.spin_once(self)

            rclpy.spin_once(self)
            self.set_init_yaw()
            while not self.rotate_angle(math.pi/2):
                rclpy.spin_once(self)
            self.set_vel(0.0, 0.0)
            rclpy.spin_once(self)

        return True

    def draw_circle(self, r):
        linear_speed = 0.25  # 前進速度 [m/s]
        angular_speed = linear_speed / r  # 円軌道を保つ角速度 [rad/s]
        circumference = 2 * math.pi * r  # 円周の長さ
        duration = circumference / linear_speed  # 円を描くのに必要な時間 [秒]

        if not self.move_time(linear_speed, angular_speed, duration):  # 円を描く処理
            self.get_logger().error("Failed to move in a circle.")
          
    def draw_half_circle(self, r, clockwise=True):
        linear_speed = 0.25  # 前進速度 [m/s]
        angular_speed = linear_speed / r  # 円軌道を保つ角速度 [rad/s]
        circumference = math.pi * r  # 半円周の長さ
        duration = circumference / linear_speed  # 半円を描くのに必要な時間 [秒]

        if not self.move_time(linear_speed, angular_speed, duration):  # 半円を描く処理
            self.get_logger().error("Failed to move in a half circle.")          

    def draw_heart(self):
        while not self.rotate_angle(math.pi / 4):
            rclpy.spin_once(self)
        self.yaw0 = self.yaw

        while not self.move_distance(math.sqrt(2)):
            rclpy.spin_once(self)
        self.x0, self.y0 = self.x, self.y

        while not self.rotate_angle(-math.pi / 4):
            rclpy.spin_once(self)
        self.yaw0 = self.yaw

        self.draw_half_circle(0.5, clockwise=True)
        self.yaw0 = self.yaw
        self.x0, self.y0 = self.x, self.y

        while not self.rotate_angle(-math.pi):
            rclpy.spin_once(self)
        self.yaw0 = self.yaw

        self.draw_half_circle(0.5, clockwise=True)
        self.yaw0 = self.yaw
        self.x0, self.y0 = self.x, self.y

        while not self.rotate_angle(-math.pi / 4):
            rclpy.spin_once(self)
        self.yaw0 = self.yaw

        while not self.move_distance(math.sqrt(2)):
            rclpy.spin_once(self)
        self.x0, self.y0 = self.x, self.y


def main(args=None):
    rclpy.init(args=args)
    node = HappyMove()

    try:
        print("Select shape: 1. Square  2. Circle  3. Heart")
        shape = input("Enter choice (1/2/3): ")

        if shape == '1':
            node.draw_square(1.0)
        elif shape == '2':
            node.draw_circle(1.0)
        elif shape == '3':
            node.draw_heart()
        elif shape == '4':
            node.draw_half_circle(0.5, clockwise=True)
        else:
            print("Invalid input!")

    except KeyboardInterrupt:
        print('Ctrl+C detected, shutting down...')
    except ExternalShutdownException:
        sys.exit(1)
    finally:
        rclpy.try_shutdown()

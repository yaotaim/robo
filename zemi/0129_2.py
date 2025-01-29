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
        error = 0.05  # 許容誤差 [rad]
        max_speed = 0.3  # 最大回転速度 [rad/s]
        slow_speed = 0.1  # 微調整用の低速回転 [rad/s]
    
        target_angle = self.yaw0 + angle
        target_angle = math.atan2(math.sin(target_angle), math.cos(target_angle))  # -pi ~ pi の範囲に正規化
    
        while rclpy.ok():
            diff = target_angle - self.yaw
            diff = math.atan2(math.sin(diff), math.cos(diff))  # -pi ~ pi に正規化
    
            if abs(diff) < error:  # 目標角度に到達
                self.set_vel(0.0, 0.0)
                return True
    
            # 角度の誤差に応じて回転速度を変える
            if abs(diff) > 0.2:
                angular_speed = max_speed
            else:
                angular_speed = slow_speed
    
            self.set_vel(0.0, angular_speed if diff > 0 else -angular_speed)
            rclpy.spin_once(self)

     
    def move_time(self, linear_vel, angular_vel, duration):       
        self.set_vel(linear_vel, angular_vel)
        while rclpy.ok():
            if time.time() - self.start_time >= duration:
                self.set_vel(0.0, 0.0)
                return True            
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
        linear_speed = 0.25
        angular_speed = linear_speed / r
        duration = 0.01
        steps = int(2 * math.pi / (angular_speed * duration))            
        for _ in range(steps):
            self.set_vel(linear_speed, angular_speed)
            rclpy.spin_once(self)
            time.sleep(0.01)               
        self.set_vel(0.0, 0.0)
        rclpy.spin_once(self)
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
        # Start by rotating the robot to the right angle
        while not self.rotate_angle(math.pi / 4):
            rclpy.spin_once(self)
        self.yaw0 = self.yaw  # Set the initial yaw position
    
        # Move the robot along the diagonal of the heart shape
        self.set_init_pos()  # Store the initial position
        while not self.move_distance(2.0 * math.sqrt(2)):  # Move distance for diagonal line
            rclpy.spin_once(self)
        self.x0, self.y0 = self.x, self.y  # Update the current position
    
        # Rotate the robot to form the heart's curve
        while not self.rotate_angle(-math.pi / 4):  # Rotate to the next position
            rclpy.spin_once(self)
        self.yaw0 = self.yaw  # Set the new yaw position
    
        # Draw the first half-circle of the heart
        self.draw_half_circle(1, clockwise=True)
        self.yaw0 = self.yaw
        self.x0, self.y0 = self.x, self.y
    
        # Rotate the robot to the next position to complete the second half-circle
        while not self.rotate_angle(-math.pi / 2):
            rclpy.spin_once(self)
        self.yaw0 = self.yaw  # Update yaw position
    
        # Draw the second half-circle of the heart
        self.draw_half_circle(1, clockwise=True)
        self.yaw0 = self.yaw
        self.x0, self.y0 = self.x, self.y
    
        # Complete the remaining diagonal move
        while not self.rotate_angle(-math.pi / 4):  # Final rotation to complete the heart
            rclpy.spin_once(self)
        self.yaw0 = self.yaw
    
        self.set_init_pos()  # Set initial position again
        while not self.move_distance(2.0 * math.sqrt(2)):  # Move along the final diagonal
            rclpy.spin_once(self)
        self.x0, self.y0 = self.x, self.y  # Update position at the end
    
        return True
    
         


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
        else:
            print("Invalid input!")

    except KeyboardInterrupt:
        print('Ctrl+C detected, shutting down...')
    except ExternalShutdownException:
        sys.exit(1)
    finally:
        rclpy.try_shutdown()

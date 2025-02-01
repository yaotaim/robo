import math
import sys
import rclpy
import tf_transformations
from rclpy.node import Node   
from rclpy.executors import ExternalShutdownException   
from geometry_msgs.msg import Twist  # Twistメッセージ型をインポート
from nav_msgs.msg import Odometry    # Odometryメッセージ型をインポート 
from tf_transformations import euler_from_quaternion 
import time

class HappyMove(Node):  # 簡単な移動クラス
    def __init__(self):   # コンストラクタ
        super().__init__('happy_move_node')        
        self.pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.sub = self.create_subscription(Odometry, 'odom', self.odom_cb, 10)   
        self.timer = self.create_timer(0.01, self.timer_callback)
        self.x, self.y, self.yaw = 0.0, 0.0, 0.0
        self.x0, self.y0, self.yaw0 = 0.0, 0.0, 0.0
        self.vel = Twist()  # Twist メッセージ型インスタンスの生成
        self.set_vel(0.0, 0.0)  # 速度の初期化

    def get_pose(self, msg):      # 姿勢を取得する
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        q_x = msg.pose.pose.orientation.x
        q_y = msg.pose.pose.orientation.y
        q_z = msg.pose.pose.orientation.z
        q_w = msg.pose.pose.orientation.w
        (roll, pitch, yaw) = tf_transformations.euler_from_quaternion((q_x, q_y, q_z, q_w))
        return x, y, yaw
  
    def odom_cb(self, msg):         # オドメトリのコールバック関数
        self.x, self.y, self.yaw = self.get_pose(msg)
        self.get_logger().info(f'x={self.x: .2f} y={self.y: .2f}[m] yaw={self.yaw: .2f}[rad/s]')     
    
    def set_vel(self, linear, angular):  # 速度を設定する
        self.vel.linear.x = linear   # [m/s]
        self.vel.angular.z = angular  # [rad/s]  
    
    def move_distance(self, dist):  # 指定した距離distを移動する
        error = 0.05  # 許容誤差 [m] 
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
        moku_angle = abs(angle - diff)

        if moku_angle > error:
            if angle > diff:
                self.set_vel(0.0, 0.25)
            else:
                self.set_vel(0.0, -0.25)
            return False
        else:
            self.set_vel(0.0, 0.0)
            return True
     
    def timer_callback(self):  # タイマーのコールバック関数
        self.pub.publish(self.vel)  # 速度指令メッセージのパブリッシュ 

    def draw_square(self, x):
        for i in range(4):
            rclpy.spin_once(self)
            self.x0,self.y0 = self.x,self.y
        
            while not self.move_distance(x):
                rclpy.spin_once(self)
            self.set_vel(0.0, 0.0)

            rclpy.spin_once(self)
            self.yaw0 = self.yaw

            while not self.rotate_angle(math.pi/2):
                rclpy.spin_once(self)
            self.set_vel(0.0, 0.0)
            rclpy.spin_once(self)

        return True

    def draw_circle(self, r):
        linear_speed = 0.25
        angular_speed = linear_speed / r
        error = 0.05 

        s_yaw = self.yaw
        self.set_vel(linear_speed, angular_speed)
    
        while abs(math.atan2(math.sin(self.yaw - s_yaw), math.cos(self.yaw - s_yaw)) ) < (2 * math.pi - error): 
            rclpy.spin_once(self)
            time.sleep(0.01)  

        self.set_vel(0.0, 0.0)
        return True     

    def draw_half_circle(self, r):
        linear_speed = 0.25
        angular_speed = linear_speed / r
        error = 0.05 
        
        s_yaw = self.yaw
        self.set_vel(linear_speed, angular_speed)
    
        while abs(math.atan2(math.sin(self.yaw - s_yaw), math.cos(self.yaw - s_yaw)) ) < (math.pi - error): 
            rclpy.spin_once(self)
            time.sleep(0.01)  

        self.set_vel(0.0, 0.0)
        return True        

    def draw_heart(self):
        self.draw_half_circle(0.5)
        self.yaw0 = self.yaw
        self.x0, self.y0 = self.x, self.y

        while not self.rotate_angle(math.pi / 4):
            rclpy.spin_once(self)
        self.yaw0 = self.yaw

        while not self.move_distance( math.sqrt(2)):
            rclpy.spin_once(self)
        self.x0, self.y0 = self.x, self.y

        while not self.rotate_angle(math.pi / 2):
            rclpy.spin_once(self)
        self.yaw0 = self.yaw

        while not self.move_distance( math.sqrt(2)):
            rclpy.spin_once(self)
        self.x0, self.y0 = self.x, self.y

        while not self.rotate_angle(math.pi / 4):
            rclpy.spin_once(self)
        self.yaw0 = self.yaw

        self.draw_half_circle(0.5)
        self.yaw0 = self.yaw
        self.x0, self.y0 = self.x, self.y

        self.set_vel(0.0, 0.0)
        return True   
    
def main(args=None):
    rclpy.init(args=args)
    node = HappyMove()

    try:
        op= input("1:square/2:circle/3:half_cercle/4:heart====>")
        if op == '1':
            node.draw_square(1.0)
        elif op == '2':
            node.draw_circle(0.5)
        elif op == '3':
            node.draw_half_circle(0.5)
        elif op == '4':
            node.draw_heart()
        else:
            print("error")

    except KeyboardInterrupt:
        print('Ctrl+Cが押されました．')     
    except ExternalShutdownException:
        sys.exit(1)
    finally:
        rclpy.try_shutdown()

#ros2 run happy_move happy_move_tnk
#ros2 launch turtlebot3_gazebo empty_world.launch.py

#heartを描く
import math
import sys
import rclpy 
import tf_transformations 
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from geometry_msgs.msg import Twist  # Twistメッセージ型をインポート
from nav_msgs.msg import Odometry    # Odometryメッセージ型をインポート
from tf_transformations import euler_from_quaternion 

class HappyMove(Node):  # 簡単な移動クラス
    def __init__(self):   # コンストラクタ
        super().__init__('happy_move_node')
        self.pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.sub = self.create_subscription(Odometry, 'odom', self.odom_cb, 10) 
        self.timer = self.create_timer(0.01, self.timer_callback)
        self.x, self.y, self.yaw = 0.0, 0.0, 0.0  # 現在位置 
        self.x0, self.y0, self.yaw0 = 0.0, 0.0, 0.0  # 初期位置
        self.vel = Twist()  # Twist メッセージ型インスタンスの生成
        self.set_vel(0.0, 0.0)  # 速度の初期化
        
    def get_pose(self, msg):      # 姿勢を取得する
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        q_x = msg.pose.pose.orientation.x
        q_y = msg.pose.pose.orientation.y
        q_z = msg.pose.pose.orientation.z
        q_w = msg.pose.pose.orientation.w
        (_, _, yaw) = euler_from_quaternion((q_x, q_y, q_z, q_w))#オイラー角 (roll, pitch, yaw) に変換
        return x, y, yaw

    def odom_cb(self, msg):         # オドメトリのコールバック関数
        self.x, self.y, self.yaw = self.get_pose(msg)  # 現在位置を更新
        self.get_logger().info(f'x={self.x: .2f} y={self.y: .2f}[m] yaw={self.yaw: .2f}[rad/s]')

    def set_vel(self, linear, angular):# 速度を設定する
        self.vel.linear.x = linear  # 前進速度 [m/s]
        self.vel.angular.z = angular  # 回転速度 [rad/s]

    def move_distance(self, dist):# 指定距離を移動する
        error = 0.01  # 許容誤差 [m]
        # 現在位置と目標位置の差分を計算
        diff = dist - math.sqrt((self.x - self.x0) ** 2 + (self.y - self.y0) ** 2)
        if math.fabs(diff) > error:  # 誤差が許容範囲を超える
            self.set_vel(0.20, 0.0)  # 前進速度を設定
            return False  # 移動中
        else:  # 許容範囲内に到達した
            self.set_vel(0.0, 0.0)  # 停止
            return True  # 移動完了

    def rotate_angle(self, angle):  # Challenge 4.1
        error = 0.05  # Allowable error [rad]
        diff = self.yaw - self.yaw0
        # Normalization: diff range falls between -pi and pi.
        while diff <= -math.pi:
            diff += 2 * math.pi
        while diff > math.pi:
            diff -= 2 * math.pi
        target_angle = angle

        # Normalizatoin
        while target_angle <= -math.pi:
            target_angle += 2 * math.pi
        while target_angle > math.pi:
            target_angle -= 2 * math.pi
        angle_error = abs(target_angle - diff)

        # Normalization
        if angle_error > math.pi:
            angle_error = 2 * math.pi - angle_error
        if angle_error > error:
            if target_angle > diff:
                self.set_vel(0.0, 0.25)
            else:
                self.set_vel(0.0, -0.25)
            return False
        else:
            self.set_vel(0.0, 0.0)
            rclpy.spin_once(self)
            return True

    def move_time(self, time, linear_speed, angular_speed):#移動させる時間,直線速度,角速度
        start_time = self.get_clock().now().seconds_nanoseconds()[0]# 現在の時刻を記録  

        while rclpy.ok():# ノードがアクティブな間はループを実行
            current_time = self.get_clock().now().seconds_nanoseconds()[0]# 現在時刻を取得
            # 経過時間を計算
            elapsed_time = current_time - start_time  

            if elapsed_time < time:  # 指定時間内の場合
                self.set_vel(linear_speed, angular_speed)# 指定された直線速度と角速度を設定
            else:  # 指定時間を超えた場合
                self.set_vel(0.0, 0.0)# ロボットを停止
                break 
            self.pub.publish(self.vel)# 現在の速度コマンドをパブリッシュ
            rclpy.spin_once(self)

    def draw_square(self, x):
        linear_vel = 0.25
        angular_vel = 0.3
        for num in range(4):
            rclpy.spin_once(self)
            self.set_init_pos()
            
            while rclpy.ok():
                if not self.move_distance(x):
                    self.set_vel(linear_vel, 0.0)
                    rclpy.spin_once(self, timeout_sec=0.01)
                else:
                    self.set_vel(0.0, 0.0)
                    rclpy.spin_once(self, timeout_sec=0.01)
                    break;                
            rclpy.spin_once(self)
            self.set_init_yaw()
            while rclpy.ok():            
                if not self.rotate_angle(math.pi/2):
                    self.set_vel(0.0, angular_vel)
                    rclpy.spin_once(self, timeout_sec=0.01)
                else:
                    self.set_vel(0.0, 0.0)
                    rclpy.spin_once(self, timeout_sec=0.01)
                    break;
            num += 1                
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
        linear_speed = 0.20  # 前進速度
        angular_speed = (linear_speed / r) * (-1 if clockwise else 1)  # 角速度
        target_angle = self.yaw + (math.pi) * (-1 if clockwise else 1)  # 180度回転の目標角度
        
        self.yaw0 = self.yaw  # 基準角度をセット
        
        while True:
            diff = target_angle - self.yaw
            diff = math.atan2(math.sin(diff), math.cos(diff))  # -π ~ π に正規化
            
            if abs(diff) < 0.05:  # 誤差が小さければ終了
                break
            
            self.set_vel(linear_speed, angular_speed)  # 速度指令
            rclpy.spin_once(self)  # オドメトリ更新
    
        self.set_vel(0.0, 0.0)  # 停止
    

    def draw_heart(self):
        #1.時計45度回転
        while not self.rotate_angle(math.pi / 4): 
            rclpy.spin_once(self)
        self.yaw0 = self.yaw

        #2. √2 移動
        while not self.move_distance(2.0 * math.sqrt(2)):
            rclpy.spin_once(self)
        self.x0, self.y0 = self.x, self.y
        
        #3. 反時計45度回転
        while not self.rotate_angle(-math.pi / 4): 
            rclpy.spin_once(self)
        self.yaw0 = self.yaw

        # 4. 半径1の半円右回り
        self.draw_half_circle(2/ 2, clockwise=True)
        self.yaw0 = self.yaw
        self.x0, self.y0 = self.x, self.y
        
        # 5. 90度回転
        while not self.rotate_angle(-math.pi/2):
            rclpy.spin_once(self)
        self.yaw0 = self.yaw

        # 6. 90度回転
        while not self.rotate_angle(-math.pi/2):
            rclpy.spin_once(self)
        self.yaw0 = self.yaw

        # 7. 半径1の半円右回り
        self.draw_half_circle(2/ 2, clockwise=True)
        self.yaw0 = self.yaw
        self.x0, self.y0 = self.x, self.y

        # 8. 45度回転
        while not self.rotate_angle(-math.pi / 4): 
            rclpy.spin_once(self)
        self.yaw0 = self.yaw

        # 9. 2√2 移動
        while not self.move_distance(2.0 * math.sqrt(2)):
            rclpy.spin_once(self)
        self.x0, self.y0 = self.x, self.y


    def timer_callback(self):  # タイマーのコールバック関数
        self.pub.publish(self.vel)  # 速度指令メッセージのパブリッシュ 
        
    def happy_move(self,  distance, angle):  # 簡単な状態遷移
        state = 0
        while rclpy.ok():
            if state == 0:
                if self.move_distance(distance):
                    state = 1
            elif state == 1:                
                if self.rotate_angle(angle):
                    break
            else:
                print('エラー状態')
            rclpy.spin_once(self) 

def main(args=None):  # main関数
    rclpy.init(args=args)  
    node = HappyMove()

    try:
        print("heart")
        node.draw_heart()
    except KeyboardInterrupt:
        print('Ctrl+Cが押されました') 
    except ExternalShutdownException:
        sys.exit(1) 
    finally:
        rclpy.try_shutdown()

import math
import sys
import rclpy  # ROS 2 Python クライアントライブラリ
import tf_transformations  # クォータニオンとオイラー角の変換を行うライブラリ
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from geometry_msgs.msg import Twist  # ロボットの速度制御メッセージ型
from nav_msgs.msg import Odometry  # ロボットの位置と姿勢情報を含むメッセージ型
from tf_transformations import euler_from_quaternion  # クォータニオンをオイラー角に変換する関数

# ロボットの動きを管理するクラス
class HappyMove(Node):
    def __init__(self):
        super().__init__('happy_move_node')  # ノード名を指定して初期化
        self.pub = self.create_publisher(Twist, 'cmd_vel', 10)  # /cmd_vel トピックに速度指令を送るパブリッシャーを作成
        self.sub = self.create_subscription(Odometry, 'odom', self.odom_cb, 10)  # /odom トピックからオドメトリデータを受信するサブスクライバーを作成
        self.timer = self.create_timer(0.01, self.timer_callback)  # 10msごとにタイマーコールバックを呼び出す

        # ロボットの現在位置と初期位置
        self.x, self.y, self.yaw = 0.0, 0.0, 0.0  # 現在の位置 (x, y, yaw)
        self.x0, self.y0, self.yaw0 = 0.0, 0.0, 0.0  # 初期位置 (x0, y0, yaw0)

        # ロボットの速度メッセージ
        self.vel = Twist()  # Twistメッセージのインスタンスを生成
        self.set_vel(0.0, 0.0)  # 初期状態ではロボットを停止

    # オドメトリデータからロボットの位置と姿勢を取得
    def get_pose(self, msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        q_x = msg.pose.pose.orientation.x
        q_y = msg.pose.pose.orientation.y
        q_z = msg.pose.pose.orientation.z
        q_w = msg.pose.pose.orientation.w

        # クォータニオンをオイラー角 (roll, pitch, yaw) に変換
        (_, _, yaw) = euler_from_quaternion((q_x, q_y, q_z, q_w))
        return x, y, yaw

    # オドメトリコールバック関数: ロボットの位置と姿勢を更新
    def odom_cb(self, msg):
        self.x, self.y, self.yaw = self.get_pose(msg)  # 現在位置を更新
        self.get_logger().info(f'x={self.x: .2f} y={self.y: .2f}[m] yaw={self.yaw: .2f}[rad/s]')  # デバッグ情報をログに表示

    # 速度を設定する
    def set_vel(self, linear, angular):
        self.vel.linear.x = linear  # 前進速度 [m/s]
        self.vel.angular.z = angular  # 回転速度 [rad/s]

    # 指定距離を移動する
    def move_distance(self, dist):
        error = 0.05  # 許容誤差 [m]
        # 現在位置と目標位置の差分を計算
        diff = dist - math.sqrt((self.x - self.x0) ** 2 + (self.y - self.y0) ** 2)
        if math.fabs(diff) > error:  # 誤差が許容範囲を超える場合
            self.set_vel(0.25, 0.0)  # 前進速度を設定
            return False  # 移動中
        else:  # 許容範囲内に到達した場合
            self.set_vel(0.0, 0.0)  # 停止
            return True  # 移動完了

    # 指定角度を回転する
    def rotate_angle(self, angle):
        error = 0.05  # 許容誤差 [rad]
        # 現在の角度と目標角度の差分を計算
        diff = angle - (self.yaw - self.yaw0)
        diff = (diff + math.pi) % (2 * math.pi) - math.pi  # 角度を-π～πに正規化

        if math.fabs(diff) > error:  # 誤差が許容範囲を超える場合
            angular_speed = 0.25 if diff > 0 else -0.25  # 回転方向を決定
            self.set_vel(0.0, angular_speed)  # 回転速度を設定
            return False  # 回転中
        else:  # 許容範囲内に到達した場合
            self.set_vel(0.0, 0.0)  # 停止
            return True  # 回転完了

    # 指定時間の間、指定速度で移動する
    def move_time(self, time, linear_speed, angular_speed):
        start_time = self.get_clock().now().seconds_nanoseconds()[0]  # 開始時刻を記録
        while rclpy.ok():
            current_time = self.get_clock().now().seconds_nanoseconds()[0]  # 現在時刻を取得
            elapsed_time = current_time - start_time  # 経過時間を計算

            if elapsed_time < time:  # 指定時間内
                self.set_vel(linear_speed, angular_speed)  # 指定速度を設定
            else:  # 指定時間を超えたら停止
                self.set_vel(0.0, 0.0)
                break

            self.pub.publish(self.vel)  # 現在の速度をパブリッシュ
            rclpy.spin_once(self)  # ノードのスピンを継続

    # 正方形を描く
    def draw_square(self, x):
        for _ in range(4):  # 正方形の4辺を描く
            # 1辺を移動
            while not self.move_distance(x):
                rclpy.spin_once(self)
            self.x0, self.y0 = self.x, self.y  # 次の辺の開始位置を更新

            # 90度回転
            while not self.rotate_angle(math.pi / 2):  # π/2ラジアン (90度) 回転
                rclpy.spin_once(self)
            self.yaw0 = self.yaw  # 次の回転の基準角度を更新

    # 円を描く
    def draw_circle(self, r):
        linear_speed = 0.2  # 前進速度 [m/s]
        angular_speed = linear_speed / r  # 円軌道を保つ角速度 [rad/s]
        circumference = 2 * math.pi * r  # 円周の長さ
        duration = circumference / linear_speed  # 円を描くのに必要な時間 [秒]

        self.move_time(duration, linear_speed, angular_speed)  # 円軌道を維持

    # タイマーコールバック: 現在の速度をパブリッシュ
    def timer_callback(self):
        self.pub.publish(self.vel)


# メイン関数
def main(args=None):
    rclpy.init(args=args)  # ROS 2 ノードを初期化
    node = HappyMove()

    try:
        print("正方形を描きます...")
        node.draw_square(1.0)  # 1辺が1mの正方形を描く
        print("円を描きます...")
        node.draw_circle(0.5)  # 半径0.5mの円を描く
    except KeyboardInterrupt:
        print('Ctrl+Cが押されました．')  # ユーザーが終了した場合
    except ExternalShutdownException:
        sys.exit(1)  # 外部からシャットダウンされた場合
    finally:
        rclpy.try_shutdown()  # ROS 2 ノードを安全にシャットダウン

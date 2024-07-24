import cv2
import numpy as np
import pyrealsense2.pyrealsense2 as rs
import time
import Adafruit_PCA9685
import paho.mqtt.client as mqtt
import math
import simpleaudio as sa
import asyncio
import threading


#ブローカーに接続できたときの処理
def on_connect(client,userdata,flag,rc):
    print("Connected with result code" + str(rc))

#ブローカーが切断したときの処理
def on_disconnect(client,userdata,rc):
    if rc != 0:
        print("Unexpected disconnection.")

#publishが完了したときの処理
def on_publish(client,userdata,mid):
    print(message)

client = mqtt.Client()  #クラスのインスタンス(実体)の作成
client.on_connect = on_connect  #接続部のコールバック関数を登録
client.on_disconnect = on_disconnect  #切断時のコールバックを登録
client.on_publish = on_publish  #メッセージ送信時のコールバック
client.connect("localhost",1883,60)  #接続先は自分自身

#通信処理スタート
client.loop_start()  #subはloop_forever()だが、pubはloop_start()で起動だけさせる
# Realsense デバイスの初期化
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)  # 深度ストリームを有効にする
config.enable_device('00000000f0211359')  # ここにシリアル番号を指定します
pipeline.start(config)

class servo_Class:
    def __init__(self, Channel, ZeroOffset):
        self.Channel = Channel
        self.ZeroOffset = ZeroOffset
        self.pwm = Adafruit_PCA9685.PCA9685(address=0x40, busnum=1)
        self.pwm.set_pwm_freq(int(60))

    def SetPos(self, pos):
        pulse = int((650 - 150) / 180 * pos + 150 + self.ZeroOffset)
        self.pwm.set_pwm(self.Channel, 0, pulse)

    def Cleanup0(self):
        self.SetPos(int(0))
        print('0')
    def Cleanup1(self):
        self.SetPos(int(70))
        print('110')
    def Cleanup2(self):
        self.SetPos(int(15))
        print('20')

Servo0 = servo_Class(Channel=0, ZeroOffset=0)
Servo1 = servo_Class(Channel=1, ZeroOffset=0)
Servo2 = servo_Class(Channel=2, ZeroOffset=0)
count=0
flag=0

def oto1():
    wave_obj=sa.WaveObject.from_wave_file("men3.wav")
    play_obj=wave_obj.play()
    play_obj.wait_done() 

def oto2():
    wave_obj=sa.WaveObject.from_wave_file("dou3.wav")
    play_obj=wave_obj.play()
    play_obj.wait_done() 

async def oto3():
    wave_obj=sa.WaveObject.from_wave_file("aisatu1.wav")
    play_obj=wave_obj.play()
    play_obj.wait_done() 

async def oto4():
    wave_obj=sa.WaveObject.from_wave_file("aisatu2.wav")
    play_obj=wave_obj.play()
    play_obj.wait_done() 
    
def men():
    Servo1.SetPos(int(0))
    time.sleep(0.6)
    Servo1.SetPos(int(50))
    time.sleep(0.3)
    Servo2.SetPos(int(kaku))
    time.sleep(0.4)
    Servo2.SetPos(int(10))
    time.sleep(0.3)

def menm():
    Servo1.SetPos(int(0))
    time.sleep(0.6)
    Servo1.SetPos(int(50))
    time.sleep(0.3)
    Servo2.SetPos(int(kaku))
    time.sleep(0.4)
    Servo2.SetPos(int(10))
    time.sleep(0.3)
  
def dou():
    Servo0.SetPos(int(kata))
    time.sleep(0.3)
    Servo1.SetPos(int(0))
    time.sleep(0.3)
    Servo1.SetPos(int(80))
    time.sleep(0.3)
    Servo2.SetPos(int(90))
    time.sleep(0.3)
    Servo2.SetPos(int(10))
    time.sleep(0.3)
    Servo0.SetPos(int(0))
    time.sleep(0.3)

def tyudan():
    Servo2.SetPos(int(15))
    time.sleep(0.3)
    Servo1.SetPos(int(70))
    time.sleep(0.3)

# アラインメントオブジェクトの作成
align_to = rs.stream.color
align = rs.align(align_to)
sensor = pipeline.get_active_profile().get_device().query_sensors()[0]
sensor.set_option(rs.option.min_distance, 0)


def print_and_play_audio(msg, audio_task):
    print(msg)
    asyncio.run(audio_task)

def thcount():
    timer = threading.Timer(3,flags)
    timer.start()

def flags():
    global flag
    flag=0

def rengeki1():
    global flag
    if flag == 0:
        random_numbers = [0,1]
        for i in random_numbers:
            if i == 0:
                message = f"{600}|{600}"
                client.publish("drone/001",message)
                thread_men = threading.Thread(target=men)
                thread_oto1 = threading.Thread(target=oto1)
                thread_men.start()
                thread_oto1.start()
                time.sleep(1.5)

            else:
                message = f"{700}|{700}"
                client.publish("drone/001",message)
                thread_dou = threading.Thread(target=dou)
                thread_oto2 = threading.Thread(target=oto2)
                thread_dou.start()
                thread_oto2.start()
                time.sleep(2)    
        flag=1
        my_thread = threading.Thread(target=thcount())
        my_thread.start()

def rengeki2():
    global flag
    if flag == 0:
        random_numbers = [1,0]
        for i in random_numbers:
            if i == 0:
                thread_men = threading.Thread(target=men)
                thread_oto1 = threading.Thread(target=oto1)
                thread_men.start()
                thread_oto1.start()
                time.sleep(1.5)

            else:              
                thread_dou = threading.Thread(target=dou)
                thread_oto2 = threading.Thread(target=oto2)
                thread_dou.start()
                thread_oto2.start()
                time.sleep(2)           
        flag=1
        my_thread = threading.Thread(target=thcount())
        my_thread.start()


try:
    last_detection_time = time.time()
    error_x = 500
    error_y = 0
    distance = 500
    message = 0

    #x=int(input())
    if True:
        #asyncio.run(oto3())
        while True:         
            # フレームの取得だけさせる
            k=int(cv2.waitKey(1))
            if k==49:
                asyncio.run(oto3())

            frames = pipeline.wait_for_frames()
            aligned_frames=align.process(frames)
            color_frame = aligned_frames.get_color_frame()
            depth_frame = aligned_frames.get_depth_frame()  # 深度フレームを取得

            # カウントスレッドを作成して実行
            color_image=np.asanyarray(color_frame.get_data())
            # BGRからHSVへの変換
            hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)
            # 赤色のHSVの範囲を定義
            lower_red = np.array([170, 100, 100])
            upper_red = np.array([179, 255, 255])

            lower_red2 = np.array([0, 100, 100])
            upper_red2 = np.array([1, 255, 255])

            lower_blue= np.array([100, 100, 100])
            upper_blue= np.array([106, 255, 255])     

            print(hsv[320,240])       
            # 画像を赤色にしきい値処理
            mask = cv2.inRange(hsv, lower_red, upper_red)
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
            mask3 = cv2.inRange(hsv, lower_blue, upper_blue)
            mask = mask | mask2

            # 物体を輪郭検出 akaao
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours2, _ = cv2.findContours(mask3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # x軸、y軸に線を描画
            cv2.line(img=color_image, pt1=(0,240),pt2=(640,240),color=(0,255,0),thickness=2)
            cv2.line(img=color_image, pt1=(320,0),pt2=(320,480),color=(0,255,0),thickness=2)

            # 中心のピクセル座標を計算
            width = depth_frame.get_width()
            height = depth_frame.get_height()
            x = int(width / 2)
            y = int(height / 2)

        
            #赤岳を探す
            if  contours and cv2.contourArea(max(contours, key=cv2.contourArea)) > 5:
                max_contour = max(contours, key=cv2.contourArea)
                
                # 重心を計算
                M = cv2.moments(max_contour)
                centroid_xk2 = int(M['m10'] / M['m00'])
                centroid_yk2 = int(M['m01'] / M['m00'])

                #print(hsv[centroid_yk2,centroid_xk2])

                
                # 中心のピクセル座標の距離を取得
                distance = depth_frame.get_distance(centroid_xk2, centroid_yk2)

                if 0.25<distance<2.0 and 0.0<=centroid_yk2<=300.0:
       
                    # 重心を描画
                    cv2.circle(color_image, (centroid_xk2, centroid_yk2), 5, (0, 255, 0), -1)

                # 1秒ごとに誤差を計算
                    current_time = time.time()
                    if current_time - last_detection_time >= 1:
                        error_x = centroid_xk2 - x
                        error_y = centroid_yk2 - y
                        message = f"{error_x}|{math.ceil(distance*100)}"
                        last_detection_time = current_time 
                
                    if 310<=centroid_xk2<=330 and 320<=centroid_yk2<= 480 and 0<=distance<=0.5:  #赤だけが写ったとき
                        message = f"{700}|{700}"
                        client.publish("drone/001",message)
                        kaku=180
                        kata=60
                        rengeki1()
                        tyudan()

                    elif 310<=centroid_xk2<=330 and 160<=centroid_yk2<= 319 and 0<=distance<=0.5:   #赤だけが写ったとき
                        message = f"{700}|{700}"
                        client.publish("drone/001",message)
                        kaku=140
                        kata=60
                        rengeki1()
                        tyudan()
                        

                    elif 310<=centroid_xk2<=330 and 0<=centroid_yk2<= 159  and 0<=distance<=0.5:#赤だけが写った
                        message = f"{700}|{700}"
                        client.publish("drone/001",message)
                        kaku=100
                        kata=70
                        rengeki1()
                        tyudan()


                # 青いものが写って、輪郭が存在する場合のみ重心を計算
                elif  contours2 and cv2.contourArea(max(contours2, key=cv2.contourArea)) > 5:  # 輪郭面積が一定以上であることを確認
                    max_contour2 = max(contours2, key=cv2.contourArea)
                    N = cv2.moments(max_contour2)

                    # 重心を計算
                    centroid_x2o2 = int(N['m10'] / N['m00'])
                    centroid_y2o2 = int(N['m01'] / N['m00'])
                    
                    # 中心のピクセル座標の距離を取得
                    distance2 = depth_frame.get_distance(centroid_x2o2, centroid_y2o2)
                    if  0.25<distance2<2.0 and 0.0<=centroid_y2o2<=300.0:
                        # 重心を描画
                        cv2.circle(color_image, (centroid_x2o2, centroid_y2o2), 5, (0, 255, 0), -1)

                        # 1秒ごとに誤差を計算
                        current_time = time.time()
                        if current_time - last_detection_time >= 1:
                            error_x = centroid_x2o2 - x
                            error_y = centroid_y2o2 - y
                            message = f"{error_x}|{math.ceil(distance2*100)}"
                            last_detection_time = current_time

                        if 310<=centroid_x2o2<=330 and 320<=centroid_y2o2<= 480 and 0<=distance<=0.5:  #赤だけが写ったとき              
                            kata=60
                            message = f"{600}|{600}"
                            client.publish("drone/001",message)
                            kaku=60
                            rengeki2()
                            tyudan()

                        elif 310<=centroid_x2o2<=330 and 160<=centroid_y2o2<= 319 and 0<=distance<=0.5:   #赤だけが写ったとき       
                            kata=70
                            message = f"{600}|{600}"
                            client.publish("drone/001",message)
                            kaku=70
                            rengeki2()
                            tyudan()

                        elif 310<=centroid_x2o2<=330 and 0<=centroid_y2o2<= 159 and 0<=distance<=0.5:#赤だけが写ったとき
                            message = f"{600}|{600}"
                            client.publish("drone/001",message)
                            kata=70
                            kaku=50
                            rengeki1()
                            tyudan()

                        #どちらもなかったから500を送信
                    else:
                        current_time = time.time()
                        if current_time - last_detection_time >= 1:
                            message = f"{500}|{500}"
                            last_detection_time = current_time

                #青竹を探す
            elif  contours2 and cv2.contourArea(max(contours2, key=cv2.contourArea)) > 5:  # 輪郭面積が一定以上であることを確認
                max_contour2 = max(contours2, key=cv2.contourArea)
            
                # 重心を計算
                N = cv2.moments(max_contour2)
                centroid_x2o2 = int(N['m10'] / N['m00'])
                centroid_y2o2 = int(N['m01'] / N['m00'])
                
                # 中心のピクセル座標の距離を取得
                distance2 = depth_frame.get_distance(centroid_x2o2, centroid_y2o2)
                if  0.25<distance2<2.0 and 0.0<=centroid_y2o2<=300.0:
                    # 重心を描画
                    cv2.circle(color_image, (centroid_x2o2, centroid_y2o2), 5, (0, 255, 0), -1)

                    # 1秒ごとに誤差を計算
                    current_time = time.time()
                    if current_time - last_detection_time >= 1:
                        error_x = centroid_x2o2 - x
                        error_y = centroid_y2o2 - y
                        message = f"{error_x}|{math.ceil(distance2*100)}"
                        last_detection_time = current_time

                    if 310<=centroid_x2o2<=330 and 320<=centroid_y2o2<= 480 and 0<=distance<=0.4:  #赤だけが写ったとき
                        kata=120
                        message = f"{700}|{700}"
                        client.publish("drone/001",message)
                        kaku=60
                        rengeki2()
                        tyudan()

                    elif 310<=centroid_x2o2<=330 and 160<=centroid_y2o2<= 319 and 0<=distance<=0.4:   #赤だけが写ったとき
                        kata=90
                        message = f"{700}|{700}"
                        client.publish("drone/001",message)
                        kaku=70
                        rengeki2()
                        tyudan()

                    elif 310<=centroid_x2o2<=330 and 0<=centroid_y2o2<= 159 and 0<=distance<=0.4:#赤だけが写ったとき
                        message = f"{700}|{700}"
                        client.publish("drone/001",message)
                        kaku=60
                        kaku=70
                        rengeki2()
                        tyudan()
                #なかったので500を送信
                else:
                    current_time = time.time()
                    if current_time - last_detection_time >= 1:
                        message = f"{500}|{500}"
                        last_detection_time = current_time

                            
            #そもそも何も見つからないので500送信
            else:
                current_time = time.time()
                if current_time - last_detection_time >= 1:
                    message = f"{500}|{500}"
                    last_detection_time = current_time
            count+=1
            if(count % 5== 0): #これで送るスピードを変える
                client.publish("drone/001",message)  #トピック名とメッセージを決めて送信

            # ウィンドウに表示
            cv2.imshow('cro',color_image)

            # qキーが押されたら終了
            if cv2.waitKey(1) & 0xFF == ord('q'):
                asyncio.run(oto4())
                break

finally:
    # キャプチャを停止し、ウィンドウを閉じる
    Servo0.Cleanup0()
    Servo1.Cleanup1()
    Servo2.Cleanup2()
    pipeline.stop()
    cv2.destroyAllWindows()

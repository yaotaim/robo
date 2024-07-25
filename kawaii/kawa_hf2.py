#!/usr/bin/env python3
#04の改良版

#ライブラリインポート
from HandFaceTracker02 import HandFaceTracker
from HandFaceRenderer_sRA02 import HandFaceRenderer
import argparse
import serial
import time
import numpy as np

import pigpio
from time import sleep
import time
import sys
import serial
import random

ser = serial.Serial(
    port='/dev/ttyS0', 
    baudrate=115200,    
    timeout=1           
)
time.sleep(2) 

pig = pigpio.pi()
if not pig.connected:
    print("Failed to connect to pigpiod")
    exit()


pig.set_mode(12, pigpio.OUTPUT)#左右 
pig.set_mode(13, pigpio.OUTPUT)#上下

S_kioku12 = 90
S_kioku13 = 135
S_kioku12_zettai=0
S_kioku13_zettai=0



mode=None
mode2=None


def fast_servo(gpio_pin, angle):
    pulse_width_ms = 0.5 + (angle / 180.0) * (2.5 - 0.5)
    duty_cycle = int((pulse_width_ms / 20.0) * 1000000)
    pig.hardware_PWM(gpio_pin, 50, duty_cycle)
    
    if gpio_pin==12:
        S_kioku12 = angle
    elif gpio_pin==13:
        S_kioku13 = angle


def slow_servo(gpio_pin, start_angle, end_angle, step=1, delay=0.02):
    if gpio_pin==12:
        start_angle = S_kioku12

    elif gpio_pin==13:
        start_angle = S_kioku13

    if start_angle < end_angle:
        for angle in range(start_angle, end_angle + 1, step):
            fast_servo(gpio_pin, angle)
            sleep(delay)
    else:
        for angle in range(start_angle, end_angle - 1, -1):
            fast_servo(gpio_pin, angle)
            sleep(delay)

fast_servo(12, 110)#左右
fast_servo(13, 135)#上下



parser = argparse.ArgumentParser()
parser_tracker = parser.add_argument_group("トラッカーの引数")
parser_tracker.add_argument('-i', '--input', type=str, 
                    help="入力として使用するビデオまたは画像ファイルのパス（指定されていない場合、OAKカラーカメラを使用します）")
parser_tracker.add_argument("-a", "--with_attention", action="store_true",
                    help="注意モデルを使用した顔のランドマーク")
parser_tracker.add_argument('-p', "--use_face_pose", action="store_true", 
                    help="顔のポーズ変換行列とメトリックランドマークを計算します")
parser_tracker.add_argument('-2', "--double_face", action="store_true", 
                    help="実験的。顔ランドマークニューラルネットワークの2番目の発生を実行してfpsを向上させます。ハンドトラッキングは無効です。")
parser_tracker.add_argument('-n', '--nb_hands', type=int, choices=[0,1,2], default=2, 
                    help="トラッキングされる手の数（デフォルト=%(default)i）")                    
parser_tracker.add_argument('-xyz', "--xyz", action="store_true", 
                    help="手と顔の空間位置測定を有効にします")
parser_tracker.add_argument('-g', '--gesture', action="store_true", 
                    help="ジェスチャー認識を有効にします")
parser_tracker.add_argument('-f', '--internal_fps', type=int, 
                    help="内部カラーカメラのfps。高すぎる値はNNのfpsを下げます（デフォルト=モデルに依存します）")                    
parser_tracker.add_argument('--internal_frame_height', type=int,                                                                                 
                    help="内部カラーカメラフレームの高さ（ピクセル単位）")   
parser_tracker.add_argument('-t', '--trace', type=int, nargs="?", const=1, default=0, 
                    help="いくつかのデバッグ情報を出力します。情報の種類はオプションの引数に依存します。")                
parser_renderer = parser.add_argument_group("レンダラーの引数")
parser_renderer.add_argument('-o', '--output', 
                    help="出力ビデオファイルへのパス")
args = parser.parse_args()
dargs = vars(args)
tracker_args = {a:dargs[a] for a in ['internal_fps', 'internal_frame_height'] if dargs[a] is not None}

# トラッカーのインスタンスを作成
tracker = HandFaceTracker(
        input_src=args.input, 
        double_face=args.double_face,
        use_face_pose=args.use_face_pose,
        use_gesture=args.gesture,
        xyz=args.xyz,
        with_attention=args.with_attention,
        nb_hands=args.nb_hands,
        trace=args.trace,
        **tracker_args
        )

# レンダラーのインスタンスを作成
renderer = HandFaceRenderer(
        tracker=tracker,
        output=args.output)



#最初にモードを選択してもらうーーーーーーーーーーーーーーーーーーーーーー
while True:
    print("mode選択をまてるよ")
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8', errors='ignore').rstrip()
        print(f"受信したデータ: {data}")
        if data == "t":
            mode="sousa" 
            print("操作モード")
            break
        elif data == "y":
            mode="jidou" 
            print("自動モード")
            break
#ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー


while True:
    #操作モードーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
    if  mode=="sousa":
        while True:
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8', errors='ignore').rstrip()
                if data == "u":
                    print(f"左見て: {data}")
                    fast_servo(12,155) 
                    sleep(0.1) 

                elif data == "i":
                    print(f"前見て: {data}")
                    fast_servo(12, 110) 
                    sleep(0.1) 

                elif data == "o":
                    print(f"右見て: {data}")
                    fast_servo(12,65) 
                    sleep(0.1) 
 
                elif data == "y":
                    mode="jidou" 
                    print("自動モードにきりかえるよ")
                    break
                elif data == "q":
                    mode="end"
                    print("終了")
                    break

    #自動モードーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
    elif mode=="jidou":   
        sen_face = None  
        sen_hand = None   
        last_serial_send_time = 0
        span = 0.1 #送るラグ
        kioku_kaisuu=0
        kioku_hand=None


        while True:
            #ESPから信号が来ていたときの処理ーーーーーーーーーーーーーーーーーーーーーー
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8', errors='ignore').rstrip()  
                if data == "t":
                    mode="sousa" 
                    print("操作モードにきりかえるよ")
                    break
                elif data == "q":
                    mode=="end" 
                    print("終了")
                    break
            #ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー


            frame, faces, hands = tracker.next_frame()
            if frame is None:
                mode=="end"
                break

            frame = renderer.draw(frame, faces, hands)
            
            #顔を見つけたときの処理ーーーーーーーーーーーーーーーーーーーーーーーーー
            if faces:
                for face in faces:
                    if not np.isnan(face.xyz[0]) and not np.isnan(face.xyz[1]):
                        
                        #顔の位置x_pose，y_pose
                        x_pos = face.xyz[0] / 10
                        y_pos = face.xyz[1] / 10

                        #顔の位置によってsen_faceの値を変える
                        if x_pos < -20 and y_pos >5:
                            sen_face = "w"

                        elif -20<=x_pos<-10 and y_pos >5:
                            sen_face = "e"

                        elif -10<=x_pos<10 and y_pos >5:
                            sen_face = "r"

                        elif 10<=x_pos<20 and y_pos >5:
                            sen_face = "t"

                        elif 20<=x_pos and y_pos >5:
                            sen_face = "y"
                        #--------------------------------------
                            
                        elif x_pos < -20 and 5 >=y_pos>= -5:
                            sen_face = "s"

                        elif -20<=x_pos<-10 and 5 >=y_pos>= -5:
                            sen_face = "d"

                        elif -10<=x_pos<10 and 5 >=y_pos>= -5:
                            sen_face = "f"

                        elif 10<=x_pos<20 and 5 >=y_pos>= -5:
                            sen_face = "g"

                        elif 20<=x_pos and 5 >=y_pos>= -5:
                            sen_face = "h"
                        #--------------------------------------
                        elif x_pos < -20 and -5 >=y_pos:
                            sen_face = "x"

                        elif -20<=x_pos<-10 and -5 >=y_pos:
                            sen_face = "c"

                        elif -10<=x_pos<10 and -5 >=y_pos:
                            sen_face = "v"

                        elif 10<=x_pos<20 and -5 >=y_pos:
                            sen_face = "b"

                        elif 20<=x_pos and -5 >=y_pos:
                            sen_face = "n"
            else:
                sen_face=None
            #ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
        

            #手を見つけたときの処理ーーーーーーーーーーーーーーーーーーーーーーーー
            if hands:
                for hand in hands:
                    
                    if hand.gesture == "PEACE":#手がピースのとき顔の位置のときみたいにsen_hand変える
                        #sen_hand = "i"
                        if not np.isnan(hand.xyz[0]) and not np.isnan(hand.xyz[1]):
                        
                            x_pos = hand.xyz[0] / 10
                            y_pos = hand.xyz[1] / 10

                            if x_pos < -10 and y_pos >5:
                                sen_hand = "w"
                            elif x_pos < -10 and 5 >=y_pos>= -5:
                                sen_hand = "s"
                            elif x_pos <= -10 and y_pos <-5:
                                sen_hand = "x"

                            elif -10<=x_pos<10 and y_pos >5:
                                sen_hand = "e"
                            elif -10<=x_pos<10 and 5 >=y_pos>= -5:
                                sen_hand = "d"
                            elif -10<=x_pos<10 and y_pos <-5:
                                sen_hand = "c"

                            elif 10<x_pos and y_pos >5:
                                sen_hand = "r"
                            elif 10<x_pos and 5 >=y_pos>= -5:
                                sen_hand = "f"
                            elif 10<x_pos and y_pos <-5:
                                sen_hand = "v"
                            
                    elif hand.gesture == "OK":
                        sen_hand = "t"
                    elif hand.gesture == "FIVE":
                        sen_hand = "u"

                    elif hand.gesture == "FIST":
                        sen_hand = "y"

                    elif hand.gesture == "ONE":
                        sen_hand = "o"
                    elif hand.gesture == "LEFT":
                        sen_hand = "h"
                    elif hand.gesture == "RIGHT":
                        sen_hand = "g"
                    elif hand.gesture == "TWO":
                        sen_hand = "p"                       
                    elif hand.gesture == "THREE":
                        sen_hand = "j"
                    elif hand.gesture == "FOUR":
                        sen_hand = "k"
            else:
                sen_hand=None
            #ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー


            #なにか動作を起こす時間的条件ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
            current_time = time.time()#時刻を取る
            if current_time - last_serial_send_time >= span:#今の時刻と最後にシリアルを送った時刻の差がspanであれば
                last_serial_send_time = current_time#最後にシリアルを送った時刻の更新
        #ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
                

                #時間的条件に満たし、顔と手が両方認識 ,手だけ認識しているときの動作ーーーーーーーーーーーーーー
                if (sen_hand!=None and sen_face!=None) or (sen_hand!=None and sen_face==None):
                    print(f"mode2:{mode2}")
                    print(f"kioku_kaisuu:{kioku_kaisuu}")
                    for hand in hands:
                        print(hand.gesture)
                    
                    if sen_hand==kioku_hand:#前の手と同じ
                        if kioku_kaisuu==1:
                            if sen_hand=="w":
                                if S_kioku12<=155:
                                    S_kioku12=S_kioku12+2
                                if S_kioku13<=180:
                                    S_kioku13=S_kioku13-2
                                kioku_kaisuu=0 

                                    
                            elif sen_hand=="s":
                                if S_kioku12<=155:
                                    S_kioku12=S_kioku12+2
                                kioku_kaisuu=0 


                            elif sen_hand=="x":
                                if S_kioku12<=155:
                                    S_kioku12=S_kioku12+2
                                if 90<=S_kioku13:
                                    S_kioku13=S_kioku13+2
                                kioku_kaisuu=0 

                      
                            elif sen_hand=="e":
                                if S_kioku13<=180:
                                    S_kioku13=S_kioku13-2
                                kioku_kaisuu=0 

                        
                            elif sen_hand=="d":
                                kioku_kaisuu=0 
                                pass     


                            elif sen_hand=="c":
                                if 90<=S_kioku13:
                                    S_kioku13=S_kioku13+2
                                    kioku_kaisuu=0 


                                    
                            elif sen_hand=="r":
                                if 65<=S_kioku12:
                                    S_kioku12=S_kioku12-2
                                if S_kioku13<=180:
                                    S_kioku13=S_kioku13-2
                                kioku_kaisuu=0 

                            elif sen_hand=="f":
                                if 65<=S_kioku12:
                                    S_kioku12=S_kioku12-2
                                kioku_kaisuu=0 
                            
                            elif sen_hand=="v":
                                if 65<=S_kioku12:
                                    S_kioku12=S_kioku12-2
                                if 90<=S_kioku13:
                                    S_kioku13=S_kioku13+2
                                kioku_kaisuu=0 

                            else:
                                kioku_kaisuu+=1

                            fast_servo(12, S_kioku12) 
                            fast_servo(13, S_kioku13)  

                        elif kioku_kaisuu==2:#一瞬のハンドサインでの誤作動をなくす

                            if sen_hand=="g":#RIGHTのときの処理ーーーーーーーーーーーーーーーーーーーーーー

                                if mode2=="atti":#あっち向いてホイの動きーーーーーーーーーーーーーーーーーー
                                    if r==1:
                                        print("敗け") 
                                        print("1")
                                        fast_servo(12, 155)  
                                        sleep(2)
                                        fast_servo(12, 110)
                                        sleep(1) 

                                        fast_servo(12, 155)
                                        fast_servo(13, 180)
                                        sleep(0.5)
                                        fast_servo(12, 65)
                                        sleep(0.5)
                                        fast_servo(12, 155)
                                        sleep(0.5) 
                                        fast_servo(12, 65)
                                        sleep(0.5) 
                                        fast_servo(12, 110)
                                        fast_servo(13, 135)
                                        
                                    elif r==2:
                                        print("勝ち")
                                        print("2")
                                        fast_servo(12, 65)  
                                        sleep(2)
                                        fast_servo(12, 110)
                                        sleep(1)
        
                                        fast_servo(12, 155)
                                        fast_servo(13, 120)
                                        sleep(0.5) 
                                        fast_servo(12, 110)
                                        fast_servo(13, 135)
                                        sleep(0.5) 
                                        fast_servo(12, 65)
                                        fast_servo(13, 120)
                                        sleep(0.5) 
                                        fast_servo(12, 110)
                                        fast_servo(13, 135)
                                    
                                    mode2="nomal"

                                #ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
                                else:#右むく
                                    fast_servo(12, 155)
                                    sleep(2)                              
                                    slow_servo(12, 155, 110, step=1, delay=0.01) 
                                
                                kioku_kaisuu=0

                            elif sen_hand=="u":#FIVEのときの処理ーーーーーーーーーーーーーーーーーーーーーーーーーーー
                                fast_servo(12, 110)
                                kioku_kaisuu=0

                            elif sen_hand=="h":#LEFTのときの処理ーーーーーーーーーーーーーーーーーーーーーーーーーーー
                                if mode2=="atti":#あっち向いてホイの動きーーーーーーーーーーーーーーーーーー
                                    if r==1:
                                        print("勝ち") 
                                        print("3")
                                        fast_servo(12, 155)  
                                        sleep(2)
                                        fast_servo(12, 110)
                                        sleep(1) 

                                        fast_servo(12, 155)
                                        fast_servo(13, 120)
                                        sleep(0.5) 
                                        fast_servo(12, 110)
                                        fast_servo(13, 135)
                                        sleep(0.5) 
                                        fast_servo(12, 65)
                                        fast_servo(13, 120)
                                        sleep(0.5) 
                                        fast_servo(12, 110)
                                        fast_servo(13, 135)


                                    elif r==2:
                                        print("敗け")
                                        print("4")
                                        fast_servo(12, 65)  
                                        sleep(2)
                                        fast_servo(12, 110)
                                        sleep(1)
                           
                                        fast_servo(12, 155)
                                        fast_servo(13, 180)
                                        sleep(0.5)
                                        fast_servo(12, 65)
                                        sleep(0.5)
                                        fast_servo(12, 155)
                                        sleep(0.5) 
                                        fast_servo(12, 65)
                                        sleep(0.5) 
                                        fast_servo(12, 110)
                                        fast_servo(13, 135)
                                    
                                    mode2="nomal"

                                else:
                                    fast_servo(12, 55)
                                    sleep(2)                              
                                    slow_servo(12, 55, 110, step=1, delay=0.01) 
                                
                                kioku_kaisuu=0 

                            

                            else:
                                kioku_kaisuu+=1

                             


                        elif  kioku_kaisuu==10:
                            if sen_hand=="t":#OK
                                mode="sousa" 
                                print("操作モードにきりかえるよ")
                                kioku_kaisuu==0
                                break
                            
                            elif sen_hand=="y":#FIST
                                print("あっちむいて")
                                mode2="atti"
                                S_kioku12_zettai=S_kioku12
                                S_kioku13_zettai=S_kioku13
                                fast_servo(13, 180)
                                sleep(0.5)
                                fast_servo(13, 135)
                                sleep(0.5)
                                fast_servo(13, 180)
                                sleep(0.5)
                                fast_servo(13, S_kioku13_zettai)
                                r=random.randint(1,2)    
                                kioku_kaisuu==0
                                break

                                  
                        elif kioku_kaisuu>=15 and kioku_kaisuu%3==0:#記憶回数が7以上かつ3の倍数
                                pass

                        else:
                            kioku_kaisuu+=1
                                
                    else:#前の手と異なる
                        kioku_hand=sen_hand
                        kioku_kaisuu=0
                #ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー

                #時間的条件に満たし、顔だけ認識しているときの動作ーーーーーーーーーーーーーー
                elif sen_hand==None and sen_face!=None:
                    print(sen_face)
                    #for face in faces:
                            #print(f"X:{int(face.xyz[0]/10)} cm, Y:{int(face.xyz[1]/10)} cm")

                    if sen_face=="w":
                        if S_kioku12<=535:
                            S_kioku12=S_kioku12+2
                        if S_kioku13<=180:
                            S_kioku13=S_kioku13-2
                            
                    elif sen_face=="s":
                        if S_kioku12<=155:
                            S_kioku12=S_kioku12+2

                    elif sen_face=="x":
                        if S_kioku12<=155:
                            S_kioku12=S_kioku12+2
                        if 90<=S_kioku13:
                            S_kioku13=S_kioku13+2


                                          
                    elif sen_face=="e":
                        if S_kioku13<=180:
                            S_kioku13=S_kioku13-2
                
                    elif sen_face=="d":
                        pass     

                    elif sen_face=="c":
                        if 90<=S_kioku13:
                            S_kioku13=S_kioku13+2

                            
                    elif sen_face=="r":
                        if 65<=S_kioku12:
                            S_kioku12=S_kioku12-2
                        if S_kioku13<=180:
                            S_kioku13=S_kioku13-2

                    elif sen_face=="f":
                        if 65<=S_kioku12:
                            S_kioku12=S_kioku12-2
                      
                    elif sen_face=="v":
                        if 65<=S_kioku12:
                            S_kioku12=S_kioku12-2
                        if 90<=S_kioku13:
                            S_kioku13=S_kioku13+2
                        
                    fast_servo(12, S_kioku12) 
                    fast_servo(13, S_kioku13)  

            #print(f"kh_send:{kioku_hand} ")
            #print(kioku_kaisuu)
            #print(S_kioku12)
            #print(S_kioku13)

            key = renderer.waitKey(delay=1)
            if key == 27 or key == ord('q'):
                break

    elif mode=="end": 
        fast_servo(12, 110)
        fast_servo(13, 155)
        break

renderer.exit()
tracker.exit()
ser.close()
pig.hardware_PWM(12, 50, 0)
pig.set_mode(12, pigpio.INPUT)
pig.hardware_PWM(13, 50, 0)
pig.set_mode(13, pigpio.INPUT)
pig.stop()

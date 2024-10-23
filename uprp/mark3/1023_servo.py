#realsenseでデプスフレームとノーマルカメラに赤青マーキング
#赤青誤差少なければ黄色で囲む
#赤色のxyz座標をシリアルでESPに送信
#ラズパイでDCうごかす
#ラズパイーサーボ
#depth,RGB調整済み
#HSV
#シリアルどっちもなしDCのみ
#depth=>xy
#sa-boに数値送れる
#menこれで調整した

import pyrealsense2 as rs
import cv2
import numpy as np
import time
import serial
import sys
import termios
import tty
import simpleaudio as sa
import pigpio

IN1=17
IN2=27
IN3=22
IN4=23
ENA=18
ENB=13
pi=pigpio.pi()
pi.set_mode(IN1,pigpio.OUTPUT)
pi.set_mode(IN2,pigpio.OUTPUT)
pi.set_mode(IN3,pigpio.OUTPUT)
pi.set_mode(IN4,pigpio.OUTPUT)
pi.set_PWM_range(ENA,255)
pi.set_PWM_range(ENB,255)

def fw(speed):
    pi.write(IN1,1)
    pi.write(IN2,0)
    pi.write(IN3,1)
    pi.write(IN4,0)
    pi.set_PWM_dutycycle(ENA,speed)
    pi.set_PWM_dutycycle(ENB,speed)

def bw(speed):
    pi.write(IN1,0)
    pi.write(IN2,1)
    pi.write(IN3,0)
    pi.write(IN4,1)
    pi.set_PWM_dutycycle(ENA,speed)
    pi.set_PWM_dutycycle(ENB,speed)

def right(speed):
    pi.write(IN1,1)
    pi.write(IN2,0)
    pi.write(IN3,0)
    pi.write(IN4,1)
    pi.set_PWM_dutycycle(ENA,speed)
    pi.set_PWM_dutycycle(ENB,speed)

def left(speed):
    pi.write(IN1,0)
    pi.write(IN2,1)
    pi.write(IN3,1)
    pi.write(IN4,0)
    pi.set_PWM_dutycycle(ENA,speed)
    pi.set_PWM_dutycycle(ENB,speed)

def stop():
    pi.write(IN1,0)
    pi.write(IN2,0)
    pi.write(IN3,0)
    pi.write(IN4,0)
    pi.set_PWM_dutycycle(ENA,0)
    pi.set_PWM_dutycycle(ENB,0)



#シリアル関連
#ser1 = serial.Serial('/dev/ttyUSB1', 115200, timeout=1)
ser2 = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

def main():
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 640, 360, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, 640, 360, rs.format.z16, 30)
    pipeline.start(config)
    align_to = rs.stream.color
    align = rs.align(align_to)

    #認識する最大のデプス決める###########################################################################
    max_depth = 2

    depth_filter = rs.threshold_filter()
    depth_filter.set_option(rs.option.min_distance, 0.0)
    depth_filter.set_option(rs.option.max_distance, max_depth)
    color_map = rs.colorizer()

    prev_time = time.time()
    frame_count = 0
    fps = 0

    jyoutai=None
    aka_jyoutai=None
    men_jyoutai=None

    #よろしくおねがいします
    wav_obj = sa.WaveObject.from_wave_file("/home/yaotai/oto/yorosiku.wav")
    play_obj = wav_obj.play()
    #ser2.write(b"v")#サーボ側ESPにｖ送る
    play_obj.wait_done()

    try:
        while True:

            Kin=input("角度:")
            if Kin.lower()=='q':
                break
            
            if Kin.isdigit():
                ser2.write(Kin.encode('utf-8'))
                ser2.write(b'\n')
                print(f"{Kin}送信")
                
            frames = pipeline.wait_for_frames()
            aligned_frames = align.process(frames)

            color_frame = aligned_frames.get_color_frame()
            depth_frame = aligned_frames.get_depth_frame()

            if not depth_frame or not color_frame:
                continue

            filtered_depth = depth_filter.process(depth_frame)
            colorized_depth = color_map.process(filtered_depth)
            color_img = np.asanyarray(color_frame.get_data())
            depth_img = np.asanyarray(colorized_depth.get_data())
            depth_img_single = cv2.cvtColor(depth_img, cv2.COLOR_BGR2GRAY)
            _, depth_mask = cv2.threshold(depth_img_single, max_depth, 255, cv2.THRESH_BINARY)
            depth_height, depth_width = depth_img.shape[:2]
            color_resized = cv2.resize(color_img, (depth_width, depth_height), interpolation=cv2.INTER_LINEAR)
            depth_mask_resized = cv2.resize(depth_mask, color_resized.shape[1::-1], interpolation=cv2.INTER_NEAREST)
            color_masked = np.zeros_like(color_resized)
            color_masked[depth_mask_resized == 255] = color_resized[depth_mask_resized == 255]
            hsv_img = cv2.cvtColor(color_masked, cv2.COLOR_BGR2HSV)

            # 赤色の範囲を定義#####################################################################
            lower_red1 = np.array([0, 200, 90])
            upper_red1 = np.array([80, 240, 110])
            lower_red2 = np.array([120, 100, 100])
            upper_red2 = np.array([180, 200, 150])

            # 青色の範囲を定義#####################################################################
            lower_blue1 = np.array([100, 200, 100])
            upper_blue1 = np.array([120, 260, 120])
            lower_blue2 = np.array([180, 200, 50])
            upper_blue2 = np.array([190, 240, 70])

            mask_red1 = cv2.inRange(hsv_img, lower_red1, upper_red1)
            mask_red2 = cv2.inRange(hsv_img, lower_red2, upper_red2)
            red_mask = cv2.bitwise_or(mask_red1, mask_red2)
            mask_blue1 = cv2.inRange(hsv_img, lower_blue1, upper_blue1)
            mask_blue2 = cv2.inRange(hsv_img, lower_blue2, upper_blue2)
            blue_mask = cv2.bitwise_or(mask_blue1, mask_blue2)
            red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # 最大の赤色領域を探す
            max_area_red = 0
            largest_contour_red = None
            for contour_red in red_contours:
                area_red = cv2.contourArea(contour_red)
                if area_red > max_area_red:
                    max_area_red = area_red
                    largest_contour_red = contour_red

            # 最大の青色領域を探す
            max_area_blue = 0
            largest_contour_blue = None
            for contour_blue in blue_contours:
                area_blue = cv2.contourArea(contour_blue)
                if area_blue > max_area_blue:
                    max_area_blue = area_blue
                    largest_contour_blue = contour_blue

            # 結果画像を初期化
            output_img = color_resized.copy()
            center_offset = (depth_width // 2, depth_height // 2)

            # 最大の赤色領域とそのバウンディングボックスを描画
            if largest_contour_red is not None:
                bounding_rect_red = cv2.boundingRect(largest_contour_red)
                cv2.rectangle(output_img, bounding_rect_red, (0, 0, 255), 2)

                # バウンディングボックスの中心を計算
                center_red = (bounding_rect_red[0] + bounding_rect_red[2] // 2,
                             bounding_rect_red[1] + bounding_rect_red[3] // 2)

                # (0, 0) を中心にし、Y軸を逆にした座標系に変換
                center_in_screen_red = (center_red[0] - center_offset[0], center_offset[1] - center_red[1])

                # 赤色領域の中心の深度値を確認
                if 0 <= center_red[0] < depth_width and 0 <= center_red[1] < depth_height:
                    depth_value_red = depth_frame.get_distance(center_red[0], center_red[1])  # 赤色領域の中心の深度値を取得
                    print(f"Red Center: ({center_in_screen_red[0]}, {center_in_screen_red[1]}, {depth_value_red})")

                    if depth_value_red > 1.5 and depth_value_red < 2:#1.5<depth<2
                        if center_in_screen_red[0] > 140:#ｘ>130
                            right(150)
                            print("超右1.5~2")
                        
                        elif center_in_screen_red[0] <= 140 and center_in_screen_red[0] >= 100:#60<ｘ<130
                            right(100)
                            print("右1.5~2")
                        
                        elif center_in_screen_red[0] < 100 and center_in_screen_red[0] > 0:#40<ｘ<60
                            fw(255)
                            print("超前1.5~2")

                        elif center_in_screen_red[0] < 0 and center_in_screen_red[0] > -40:#-30<ｘ<40
                            left(100)
                            print("左1.5~2")

                        else:
                            left(150)
                            print("超左1.5~2")

                    elif depth_value_red >= 1 and depth_value_red <= 1.5:#1<depth<1.5
                        if center_in_screen_red[0] > 140:#ｘ>130
                            right(150)
                            print("超右1~1.5")
                        
                        elif center_in_screen_red[0] <= 140 and center_in_screen_red[0] >= 100:#60<ｘ<130
                            right(100)
                            print("右1~1.5")
                        
                        elif center_in_screen_red[0] < 100 and center_in_screen_red[0] > 0:#40<ｘ<60
                            fw(255)
                            print("超前1~1.5")

                        elif center_in_screen_red[0] < 0 and center_in_screen_red[0] > -40:#-30<ｘ<40
                            left(100)
                            print("左1~1.5")

                        else:
                            left(150)
                            print("超左1~1.5")

                    elif depth_value_red > 0.5 and depth_value_red < 1:#0.5<depth<1
                        if center_in_screen_red[0] > 140:#ｘ>130
                            right(150)
                            print("超右0.5~1")
                        
                        elif center_in_screen_red[0] <= 140 and center_in_screen_red[0] >= 100:#60<ｘ<130
                            right(100)
                            print("右0.5~1")
                        
                        elif center_in_screen_red[0] < 100 and center_in_screen_red[0] > 0:#40<ｘ<60
                            fw(255)
                            print("超前0.5~1")

                        elif center_in_screen_red[0] < 0 and center_in_screen_red[0] > -40:#-30<ｘ<40
                            left(100)
                            print("左0.5~1")

                        else:
                            left(150)
                            print("超左0.5~1")

                    elif depth_value_red > 0.3 and depth_value_red < 0.5:#men
                        stop()  
                        print("止まれ0.3~0.5")

                        curr_time = time.time()
                        elapsed_time = curr_time - prev_time
                        print(elapsed_time)
                        if elapsed_time >= 3:
                            prev_time = curr_time
                            wav_obj = sa.WaveObject.from_wave_file("/home/yaotai/oto/mendoukote.wav")
                            play_obj = wav_obj.play()
                            #ser2.write(b"o")
                            print("メンドウコテスタート")

                    elif depth_value_red >= 0 and depth_value_red < 0.3:#0<depth<0.5     
                        if center_in_screen_red[0] > 140:#ｘ>130
                            right(150)
                            print("超右0~0.3")
                        
                        elif center_in_screen_red[0] <= 140 and center_in_screen_red[0] >= 100:#60<ｘ<130
                            right(100)
                            print("右0~0.3")
                        
                        elif center_in_screen_red[0] < 100 and center_in_screen_red[0] > 0:#40<ｘ<60
                            bw(255)  
                            print("後ろ0~0.3")

                        elif center_in_screen_red[0] < 0 and center_in_screen_red[0] > -40:#-30<ｘ<40
                            left(100)
                            print("左0~0.3")

                        else:
                            left(150)
                            print("超左0~0.3")

                    # 中心に赤い点を描画
                    cv2.circle(output_img, center_red, 5, (0, 0, 255), -1)  # 赤い点を描画
            else:
                stop()
                print("あかなし")

            # 画像のサイズを取得 (color_resized または depth_img から)
            height, width = color_resized.shape[:2]

            # (0, 0) を中心とし、Y軸を逆にした座標系に基づく変換
            # X軸とY軸に線を描画
            cv2.line(img=output_img, pt1=(0, center_offset[1]), pt2=(width, center_offset[1]), color=(255, 255, 255), thickness=1)  # X軸
            cv2.line(img=output_img, pt1=(center_offset[0], 0), pt2=(center_offset[0], height), color=(255, 255, 255), thickness=1)  # Y軸

            # 特定のX座標に垂直線を描画 (新しい座標系で)
            cv2.line(img=output_img, pt1=(center_offset[0] + 140, 0), pt2=(center_offset[0] + 140, height), color=(0, 255, 0), thickness=1)  # X = 100の位置
            cv2.line(img=output_img, pt1=(center_offset[0] - 40, 0), pt2=(center_offset[0] - 40, height), color=(0, 255, 0), thickness=1)  # X = -100の位置
            cv2.line(img=output_img, pt1=(center_offset[0] + 0, 0), pt2=(center_offset[0] + 0, height), color=(0, 255, 0), thickness=1)  # X = 40の位置
            cv2.line(img=output_img, pt1=(center_offset[0] + 100, 0), pt2=(center_offset[0] + 100, height), color=(0, 255, 0), thickness=1)  # X = 60の位置

            # 最大の青色領域とそのバウンディングボックスを描画
            if largest_contour_blue is not None:
                bounding_rect_blue = cv2.boundingRect(largest_contour_blue)
                cv2.rectangle(output_img, bounding_rect_blue, (255, 0, 0), 2)  # 青の矩形を描画

                # バウンディングボックスの中心を計算
                center_blue = (bounding_rect_blue[0] + bounding_rect_blue[2] // 2,
                              bounding_rect_blue[1] + bounding_rect_blue[3] // 2)

                # (0, 0) を中心にし、Y軸を逆にした座標系に変換
                center_in_screen_blue = (center_blue[0] - center_offset[0], center_offset[1] - center_blue[1])

                # 青色領域の中心の深度値を確認
                if 0 <= center_blue[0] < depth_width and 0 <= center_blue[1] < depth_height:
                    depth_value_blue = depth_frame.get_distance(center_blue[0], center_blue[1])  # 青色領域の中心の深度値を取得

                    if depth_value_blue < max_depth:  # 深度値が2メートル未満
                        # 青色領域の中心の座標を新しい座標系で出力
                        #print(f"Blue Center: ({center_in_screen_blue[0]}, {center_in_screen_blue[1]}, {depth_value_blue})")

                        # 中心に青い点を描画
                        cv2.circle(output_img, center_blue, 5, (255, 0, 0), -1)  # 青い点を描画
                        
            # 赤と青のx軸の誤差を計算
            if largest_contour_red is not None:
                if largest_contour_blue is not None:
                    x_diff = abs(center_red[0] - center_blue[0])
                    if x_diff <=  80:
                        # 黄色で両方の領域を囲む
                        combined_rect = cv2.boundingRect(np.concatenate((largest_contour_red, largest_contour_blue)))
                        cv2.rectangle(output_img, combined_rect, (0, 255, 255), 2)  # 黄色の矩形を描画

                        # 黄色の矩形の中心を計算
                        center_combined = (combined_rect[0] + combined_rect[2] // 2,
                                        combined_rect[1] + combined_rect[3] // 2)

                        # (0, 0) を中心にし、Y軸を逆にした座標系に変換
                        center_in_screen_center_combined = (center_combined[0] - center_offset[0], center_offset[1] - center_blue[1])


                        # 中心に黄色い点を描画
                        cv2.circle(output_img, center_combined, 5, (0, 255, 255), -1)  # 黄色い点を描画
                        # 黄色点の座標を出力
                        #print(f"敵 Center: ({center_in_screen_center_combined[0]}, {center_in_screen_center_combined[1]})")

                        data = f"{center_in_screen_red[0]},{center_in_screen_red[1]},{depth_value_red}"

            else:
                jyoutai=None
                #print(jyoutai)        

            # FPSを計算
            #curr_time = time.time()
            #elapsed_time = curr_time - prev_time
            #frame_count += 1
            #if elapsed_time >= 0.1:
            #    fps = frame_count / elapsed_time
            #    frame_count = 0
            #    prev_time = curr_time

                # FPSをコンソールに表示
                #print(f"FPS: {fps:.2f}")

                # FPSを画像に表示
                #cv2.putText(output_img, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # 結果を表示
            #cv2.imshow("Depth Frame", depth_img)  # 深度フレームを表示
            cv2.imshow("Masked Result", output_img)  # 最大の赤色と青色領域を強調した結果を表示

            if cv2.waitKey(1) & 0xff == 27:#ESCで終了
                cv2.destroyAllWindows()
                break


    finally:
        stop()
        #ser2.write(b"v")
        #ser1.close()
        ser2.close()
        data = f"0,0,0"
        # データを送信
        #ser.write((data + "\n").encode())
        wav_obj = sa.WaveObject.from_wave_file("/home/yaotai/oto/arigatou.wav")
        play_obj = wav_obj.play()
        play_obj.wait_done()

        # パイプラインを停止
        pipeline.stop()


if __name__ == "__main__":
    main()

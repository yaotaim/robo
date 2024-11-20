#停止なし
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


IN1, IN2, IN3, IN4 = 17, 27, 22, 23
ENA, ENB = 18, 13

pi = pigpio.pi()
for pin in [IN1, IN2, IN3, IN4]:
    pi.set_mode(pin, pigpio.OUTPUT)
for pwm_pin in [ENA, ENB]:
    pi.set_PWM_range(pwm_pin, 255)

def motor(direction, speed=128):
    settings = {
        'fw': (1, 0, 1, 0),
        'bw': (0, 1, 0, 1),
        'right': (1, 0, 0, 1),
        'left': (0, 1, 1, 0),
        'stop': (0, 0, 0, 0)
    }
    if direction in settings:
        states = settings[direction]
        pi.write(IN1, states[0])
        pi.write(IN2, states[1])
        pi.write(IN3, states[2])
        pi.write(IN4, states[3])
        pi.set_PWM_dutycycle(ENA, speed if direction != 'stop' else 0)
        pi.set_PWM_dutycycle(ENB, speed if direction != 'stop' else 0)

def find_largest_contour(contours):
    max_area = 0
    largest_contour = None
    for contour in contours:
        area = cv2.contourArea(contour)
        #print(f"大きさ:{area}")
        if area > max_area:
            if 0.5<=area<1000:
                max_area = area
                largest_contour = contour
    return max_area, largest_contour

def process_contour(contour, output_img, color, center_offset, depth_frame, depth_width, depth_height):
    if contour is not None:
        bounding_rect = cv2.boundingRect(contour)# バウンディングボックスを取得して描画
        cv2.rectangle(output_img, bounding_rect, color, 2)
        center = (bounding_rect[0] + bounding_rect[2] // 2, bounding_rect[1] + bounding_rect[3] // 2)# 中心座標を計算
        adjusted_center = (center[0] - center_offset[0], center_offset[1] - center[1])
        cv2.circle(output_img, center, 5, color, -1)# 中心に円を描画
        if 0 <= center[0] < depth_width and 0 <= center[1] < depth_height:# 距離を取得
            distance = depth_frame.get_distance(center[0], center[1])
        else:
            distance = None
        return adjusted_center, distance
    else:
        return (None, None), None

def getch():
    # ユーザーのキーボード入力を取得する関数
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def send_sound(action, angle, angle2, sound_file):
    ser.write(f"{action} {angle} {angle2}\n".encode())
    print(f"送信: {action} {angle} {angle2}")
    wav_obj = sa.WaveObject.from_wave_file(sound_file)
    play_obj = wav_obj.play()

def men1():
    global waza, curr_time, prev_time
    curr_time = time.time()
    elapsed_time = curr_time - prev_time
    if elapsed_time >= 3:
        motor('stop')
        print("止まれ0.3~0.5")
        print("面１")
        angle = str(int(-0.1265 * c_r[0] + 95.276) - 5)
        if c_b[0] is not None:
            angle2 = str(int(-0.1265 * c_b[0] + 95.276) - 5)
        elif c_y[0] is not None:
            angle2 = str(int(-0.1265 * c_y[0] + 95.276) - 5)
        else:
            angle2 = angle
        send_sound('y', angle, angle2, "/home/yaotai/oto/men2.wav")
        time.sleep(cstop)
        waza = 1
        curr_time = time.time()
        prev_time = curr_time

def dou1():
    global waza, curr_time, prev_time
    curr_time = time.time()
    elapsed_time = curr_time - prev_time
    if elapsed_time >= 3:
        motor('stop')
        print("胴１")
        angle = str(int(0.0892 * c_b[1] + 126.92))
        angle2 = str(int(-0.1265 * c_b[0] + 95.276) - 5)
        send_sound('u', angle, angle2, "/home/yaotai/oto/dou2.wav")
        time.sleep(cstop)
        waza = 2
        curr_time = time.time()
        prev_time = curr_time

def kote1():
    global waza, curr_time, prev_time
    print(f"Yellow Center: ({c_y[0]}, {c_y[1]}, {d_y:.3f})")
    curr_time = time.time()
    elapsed_time = curr_time - prev_time
    if elapsed_time >= 3:
        motor('stop')
        print("小手１")
        angle = str(int(0.0892 * c_y[1] + 126.92))
        angle2 = str(int(-0.1265 * c_y[0] + 95.276) - 5)
        send_sound('i', angle, angle2, "/home/yaotai/oto/kote2.wav")
        time.sleep(cstop)
        waza = 3
        curr_time = time.time()
        prev_time = curr_time

def men2():
    global curr_time, prev_time
    print(f"Red Center: ({c_r[0]}, {c_r[1]}, {d_r:.3f})")
    k_c_r = (c_r[0], c_r[1])
    print("面2")
    angle = str(int(-0.1265 * c_r[0] + 95.276) - 5)
    angle2 = angle
    send_sound('y', angle, angle2, "/home/yaotai/oto/men2.wav")
    if d_r < 0.4:
        motor('bw', 200)
    elif 0.4 <= d_r <= 0.8:
        motor('stop')
    else:
        motor('fw', 200)
    time.sleep(cstop)
    motor('stop')
    curr_time = time.time()
    prev_time = curr_time

def dou2():
    global curr_time, prev_time
    print(f"Blue Center: ({c_b[0]}, {c_b[1]}, {d_b:.3f})")
    k_c_b = (c_b[0], c_b[1])
    print("胴2")
    angle = str(int(0.0892 * c_b[1] + 126.92) - 3)
    angle2 = str(int(-0.1265 * c_b[0] + 95.276) - 5)
    send_sound('u', angle, angle2, "/home/yaotai/oto/dou2.wav")
    if d_b < 0.4:
        motor('bw', 200)
    elif 0.4 <= d_b <= 0.8:
        motor('stop')
    else:
        motor('fw', 200)
    time.sleep(cstop)
    motor('stop')
    curr_time = time.time()
    prev_time = curr_time   


def kote2():
    global curr_time, prev_time
    print(f"Yellow Center: ({c_y[0]}, {c_y[1]}, {d_y:.3f})")
    k_c_y = (c_y[0], c_y[1])
    print("小手2")
    angle = str(int(0.0892 * c_y[1] + 126.92))
    angle2 = str(int(-0.1265 * c_y[0] + 95.276) - 5)
    send_sound('i', angle, angle2, "/home/yaotai/oto/kote2.wav")
    if d_y < 0.4:
        motor('bw', 200)
    elif 0.4 <= d_y <= 0.8:
        motor('stop')
    else:
        motor('fw', 200)
    time.sleep(cstop)
    motor('stop')
    curr_time = time.time()
    prev_time = curr_time


ser = serial.Serial('/dev/ttyUSB1', 115200, timeout=1)
ser1 = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

def main():
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 640, 360, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, 640, 360, rs.format.z16, 30)
    pipeline.start(config)
    align_to = rs.stream.color
    align = rs.align(align_to)
    max_depth = 1.5

    depth_filter = rs.threshold_filter()
    depth_filter.set_option(rs.option.min_distance, 0.0)
    depth_filter.set_option(rs.option.max_distance, max_depth)
    color_map = rs.colorizer()

    prev_time = time.time()

    waza=0
    strt=0
    mode=None
    nigeru=None
    mati_min=0.4
    mati=0.8
    cstop=0.2
    d_r=None
    d_b=None
    d_y=None

    try:
        while True:
            if ser1.in_waiting > 0:
                data = ser1.readline().decode('utf-8', errors='ignore').rstrip()
                print(f"受信したデータ: {data}")
                if data == "1":#左前ｘ
                    mode=="1"
                    motor('stop') 
                    time.sleep(0.2)    
                    ser1.write(b"1")
                    motor('bw',255)
                    time.sleep(0.5)
                    motor('right',255)
                    time.sleep(2)
                    motor('fw',255)
                    ser1.write(b"2")

                elif data =="2":#右前ｘ
                    mode=="2"
                    motor('stop') 
                    time.sleep(0.5)
                    ser1.write(b"1")
                    motor('bw',255)
                    time.sleep(0.5)
                    motor('left',255)
                    time.sleep(2)
                    motor('fw',255)
                    ser1.write(b"2")

                elif data =="3":#前ｘ
                    mode=="3"
                    motor('stop') 
                    time.sleep(0.5)
                    ser1.write(b"1")
                    motor('bw',255)
                    time.sleep(0.5)
                    motor('right',255)
                    time.sleep(2)
                    motor('fw',255)
                    ser1.write(b"2")
                
                if data == "4":#左後ろｘ
                    mode=="4"
                    motor('stop') 
                    time.sleep(0.5)
                    ser1.write(b"1")
                    motor('right',255)
                    time.sleep(0.2)
                    motor('fw',255)
                    time.sleep(0.2)
                    ser1.write(b"2")
                    waza=0
                    nigeru=None
    
                elif data =="5":#右後ろｘ
                    mode=="5"
                    motor('stop') 
                    time.sleep(0.5)
                    ser1.write(b"1")
                    motor('left',255)
                    time.sleep(0.2)
                    motor('fw',255)
                    time.sleep(0.2)
                    ser1.write(b"2")
                    waza=0
                    nigeru=None

                elif data =="6":#後ろｘ
                    mode=="6"
                    motor('stop') 
                    time.sleep(0.5)
                    ser1.write(b"1")
                    motor('fw',255)
                    time.sleep(0.5)
                    ser1.write(b"2")
                    waza=0
                    nigeru=None
                
                elif data =="7":#後ろ敵
                    mode=="7"
                    ser1.write(b"1")
                    motor('right',255)
                    time.sleep(2.2)
                    ser1.write(b"2")
                    motor('stop')
                
                elif data =="8":#左敵
                    mode=="8"
                    ser1.write(b"1")
                    motor('left',255)
                    time.sleep(1.3)
                    ser1.write(b"2")
                    motor('stop')

                
                elif data =="9":#右敵
                    mode=="9"
                    ser1.write(b"1")
                    motor('right',255)
                    time.sleep(0.7)
                    ser1.write(b"2")
                    motor('stop')

                elif data =="w":#正常
                    mode=="w"
                    #motor('stop')
                    motor('fw',255)
            
            elif strt==0:       
                n=int(input())
                if n==1:
                    strt=1
                    wav_obj = sa.WaveObject.from_wave_file("/home/yaotai/oto/yorosiku2.wav")#よろしくおねがいします
                    play_obj = wav_obj.play()
                    ser.write(f"v 0 0\n".encode())
                    print(f"送信:v 0 0")
                    play_obj.wait_done()
                    motor('fw',255)
            
            else:
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

                output_img = color_resized.copy()
                center_offset = (depth_width // 2, depth_height // 2)
                height, width = color_resized.shape[:2]

                cv2.line(img=output_img, pt1=(0, center_offset[1]), pt2=(width, center_offset[1]), color=(255, 255, 255), thickness=1)  # X軸
                cv2.line(img=output_img, pt1=(center_offset[0], 0), pt2=(center_offset[0], height), color=(255, 255, 255), thickness=1)  # Y軸
                cv2.line(img=output_img, pt1=(center_offset[0] + 140, 0), pt2=(center_offset[0] + 140, height), color=(0, 255, 0), thickness=1)  # X = 100の位置
                cv2.line(img=output_img, pt1=(center_offset[0] - 40, 0), pt2=(center_offset[0] - 40, height), color=(0, 255, 0), thickness=1)  # X = -100の位置
                cv2.line(img=output_img, pt1=(center_offset[0] + 0, 0), pt2=(center_offset[0] + 0, height), color=(0, 255, 0), thickness=1)  # X = 40の位置
                cv2.line(img=output_img, pt1=(center_offset[0] + 100, 0), pt2=(center_offset[0] + 100, height), color=(0, 255, 0), thickness=1)  # X = 60の位置
                
                lower_red1 = np.array([0, 103, 92])
                upper_red1 = np.array([2, 163, 152])
                lower_red2 = np.array([177, 93, 95])
                upper_red2 = np.array([179, 153, 155])
 
                lower_blue = np.array([104, 104, 57])
                upper_blue = np.array([108, 164, 117])
 
                lower_yellow = np.array([20, 140, 128])
                upper_yellow = np.array([24, 200, 188])

                mask_red1 = cv2.inRange(hsv_img, lower_red1, upper_red1)
                mask_red2 = cv2.inRange(hsv_img, lower_red2, upper_red2)
                red_mask = cv2.bitwise_or(mask_red1, mask_red2)
                blue_mask= cv2.inRange(hsv_img, lower_blue, upper_blue)
                yellow_mask= cv2.inRange(hsv_img, lower_yellow, upper_yellow)
            
                red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                yellow_contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                max_area_red, largest_contour_red = find_largest_contour(red_contours)
                max_area_blue, largest_contour_blue = find_largest_contour(blue_contours)
                max_area_yellow, largest_contour_yellow = find_largest_contour(yellow_contours)

                c_r, d_r = process_contour(largest_contour_red, output_img, (0, 0, 255), center_offset, depth_frame, depth_width, depth_height)
                c_b, d_b = process_contour(largest_contour_blue, output_img, (255, 0, 0), center_offset, depth_frame, depth_width, depth_height)
                c_y, d_y = process_contour(largest_contour_yellow, output_img, (0, 255, 255), center_offset, depth_frame, depth_width, depth_height)

                if waza==0:#技なし
                    if c_r[0] is not None and c_r[1] is not None and d_r is not None:#赤発見
                        print(f"Red   Center: ({c_r[0]}, {c_r[1]}, {d_r:.3f})")
                        k_c_r=(c_r[0],c_r[1])
                        
                        if 1.1 < d_r < 1.2:
                            if c_r[0] > 140: 
                                motor('right',130)
                                print("超右1.5~2")
                            elif 100 <= c_r[0] <= 140: 
                                motor('right',100)
                                print("右1.5~2")
                            elif 0 < c_r[0] < 100: 
                                motor('fw',255)
                                print("超前1.5~2")
                            elif -40 < c_r[0] < 0:  
                                motor('left',100)
                                print("左1.5~2")
                            else:
                                motor('left',150)
                                print("超左1.5~2")

                        elif 1 <= d_r <= 1.1:
                            if c_r[0] > 140:
                                motor('right',130)
                                print("超右1~1.5")
                            elif 100 <= c_r[0] <= 140:
                                motor('right',100)
                                print("右1~1.5")
                            elif 0 < c_r[0] < 100:
                                motor('fw',255)
                                print("超前1~1.5")
                            elif -40 < c_r[0] < 0:
                                motor('left',100)
                                print("左1~1.5")
                            else:
                                motor('left',150)
                                print("超左1~1.5")

                        elif 0.6 < d_r < 1:
                            if c_r[0] > 140:
                                motor('right',150)
                                print("超右0.5~1")
                            elif 100 <= c_r[0] <= 140:
                                motor('right',100)
                                print("右0.5~1")
                            elif 0 < c_r[0] < 100:
                                motor('fw',255)
                                print("超前0.5~1")
                            elif -40 < c_r[0] < 0:
                                motor('left',100)
                                print("左0.5~1")
                            else:
                                motor('left',150)
                                print("超左0.5~1")

                        elif 0.4 <= d_r <= 0.6:
                            men1()

                        elif 0 <= d_r < 0.4:
                            if c_r[0] > 140:
                                motor('right',150)
                                print("超右0~0.3")
                            elif 100 <= c_r[0] <= 140:
                                motor('right',100)
                                print("右0~0.3")
                            elif 0 < c_r[0] < 100:
                                motor('bw',255)
                                print("後ろ0~0.3")
                            elif -40 < c_r[0] < 0:
                                motor('left',100)
                                print("左0~0.3")
                            else:
                                motor('left',150)
                                print("超左0~0.3")

                    elif c_b[0] is not None and c_b[1] is not None and d_b is not None:#青発見
                        print(f"Blue  Center: ({c_b[0]}, {c_b[1]}, {d_b:.3f})")
                        k_c_b=(c_b[0],c_b[1])

                        if 1.1 < d_b < 1.2:
                            if c_b[0] > 140: 
                                motor('right',100)
                                print("超右1.5~2")
                            elif 100 <= c_b[0] <= 140: 
                                motor('right',90)
                                print("右1.5~2")
                            elif 0 < c_b[0] < 100: 
                                motor('fw',255)
                                print("超前1.5~2")
                            elif -40 < c_b[0] < 0:  
                                motor('left',90)
                                print("左1.5~2")
                            else:
                                motor('left',100)
                                print("超左1.5~2")

                        elif 1 <= d_b <= 1.1:
                            if c_b[0] > 140:
                                motor('right',100)
                                print("超右1~1.5")
                            elif 100 <= c_b[0] <= 140:
                                motor('right',90)
                                print("右1~1.5")
                            elif 0 < c_b[0] < 100:
                                motor('fw',255)
                                print("超前1~1.5")
                            elif -40 < c_b[0] < 0:
                                motor('left',90)
                                print("左1~1.5")
                            else:
                                motor('left',100)
                                print("超左1~1.5")

                        elif 0.55 < d_b < 1:   
                            if c_b[0] > 140:
                                motor('right',100)
                                print("超右0.5~1")
                            elif 100 <= c_b[0] <= 140:
                                motor('right',90)
                                print("右0.5~1")
                            elif 0 < c_b[0] < 100:
                                motor('fw',255)
                                print("超前0.5~1")
                            elif -40 < c_b[0] < 0:
                                motor('left',90)
                                print("左0.5~1")
                            else:
                                motor('left',100)
                                print("超左0.5~1")

                        elif 0.4 <= d_b <= 0.55:
                            dou1()

                        elif 0 <= d_b < 0.3:
                            if c_b[0] > 140:
                                motor('right',100)
                                print("超右0~0.3")
                            elif 100 <= c_b[0] <= 140:
                                motor('right',90)
                                print("右0~0.3")
                            elif 0 < c_b[0] < 100:
                                motor('bw',255)
                                print("後ろ0~0.3")
                            elif -40 < c_b[0] < 0:
                                motor('left',90)
                                print("左0~0.3")
                            else:
                                motor('left',100)
                                print("超左0~0.3")

                    elif c_y[0] is not None and c_y[1] is not None and d_y is not None:#黃発見
                        k_c_y=(c_y[0],c_y[1])
                        if 1.1 < d_y < 1.2:
                            print(f"yellow Center: ({c_y[0]}, {c_y[1]}, {d_y:.3f})")
                            if c_y[0] > 140: 
                                motor('right',100)
                                print("超右1.5~2")
                            elif 100 <= c_y[0] <= 140: 
                                motor('right',90)
                                print("右1.5~2")
                            elif 0 < c_y[0] < 100: 
                                motor('fw',255)
                                print("超前1.5~2")
                            elif -40 < c_y[0] < 0:  
                                motor('left',90)
                                print("左1.5~2")
                            else:
                                motor('left',100)
                                print("超左1.5~2")

                        elif 1 <= d_y <= 1.5:
                            print(f"yellow Center: ({c_y[0]}, {c_y[1]}, {d_y:.3f})")
                            if c_y[0] > 140:
                                motor('right',100)
                                print("超右1~1.5")
                            elif 100 <= c_y[0] <= 140:
                                motor('right',90)
                                print("右1~1.5")
                            elif 0 < c_y[0] < 100:
                                motor('fw',255)
                                print("超前1~1.5")
                            elif -40 < c_y[0] < 0:
                                motor('left',90)
                                print("左1~1.5")
                            else:
                                motor('left',100)
                                print("超左1~1.5")

                        elif 0.6 < d_y < 1:
                            print(f"yellow Center: ({c_y[0]}, {c_y[1]}, {d_y:.3f})")
                            if c_y[0] > 140:
                                motor('right',100)
                                print("超右0.5~1")
                            elif 100 <= c_y[0] <= 140:
                                motor('right',90)
                                print("右0.5~1")
                            elif 0 < c_y[0] < 100:
                                motor('fw',255)
                                print("超前0.5~1")
                            elif -40 < c_y[0] < 0:
                                motor('left',90)
                                print("左0.5~1")
                            else:
                                motor('left',100)
                                print("超左0.5~1")

                        elif 0.5 <= d_y <= 0.6:
                            kote1()

                        # elif 0 <= d_y < 0.3:
                        #     if c_y[0] > 140:
                        #         motor('right',150)
                        #         print("超右0~0.3")
                        #     elif 100 <= c_y[0] <= 140:
                        #         motor('right',100)
                        #         print("右0~0.3")
                        #     elif 0 < c_y[0] < 100:
                        #         motor('bw',255)
                        #         print("後ろ0~0.3")
                        #     elif -40 < c_y[0] < 0:
                        #         motor('left',100)
                        #         print("左0~0.3")
                        #     else:
                        #         motor('left',150)
                        #         print("超左0~0.3")
                    
                    else:
                        motor('fw',255)
                        print("まっすぐ")


                elif waza==1:#面１のあと
                    curr_time = time.time()
                    elapsed_time = curr_time - prev_time
                    #print(elapsed_time)
                    if mati_min <= elapsed_time <= mati:#時間内に色発見＝＞座標に
                        if c_b[0] is not None and c_b[1] is not None and d_b is not None:#胴2
                            dou2()
                            waza=4

                        elif c_y[0] is not None and c_y[1] is not None and d_y is not None:#小手2
                            kote2()
                            waza=5
                            
                    elif elapsed_time>mati:#時間内に色発見できなかった＝＞適当に胴    
                        print("胴2_適当")
                        angle=str((int(0.0892*k_c_r[1]+126.92))-10)
                        angle2=str(int(-0.1265*k_c_r[0]+95.276)-5)
                        send_sound('u', angle, angle2, "/home/yaotai/oto/dou2.wav")                 
                        time.sleep(cstop)
                        curr_time = time.time()
                        prev_time = curr_time
                        waza=4  

                elif waza==2:#胴１のあと
                    curr_time = time.time()
                    elapsed_time = curr_time - prev_time
                    #print(elapsed_time)      
                    if mati_min <= elapsed_time <= mati:#時間内に色発見＝＞座標に
                        if c_r[0] is not None and c_r[1] is not None and d_r is not None:#赤発見2
                            men2()
                            waza=6
                       
                        elif c_y[0] is not None and c_y[1] is not None and d_y is not None:#黃発見2
                            kote2()
                            waza=7

                    elif elapsed_time>mati:#時間内に色発見できなかった
                        motor('stop')
                        print("面２＿適当")
                        angle=str(int(-0.1265*k_c_b[0]+95.276)-5)
                      
                        if c_b[0] is not None: 
                            angle2=str(int(-0.1265*c_b[0]+95.276)-5)
                        elif c_y[0] is not None: 
                            angle2=str(int(-0.1265*c_y[0]+95.276)-5)
                        else:
                            angle2=angle

                        send_sound('y', angle, angle2, "/home/yaotai/oto/men2.wav")
                        waza=6
                        time.sleep(cstop)
                        curr_time = time.time()
                        prev_time = curr_time
                            
                elif waza==3:#小手１のあと
                    curr_time = time.time()
                    elapsed_time = curr_time - prev_time
                    #print(elapsed_time)
                    if mati_min <= elapsed_time <= mati:#時間内に色発見＝＞座標に
                        if c_r[0] is not None and c_r[1] is not None and d_r is not None:#赤発見2
                            men2()
                            waza=8
                        
                        elif c_b[0] is not None and c_b[1] is not None and d_b is not None:#青発見2
                            dou2()
                            waza=9
                        
                    elif elapsed_time>mati:#時間内に色発見できなかった＝＞適当に胴    
                        print("胴2_適当")
                        angle=str((int(0.0892*k_c_y[1]+126.92)))
                        angle2=str(int(-0.1265*k_c_y[0]+95.276)-5)
                        send_sound('u', angle, angle2, "/home/yaotai/oto/dou2.wav")
                        waza=9
                        time.sleep(cstop)
                        motor('stop')
                        curr_time = time.time()
                        prev_time = curr_time
                    
                elif waza==7 or waza==9:#最後の面
                    curr_time = time.time()
                    elapsed_time = curr_time - prev_time
                    #print(elapsed_time)
                    
                    if mati_min <= elapsed_time <= mati:#時間内に色発見＝＞座標に
                        if c_r[0] is not None and c_r[1] is not None and d_r is not None:#赤発見3
                            print(f"Red   Center: ({c_r[0]}, {c_r[1]}, {d_r:.3f})")
                            k_c_r=(c_r[0],c_r[1])
                            print("面３")
                            angle=str(int(-0.1265*c_r[0]+95.276)-5)
                            angle2=angle
                            send_sound('y', angle, angle2, "/home/yaotai/oto/men2.wav")
                            waza=10
                            if d_r < 0.4:
                                motor('fw',200)
                            elif 0.4 <= d_r <= 0.8:
                                motor('stop')
                            else:
                                motor('bw',200)
                            time.sleep(0.5)
                            motor('bw',255)
                            print("逃げる")
                            curr_time = time.time()
                            prev_time = curr_time
                            
                    elif elapsed_time>mati:#時間内に色発見できなかった＝＞適当にmen    
                        print("面３_適当")

                        if waza==7:
                            angle=str(int(-0.1265*k_c_b[0]+95.276)-5)
                        elif waza==9:
                            angle=str(int(-0.1265*k_c_y[0]+95.276)-5)

                        angle2=angle
                        send_sound('y', angle, angle2, "/home/yaotai/oto/men2.wav")
                        waza=10
                        time.sleep(0.5)
                        motor('bw',255)
                        print("逃げる")
                        curr_time = time.time()
                        prev_time = curr_time
                                    
                elif waza==5 or waza==8:#最後の胴
                    curr_time = time.time()
                    elapsed_time = curr_time - prev_time
                    #print(elapsed_time)
                    if mati_min <= elapsed_time <= mati:#時間内に色発見＝＞座標に
                        if c_b[0] is not None and c_b[1] is not None and d_b is not None:#青発見3
                            print(f"Blue Center: ({c_b[0]}, {c_b[1]}, {d_b:.3f})")
                            k_c_b=(c_b[0],c_b[1])
                            print("胴３")
                            angle=str((int(0.0892*c_b[1]+126.92)))
                            angle2=str(int(-0.1265*c_b[0]+95.276)-5)
                            send_sound('u', angle, angle2, "/home/yaotai/oto/dou2.wav")
                            waza=10
                            if d_b < 0.4:
                                motor('fw',200)
                            
                            elif  0.4 <= d_b <= 0.8:
                                motor('stop')
                            else:
                                motor('fw',200)
                            time.sleep(0.5)
                            motor('bw',255)
                            print("逃げる")
                            curr_time = time.time()
                            prev_time = curr_time

                    elif elapsed_time>mati:#時間内に色発見できなかった＝＞適当に胴    
                        print("胴３_適当")
                        if waza==5:
                            angle=str((int(0.0892*k_c_r[1]+126.92)))
                            angle2=str(int(-0.1265*k_c_r[0]+95.276)-5)                           
                        elif waza==8:
                            angle=str((int(0.0892*k_c_y[1]+126.92)))
                            angle2=str(int(-0.1265*k_c_y[0]+95.276)-5)
                        send_sound('u', angle, angle2, "/home/yaotai/oto/dou2.wav")
                        waza=10
                        time.sleep(0.5)
                        motor('bw',255)
                        print("逃げる")
                        curr_time = time.time()
                        prev_time = curr_time
                    
                elif waza==4 or waza==6:#最後の小手
                    curr_time = time.time()
                    elapsed_time = curr_time - prev_time
                    #print(elapsed_time)           
                    if mati_min <= elapsed_time <= mati:#時間内に色発見＝＞座標に
                        if c_y[0] is not None and c_y[1] is not None and d_y is not None:#黃発見3
                            print(f"Yellow   Center: ({c_y[0]}, {c_y[1]}, {d_y:.3f})")
                            k_c_y=(c_y[0],c_y[1])
                            print("小手3")
                            angle=str((int(0.0892*c_y[1]+126.92)))
                            angle2=str(int(-0.1265*c_y[0]+95.276)-5)
                            send_sound('i', angle, angle2, "/home/yaotai/oto/kote2.wav")
                            if  d_y < 0.4:
                                motor('bw',200)
                            elif 0.4 <= d_y <= 0.8:
                                motor('stop')
                            else:
                                motor('fw',200)

                            time.sleep(0.5)
                            motor('bw',255)
                            print("逃げる")
                            curr_time = time.time()
                            prev_time = curr_time
                            
         
                    elif elapsed_time>mati:#時間内に色発見できなかった＝＞適当に胴    
                        print("小手３_適当")

                        if waza==4:
                            angle=str((int(0.0892*k_c_r[1]+126.92)-10))
                            angle2=str(int(-0.1265*k_c_r[0]+95.276)-5) 
                        elif waza==6:
                            angle=str((int(0.0892*k_c_b[1]+126.92)))
                            angle2=str(int(-0.1265*k_c_b[0]+95.276)-5)
                        
                        send_sound('i', angle, angle2, "/home/yaotai/oto/kote2.wav")
                        waza=10
                        motor('bw',255)
                        print("逃げる")
                        curr_time = time.time()
                        prev_time = curr_time
                
                elif waza==10:
                    curr_time = time.time()
                    elapsed_time = curr_time - prev_time
                    #print(elapsed_time)     
                    if nigeru==None:      
                        if 2 <= elapsed_time :
                            if  c_r[0] is not None or c_b[0] is not None :
                                waza=0
                                nigeru=None
                                curr_time = time.time()
                                prev_time = curr_time

                            elif elapsed_time<=5:
                                motor('right',100)
                                nigeru="right"
                                print("rightttttttttttttttttttttttttttt")
                                curr_time = time.time()
                                prev_time = curr_time

                    elif nigeru=="right":
                        if  c_r[0] is not None or c_b[0] is not None :
                            waza=0
                            nigeru=None
                            curr_time = time.time()
                            prev_time = curr_time
                        elif 1<=elapsed_time<=2:
                            motor('left',100)
                            nigeru="left"
                            print("lefttttttttttttttttttttttttttt")
                            curr_time = time.time()
                            prev_time = curr_time
                    
                    elif nigeru=="left":
                        if  c_r[0] is not None or c_b[0] is not None:
                                waza=0
                                nigeru=None
                                curr_time = time.time()
                                prev_time = curr_time

                        elif 1<=elapsed_time<=2:
                            motor('bw',255)
                            nigeru="bw"
                            print("bwwwwwwwwwwwwwwwwwwwwwww")
                            curr_time = time.time()
                            prev_time = curr_time
                    
                    elif nigeru=="bw":
                        if  c_r[0] is not None or c_b[0] is not None :
                                waza=0
                                nigeru=None
                                curr_time = time.time()
                                prev_time = curr_time

                        elif 2<=elapsed_time<=3:
                            motor('right',100)
                            nigeru="right"
                            print("right")
                            curr_time = time.time()
                            prev_time = curr_time

                #cv2.imshow("Depth Frame", depth_img)  
                cv2.imshow("Masked Result", output_img)  
                if cv2.waitKey(1) & 0xff == 27:#ESCで終了
                    motor('stop')
                    ser.write(f"z 0 0\n".encode())
                    print(f"送信:z 0 0")
                    while True:
                        char = getch()  # キーボード入力を取得
                        if char == "w":
                            motor('fw',255)
                        elif char == "x":
                            motor('bw',255)
                        elif char == "a":
                            motor('left',255)
                        elif char == "d":
                            motor('right',255)
                        elif char == "s":
                            motor('stop')
                        
                        elif char == "q":
                            motor('stop')
                            break  # "q" を押すとプログラムを終了
                        else:
                            continue  # 認識できない入力は無視
                    break
    
    finally:
        motor('stop')
        ser.write(f"z 0 0\n".encode())
        print(f"送信:z 0 0")
        ser.close()
        ser1.close()
        wav_obj = sa.WaveObject.from_wave_file("/home/yaotai/oto/arigatou2.wav")
        play_obj = wav_obj.play()
        play_obj.wait_done()
        cv2.destroyAllWindows()
        pipeline.stop()

if __name__ == "__main__":
    main()

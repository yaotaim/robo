#DCモーターESPからの指示で動く
import pigpio
import time
import serial

import sys
import termios
import tty

import simpleaudio as sa

IN1=17
IN2=27
IN3=22
IN4=23
ENA=18
ENB=13

pi=pigpio.pi()


#ser1 = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

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

try:
    while True:
        char = getch()  # キーボード入力を取得
        if char == "w":
            wav_obj = sa.WaveObject.from_wave_file("/home/yaotai/oto/yorosiku.wav")
            fw(255)
      
        elif char == "s":
            wav_obj = sa.WaveObject.from_wave_file("/home/yaotai/oto/yorosiku_nagai.wav")
            stop()
          
        elif char == "x":
            wav_obj = sa.WaveObject.from_wave_file("/home/yaotai/oto/men.wav")
            bw(255)
   
        elif char == "q":
            wav_obj = sa.WaveObject.from_wave_file("/home/yaotai/oto/dou.wav")
            left(255)
         
        elif char == "e":
            wav_obj = sa.WaveObject.from_wave_file("/home/yaotai/oto/kote.wav")
            right(255)
            
        elif char == "f":
            wav_obj = sa.WaveObject.from_wave_file("/home/yaotai/oto/agari.wav")
            #ser1.write(char.encode())
        elif char == "g":
            wav_obj = sa.WaveObject.from_wave_file("/home/yaotai/oto/sagari.wav")
            #ser1.write(char.encode())
        elif char == "v":
            wav_obj = sa.WaveObject.from_wave_file("/home/yaotai/oto/arigatou.wav")
            #ser1.write(char.encode())
        elif char == "u":
            wav_obj = sa.WaveObject.from_wave_file("/home/yaotai/oto/aka.wav")
            #ser1.write(char.encode())
        elif char == "i":
            wav_obj = sa.WaveObject.from_wave_file("/home/yaotai/oto/aka.wav")
            #ser1.write(char.encode())
        elif char == "o":
            wav_obj = sa.WaveObject.from_wave_file("/home/yaotai/oto/aka.wav")
            #ser1.write(char.encode())
        elif char == "z":
            #ser1.close()
            stop()
            pi.stop()   
            break  # "z" を押すとプログラムを終了
        else:
            continue  # 認識できない入力は無視
        
        play_obj = wav_obj.play()
        #play_obj.wait_done()
   
except KeyboardInterrupt:
    #ser1.close()
    stop()
    pi.stop()    


finally:
    pass
 
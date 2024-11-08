#DCモーター動かすだけ
import pigpio
import time

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

try:
    while True:
        bw(255)
        time.sleep(2)

        motor_stop()
        time.sleep(2)

        fw(255)
        time.sleep(2)

        stop()
        time.sleep(2)

except KeyboardInterrupt:
    motor_stop()
    pi.stop()

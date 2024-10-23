import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

print("数値入力")

while True:
    Kin=input("角度:")
    if Kin.lower()=='q':
        break
    
    if Kin.isdigit():
        ser.write(Kin.encode('utf-8'))
        ser.write(b'\n')
        print(f"{Kin}送信")
    else:
        print("x")

ser.close()
print("数値入力")

while True:
    Kin=input("角度:")
    if Kin.lower()=='q':
        break
    
    if Kin.isdigit():
        ser.write(Kin.encode('utf-8'))
        ser.write(b'\n')
        print(f"{Kin}送信")
    else:
        print("x")

ser.close()

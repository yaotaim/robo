//シリアル入力でMD動かす　モーター操作の基本形
#include <AFMotor.h>
AF_DCMotor motor1(1, MOTOR12_64KHZ);
AF_DCMotor motor2(2, MOTOR12_64KHZ);
AF_DCMotor motor3(3, MOTOR12_64KHZ);
AF_DCMotor motor4(4, MOTOR12_64KHZ);

byte val = 0;
int f=FORWARD;
int b=BACKWARD;

void setup() {
  Serial.begin(9600);
  motor1.setSpeed(255);
  motor2.setSpeed(255);
  motor3.setSpeed(255);
  motor4.setSpeed(255);
}

void loop() {
  if (Serial.available() > 0) {
    val = Serial.read();
    if (val =='w' ){//前
      motor1.run(f);
      motor2.run(f);
      motor3.run(f);
      motor4.run(f);
      delay(1000);  
    }else if (val =='x'){//後
      motor1.run(b);
      motor2.run(b);
      motor3.run(b);
      motor4.run(b);
      delay(1000);  
    }else if (val =='q') {//左回
      motor1.run(f);
      motor2.run(b);
      motor3.run(b);
      motor4.run(f);
      delay(1000);  
    }else if (val =='e') {//右回
      motor1.run(b);
      motor2.run(f);
      motor3.run(f);
      motor4.run(b);
      delay(1000);  
    }else if (val =='a') {//左
      motor1.run(f);
      motor2.run(b);
      motor3.run(f);
      motor4.run(b);
      delay(1000);  
    }else if (val =='d') {//右
      motor1.run(b);
      motor2.run(f);
      motor3.run(b);
      motor4.run(f);
      delay(1000);  
    }
    
    else if (val =='s') {//止
      motor1.run(RELEASE);
      motor2.run(RELEASE);
      motor3.run(RELEASE);
      motor4.run(RELEASE);
      delay(1000);  
    }
    else if (val =='g') {//止
      motor1.run(RELEASE);
      motor2.run(RELEASE);
      motor3.run(RELEASE);
      motor4.run(RELEASE);
      delay(1000);  
    }
  }
}

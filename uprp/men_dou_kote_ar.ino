//めんどうこて試し
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

#define SERVOMIN 500    // 最小パルス幅(μs)
#define SERVOMAX 2400   // 最大パルス幅(μs)

byte val = 0;

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40); // PCA9685のI2Cアドレスを指定

int Servo_pin0 = 0; // サーボ接続ピンを0番に
int Servo_pin1 = 1; // サーボ接続ピンを1番に
int Servo_pin2 = 2; // サーボ接続ピンを1番に



void setup(){
  Serial.begin(9600);
  servoSetup(); // サーボの初期設定
  moveServos(130, 10, 130); // 両方のサーボを同じ角度に動かす
}


void loop() {
  moveServos(130, 10, 130);
  if (Serial.available() > 0){//もしjetson側から命令きていたら
    val = Serial.read();
    if (val =='j' ){//jetsonから面命令　未実装
      Serial.println("men");
      men1();
      men2();
      men3();
    }else if (val =='k' ){//jetsonから面命令　未実装
      Serial.println("left_dou");
      left_dou1();
      left_dou2();
      left_dou3();
      left_dou4();
   
    }else if (val =='l' ){//jetsonから面命令　未実装
      Serial.println("right_dou");
      right_dou1();
      right_dou2();
      right_dou3(); 
      right_dou4(); 
        
      }
  }
}


// サーボの初期設定
void servoSetup() {
  pwm.begin(); // 初期設定
  pwm.setPWMFreq(50); // PWM周期を50Hzに設定
}


// サーボを動かす
void moveServos(int angle0, int angle1, int angle2) {
  angle0 = map(angle0, 0, 180, SERVOMIN, SERVOMAX); // 角度(0~180)をパルス幅(500~2400μs)に変換
  angle1 = map(angle1, 0, 180, SERVOMIN, SERVOMAX); // 角度(0~180)をパルス幅(500~2400μs)に変換
  angle2 = map(angle2, 0, 180, SERVOMIN, SERVOMAX); // 角度(0~180)をパルス幅(500~2400μs)に変換
  pwm.writeMicroseconds(Servo_pin0, angle0); // サーボを動作させる
  pwm.writeMicroseconds(Servo_pin1, angle1); // サーボを動作させる
  pwm.writeMicroseconds(Servo_pin2, angle2); // サーボを動作させる
}

void men1() {// 面前半
  moveServos(110, 10, 130); // 両方のサーボを同じ角度に動かす
  delay(200);
}

void men2() {//面後半
  moveServos(110, 30, 130); // 両方のサーボを同じ角度に動かす
  delay(200);
}
void men3() {//面後半
  moveServos(110, 10, 130); // 両方のサーボを同じ角度に動かす
  delay(200);
}

void left_dou1() {// どう前半
  moveServos(110, 10, 130); // 両方のサーボを同じ角度に動かす 
  delay(200);
}

void left_dou2() {// どう前半
  moveServos(110, 10,90); // 両方のサーボを同じ角度に動かす 
  delay(200);
}

void left_dou3() {// どう前半
  moveServos(110, 10, 130); // 両方のサーボを同じ角度に動かす 
  delay(200);
}
void left_dou4() {// どう前半
  moveServos(140, 10,130); // 両方のサーボを同じ角度に動かす 
  delay(200);
}

void right_dou1() {// どう前半
  moveServos(110, 10, 130); // 両方のサーボを同じ角度に動かす 
  delay(200);

}

void right_dou2() {// どう前半
  moveServos(110, 10, 170); // 両方のサーボを同じ角度に動かす 
  delay(200);
}

void right_dou3() {// どう前半
  moveServos(110, 10, 130); // 両方のサーボを同じ角度に動かす 
  delay(200);
}
void right_dou4() {// どう前半
  moveServos(140, 10, 130); // 両方のサーボを同じ角度に動かす 
  delay(200);
}





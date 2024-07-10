#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

#define SERVOMIN 500    // 最小パルス幅(μs)
#define SERVOMAX 2400   // 最大パルス幅(μs)


Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40); // PCA9685のI2Cアドレスを指定

int Servo_pin0 = 7; // サーボ接続ピンを0番に
int Servo_pin1 = 6; // サーボ接続ピンを1番に
int Servo_pin2 = 8; // サーボ接続ピンを1番に



void setup() {
  Serial.begin(9600);
  servoSetup(); // サーボの初期設定
  moveServos(90,90,90);
}

void loop() {
  if (Serial.available() >= 3) {
    int angle0 = Serial.parseInt();
    int angle1 = Serial.parseInt();
    int angle2 = Serial.parseInt();
    moveServos(angle0, angle1, angle2);
    Serial.println(angle0);
    Serial.println(angle1);
    Serial.println(angle2);
    Serial.println("done");
  }
}


// サーボの初期設定
void servoSetup() {
  pwm.begin(); // 初期設定
  pwm.setPWMFreq(50); // PWM周期を50Hzに設定
  delay(1000);
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



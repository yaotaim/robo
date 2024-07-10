//面中落ちない+サーボとDC動かすモーション試せる
#include <AFMotor.h>//DCモーター関連
#include <Wire.h>//サーボモーター関連
#include <Adafruit_PWMServoDriver.h>//サーボモーター関連

#define SERVOMIN 500    // サーボの最小パルス幅(μs)
#define SERVOMAX 2400   // サーボの最大パルス幅(μs)
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40); // PCA9685のI2Cアドレスを指定
int Servo_pin0 = 0; // サーボ接続ピンを0番に
int Servo_pin1 = 1; // サーボ接続ピンを1番に
int Servo_pin2 = 2; // サーボ接続ピンを2番に


AF_DCMotor dcrf(1, MOTOR12_64KHZ);//DCモーター右前
AF_DCMotor dclf(2, MOTOR12_64KHZ);//DCモーター左前
AF_DCMotor dclb(3, MOTOR12_64KHZ);//DCモーター左後ろ
AF_DCMotor dcrb(4, MOTOR12_64KHZ);//DCモーター右後ろ

int usrf = 52;//落下防止用距離センサー右前
int uslf = 51;//落下防止用距離センサー左前
int uslb = 50;//落下防止用距離センサー左後ろ
int usrb = 53;//落下防止用距離センサー右後ろ

int osl  = 42;//敵感知用センサー左
int osr  = 44;//敵感知用センサー右
//int osb  = 41;//敵感知用センサー後ろ
int osrf = 43;//敵感知センサー右前


byte val = 0;

int f=FORWARD;
int b=BACKWARD;
int r=RELEASE;

void setup() {
  Serial.begin(9600);//シリアル通信
  dcrf.setSpeed(255);//DCモーター右前の速さ設定
  dclf.setSpeed(255);//DCモーター左前の速さ設定
  dclb.setSpeed(255);//DCモーター左後ろの速さ設定
  dcrb.setSpeed(255);//DCモーター右後ろの速さ設定
  servoSetup(); // サーボの初期設定
  moveServos(130, 30, 130); // 両方のサーボを同じ角度に動かす
}

void servoSetup() {// サーボの初期設定
  pwm.begin(); // 初期設定
  pwm.setPWMFreq(50); // PWM周期を50Hzに設定
  delay(1000);
}

void moveServos(int angle0, int angle1 ,int angle2) {// サーボを動かす
  angle0 = map(angle0, 0, 180, SERVOMIN, SERVOMAX); // 角度(0~180)をパルス幅(500~2400μs)に変換
  angle1 = map(angle1, 0, 180, SERVOMIN, SERVOMAX); // 角度(0~180)をパルス幅(500~2400μs)に変換
  angle2 = map(angle2, 0, 180, SERVOMIN, SERVOMAX); // 角度(0~180)をパルス幅(500~2400μs)に変換
  pwm.writeMicroseconds(Servo_pin0, angle0); // サーボを動作させる
  pwm.writeMicroseconds(Servo_pin1, angle1); // サーボを動作させる
  pwm.writeMicroseconds(Servo_pin2, angle2); // サーボを動作させる
}




void  rakka_backward(int kaisu){
  for (int i=0; i <= kaisu ; i++){
    if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//もし落下防止用距離センサー全部異常なしなら
      backward();
      delay(10);  
    }else{
      release();
      break;
    }
  }
}

void  rakka_forward(int kaisu){
  for (int i=0; i <= kaisu ; i++){
    if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//もし落下防止用距離センサー全部異常なしなら
      forward();
      delay(10);  
    }else{
      release();
      break;
    }
  }
}

void  rakka_right_forward(int kaisu){
  for (int i=0; i <= kaisu ; i++){
    if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//もし落下防止用距離センサー全部異常なしなら
      right_forward();
      delay(10);  
    }else{
      release();
      break;
    }
  }
}

void  rakka_left_forward(int kaisu){
  for (int i=0; i <= kaisu ; i++){
    if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//もし落下防止用距離センサー全部異常なしなら
      left_forward();
      delay(10);  
    }else{
      release();
      break;
    }
  }
}

void forward() {// モーターを前進させる
  dcrf.run(f);
  dclf.run(f);
  dclb.run(f);
  dcrb.run(f);
}

void backward() {// モーターを後退させる
  dcrf.run(b);
  dclf.run(b);
  dclb.run(b);
  dcrb.run(b);
}

void right_rotate() {// モーターを右回転させる
  dcrf.run(b);
  dclf.run(f);
  dclb.run(f);
  dcrb.run(b);
}

void left_rotate(){// モーターを左回転させる
  dcrf.run(f);
  dclf.run(b);
  dclb.run(b);
  dcrb.run(f);
}

void right() {// モーターを右移動させる
  dcrf.run(b);
  dclf.run(f);
  dclb.run(b);
  dcrb.run(f);
}

void left() {// モーターを左移動させる
  dcrf.run(f);
  dclf.run(b);
  dclb.run(f);
  dcrb.run(b);
}

void right_forward() {// モーターを右前移動させる
  dcrf.run(r);
  dclf.run(f);
  dclb.run(r);
  dcrb.run(f);
}

void left_forward() {// モーターを左前移動させる
  dcrf.run(f);
  dclf.run(r);
  dclb.run(f);
  dcrb.run(r);
}

void release() {// モーターを停止させる
  dcrf.run(r);
  dclf.run(r);
  dclb.run(r);
  dcrb.run(r);
}


void loop() {
  if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//もし落下防止用距離センサー全部異常なしなら
    Serial.println("rakka seijyou");
    if (Serial.available() > 0){//もしjetson側から命令きていたら
      val = Serial.read();
      if (val =='j' ){//jetsonから面命令　未実装
        Serial.println("men");
        men1();
        men2();
        release();
      }else if (val =='k' ){//jetsonから面命令　未実装
        Serial.println("left_dou");
        left_dou1();
        left_dou2();
        left_dou3();
        release();
      
      }else if (val =='l' ){//jetsonから面命令　未実装
        Serial.println("right_dou");
        right_dou1();
        right_dou2();
        right_dou3();
        release();
      
      }
    }else{
      release();
    }
  }
}

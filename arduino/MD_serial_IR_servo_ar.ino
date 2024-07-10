//MD_serial_IR.inoの進化系。サーボの動き追加　ロボ剣用
//(サーボとDCの並列処理~面でバック~)の合体+面中落ちない
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


int osl  = 44;//敵感知用センサー左
int osr  = 45;//敵感知用センサー右
//int osb  = 41;//敵感知用センサー後ろ
int osff = 42;//敵感知センサー前前
int osrf = 41;//敵感知センサー右前
int oslf = 43;//敵感知センサー左前


byte val = 0;

int f=FORWARD;
int b=BACKWARD;
int r=RELEASE;

void setup() {
  Serial.begin(115200);//シリアル通信
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

void slow_right_rotate() {// モーターを右回転させる osoku
  dcrf.setSpeed(100);//DCモーター右前の速さ設定
  dclf.setSpeed(100);//DCモーター左前の速さ設定
  dclb.setSpeed(100);//DCモーター左後ろの速さ設定
  dcrb.setSpeed(100);//DCモーター右後ろの速さ設定
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

void slow_left_rotate() {// モーターを右回転させる osoku
  dcrf.setSpeed(100);//DCモーター右前の速さ設定
  dclf.setSpeed(100);//DCモーター左前の速さ設定
  dclb.setSpeed(100);//DCモーター左後ろの速さ設定
  dcrb.setSpeed(100);//DCモーター右後ろの速さ設定
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

void  rakka_left_rotate(int kaisu){
  for (int i=0; i <= kaisu ; i++){
    if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//もし落下防止用距離センサー全部異常なしなら
      left_rotate();
      delay(10);  
    }else{
      release();
      break;
    }
  }
}

void  slow_rakka_left_rotate(int kaisu){
  for (int i=0; i <= kaisu ; i++){
    if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//もし落下防止用距離センサー全部異常なしなら
      slow_left_rotate();
      delay(10);  
    }else{
      release();
      break;
    }
  }
}

void  rakka_right_rotate(int kaisu){
  for (int i=0; i <= kaisu ; i++){
    if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//もし落下防止用距離センサー全部異常なしなら
      right_rotate();
      delay(10);  
    }else{
      release();
      break;
    }
  }
}

void  slow_rakka_right_rotate(int kaisu){
  for (int i=0; i <= kaisu ; i++){
    if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//もし落下防止用距離センサー全部異常なしなら
      slow_right_rotate();
      delay(10);  
    }else{
      release();
      break;
    }
  }
}

void  rakka_left(int kaisu){
  for (int i=0; i <= kaisu ; i++){
    if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//もし落下防止用距離センサー全部異常なしなら
      left();
      delay(10);  
    }else{
      release();
      break;
    }
  }
}

void  rakka_right(int kaisu){
  for (int i=0; i <= kaisu ; i++){
    if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//もし落下防止用距離センサー全部異常なしなら
      right();
      delay(10);  
    }else{
      release();
      break;
    }
  }
}


void men1() {// 面前半
  moveServos(110, 30, 130); // 両方のサーボを同じ角度に動かす
  rakka_backward(70);
}

void men2() {//面後半
  rakka_forward(70);
  moveServos(130, 30, 130); // 両方のサーボを同じ角度に動かす
  release();
  delay(100);
}


void right_dou1() {// どう前半
  moveServos(110, 30, 130); // 両方のサーボを同じ角度に動かす 
  rakka_right_forward(20);
}

void right_dou2() {// どう前半
  moveServos(110, 30, 90); // 両方のサーボを同じ角度に動かす 
  rakka_right_forward(50);
}

void right_dou3() {// どう前半
  moveServos(110, 30, 130); // 両方のサーボを同じ角度に動かす 
  rakka_backward(80);
}

void right_dou4() {// どう前半
  moveServos(130, 30,130); // 両方のサーボを同じ角度に動かす 
  rakka_backward(80);
}
void left_dou1() {// どう前半
  moveServos(110, 30, 130); // 両方のサーボを同じ角度に動かす 
  rakka_left_forward(20);
}

void left_dou2() {// どう前半
  moveServos(110, 30, 170); // 両方のサーボを同じ角度に動かす 
  rakka_left_forward(50);
}

void left_dou3() {// どう前半
  moveServos(110, 30, 130); // 両方のサーボを同じ角度に動かす 
  rakka_backward(80);
}
void left_dou4() {// どう前半
  moveServos(130, 30, 130); // 両方のサーボを同じ角度に動かす 
  rakka_backward(80);
}


void loop() {
  dcrf.setSpeed(255);//DCモーター右前の速さ設定
  dclf.setSpeed(255);//DCモーター左前の速さ設定
  dclb.setSpeed(255);//DCモーター左後ろの速さ設定
  dcrb.setSpeed(255);//DCモーター右後ろの速さ設定
  moveServos(130, 30, 130); // 両方のサーボを同じ角度に動かす
  delay(10);
  if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//もし落下防止用距離センサー全部異常なしなら
    Serial.println("rakka seijyou");
    if(digitalRead(osl)==LOW && digitalRead(osr) == HIGH && digitalRead(osff)==HIGH && digitalRead(oslf)==HIGH && digitalRead(osrf)==HIGH ){//敵感知用センサー左反応=>左回転
      Serial.println("left teki");
      rakka_left_rotate(100);

    }else if(digitalRead(osl)==HIGH && digitalRead(osr) == LOW && digitalRead(osff)==HIGH && digitalRead(oslf)==HIGH && digitalRead(osrf)==HIGH ){//敵感知用センサー右反応=>右回転
      Serial.println("right teki");
      rakka_right_rotate(100);

    }else if(digitalRead(osl)==HIGH && digitalRead(osr) == HIGH && digitalRead(osff)==LOW && digitalRead(oslf)==HIGH && digitalRead(osrf)==HIGH ){//敵感知用センサー前前反応=>面
      Serial.println("forward-forward teki");
      men1();
      men2();
      release();

    }else if(digitalRead(osl)==HIGH && digitalRead(osr) == HIGH && digitalRead(osff)==HIGH && digitalRead(oslf)==LOW && digitalRead(osrf)==HIGH ){//敵感知用センサー左前反応=>左胴
      Serial.println("left-forward teki");
      left_dou1();
      left_dou2();
      left_dou3();
      left_dou4();
      release();
    
    }else if(digitalRead(osl)==HIGH && digitalRead(osr) == HIGH && digitalRead(osff)==HIGH && digitalRead(oslf)==HIGH && digitalRead(osrf)==LOW ){//敵感知用センサー右前反応=>右胴
      Serial.println("right-forward teki");
      right_dou1();
      right_dou2();
      right_dou3();
      right_dou4();
      release();
   
    }else{//落下防止用センサーと敵感知用センサー全部異常なしなら
      if (Serial.available() > 0){//もしjetson側から命令きていたら
        val = Serial.read();
        
        if (val =='j' ){//jetsonから面命令　未実装
          Serial.println("men");
          men1();
          men2();
          release();

        }else if (val =='k'){//jetsonから前命令
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


        }else if (val =='w'){//jetsonから前命令
          rakka_forward(100);
          release();

        }else if (val =='x'){//jetsonから後ろ命令
          rakka_backward(50);
          release();

        }else if (val =='q') {//jetsonから左回命令
          slow_rakka_left_rotate(50);
          release();  

        }else if (val =='e') {//jetsonから右回命令
          slow_rakka_right_rotate(50);
          release(); 

        }else if (val =='a') {//jetsonから左命令
          rakka_left(100);
          release();  

        }else if (val =='d') {//jetsonから右命令
          rakka_right(100);
          release();  
        }
        else if (val =='s') {//jetsonから止まる命令
          release(); 
        }
        else if (val =='g') {//jetsonから通信切られた=>特にまだ作ってない
          release();  
        }

      }else{//jetsonから特に命令きてない時
        forward();
        delay(100);  
      }
      }
  
  
  }else if(digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == HIGH && digitalRead(usrb) == LOW){//落下防止センサー左後ろ反応=>右前
    Serial.println("lb ochisou");
    right_forward();
    delay(1000);  

  }else if(digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == HIGH){//落下防止センサー右後ろ反応=>左前
    Serial.println("rb ochisou");
    left_forward();
    delay(1000);  

  }else if(digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == HIGH && digitalRead(usrb) == HIGH){//落下防止センサー後ろ2つ反応=>前
    Serial.println("rblb ochisou");
    forward();
    delay(1000);

  }else if(digitalRead(usrf)==HIGH && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//落下防止センサー右前反応=>後ろ=>左回転
    Serial.println("rf ochisou");
    backward();
    delay(1000); 
    left_rotate();
    delay(1000);
  
  }else if(digitalRead(usrf)==LOW && digitalRead(uslf) == HIGH && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//落下防止センサー左前反応=>後ろ=>右回転
    Serial.println("lf ochisou");
    backward();
    delay(1000); 
    right_rotate();
    delay(1000);
  
  }else if(digitalRead(usrf)==HIGH && digitalRead(uslf) == HIGH && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//落下防止センサー前2つ反応=>後ろ=>回転
    Serial.println("rf lf ochisou");
    backward();
    delay(1000); 
    right_rotate();
    delay(2000);
    
  }else{//その他
    Serial.println("irei");
    release();
    delay(1000);
  }
}

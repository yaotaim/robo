//ロボ剣用
//MD_serial_IR_servo_ar.inoをシリアルなしで動かす(電源入れた瞬間から落下防止の動きだけする)多分...
#include <AFMotor.h>//DCモーター関連
#include <Wire.h>//サーボモーター関連
#include <Adafruit_PWMServoDriver.h>//サーボモーター関連

#define SERVOMIN 500    // サーボの最小パルス幅(μs)
#define SERVOMAX 2400   // サーボの最大パルス幅(μs)
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40); //PCA9685のI2Cアドレスを指定

int Servo_pin0 = 0; // サーボ接続ピンを0番に
int Servo_pin1 = 1; // サーボ接続ピンを1番に
int Servo_pin2 = 2; // サーボ接続ピンを2番に


AF_DCMotor dcrf(1, MOTOR12_64KHZ);//DCモーター右前
AF_DCMotor dclf(2, MOTOR12_64KHZ);//DCモーター左前
AF_DCMotor dclb(3, MOTOR12_64KHZ);//DCモーター左後ろ
AF_DCMotor dcrb(4, MOTOR12_64KHZ);//DCモーター右後ろ

int usrf = 51;//落下防止用距離センサー右前
int uslf = 50;//落下防止用距離センサー左前
int uslb = 52;//落下防止用距離センサー左後ろ
int usrb = 53;//落下防止用距離センサー右後ろ


int osl  = 40;//敵感知用センサー左
int osr  = 41;//敵感知用センサー右

int osff = 48;//敵感知センサー前前
int osrf = 43;//敵感知センサー右前
int oslf = 42;//敵感知センサー左前


byte val = 0;
byte val2 = 0;
int mode=0;

int f=FORWARD;
int b=BACKWARD;
int r=RELEASE;

void setup() {
  dcrf.setSpeed(255);//DCモーター右前の速さ設定
  dclf.setSpeed(255);//DCモーター左前の速さ設定
  dclb.setSpeed(255);//DCモーター左後ろの速さ設定
  dcrb.setSpeed(255);//DCモーター右後ろの速さ設定  
  Serial.begin(115200);//シリアル通信
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

void motorSetup(int hayasa){
  dcrf.setSpeed(hayasa);//DCモーター右前の速さ設定
  dclf.setSpeed(hayasa);//DCモーター左前の速さ設定
  dclb.setSpeed(hayasa);//DCモーター左後ろの速さ設定
  dcrb.setSpeed(hayasa);//DCモーター右後ろの速さ設定
}

void motor(char rf ,char lf ,char lb ,char rb){
  dcrf.run(rf);
  dclf.run(lf);
  dclb.run(lb);
  dcrb.run(rb);
}

/////////////////release///////////////////////////////
void release(){// モーターを停止させる
  motor(r,r,r,r);
}

void  serial_release(){
  release();
  if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){
    release();
    delay(500);
  }
  for (int i=0; i <= 10000; i++){
    if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//もし落下防止用距離センサー全部異常なしなら
      if (Serial.available() > 0){
        val2 = Serial.read();
        if (val2==val){
          delay(500);
        }else if(val2=='u'){
          mode=1;
        }else{
          val=val2;
          break;
        }
      }
    }else{
        release();
        delay(10);
        mode=1;
        break;
    }
  }
}

////////////////forward/////////////////////////
void forward(int hayasa){// モーターを前進させる
  motorSetup(hayasa);
  motor(f,f,f,f);
}

void  rakka_forward(int hayasa,int kaisu){
  for (int i=0; i <= kaisu ; i++){
    if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//もし落下防止用距離センサー全部異常なしなら
      forward(hayasa);
      delay(10);  
    }else{
      release();
      break;
    }
  }
}

void  serial_rakka_forward(int hayasa){
  forward(hayasa);
  if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){
    forward(hayasa);
    delay(100);
  }
  for (int i=0; i <= 10000; i++){
    if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//もし落下防止用距離センサー全部異常なしなら
      if (Serial.available() > 0){
        val2 = Serial.read();
        if (val2==val){
          delay(100);
        }else if(val2=='u'){
          mode=1;
          break;
        }else{
          val=val2;
          break;
        }
      }else{
        delay(100);
      }
    }else{
        release();
        delay(10);
        mode=1;
        break;
    }
  }
}

///////////////backward///////////////////////////////////
void backward(int hayasa) {// モーターを後退させる
  motorSetup(hayasa);
  motor(b,b,b,b);
}

void  rakka_backward(int hayasa,int kaisu){
  for (int i=0; i <= kaisu ; i++){
    if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//もし落下防止用距離センサー全部異常なしなら
      backward(255);
      delay(10);  
    }else{
      release();
      break;
    }
  }
}

void  serial_rakka_backward(int hayasa){
  backward(hayasa);
  if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){
    backward(hayasa);
    delay(100);
  }
  for (int i=0; i <= 10000; i++){
    if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//もし落下防止用距離センサー全部異常なしなら
      if (Serial.available() > 0){
        val2 = Serial.read();
        if (val2==val){
          delay(100);
        }else if(val2=='u'){
          mode=1;
          break;
        }else{
          val=val2;
          break;
        }
    }else{
      release();
      delay(10);
      mode=1;
      break;
      }
    }
  }
}

////////////////right_rotate////////////////////////////////
void right_rotate(int hayasa) {// モーターを右回転させる
  motorSetup(hayasa);
  motor(b,f,f,b);
}

void  serial_rakka_right_rotate(int hayasa){
  right_rotate(hayasa);
  if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){
    right_rotate(hayasa);
    delay(100);
  }
  for (int i=0; i <= 10000; i++){
    if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//もし落下防止用距離センサー全部異常なしなら
      if (Serial.available() > 0){
        val2 = Serial.read();
        if (val2==val){
          delay(100);
        }else if(val2=='u'){
          mode=1;
          break;
        }else{
          val=val2;
          break;
        }
      }
    }else{
        release();
        delay(10);
        mode=1;
        break;
    }
  }
}

///////////////left_rotate////////////////////////////////
void left_rotate(int hayasa){// モーターを左回転させる
  motorSetup(hayasa);
  motor(f,b,b,f);
}

void  serial_rakka_left_rotate(int hayasa){
  left_rotate(hayasa);
  if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){
    left_rotate(hayasa);
    delay(100);
  }
  for (int i=0; i <= 10000; i++){
    if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//もし落下防止用距離センサー全部異常なしなら
      if (Serial.available() > 0){
        val2 = Serial.read();
        if (val2==val){
          delay(100);
        }else if(val2=='u'){
          mode=1;
          break;
        }else{
          val=val2;
          break;
        }
      }
    }else{
        release();
        delay(10);
        mode=1;
        break;
    }
  }
}

///////////////right////////////////////////////////////
void right(int hayasa) {// モーターを右移動させる
  motorSetup(hayasa);
  motor(b,f,b,f);
}

void  rakka_right(int hayasa,int kaisu){
  for (int i=0; i <= kaisu ; i++){
    if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//もし落下防止用距離センサー全部異常なしなら
      right(hayasa);
      delay(10);  
    }else{
      release();
      mode=1;
      break;
    }
  }
}

void  serial_rakka_right(int hayasa){
  right(hayasa);
  if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){
    right(hayasa);
    delay(100);
  }
  for (int i=0; i <= 10000; i++){
    if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//もし落下防止用距離センサー全部異常なしなら
      if (Serial.available() > 0){
        val2 = Serial.read();
        if (val2==val){
          delay(100);
        }else if(val2=='u'){
          mode=1;
          break;
        }else{
          val=val2;
          break;
        }
      }
    }else{
        release();
        delay(10);
        mode=1;
        break;
    }
  }
}

///////////////left////////////////////////////////
void left(int hayasa) {// モーターを左移動させる
  motorSetup(hayasa);
  motor(f,b,f,b);
}

void  rakka_left(int hayasa,int kaisu){
  for (int i=0; i <= kaisu ; i++){
    if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//もし落下防止用距離センサー全部異常なしなら
      left(hayasa);
      delay(10);  
    }else{
      release();
      break;
    }
  }
}

void  serial_rakka_left(int hayasa){
  left(hayasa);
  if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){
    left(hayasa);
    delay(100);
  }
  for (int i=0; i <= 10000; i++){
    if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//もし落下防止用距離センサー全部異常なしなら
      if (Serial.available() > 0){
        val2 = Serial.read();
        if (val2==val){
          delay(100);
        }else if(val2=='u'){
          mode=1;
          break;
        }else{
          val=val2;
          break;
        }
      }
    }else{
        release();
        delay(10);
        mode=1;
        break;
    }
  }
}

///////////////right_forward//////////////////////////////
void right_forward(int hayasa) {// モーターを右前移動させる
  motorSetup(hayasa);
  motor(r,f,r,f);
}

void  rakka_right_forward(int hayasa,int kaisu){
  for (int i=0; i <= kaisu ; i++){
    if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//もし落下防止用距離センサー全部異常なしなら
      right_forward(hayasa);
      delay(10);  
    }else{
      release();
      break;
    }
  }
}

void  serial_rakka_right_forward(int hayasa){
  right_forward(hayasa);
  if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){
    right_forward(hayasa);
    delay(100);
  }
  for (int i=0; i <= 10000; i++){
    if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//もし落下防止用距離センサー全部異常なしなら
      if (Serial.available() > 0){
        val2 = Serial.read();
        if (val2==val){
          delay(100);
        }else if(val2=='u'){
          mode=1;
          break;
        }else{
          val=val2;
          break;
        }
      }
    }else{
        release();
        delay(10);
        mode=1;
        break;
    }
  }
}

///////////////left_forward///////////////////////////
void left_forward(int hayasa) {// モーターを左前移動させる
  motorSetup(hayasa);
  motor(f,r,f,r);
}

void  rakka_left_forward(int hayasa,int kaisu){
  for (int i=0; i <= kaisu ; i++){
    if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//もし落下防止用距離センサー全部異常なしなら
      left_forward(hayasa);
      delay(10);  
    }else{
      release();
      break;
    }
  }
}

void  serial_rakka_left_forward(int hayasa){
  left_forward(hayasa);
  if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){
    left_forward(hayasa);
    delay(500);
  }
  for (int i=0; i <= 10000; i++){
    if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//もし落下防止用距離センサー全部異常なしなら
      if (Serial.available() > 0){
        val2 = Serial.read();
        if (val2==val){
          delay(500);
        }else if(val2=='u'){
          mode=1;
          break;
        }else{
          val=val2;
          break;
        }
      }
    }else{
        release();
        delay(10);
        mode=1;
        break;
    }
  }
}

/////////////////men///////////////////////////////
void men1() {// 面前半
  moveServos(100, 30, 130); // 両方のサーボを同じ角度に動かす
  rakka_backward(255,70);
}

void men2() {//面後半
  rakka_backward(255,1000000);
  moveServos(130, 30, 130); // 両方のサーボを同じ角度に動かす
  release();
  delay(100);
}

/////////////////right_dou///////////////////////////////
void right_dou1() {// どう前半
  moveServos(110, 30, 130); // 両方のサーボを同じ角度に動かす 
  rakka_right(255,20);
}

void right_dou2() {// どう前半
  moveServos(110, 30, 90); // 両方のサーボを同じ角度に動かす 
  rakka_right(255,50);
}

void right_dou3() {// どう前半
  moveServos(110, 30, 130); // 両方のサーボを同じ角度に動かす 
  rakka_right(255,300);
}

void right_dou4() {// どう前半
  moveServos(130, 30,130); // 両方のサーボを同じ角度に動かす 
  left_rotate(255);
  delay(1000);
}

/////////////////left_dou///////////////////////////////
void left_dou1() {// どう前半
  moveServos(110, 30, 130); // 両方のサーボを同じ角度に動かす 
  rakka_left_forward(255,20);
}

void left_dou2() {// どう前半
  moveServos(110, 30, 170); // 両方のサーボを同じ角度に動かす 
  rakka_left(255,50);
}

void left_dou3() {// どう前半
  moveServos(110, 30, 130); // 両方のサーボを同じ角度に動かす 
  rakka_left(255,300);
}

void left_dou4() {// どう前半
  moveServos(130, 30, 130); // 両方のサーボを同じ角度に動かす 
  right_rotate(255);
  delay(1000);
}
////////////////////////////////////////////////////////



void loop() {
  moveServos(130, 30, 130); // 両方のサーボを同じ角度に動かす
  Serial.println("loop start");


  //////////////////////////////////////mode1////////////////////////////////////////////////////////
    Serial.println("mode1");
    if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//もし落下防止用距離センサー全部異常なしなら
      Serial.println("rakka seijyou");
      
      if(digitalRead(osl)==LOW && digitalRead(osr) == HIGH && digitalRead(osff)==HIGH && digitalRead(oslf)==HIGH && digitalRead(osrf)==HIGH ){//敵感知用センサー左反応=>左回転
        Serial.println("left teki"); 
        left_rotate(255);
        delay(1000); 
        release();

      }else if(digitalRead(osl)==HIGH && digitalRead(osr) == LOW && digitalRead(osff)==HIGH && digitalRead(oslf)==HIGH && digitalRead(osrf)==HIGH ){//敵感知用センサー右反応=>右回転
        Serial.println("right teki");
        right_rotate(255);
        delay(1000);
        release();

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
    
      }else{
        forward(255);
        delay(100);  
      }
    }else if(digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == HIGH && digitalRead(usrb) == LOW){//落下防止センサー左後ろ反応=>右前
      Serial.println("lb ochisou");
      release();
      delay(100);
      forward(255);
      delay(1000);  

    }else if(digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == HIGH){//落下防止センサー右後ろ反応=>左前
      Serial.println("rb ochisou");
      release();
      delay(100);
      forward(255);
      delay(1000);  

    }else if(digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == HIGH && digitalRead(usrb) == HIGH){//落下防止センサー後ろ2つ反応=>前
      Serial.println("rblb ochisou");
      release();
      delay(100);
      forward(255);
      delay(1000);

    }else if(digitalRead(usrf)==HIGH && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//落下防止センサー右前反応=>後ろ=>左回転
      Serial.println("rf ochisou");
      release();
      delay(100);
      backward(255);
      delay(1000); 
      left_rotate(255);
      delay(1000);
  
    }else if(digitalRead(usrf)==LOW && digitalRead(uslf) == HIGH && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//落下防止センサー左前反応=>後ろ=>右回転
      Serial.println("lf ochisou");
      release();
      delay(100);
      backward(255);
      delay(1000); 
      right_rotate(255);
      delay(1000);
  
    }else if(digitalRead(usrf)==HIGH && digitalRead(uslf) == HIGH && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//落下防止センサー前2つ反応=>後ろ=>回転
      Serial.println("rf lf ochisou");
      release();
      delay(100);
      backward(255);
      delay(1000); 
      right_rotate(255);
      delay(2000);
    
    }else{//その他
      Serial.println("irei");
      release();
      delay(1000);
    }
}
  ////////////////////////////////////////////////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////////////////////////////////// 

  


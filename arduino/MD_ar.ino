//arduinoのモータードライバーシールド(MD)使ってみた

#include <AFMotor.h>//DCモーター関連

AF_DCMotor dcrf(1, MOTOR12_64KHZ);//DCモーター右前
AF_DCMotor dclf(2, MOTOR12_64KHZ);//DCモーター左前
AF_DCMotor dclb(3, MOTOR12_64KHZ);//DCモーター左後ろ
AF_DCMotor dcrb(4, MOTOR12_64KHZ);//DCモーター右後ろ

byte val = 0;
byte val2 = 0;
int mode=0;

int f=FORWARD;
int b=BACKWARD;
int r=RELEASE;

void setup() {
  dcrf.setSpeed(255);
  dclf.setSpeed(255);
  dclb.setSpeed(255);
  dcrb.setSpeed(255);
  Serial.begin(115200);
}

void motorSetup(int hayasa){
  dcrf.setSpeed(hayasa);//DCモーター右前の速さ設定
  dclf.setSpeed(hayasa);
  dclb.setSpeed(hayasa);
  dcrb.setSpeed(hayasa);
}

void motor(char rf ,char lf ,char lb ,char rb){
  dcrf.run(rf);
  dclf.run(lf);
  dclb.run(lb);
  dcrb.run(rb);
}

void release(){// モーターを停止させる
  motor(r,r,r,r);
}

void forward(int hayasa){// モーターを前進させる
  motorSetup(hayasa);
  motor(f,f,f,f);
}

void backward(int hayasa) {// モーターを後退させる
  motorSetup(hayasa);
  motor(b,b,b,b);
}

void right_rotate(int hayasa) {// モーターを右回転させる
  motorSetup(hayasa);
  motor(b,f,f,b);
}

void left_rotate(int hayasa){// モーターを左回転させる
  motorSetup(hayasa);
  motor(f,b,b,f);
}

void right(int hayasa) {// モーターを右移動させる
  motorSetup(hayasa);
  motor(b,f,b,f);
}


void left(int hayasa) {// モーターを左移動させる
  motorSetup(hayasa);
  motor(f,b,f,b);
}

void right_forward(int hayasa) {// モーターを右前移動させる
  motorSetup(hayasa);
  motor(r,f,r,f);
}

///////////////left_forward///////////////////////////
void left_forward(int hayasa) {// モーターを左前移動させる
  motorSetup(hayasa);
  motor(f,r,f,r);
}

void loop() {
  right_rotate(255);
  delay(467);
  release();
  delay(2000);
}

  


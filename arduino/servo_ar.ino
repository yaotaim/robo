//サーボを動かす基本的なプログラム
#include <Servo.h>

Servo myservo1;
Servo myservo2;
Servo myservo3;
const int SV_PIN1 = 3;
const int SV_PIN2 = 15;
const int SV_PIN3 = 16;

void setup() {
  myservo1.attach(SV_PIN1, 500, 2400);
  myservo2.attach(SV_PIN2, 500, 2400);
  myservo3.attach(SV_PIN3, 500, 2400);
}

void loop() {
  myservo1.write(20);  // サーボモーターを0度の位置まで動かす
  delay(1000);
  //myservo2.write(0);  // サーボモーターを0度の位置まで動かす
  //delay(1000);
  //myservo3.write(0);  // サーボモーターを0度の位置まで動かす
  //delay(1000);

  myservo1.write(90);  // サーボモーターを90度の位置まで動かす
  delay(1000);
  //myservo2.write(90);  // サーボモーターを0度の位置まで動かす
  //delay(1000);
  //myservo3.write(90);  // サーボモーターを0度の位置まで動かす
  //delay(1000);
  myservo1.write(160);  // サーボモーターを90度の位置まで動かす
  delay(1000);

}

//VarSpeedServo.hを使ってサーボをゆっくり動かす
#include <VarSpeedServo.h>      
VarSpeedServo myservo;      
 
void setup() {
  myservo.attach(4);     
} 
 
void loop() {
  
  myservo.write(0, 30, true);    // 速度30で0°まで動かし完了を待つ
  delay(1000);
  myservo.write(90, 100, true);  // 速度100で90°まで動かし完了を待つ
  delay(1000);
  myservo.write(180, 255, true); // 速度255で180°まで動かし完了をまつ
  delay(1000);
  
}

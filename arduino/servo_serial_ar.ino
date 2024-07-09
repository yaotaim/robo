#include <Servo.h>

const int LED_PIN = 13;

Servo myservo;
const int SV_PIN = 7;

void setup(){
  myservo.attach(SV_PIN, 500, 2400);
  Serial.begin(115200);              // シリアル通信の開始(ボーレート9600bps)
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
}
 
void loop(){
 
  while(Serial.available() > 0){
    int val = Serial.read();       // 受信したデータを読み込む
    if(val == '1'){                // "1"ならLEDを消灯、"0"ならLEDを点灯
      digitalWrite(LED_PIN, LOW);
      myservo.write(0);  // サーボモーターを0度の位置まで動かす
    } else if(val == '0'){
      myservo.write(90);  // サーボモーターを90度の位置まで動かす
      digitalWrite(LED_PIN, HIGH);
    }
  }
 
 
delay(100);
}


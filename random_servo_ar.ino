//カワロボにランダムで動く頭のサーボを追加しようとした
#include <Servo.h>

Servo myservo;
const int SV_PIN = 7;

void setup() {
  Serial.begin(9600);
  myservo.attach(SV_PIN, 500, 2400);
  randomSeed(100);
}

void loop() {
  long num1;
  long num2;
  long num3;
  num1 = random(0,3);
  num2 = random(45,90);
  num3 = random(100,1000);

  if(num1==0){
    delay(2000);
    Serial.println(num1);//乱数を送信、改行

  }else{
    for(int i=0; i<=num1; i=i+1){
      Serial.println(num1);//乱数を送信、改行
      myservo.write(num2); 
      delay(num3);
      Serial.println(num2);//乱数を送信、改行
      myservo.write(0);
      delay(num3);
    }
  }

  
}

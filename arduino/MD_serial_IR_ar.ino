//MD_serialの進化系。IRセンサーが正常の時に操作可能
#include <AFMotor.h>
AF_DCMotor motor1(1, MOTOR12_64KHZ);//右前
AF_DCMotor motor2(2, MOTOR12_64KHZ);//左前
AF_DCMotor motor3(3, MOTOR12_64KHZ);//左後ろ
AF_DCMotor motor4(4, MOTOR12_64KHZ);//右後ろ

int ds1 =  22;//右前
int ds2= 23;//左前
int ds3 = 24;//左後ろ
int ds4 = 25;//右後ろ

int le = 44;//左目
int me = 26;//真ん中目
int re = 45;//右目



byte val = 0;
byte val3 = 0;
int f=FORWARD;
int b=BACKWARD;
int r=RELEASE;

void setup() {
  Serial.begin(115200);//シリアル通信
  Serial3.begin(9600);
  motor1.setSpeed(255);//右前
  motor2.setSpeed(255);//左前
  motor3.setSpeed(255);//左後ろ
  motor4.setSpeed(255);//右後ろ
}
 
void loop() {
  if (digitalRead(ds1)==LOW && digitalRead(ds2) == LOW && digitalRead(ds3) == LOW && digitalRead(ds4) == LOW){
    if (digitalRead(le)==LOW && digitalRead(me) == HIGH && digitalRead(re) == HIGH){
      motor1.run(f);
      motor2.run(b);
      motor3.run(b);
      motor4.run(f);
      delay(1000);
    }else if(digitalRead(le)==HIGH && digitalRead(me) == HIGH && digitalRead(re) == LOW){
      motor1.run(b);
      motor2.run(f);
      motor3.run(f);
      motor4.run(b);
      delay(1000);
    }else{
        
    if (Serial.available() > 0) {
      val = Serial.read();
      val3=Serial3.read();
      
      if (val3 =='m' ){//面
        Serial.println("men");
        motor1.run(b);
        motor2.run(b);
        motor3.run(b);
        motor4.run(b);
        delay(3000); 

      }else if (val =='u'){//前
        Serial.println("forward"); 
        motor1.run(f);
        motor2.run(f);
        motor3.run(f);
        motor4.run(f);
        delay(1000);  
      }else if (val =='x'){//後
        Serial.println("backward");
        motor1.run(b);
        motor2.run(b);
        motor3.run(b);
        motor4.run(b);
        delay(1000);  
      }else if (val =='q') {//左回
        motor1.run(f);
        motor2.run(b);
        motor3.run(b);
        motor4.run(f);
        delay(1000);  
      }else if (val =='e') {//右回
        motor1.run(b);
        motor2.run(f);
        motor3.run(f);
        motor4.run(b);
        delay(1000);  
      }else if (val =='a') {//左
        motor1.run(f);
        motor2.run(b);
        motor3.run(f);
        motor4.run(b);
        delay(1000);  
      }else if (val =='d') {//右
        motor1.run(b);
        motor2.run(f);
        motor3.run(b);
        motor4.run(f);
        delay(1000);  
      }
      else if (val =='s') {//止
        motor1.run(r);
        motor2.run(r);
        motor3.run(r);
        motor4.run(r);
        delay(1000);  
      }
      else if (val =='g') {//止
        motor1.run(r);
        motor2.run(r);
        motor3.run(r);
        motor4.run(r);
        delay(1000);  
      }
    }else{ 
          motor1.run(f);
          motor2.run(f);
          motor3.run(f);
          motor4.run(f);
          delay(100);  
    }

    }
  
  
  }else if(digitalRead(ds1)==LOW && digitalRead(ds2) == LOW && digitalRead(ds3) == HIGH && digitalRead(ds4) == LOW){
    motor1.run(r);//左後ろ見失う=>右前
    motor2.run(f);
    motor3.run(r);
    motor4.run(f);
    delay(1000);  

  }else if(digitalRead(ds1)==LOW && digitalRead(ds2) == LOW && digitalRead(ds3) == LOW && digitalRead(ds4) == HIGH){
    motor1.run(f);//右後ろ見失う=>左前
    motor2.run(r);
    motor3.run(f);
    motor4.run(r);
    delay(1000);  

  }else if(digitalRead(ds1)==LOW && digitalRead(ds2) == LOW && digitalRead(ds3) == HIGH && digitalRead(ds4) == HIGH){
    motor1.run(f);//後ろ見失う=>前
    motor2.run(f);
    motor3.run(f);
    motor4.run(f);
    delay(1000);

  }else if(digitalRead(ds1)==HIGH && digitalRead(ds2) == LOW && digitalRead(ds3) == LOW && digitalRead(ds4) == LOW){
    motor1.run(b);//右前見失う=>左回り
    motor2.run(b);
    motor3.run(b);
    motor4.run(b);
    delay(1000); 
    motor1.run(f);
    motor2.run(b);
    motor3.run(b);
    motor4.run(f);
    delay(4000);
  
  }else if(digitalRead(ds1)==LOW && digitalRead(ds2) == HIGH && digitalRead(ds3) == LOW && digitalRead(ds4) == LOW){
    motor1.run(b);//左前失う=>右まわり
    motor2.run(b);
    motor3.run(b);
    motor4.run(b);
    delay(1000); 
    motor1.run(b);
    motor2.run(f);
    motor3.run(f);
    motor4.run(b);
    delay(3800);
  
  }else if(digitalRead(ds1)==HIGH && digitalRead(ds2) == HIGH && digitalRead(ds3) == LOW && digitalRead(ds4) == LOW){
    motor1.run(b);//前失う=>右まわり
    motor2.run(b);
    motor3.run(b);
    motor4.run(b);
     delay(1000); 
    motor1.run(b);
    motor2.run(f);
    motor3.run(f);
    motor4.run(b);
    delay(3800);
    
  }else{
    motor1.run(r);
    motor2.run(r);
    motor3.run(r);
    motor4.run(r);
  }
  //delay(100);
}

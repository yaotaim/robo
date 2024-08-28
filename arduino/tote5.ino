#define IR_LED_L 4
#define IR_LED_R 5
#define RMO_EA   3
#define RMO_EB   6
#define RMO_MB1  7
#define RMO_MB2  8
#define RMO_MA2 11
#define RMO_MA1 12

boolean R_IRLED_R;
boolean R_IRLED_L;

#include <Servo.h>
#define SERVOPIN 9
Servo head;

#define HC_ECHO  2
#define HC_TRIG 10
double HScm = 0;

int kioku= 0;

void GetIR(){
  R_IRLED_R=digitalRead(IR_LED_R);
  R_IRLED_L=digitalRead(IR_LED_L);
}

void go() {
  analogWrite(RMO_EA, 80);
  digitalWrite(RMO_MA1, HIGH);
  digitalWrite(RMO_MA2, LOW);
  analogWrite(RMO_EB, 110);
  digitalWrite(RMO_MB1, HIGH);
  digitalWrite(RMO_MB2, LOW);
  Serial.println("前進します");
}

void turnright() {
  analogWrite(RMO_EA, 110);//////////要調整
  digitalWrite(RMO_MA1, LOW);
  digitalWrite(RMO_MA2, HIGH);
  analogWrite(RMO_EB, 130);//////////要調整
  digitalWrite(RMO_MB1, HIGH);
  digitalWrite(RMO_MB2, LOW);
  Serial.println("右折します");
}

void turnleft() {
  analogWrite(RMO_EA, 110);//////////要調整
  digitalWrite(RMO_MA1, HIGH);
  digitalWrite(RMO_MA2, LOW);
  analogWrite(RMO_EB, 130);//////////要調整
  digitalWrite(RMO_MB1, LOW);
  digitalWrite(RMO_MB2, HIGH);
  Serial.println("左折します");
}

void turnleft2() {//早く回転
  analogWrite(RMO_EA, 150);//////////要調整
  digitalWrite(RMO_MA1, HIGH);
  digitalWrite(RMO_MA2, LOW);
  analogWrite(RMO_EB, 180);//////////要調整
  digitalWrite(RMO_MB1, LOW);
  digitalWrite(RMO_MB2, HIGH);
  Serial.println("超左折します");
}

void turnright2() {//早く回転
  analogWrite(RMO_EA, 160);//////////要調整
  digitalWrite(RMO_MA1, HIGH);
  digitalWrite(RMO_MA2, LOW);
  analogWrite(RMO_EB, 190);//////////要調整
  digitalWrite(RMO_MB1, LOW);
  digitalWrite(RMO_MB2, HIGH);
  Serial.println("超左折します");
}

void stopmotor() {
  analogWrite(RMO_EA, 0); 
  digitalWrite(RMO_MA1, LOW);
  digitalWrite(RMO_MA2, LOW);
  analogWrite(RMO_EB, 0);
  digitalWrite(RMO_MB1, LOW);
  digitalWrite(RMO_MB2, LOW);
  Serial.println("止まります");
}

void setup(){
  pinMode(IR_LED_L, INPUT);
  pinMode(IR_LED_R, INPUT);
  pinMode(RMO_EA, OUTPUT);
  pinMode(RMO_EB, OUTPUT); 
  pinMode(RMO_MB1, OUTPUT);
  pinMode(RMO_MB2, OUTPUT);
  pinMode(RMO_MA1, OUTPUT);
  pinMode(RMO_MA2, OUTPUT);
  Serial.begin(115200);
  head.attach(SERVOPIN,500,2400);
  pinMode(HC_TRIG,OUTPUT);
  pinMode(HC_ECHO,INPUT);
  head.write(90);//正面向く
}

void cho(){
  digitalWrite(HC_TRIG,LOW);
  digitalWrite(HC_ECHO,LOW);
  delayMicroseconds(1);
  digitalWrite(HC_TRIG,HIGH);
  delayMicroseconds(10);
  digitalWrite(HC_ECHO,LOW);
  HScm=pulseIn(HC_ECHO,HIGH,5000)/50.0;
  Serial.print("超音波センサー=");
  Serial.println(HScm);
  Serial.println("");
}

void loop(){
  GetIR();
  if(R_IRLED_L==0 && R_IRLED_R==0){
    if(kioku>300 ){
      head.write(0);//右向く
      stopmotor();
      delay(100);
      cho();

      if(HScm==0){//右側超音波反応なし
        Serial.print("超右折");
        head.write(90);//正面向く
        turnright2();
        delay(400);

      }else{//右側超音波反応あり
        head.write(180);//左向く
        delay(500);

        cho();
        if(HScm==0){//左側超音波反応なし
          Serial.print("超左折");
          head.write(90);//正面向く
          turnleft2();
          delay(400);
        }else{
          Serial.print("Uターン");
          head.write(90);
          turnleft2();
          delay(1000);
        }
      }
    kioku=0;
    }else{
      kioku+=1;
    }

  }else if(R_IRLED_L==1 && R_IRLED_R==0){//右反応
    head.write(90);/////////////////////ここ間違ってた
    if(kioku>500){
      turnleft();
      delay(100);
      kioku=0;
    }else{
      kioku+=1;
    }

  }else if(R_IRLED_L==1 && R_IRLED_R==0){//IRセンサ左反応
    head.write(90);/////////////////////ここ間違ってた
    if(kioku>500){
      turnright();
      delay(100);////////////要調整
      kioku=0;
    }else{
      kioku+=1;
    }

  }else{//IRどっちも反応なし
    cho();
    if(HScm!=0){//超音波反応あれば
      Serial.println("ペットボトル発見");
      stopmotor();
      delay(100);
      if(HScm!>14){
        Serial.println("チキンレース");
        go();
        delay(100);
      }else{
        Serial.println("もう近づけないよ");
        stopmotor();
      }
    }else{
      go();
    }
  }
  Serial.println(kioku);
}



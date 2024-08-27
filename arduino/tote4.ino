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

//int speed_right = 70; 消す
//int speed_left = 100;　消す

#include <Servo.h>
#define SERVOPIN 9
Servo head;

#define HC_ECHO  2
#define HC_TRIG 10
double HScm = 0;

int kioku= 0;

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
  //head.attach(SERVOPIN,500,2400);/////////////////////いらん
  head.write(0);//正面向く
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
  //delay(500);////////////////////////////ここ調整
}

void loop(){
  GetIR();
  if(R_IRLED_L==0 && R_IRLED_R==0){//IRセンサどっちも反応
    if(kioku>300 ){
      stopmotor();
      delay(100);

      //head.write(0);//右向く
      //delay(500);//////////////////////////////////短くする

      cho();
      if(HScm==0){//右側超音波反応なし
        Serial.print("右折開始するぞ");
        //head.write(90);//正面向く
        turnright();
        delay(1000);
        //stopmotor();
        //delay(1000);
        //go();//まっすぐに戻す.     消してみる
        //delay(100);
      }else{
        head.write(180);//左向く
        delay(500);//////////////////////////////短くする

        cho();
        if(HScm==0){//右側超音波反応なし
          Serial.print("左折開始するぞ");
          head.write(0);//正面向く
          turnleft();
          delay(1000);
          //stopmotor();
          //delay(500);
          //go();//まっすぐに戻す.     消してみる
          //delay(100);
        }else{
          Serial.print("Uターン開始するぞ");
          head.write(0);
          turnleft2();
          delay(1500);
          //head.write(90);//正面向く            追加する!!
          //delay(500);//.                     追加する!!
          //go();//まっすぐに戻す
          //delay(100);
        }
      }
    kioku=0;
    }else{
      kioku+=1;
    }

  }else if(R_IRLED_L==1 && R_IRLED_R==0){//IRセンサ右反応
    if(kioku>300){
      //head.write(0);//正面向く       消してみる
      turnleft();
      delay(200);////////////要調整
      kioku=0;
    }else{
      kioku=1;
    }

  }else if(R_IRLED_L==1 && R_IRLED_R==0){//IRセンサ左反応
    if(kioku>300){
      //head.write(0);//正面向く       消してみる
      turnright();
      delay(200);////////////要調整
      kioku=0;
    }else{
      kioku+=1;
    }

  }else{//IRどっちも反応なし
    cho();
    if(HScm!=0){//反応あり
      go();
      Serial.println("壁あり");
    }else{//反応なし
      head.write(180);//左向く
      delay(500);//////////////////////////////短くする
      cho();
      if(HScm==0){//右側超音波反応なし
        Serial.print("壁なし=ペット前");
        head.write(90);//前向く
        while(HScm>5){
          cho();
          go();
          delay(100);
        }
      }
    }
    kioku=0;
  }
  Serial.println(kioku);
}

void GetIR(){
  R_IRLED_R=digitalRead(IR_LED_R);
  R_IRLED_L=digitalRead(IR_LED_L);
  //Serial.print("赤外線センサー右=");
  //Serial.println(R_IRLED_R);
  //Serial.print("赤外線センサー左=");
  //Serial.println(R_IRLED_L);
  //Serial.print("");
  //kioku_L+=1;//       消してみる
  //kioku_R+=1;//       消してみる
}

void go() {
  analogWrite(RMO_EA, 70);//実数値に変えた
  digitalWrite(RMO_MA1, HIGH);
  digitalWrite(RMO_MA2, LOW);
  analogWrite(RMO_EB, 100);//実数値に変えた
  digitalWrite(RMO_MB1, HIGH);
  digitalWrite(RMO_MB2, LOW);
  Serial.println("前進します");
}

void turnright() {
  analogWrite(RMO_EA, 200);//////////要調整
  digitalWrite(RMO_MA1, HIGH);//ここLOWでスピード落とすのも作る100ぐらい
  digitalWrite(RMO_MA2, HIGH);
  analogWrite(RMO_EB, 200);//////////要調整
  digitalWrite(RMO_MB1, HIGH);
  digitalWrite(RMO_MB2, LOW);
  Serial.println("右折します");
}

void turnleft() {
  analogWrite(RMO_EA, 190);//////////要調整
  digitalWrite(RMO_MA1, HIGH);
  digitalWrite(RMO_MA2, LOW);
  analogWrite(RMO_EB, 190);//////////要調整
  digitalWrite(RMO_MB1, HIGH);
  digitalWrite(RMO_MB2, HIGH);//ここLOWでスピード落とすのも作る100ぐらい
  Serial.println("左折します");
}

void turnleft2() {//早く回転
  analogWrite(RMO_EA, 190);//////////要調整
  digitalWrite(RMO_MA1, HIGH);
  digitalWrite(RMO_MA2, LOW);
  analogWrite(RMO_EB, 190);//////////要調整
  digitalWrite(RMO_MB1, LOW);
  digitalWrite(RMO_MB2, HIGH);
  Serial.println("超左折します");
}

void stopmotor() {
  analogWrite(RMO_EA, 0); //0にする
  digitalWrite(RMO_MA1, LOW);//全部LOWにしてみる
  digitalWrite(RMO_MA2, LOW);//全部LOWにしてみる
  analogWrite(RMO_EB, 0); //0にする
  digitalWrite(RMO_MB1, LOW);//全部LOWにしてみる
  digitalWrite(RMO_MB2, LOW);//全部LOWにしてみる
  Serial.println("止まります");
}

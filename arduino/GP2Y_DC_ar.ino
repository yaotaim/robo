//GP2YとDCの合体。距離センサー反応中はDCモーター動く
float Vcc = 5.0;//電源電圧
float distance_1;
float distance_2;
const int ANALOG = 8;//センサ信号入力
int ledPin = 50;

#define IN1 9
#define IN2 8

void setup(){
  Serial.begin(9600);//シリアル通信
  pinMode(IN1,OUTPUT);
  pinMode(IN2,OUTPUT);
  }

void loop(){ 
 distance_1 = Vcc*analogRead(ANALOG)/1023; //(5.0V*センサ数値/1023)1023は5V入力時の値
 distance_2 = 26.549*pow(distance_1,-1.2091); //距離換算
 Serial.println(distance_2);
 if (distance_2<15){
  digitalWrite(IN1,LOW);
  digitalWrite(IN2,HIGH);
  delay(100);    
  }
  else{
  digitalWrite(IN1,HIGH);     //どちらかがHIGHでモータが周ります。
  digitalWrite(IN2,HIGH);
  delay(100);    
  }
 delay(100); 
 } 

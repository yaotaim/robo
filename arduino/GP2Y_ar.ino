//arduinoでシャープの距離センサーを使う
float Vcc = 5.0;//電源電圧
float distance_1;
float distance_2;
const int ANALOG = 0;//センサ信号入力
int ledPin = 50;

void setup(){
  pinMode(ledPin, OUTPUT);
 Serial.begin(9600);//シリアル通信
  }

void loop(){ 
 distance_1 = Vcc*analogRead(ANALOG)/1023; //(5.0V*センサ数値/1023)1023は5V入力時の値
 distance_2 = 26.549*pow(distance_1,-1.2091); //距離換算
 Serial.println(distance_2);
 if (distance_2<15){
  digitalWrite(ledPin, HIGH);  
  }
  else{
    digitalWrite(ledPin, LOW);  
  }
 delay(100); 
 } 

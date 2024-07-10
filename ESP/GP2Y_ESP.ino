int LED =4;
const int voutPin = 35;
const int volt = 3.3;
const int ANALOG_MAX = 4096;
const int Threshold = 1000; //点灯する電圧値[mV]

void setup() {
 
Serial.begin (115200);
pinMode(LED,OUTPUT);
}

void loop() {
 
  int reading = analogRead(voutPin) ;//25pinを読み取る
  float voltage = ((long)reading*volt*1000)/ANALOG_MAX ;//読み取りした値を電圧に計算する
  Serial.print(voltage);//シリアル通信で表示
  Serial.println("mV");

  if(voltage>Threshold){
    Serial.println("正常");
  }else if(voltage<Threshold){
    Serial.println("あぶない");
  }

/*
if(voltage>Threshold){
  digitalWrite (LED,HIGH);
  delay (500);//電圧値が1300mV以上はLED点灯
  } else if(voltage<Threshold)
  {digitalWrite (LED,LOW);
*/
delay (100);//電圧値が1300mV以上はLED消灯
    

}

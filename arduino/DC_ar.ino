//arduinoでL293DでDCモーター動かす
#define IN1 9
#define IN2 8
#define ENA 10

void setup() {
  pinMode(IN1,OUTPUT);
  pinMode(IN2,OUTPUT);
  pinMode(ENA,OUTPUT);
}

void analog1(){
  int i;
  digitalWrite(IN1,HIGH);
  digitalWrite(IN2,LOW);
  for(i=0;i<256;i++){
    analogWrite(ENA,i);
    delay(20);
  }

  for(i=255;i>=0;i--){
    analogWrite(ENA,i);
    delay(20);
  }

  digitalWrite(IN1,LOW);  //無くても動くが、
  digitalWrite(IN2,LOW);  //リフレッシュの意味で
}                         //あった方がいいみたい

void loop() {
  analog1();
}

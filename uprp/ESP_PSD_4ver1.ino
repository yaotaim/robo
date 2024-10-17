// ESP_PSD_4ver1
#include <Arduino.h>
const int PSD_1 = 14;
const int PSD_2 = 26;
const int PSD_3 = 12;
const int PSD_4 = 27;

int sensa_1[10];
int sensa_2[10];
int sensa_3[10];
int sensa_4[10];

int jyotai_1 = 0; 
int jyotai_2 = 0; 
int jyotai_3 = 0; 
int jyotai_4 = 0; 

String State = "初期";

void US(int reading, int lowerBound, int upperBound, int sensa[]) {
  for (int i = 9; i > 0; i--) {
    sensa[i] = sensa[i - 1];
  }
  if (reading > lowerBound && reading < upperBound) {
    sensa[0] = 0;
  } else {
    sensa[0] = 1;
  }
}

int SUM(int sensa[]) {
  int sum = 0;
  for (int i = 0; i < 10; i++) {
    sum += sensa[i];
  }
  return sum;
}

void setup() {
  Serial.begin(115200);
}

void loop() {
  int reading_1 = analogRead(PSD_1);
  int reading_2 = analogRead(PSD_2);
  int reading_3 = analogRead(PSD_3);
  int reading_4 = analogRead(PSD_4);
  
  Serial.println(reading_1);
  Serial.println(reading_2);
  Serial.println(reading_3);
  Serial.println(reading_4);

  US(reading_1, 1000, 1300, sensa_1);
  US(reading_2, 1500, 1700, sensa_2);
  US(reading_3, 1100, 1300, sensa_3);
  US(reading_4, 1100, 1300, sensa_4);

  int sum_1 = SUM(sensa_1);
  int sum_2 = SUM(sensa_2);
  int sum_3 = SUM(sensa_3);
  int sum_4 = SUM(sensa_4);

  if (sum_1 >= 7) {
    Serial.print("1:x");
    jyotai_1 = 1;  
  } else {
    Serial.print("1:o");
    jyotai_1 = 0;  
  }

  if (sum_2 >= 7) {
    Serial.print("2:x");
    jyotai_2 = 1;  
  } else {
    Serial.print("2:o");
    jyotai_2 = 0;  
  }

  if (sum_3 >= 7) {
    Serial.print("3:x");
    jyotai_3 = 1;  
  } else {
    Serial.print("3:o");
    jyotai_3 = 0;  
  }

  if (sum_4 >= 7) {
    Serial.print("4:x");
    jyotai_4 = 1;  
  } else {
    Serial.print("4:o");
    jyotai_4 = 0;  
  }

  if (jyotai_1 == 1 && jyotai_2 == 1 && jyotai_3 == 1 && jyotai_4 == 1) {//全部バツ
      if(State!="s"){
        Serial.println("s");
        State = "s";
      }
  } else if (jyotai_1 == 1 && jyotai_2 == 0 && jyotai_3 == 0 && jyotai_4 == 0) {//右前だけバツ
      if(State!="e"){
        Serial.println("e");
        State = "e";
      }
    } else if (jyotai_1 == 0 && jyotai_2 == 1 && jyotai_3 == 0 && jyotai_4 == 0) {//左前だけバツ
      if(State!="q"){
        Serial.println("q");
        State = "q";
      }
    } else if (jyotai_1 == 0 && jyotai_2 == 0 && jyotai_3 == 1 && jyotai_4 == 0) {//右後ろだけバツ
      if(State!="c"){
        Serial.println("c");
        State = "c";
      }
    } else if (jyotai_1 == 0 && jyotai_2 == 0 && jyotai_3 == 1 && jyotai_4 == 0) {//左後ろだけバツ
      if(State!="z"){
        Serial.println("z");
        State = "z";
      }
    } else if (jyotai_1 == 1 && jyotai_2 == 1 && jyotai_3 == 0 && jyotai_4 == 0) {//前両方バツ
      if(State!="w"){
        Serial.println("w");
        State = "w";
      }
    } else if (jyotai_1 == 0 && jyotai_2 == 0 && jyotai_3 == 1 && jyotai_4 == 1) {//後ろ両方バツ
      if(State!="x"){
        Serial.println("x");
        State = "x";
      }
    } else{ //正常
      if(State!="r"){
        Serial.println("r");
        State = "r";
      }
  delay(100);
}

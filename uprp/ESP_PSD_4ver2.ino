//ESP_PSD_4_serial
#include <Arduino.h>
const int PSD_1 = 14;//右前
const int PSD_2 = 26;//左前
const int PSD_3 = 12;//右後ろ
const int PSD_4 = 27;//左後ろ

int PSData_1 = 0; 
int PSData_2 = 0; 
int PSData_3 = 0; 
int PSData_4 = 0; 

int jyotai_1 = 0; 
int jyotai_2 = 0; 
int jyotai_3 = 0; 
int jyotai_4 = 0; 

String State = "初期";

void  US(int reading, int lower, int upper, int &PSData) {
  if (lower < reading && reading < upper) {
    PSData = 0;
  } else {
    PSData += 1;
  }
}

void setup() {
  Serial.begin(115200);
}

void loop() {
  int reading_1 = analogRead(PSD_1);
  int reading_2 = analogRead(PSD_2);
  int reading_3 = analogRead(PSD_3);
  int reading_4 = analogRead(PSD_4);
  //Serial.println(reading_1);
  //Serial.println(reading_2);
  //Serial.println(reading_3);
  //Serial.println(reading_4);

  US(reading_1, 1700, 1800, PSData_1);
  US(reading_2, 1500, 1700, PSData_2);
  US(reading_3, 1200, 1600, PSData_3);
  US(reading_4, 1400, 1700, PSData_4);

  //Serial.println(PSData_1);
  //Serial.println(PSData_2);
  //Serial.println(PSData_3);
  //Serial.println(PSData_4);

  if (PSData_1 >= 5) {
    //Serial.print("1:x");
    jyotai_1 = 1;  
  } else {
    //Serial.print("1:o");
    jyotai_1 = 0;  
  }

  if (PSData_2 >= 5) {
    //Serial.print("2:x");
    jyotai_2 = 1;  
  } else {
    //Serial.print("2:o");
    jyotai_2 = 0;  
  }

  if (PSData_3 >= 5) {
    //Serial.print("3:x");
    jyotai_3 = 1;  
  } else {
    //Serial.print("3:o");
    jyotai_3 = 0;  
  }

  if (PSData_4 >= 5) {
    //Serial.println("4:x");
    jyotai_4 = 1;  
  } else {
    //Serial.println("4:o");
    jyotai_4 = 0;  
  }

  if (jyotai_1 == 1 && jyotai_2 == 1 && jyotai_3 == 1 && jyotai_4 == 1) {//全部バツ
      if(State!="s"){
        Serial.println("s");
        State = "s";
      }
      PSData_1=0;
      PSData_2=0;
      PSData_3=0;
      PSData_4=0;
    } else if (jyotai_1 == 1 && jyotai_2 == 0 && jyotai_3 == 0 && jyotai_4 == 0) {//右前だけバツ
      if(State!="e"){
        Serial.println("e");
        State = "e";
      }
      PSData_1=0;
      PSData_2=0;
      PSData_3=0;
      PSData_4=0;
    } else if (jyotai_1 == 0 && jyotai_2 == 1 && jyotai_3 == 0 && jyotai_4 == 0) {//左前だけバツ
      if(State!="q"){
        Serial.println("q");
        State = "q";
      }
      PSData_1=0;
      PSData_2=0;
      PSData_3=0;
      PSData_4=0;
    } else if (jyotai_1 == 0 && jyotai_2 == 0 && jyotai_3 == 1 && jyotai_4 == 0) {//右後ろだけバツ
      if(State!="c"){
        Serial.println("c");
        State = "c";
      }
      PSData_1=0;
      PSData_2=0;
      PSData_3=0;
      PSData_4=0;
    } else if (jyotai_1 == 0 && jyotai_2 == 0 && jyotai_3 == 1 && jyotai_4 == 0) {//左後ろだけバツ
      if(State!="z"){
        Serial.println("z");
        State = "z";
      }
      PSData_1=0;
      PSData_2=0;
      PSData_3=0;
      PSData_4=0;
    } else if (jyotai_1 == 1 && jyotai_2 == 1 && jyotai_3 == 0 && jyotai_4 == 0) {//前両方バツ
      if(State!="w"){
        Serial.println("w");
        State = "w";
      }
      PSData_1=0;
      PSData_2=0;
      PSData_3=0;
      PSData_4=0;
    } else if (jyotai_1 == 0 && jyotai_2 == 0 && jyotai_3 == 1 && jyotai_4 == 1) {//後ろ両方バツ
      if(State!="x"){
        Serial.println("x");
        State = "x";
      }
      PSData_1=0;
      PSData_2=0;
      PSData_3=0;
      PSData_4=0;
    } else{ //正常
      if(State!="r"){
        Serial.println("r");
        State = "r";
      }
    }
  delay(100);
}


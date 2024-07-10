//リフト。シリアルで動かすシリアル来ていなかったらゆっくり上下に動く
#include <ESP32Servo.h>

#define SP1 26 // 右前1
#define SP2 25 // 左前2
#define SP3 33 // 右後3
#define SP4 32 // 左後4

#define SP5 27 //手首
#define SP6 14 //肩
#define SP7 12 //腰

Servo Servo1;
Servo Servo2;
Servo Servo3;
Servo Servo4;

Servo Servo5;
Servo Servo6;
Servo Servo7;


int S_kioku1 = 60;
int S_kioku2 = 40;
int S_kioku3 = 30;
int S_kioku4 = 60;

int S_kioku5 = 30;
int S_kioku6 = 130;
int S_kioku7 = 130;


int kioku_dousa=0;

byte val = 0;

const int IR1 = 4;
const int IR2 = 5;
const int IR3 = 16;
const int IR4 = 17;

int IR1_kioku=0;

byte lastSt1 = 0xFF;  // 前回のIR1状態
byte lastSt2 = 0xFF;  // 前回のIR2状態
byte lastSt3 = 0xFF;  // 前回のIR3状態
byte lastSt4 = 0xFF;  // 前回のIR4状態

byte fixedSt1 = 0xFF; // 確定IR1状態
byte fixedSt2 = 0xFF; // 確定IR2状態
byte fixedSt3 = 0xFF; // 確定IR3状態
byte fixedSt4 = 0xFF; // 確定IR4状態

unsigned long smpltmr = 0;  // サンプル時間
unsigned long lastSerialTime = 0; // 最後にシリアル通信があった時間

TaskHandle_t thp[1]; // マルチスレッドのタスクハンドル格納用
volatile bool stopServos = false; // サーボモーターの動作を制御するフラグ

void setup() {
  Serial.begin(115200);
  Servo1.attach(SP1);
  Servo2.attach(SP2);
  Servo3.attach(SP3);
  Servo4.attach(SP4);

  Servo5.attach(SP5);
  Servo6.attach(SP6);
  Servo7.attach(SP7);


  Servo(60, 40, 30, 60);
  Servo_arm(30,130,130);
  delay(500);
  

  pinMode(IR1, INPUT);
  pinMode(IR2, INPUT);
  pinMode(IR3, INPUT);
  pinMode(IR4, INPUT);

  // タスクの作成
  xTaskCreatePinnedToCore(IRTask, "IRTask", 4096, NULL, 3, &thp[0], 0);
}


void Servo(int S_moku1, int S_moku2, int S_moku3, int S_moku4) {
  Servo1.write(S_moku1);
  Servo2.write(S_moku2);
  Servo3.write(S_moku3);
  Servo4.write(S_moku4);

  S_kioku1 = S_moku1;
  S_kioku2 = S_moku2;
  S_kioku3 = S_moku3;
  S_kioku4 = S_moku4;
}

void Servo_arm(int S_moku5, int S_moku6, int S_moku7) {
  Servo5.write(S_moku5);
  Servo6.write(S_moku6);
  Servo7.write(S_moku7);

  S_kioku5 = S_moku5;
  S_kioku6 = S_moku6;
  S_kioku7 = S_moku7;
}

void slow_Servo(int S_moku1, int S_moku2, int S_moku3, int S_moku4) {
  bool zou1 = S_kioku1 < S_moku1;
  bool zou2 = S_kioku2 < S_moku2;
  bool zou3 = S_kioku3 < S_moku3;
  bool zou4 = S_kioku4 < S_moku4;

  while (S_kioku1 != S_moku1 || S_kioku2 != S_moku2 || S_kioku3 != S_moku3 || S_kioku4 != S_moku4) {
    if (S_kioku1 != S_moku1) {
      S_kioku1 += zou1 ? 1 : -1;
      Servo1.write(S_kioku1);
    }
    if (S_kioku2 != S_moku2) {
      S_kioku2 += zou2 ? 1 : -1;
      Servo2.write(S_kioku2);
    }
    if (S_kioku3 != S_moku3) {
      S_kioku3 += zou3 ? 1 : -1;
      Servo3.write(S_kioku3);
    }
    if (S_kioku4 != S_moku4) {
      S_kioku4 += zou4 ? 1 : -1;
      Servo4.write(S_kioku4);
    }
    delay(20);
  }
}


void loop() {
  //Serial.println(kioku_dousa);
  if (Serial.available() > 0) {
    val = Serial.read();
    lastSerialTime = millis();

    if ((val == 'v' || val == 'b' || val == 'n') && !stopServos) {//よろしく
      Servo(60, 40, 30, 60);//下
      delay(500);
      kioku_dousa=0;
    
      Servo_arm(0,90,130);
      delay(500);
      Servo_arm(30,130,130);
      delay(1000);
    }

    else if (val == 'f' && !stopServos) {//上がります
      Servo(20, 70, 60, 20);//上
      //下
      kioku_dousa=1;
    }
    else if (val == 'g' && !stopServos) {//下がります
      Servo(60, 40, 30, 60);//下
      kioku_dousa=0;
    }
    else if (val == 'r' && !stopServos) {//めん
      Servo(20, 70, 60, 20);//上
      delay(500);
      Servo_arm(40,100,130);
      delay(500);
      Servo_arm(30,130,130);
      delay(1000);
      
      kioku_dousa=1;
    }
    else if (val == 't' && !stopServos) {//どう
      Servo(60, 40, 30, 60);//下
      delay(500);
      kioku_dousa=0;
      Servo_arm(30,110,50);
      delay(700);
      Servo_arm(30,130,130);
      delay(1000);
    }
    lastSerialTime = millis(); // 繰り返し間隔を維持するためにタイムスタンプを更新
  }

  if (millis() - lastSerialTime >= 3000) {
    //Serial.println("machi");

    if (kioku_dousa==0) {
      //Serial.println("machi0");
      if(S_kioku1 != 20 || S_kioku2 != 70 || S_kioku3 != 60 || S_kioku4 != 20){
        if(S_kioku1 != 20){
          S_kioku1=S_kioku1-1;
        }
        if(S_kioku2 != 70){
          S_kioku2=S_kioku2+1;
        }
        if(S_kioku3 != 60){
          S_kioku3=S_kioku3+1;
        }
        if(S_kioku4 != 20){
          S_kioku4=S_kioku4-1;
        }
        Servo(S_kioku1, S_kioku2, S_kioku3, S_kioku4);
        //Serial.print("Servo1:");
        //Serial.println(S_kioku1);
        //Serial.print("Servo2:");
        //Serial.println(S_kioku2);
        //Serial.print("Servo3:");
        //Serial.println(S_kioku3);
        //Serial.print("Servo4:");
        //Serial.println(S_kioku4);
        delay(20);
      }else if(S_kioku1 == 20 && S_kioku2 == 70 && S_kioku3 == 60 && S_kioku4 == 20){
        kioku_dousa=1;
      }
    }else{
      //Serial.println("machi1");
      if(S_kioku1 != 60 || S_kioku2 != 40 || S_kioku3 != 30 || S_kioku4 != 60){
        if(S_kioku1 != 60){
          S_kioku1=S_kioku1+1;
        }
        if(S_kioku2 != 40){
          S_kioku2=S_kioku2-1;
        }
        if(S_kioku3 != 30){
          S_kioku3=S_kioku3-1;
        }
        if(S_kioku4 != 60){
          S_kioku4=S_kioku4+1;
        }
        Servo(S_kioku1, S_kioku2, S_kioku3, S_kioku4);
        //Serial.print("Servo1:");
        //Serial.println(S_kioku1);
        //Serial.print("Servo2:");
        //Serial.println(S_kioku2);
        //Serial.print("Servo3:");
        //Serial.println(S_kioku3);
        //Serial.print("Servo4:");
        //Serial.println(S_kioku4);
        delay(20);
      }else if(S_kioku1 == 60 && S_kioku2 == 40 && S_kioku3 == 30 && S_kioku4 == 60){
        kioku_dousa=0;
      }
    }  
  }
}

void IRTask(void *args) {
  while (1) {
    if (millis() - smpltmr >= 10) {
      smpltmr = millis();

      byte st1 = digitalRead(IR1);
      byte st2 = digitalRead(IR2);
      byte st3 = digitalRead(IR3);
      byte st4 = digitalRead(IR4);

      if (st1 == lastSt1 && st2 == lastSt2 && st3 == lastSt3 && st4 == lastSt4) {
        if (st1 != fixedSt1 || st2 != fixedSt2 || st3 != fixedSt3 || st4 != fixedSt4) {
          fixedSt1 = st1;
          fixedSt2 = st2;
          fixedSt3 = st3;
          fixedSt4 = st4;

          st1 = (~st1) & 0x01;
          st2 = (~st2) & 0x01;
          st3 = (~st3) & 0x01;
          st4 = (~st4) & 0x01;

          //Serial.print("Sensor IR1:");
          //Serial.println(st1);
          //Serial.print("Sensor IR2:");
          //Serial.println(st2);
          //Serial.print("Sensor IR3:");
          //Serial.println(st3);
          //Serial.print("Sensor IR4:");
          //Serial.println(st4);

          
          if (st1 == 1) {
            if(IR1_kioku==0 ){
              Serial.println("i");
              IR1_kioku=1;
            }
            else{
              IR1_kioku=0;
            }
            
          }
        }
      }
      lastSt1 = st1;
      lastSt2 = st2;
      lastSt3 = st3;
      lastSt4 = st4;
    }
    vTaskDelay(1); //
  }
}


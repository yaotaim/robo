//IRセンサーとservoのマルチ処理
#include <ESP32Servo.h>

#define SP1 32
#define SP2 33

Servo myServo1;
Servo myServo2;

byte val = 0;

const int IR_SENSOR = 5;  // 赤外線センサ
const int LED = 12;       // LED
byte lastSt = 0xFF;       // 前回赤外線センサ状態
byte fixedSt = 0xFF;      // 確定赤外線センサ状態
unsigned long smpltmr = 0;  // サンプル時間

TaskHandle_t thp[1];//マルチスレッドのタスクハンドル格納用
volatile bool stopServos = false; // サーボモーターの動作を制御するフラグ

void setup() {
  Serial.begin(115200);
  myServo1.attach(SP1);
  myServo2.attach(SP2);
  pinMode(IR_SENSOR, INPUT);

  // タスクの作成
  xTaskCreatePinnedToCore(IRTask, "IRTask", 4096, NULL, 3, &thp[0], 0); 
}

void loop() {
  if (Serial.available() > 0) { // もしJetson側から命令が来ていたら
    val = Serial.read();
    
    if (val == 'm' && !stopServos) { // Jetsonから面命令、かつサーボが停止指示されていない場合
      myServo1.write(0);
      delay(500);
      myServo1.write(90);
      delay(500);
      myServo1.write(180);
      delay(500);
      myServo1.write(0);
      delay(500);
    }
  }
}

void IRTask(void *args) {
  while (1) {
    if (millis() - smpltmr >= 40) {
      smpltmr = millis();
      
      byte st = digitalRead(IR_SENSOR);
      if (st == lastSt) {
        if (st != fixedSt) {
          fixedSt = st;
          st = (~st) & 0x01;
          Serial.print("Sensor:");
          Serial.println(st);
/*
          // センサーが1の場合、サーボを停止する
          if (st == 1) {
            stopServos = true;
            myServo1.detach();
            myServo2.detach();
          } else {
            stopServos = false;
            myServo1.attach(SP1);
            myServo2.attach(SP2);
          }
          */
        }
      }
      lastSt = st;
    }
    vTaskDelay(1); // タスクの一時停止
  }
}

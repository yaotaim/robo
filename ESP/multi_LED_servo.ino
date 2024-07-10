//ESPでマルチタスク+シリアル入力でLチカ+サーボ
#include <ESP32Servo.h>

byte val = 0;

#define SP1 32

Servo myServo1;

// プロトタイプ宣言
void taskServo(void *pvParameters);
void taskLED(void *pvParameters);

void setup() {
    Serial.begin(115200);

    myServo1.attach(SP1);

    // GPIOピンモードを設定
    pinMode(23, OUTPUT);
    digitalWrite(23, LOW);

    // FreeRTOSを使用してタスクを作成
    xTaskCreate(taskServo, "TaskServo", 2048, NULL, 1, NULL);
    xTaskCreate(taskLED, "TaskLED", 2048, NULL, 1, NULL);
}

void loop() {
  // メインループは空。すべての処理はタスクで行われる。
}

void taskServo(void *pvParameters) {
  while (true) {
    myServo1.write(0);
    delay(4000);
    myServo1.write(90);
    delay(4000);
    myServo1.write(180);
    delay(4000);
    myServo1.write(90);
    delay(4000);
  }
}

void taskLED(void *pvParameters) {
  while (true) {
    if (Serial.available() > 0) {
      val = Serial.read();
    
      if(val == 'n') {
          Serial.println("点灯");
          digitalWrite(23, HIGH);  
      } else if (val == 'm'){
          Serial.println("消灯");
          digitalWrite(23, LOW);  
      }
    }
    delay(100); // 少し待機してCPU使用率を下げる
  }
}


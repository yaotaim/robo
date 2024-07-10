const int IR1 = 5;  // 赤外線センサ

byte lastSt = 0xFF;       // 前回赤外線センサ状態
unsigned long smpltmr = 0;  // サンプル時間
 
void setup() {
  pinMode(IR1, INPUT);
  Serial2.begin(115200);
  Serial.begin(115200);
}
 
void loop() {
 while (1) {
    byte newSt= digitalRead(IR1);
    if (newSt != lastSt) {
      lastSt = newSt;
      if (newSt == LOW) {
        Serial2.println("u");
        Serial.println("u");
      }
    }
    delay(10);
  }
}

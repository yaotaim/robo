//ESPとESPの通信送る側
//今回serial2使う
byte val = 0;
void setup() {
  // シリアル初期化
  Serial.begin(115200);
  while(!Serial);
  Serial2.begin(115200); // TX=16,RX=17 がデフォルト
  while(!Serial2);
}
void loop() {
  if (Serial.available() > 0) {
    val = Serial.read();
    if (val == 'm') {
      Serial.println("m");
      Serial2.println("m");
      
    } else if (val == 'n') {
      Serial.println("n");
      Serial2.println("n");
    }
  }
 } 

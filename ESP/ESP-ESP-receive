//ESPとESPの通信
//今回serial2使う
void setup() {
  // シリアル初期化
  
  Serial2.begin(115200); // TX=16,RX=17 がデフォルト
  while(!Serial2);
  
  // LED出力ピン
  pinMode(22, OUTPUT);
  // 初期はLED消灯
  digitalWrite(22, LOW);
}
void loop() {
  String command;
  if (Serial2.available() > 0) {
    // 改行までをコマンドとして受付
    command = Serial2.readStringUntil('\n');
    // コマンド文字列をトリム
    command.trim();
    if (command.equals("m")) {
      // コマンドがONなら点灯
      digitalWrite(22, HIGH);
    }
    else if (command.equals("n")) {
      // コマンドがOFFなら消灯
      digitalWrite(22, LOW); 
    }
  }
  delay(100);
}

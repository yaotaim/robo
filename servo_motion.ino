//VarSpeedServo.hでサーボモータをゆっくり動かしモーション作ってみた
//シリアル入力で入力した値によってモーション起こす

#include <VarSpeedServo.h>
byte val = 0;

VarSpeedServo myservo7;
VarSpeedServo myservo6;
VarSpeedServo myservo5;
VarSpeedServo myservo4;
// Function prototypes
void nameten();
void runrun();
void nani();

// タイミング用の変数
unsigned long lastTime = 0;
unsigned long interval = 0;

void setup() {
  myservo7.attach(7); 
  myservo6.attach(6);  
  myservo5.attach(5);  
  myservo4.attach(4); 

  // シリアル通信開始
  Serial.begin(9600);
}

void loop() {
  // 現在の時間を取得
  unsigned long currentTime = millis();

  // シリアル入力の処理
  if (Serial.available() > 0) {
    val = Serial.read();
    if (val == 'a') {
      nameten();
      interval = 1000; // 1秒の間隔で実行
    } else if (val == 's') {
      runrun();
      interval = 10000; // 10秒の間隔で実行
    } else if (val == 'd') {
      nani();
      interval = 10000; // 10秒の間隔で実行
    }
    // 最後の実行時間を更新
    lastTime = currentTime;
  }

  // タイミングに従ってサーボを制御
  if (currentTime - lastTime >= interval) {
    // タイミングに達したらここに入る
    // ここでサーボの制御を行う
  }
}

// 以下、サーボ制御関数は先ほどと同じ
void nameten(){
  myservo7.write(90, 70, true);
  myservo6.write(90, 70, true);
  myservo5.write(90, 70, true);
  myservo4.write(90, 150, true);

  myservo7.write(70, 70, true);
  myservo6.write(50, 70, true);
  myservo5.write(60, 70, true);
  myservo4.write(50, 150, true);
  
  myservo7.write(90, 70, true);
  myservo6.write(90, 70, true);
  myservo5.write(90, 70, true);
  myservo4.write(90, 150, true);
}

void runrun(){
  myservo7.write(90, 40, true);
  myservo6.write(90, 40, true);
  myservo5.write(90, 40, true);
  myservo4.write(50, 100, true);

  myservo7.write(110, 40, true);
  myservo6.write(50, 40, true);
  myservo5.write(70, 40, true);
  myservo4.write(20, 100, true);

  myservo7.write(90, 40, true);
  myservo6.write(90, 40, true);
  myservo5.write(90, 40, true);
  myservo4.write(50, 100, true);

  myservo7.write(110, 40, true);
  myservo6.write(130, 40, true);
  myservo5.write(110, 40, true);
  myservo4.write(20, 100, true);

  myservo7.write(90, 40, true);
  myservo6.write(90, 40, true);
  myservo5.write(90, 40, true);
  myservo4.write(50, 100, true);
}

void nani(){
  myservo7.write(90, 70, true);
  myservo6.write(90, 70, true);
  myservo5.write(90, 70, true);
  myservo4.write(50, 150, true);
  delay(500);

  myservo7.write(90, 70, true);
  myservo6.write(50, 70, true);
  myservo5.write(90, 70, true);
  myservo4.write(50, 150, true);
  delay(500);

  myservo7.write(90, 70, true);
  myservo6.write(90, 70, true);
  myservo5.write(90, 70, true);
  myservo4.write(50, 150, true);
  delay(500);
}

// ESPでシリアル入力してDCモーターを操作(L298N)

// モーターAのピン
int ENA = 33;
int IN1 = 32;
int IN2 = 26;

// モーターBのピン
int IN3 = 27;
int IN4 = 14;
int ENB = 12;

// PWM設定
const int freq = 30000;
const int pwmChannelA = 0;
const int pwmChannelB = 1;
const int resolution = 8;
int dutyCycle = 255;  // 初期速度

void setup() {
  // ピンを出力として設定
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENB, OUTPUT);

  // LED PWM機能を設定
  ledcSetup(pwmChannelA, freq, resolution);
  ledcSetup(pwmChannelB, freq, resolution);

  // チャンネルをGPIOに接続
  ledcAttachPin(ENA, pwmChannelA);
  ledcAttachPin(ENB, pwmChannelB);

  Serial.begin(115200);

  // 初期メッセージ
  Serial.println("モーター制御の準備完了。1: 前進, 2: 後退, 3: 停止, 4: 右回り, 5: 左回り, 速度調整: 0-9");
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();

    switch (command) {
      case 'w':
        Serial.println("前進");
        // モーターA前進
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        ledcWrite(pwmChannelA, dutyCycle);
        // モーターB前進
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);
        ledcWrite(pwmChannelB, dutyCycle);
        break;

      case 'x':
        Serial.println("後退");
        // モーターA後退
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        ledcWrite(pwmChannelA, dutyCycle);
        // モーターB後退
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);
        ledcWrite(pwmChannelB, dutyCycle);
        break;

      case 's':
        Serial.println("停止");
        // モーターA停止
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, LOW);
        ledcWrite(pwmChannelA, 0);
        // モーターB停止
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, LOW);
        ledcWrite(pwmChannelB, 0);
        break;

      case 'e':
        Serial.println("右回り");
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        ledcWrite(pwmChannelA, dutyCycle);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);
        ledcWrite(pwmChannelB, dutyCycle);
        break;

      case 'q':
        Serial.println("左回り");
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        ledcWrite(pwmChannelA, dutyCycle);
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);
        ledcWrite(pwmChannelB, dutyCycle);
        break;
      
      // 速度調整（0-9のキー入力によりデューティサイクルを変更）
      case '0' ... '9':
        dutyCycle = map(command - '0', 0, 9, 0, 255);  // 0から9を0から255の範囲にマップ
        Serial.print("速度調整: ");
        Serial.println(dutyCycle);
        break;

      default:
        Serial.println("無効なコマンド");
    }
  }
}

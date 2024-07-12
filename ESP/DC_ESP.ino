//ESPでシリアル入力してDCモーターを操作(L298N)

// モーターAのピン
int ENA = 12;
int IN1 = 14;
int IN2 = 27;

// モーターBのピン
int ENB = 33;
int IN3 = 26;
int IN4 = 25;

// PWM設定
const int freq = 30000;
const int pwmChannelA = 0;
const int pwmChannelB = 1;
const int resolution = 8;
int dutyCycle = 255;

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
  Serial.println("モーター制御の準備完了。1: 前進, 2: 後退, 3: 停止");
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();

    switch (command) {
      case '1':
        Serial.println("前進");
        // モーターA前進
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        ledcWrite(pwmChannelA, dutyCycle);
        // モーターB前進
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);
        ledcWrite(pwmChannelB, dutyCycle);
        break;

      case '2':
        Serial.println("後退");
        // モーターA後退
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        ledcWrite(pwmChannelA, dutyCycle);
        // モーターB後退
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);
        ledcWrite(pwmChannelB, dutyCycle);
        break;

      case '3':
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

      default:
        Serial.println("無効なコマンド");
    }
  }
}
        

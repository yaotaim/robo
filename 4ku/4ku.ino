//四駆ゲート_スタート＿各ゲート開けれる
#include <Wire.h>  // I2C通信ライブラリ（PWMサーボドライバ用）
#include <Adafruit_PWMServoDriver.h>  // Adafruit製 PWM サーボドライバライブラリ（PCA9685用）

// サーボのパルス幅設定（マイクロ秒）
// 0度時の最小値、180度時の最大値（サーボによって異なることもある）
#define SERVOMIN 500    
#define SERVOMAX 2400   

// サーボの角度設定（調整用）
// Set 0の角度設定
#define SERVO_OPEN_ANGLE_0 5    
#define SERVO_CLOSE_ANGLE_0 40  

// Set 1の角度設定
#define SERVO_OPEN_ANGLE_1 0    
#define SERVO_CLOSE_ANGLE_1 40 

// Set 2の角度設定
#define SERVO_OPEN_ANGLE_2 5  
#define SERVO_CLOSE_ANGLE_2 40   

// Set 3の角度設定
#define SERVO_OPEN_ANGLE_3 10     //大きくすると閉じる__完了
#define SERVO_CLOSE_ANGLE_3 40   //小さくすると開く

// PSDセンサーの検知範囲設定（調整用）
// Set 0の検知範囲
#define SENSOR_IGNORE_MIN_0 8   
#define SENSOR_IGNORE_MAX_0 12  

// Set 1の検知範囲
#define SENSOR_IGNORE_MIN_1 8
#define SENSOR_IGNORE_MAX_1 13  

// Set 2の検知範囲
#define SENSOR_IGNORE_MIN_2 8   
#define SENSOR_IGNORE_MAX_2 12 

// Set 3の検知範囲
#define SENSOR_IGNORE_MIN_3 8  
#define SENSOR_IGNORE_MAX_3 12 

// タイミングや動作時間に関する定数
const unsigned long playDuration = 500;         // ブザー・LEDが鳴る時間（ms）
const unsigned long sensorInterval = 100;       // センサーの読み取り間隔（ms）
const unsigned long waitBeforeClose = 3000;     // 開いてから閉じるまでの待機時間（ms）
const unsigned long servoIntervalNormal = 10;   // サーボ通常速度の更新間隔（ms）
const unsigned long servoIntervalSlow = 80;     // サーボスロー速度の更新間隔（ms）
const int DETECTION_THRESHOLD = 2;              // センサー検知の必要回数

// センサー検知範囲取得用の関数を追加
float getSensorIgnoreMin(int setIndex) {
    switch(setIndex) {
        case 0: return SENSOR_IGNORE_MIN_0;
        case 1: return SENSOR_IGNORE_MIN_1;
        case 2: return SENSOR_IGNORE_MIN_2;
        case 3: return SENSOR_IGNORE_MIN_3;
        default: return SENSOR_IGNORE_MIN_0;
    }
}

float getSensorIgnoreMax(int setIndex) {
    switch(setIndex) {
        case 0: return SENSOR_IGNORE_MAX_0;
        case 1: return SENSOR_IGNORE_MAX_1;
        case 2: return SENSOR_IGNORE_MAX_2;
        case 3: return SENSOR_IGNORE_MAX_3;
        default: return SENSOR_IGNORE_MAX_0;
    }
}

// 角度取得用の関数を追加
int getServoOpenAngle(int setIndex) {
    switch(setIndex) {
        case 0: return SERVO_OPEN_ANGLE_0;
        case 1: return SERVO_OPEN_ANGLE_1;
        case 2: return SERVO_OPEN_ANGLE_2;
        case 3: return SERVO_OPEN_ANGLE_3;
        default: return SERVO_OPEN_ANGLE_0;
    }
}

int getServoCloseAngle(int setIndex) {
    switch(setIndex) {
        case 0: return SERVO_CLOSE_ANGLE_0;
        case 1: return SERVO_CLOSE_ANGLE_1;
        case 2: return SERVO_CLOSE_ANGLE_2;
        case 3: return SERVO_CLOSE_ANGLE_3;
        default: return SERVO_CLOSE_ANGLE_0;
    }
}


// サーボドライバ（I2Cアドレス0x40）を初期化
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40);

// セット数（今回は4個の装置セットを扱う）
#define SET_COUNT 4

// 電源電圧（PSDセンサーの電圧計算に使う）
float Vcc = 5.0;

enum SystemState { NORMAL, WAITING, SERVO_OPENED } systemState = NORMAL;//モードの挙動を切り替えるため、グローバル変数を追加：

// 1つの装置（ボタン・ブザー・LED・サーボ・センサ）の情報をまとめる構造体
struct DeviceSet {
  int buttonPin;       // ボタン入力ピン（プルアップ使用）
  int buzzerPin;       // ブザー出力ピン
  int ledPin;          // LED出力ピン
  int servoChannel;    // サーボ出力チャンネル（PWM）
  int sensorPin;       // PSDセンサのアナログ入力ピン

  int currentAngle;    // 現在のサーボ角度
  int targetAngle;     // 目標とするサーボ角度
  int mode;            // 動作モード（例：通常=0, スロー=1）

  bool isServoMoving;  // サーボが現在動いているかどうか
  bool waitToClose;    // 自動で閉じるまで待っているか
  bool isPlaying;      // ブザー・LEDが現在ON中かどうか

  unsigned long playStartTime;   // ブザー・LEDがONになった時間（ms）
  unsigned long lastServoMove;   // 最後にサーボを動かした時間（ms）
  unsigned long openedTime;      // サーボを開いた時間（自動で閉じるために使う
  unsigned long lastSensorRead;  // 最後にセンサーを読んだ時間（間引き処理のため）

  int detectionCount;    // センサー検知カウント
  unsigned long lastDetectionTime; // 最後に検知した時間

  // 構造体の初期化（コンストラクタ）
  DeviceSet(int b, int buzz, int led, int servo, int sensor)
    : buttonPin(b), buzzerPin(buzz), ledPin(led), servoChannel(servo), sensorPin(sensor),
      currentAngle(getServoCloseAngle(servo)), targetAngle(getServoCloseAngle(servo)), mode(0),
      isServoMoving(false), waitToClose(false), isPlaying(false),
      playStartTime(0), lastServoMove(0), openedTime(0), lastSensorRead(0),
      detectionCount(0), lastDetectionTime(0) {}
};

// 装置セットのピンアサイン（4セット分定義）
// {ボタン, ブザー, LED, サーボチャンネル, センサピン}
DeviceSet sets[SET_COUNT] = {
  DeviceSet(2,  3,  4, 3, A0),
  DeviceSet(5,  7,  8, 2, A1),
  DeviceSet(6, 11, 10, 1, A2),
  DeviceSet(9, 13, 12, 0, A3)
};


void setup() {
  Serial.begin(115200);         // シリアルモニター用に通信初期化（115200bps）
  pwm.begin();                  // PWMサーボドライバの初期化
  pwm.setPWMFreq(50);           // サーボのためのPWM周波数設定（50Hz = 20ms周期）
  delay(1000);                  // 初期化安定化のための待機

  // 各装置セットのピンを初期化
  for (int i = 0; i < SET_COUNT; ++i) {
    pinMode(sets[i].buttonPin, INPUT_PULLUP);  // ボタンはプルアップ入力
    pinMode(sets[i].buzzerPin, OUTPUT);        // ブザーは出力
    pinMode(sets[i].ledPin, OUTPUT);           // LEDは出力
    setServoAngle(i, sets[i].currentAngle);    // サーボを初期角度に設定
  }
  Serial.println("Setup complete"); // シリアルにセットアップ完了表示
  systemState = NORMAL;//モードをノーマルに変更
}

// 指定したセットのサーボを角度で制御する関数
void setServoAngle(int index, int angle) {
  int pulse = map(angle, 0, 180, SERVOMIN, SERVOMAX); // 角度をパルス幅に変換
  pwm.writeMicroseconds(sets[index].servoChannel, pulse); // PWM信号を送信
}

// ブザーとLEDを一時的にONにする関数（非ブロッキング）
void blinkAndPlay(int index, int freq) {
  digitalWrite(sets[index].ledPin, HIGH);    // LED ON
  tone(sets[index].buzzerPin, freq);         // ブザーを指定周波数で鳴らす
  sets[index].playStartTime = millis();      // 開始時刻を記録
  sets[index].isPlaying = true;              // 状態フラグ更新
  sets[index].mode = 1;                      // スローモードに設定
}

// PSDセンサーから距離を読み取る関数（電圧を距離に変換）
// ※干渉防止のため、ダミー読み・安定化待機を含む
float readDistance(int analogPin) {
  analogRead(analogPin);  // ダミー読み取りでADCを安定させる
  delayMicroseconds(20); // 短い待機で電圧安定化
  float voltage = Vcc * analogRead(analogPin) / 1023.0; // ADC値→電圧変換
  return 26.549 * pow(voltage, -1.2091); // シャープセンサーの特性式で距離(cm)に変換
}

void loop() {
  if (Serial.available()) {
    char cmd = Serial.read();
    if (cmd == 'q') {//初期状態にリセットして 待機モード へ。センサー読み取り、ボタン、サーボ操作は停止。
      Serial.println("Entering WAITING mode (no sensor/button/servo activity)");
      systemState = WAITING;
    } else if (cmd == 'w') {//全サーボを 0度に開く。センサーやボタンは無視。
      if (systemState == WAITING) {
        Serial.println("Opening all servos");
        for (int i = 0; i < SET_COUNT; ++i) {
          sets[i].currentAngle = getServoOpenAngle(i);
          setServoAngle(i, getServoOpenAngle(i));
        }
        systemState = SERVO_OPENED;
      }
    } else if (cmd == 'e') {//全サーボを 閉じて通常モードに戻る。以後、センサーやボタンが有効。
      if (systemState == SERVO_OPENED) {
        Serial.println("Closing all servos and resuming normal mode");
        for (int i = 0; i < SET_COUNT; ++i) {
          sets[i].currentAngle = getServoCloseAngle(i);
          sets[i].targetAngle = getServoCloseAngle(i);
          setServoAngle(i, getServoCloseAngle(i));
          sets[i].isServoMoving = false;
          sets[i].waitToClose = false;
          sets[i].isPlaying = false;
          sets[i].mode = 0;
        }
        systemState = NORMAL;
      }
    } 
    // キー制御を追加（a,s,d,fで開く、z,x,c,vでスロー開き）
    else if (cmd == 'a' || cmd == 's' || cmd == 'd' || cmd == 'f' || 
             cmd == 'z' || cmd == 'x' || cmd == 'c' || cmd == 'v') {
        int setIndex;
        bool isOpen = true;  // すべてのコマンドで開く動作のみに
        bool isSlowMode = false;
        
        switch(cmd) {
            case 'a': setIndex = 0; isSlowMode = false; break;
            case 's': setIndex = 1; isSlowMode = false; break;
            case 'd': setIndex = 2; isSlowMode = false; break;
            case 'f': setIndex = 3; isSlowMode = false; break;
            case 'z': setIndex = 0; isSlowMode = true; break;
            case 'x': setIndex = 1; isSlowMode = true; break;
            case 'c': setIndex = 2; isSlowMode = true; break;
            case 'v': setIndex = 3; isSlowMode = true; break;
            default: return;
        }
        
        // デバッグ用のログを追加
        Serial.print("Received command: ");
        Serial.write(cmd);
        Serial.print(", setIndex: ");
        Serial.print(setIndex);
        Serial.print(isSlowMode ? " (Slow mode)" : " (Normal mode)");
        Serial.println();
        
        if (setIndex >= 0 && setIndex < SET_COUNT) {
            Serial.print("Opening set ");
            Serial.print(setIndex);
            Serial.println(isSlowMode ? " (Slow)" : " (Normal)");
            
            DeviceSet &s = sets[setIndex];
            if (!s.isServoMoving && !s.waitToClose) {
                s.targetAngle = getServoOpenAngle(setIndex);
                s.isServoMoving = true;
                s.mode = isSlowMode ? 1 : 0;  // スローモード=1、通常モード=0
            }
        }
    }
  }

  if (systemState == NORMAL) {
    unsigned long now = millis();   // 現在時刻を取得（ms単位）
    String distanceLog = "sensor "; // センサー距離ログ用文字列
    bool sensorUpdated = false;    // センサー更新があったかのフラグ

    // 各セットごとの処理
    for (int i = 0; i < SET_COUNT; ++i) {
      DeviceSet &s = sets[i]; // セットを参照で取得（可読性向上）

      // ボタンが押されたかチェック（プルアップなのでLOWが押下状態）
      if (digitalRead(s.buttonPin) == LOW) {
        blinkAndPlay(i, 1000); // LED＆ブザー起動（1000Hz）
      }

      // ブザー・LEDをOFFにする処理（playDuration経過後）
      if (s.isPlaying && now - s.playStartTime >= playDuration) {
        digitalWrite(s.ledPin, LOW);  // LED OFF
        noTone(s.buzzerPin);          // ブザー OFF
        s.isPlaying = false;          // 状態フラグ更新
      }

      // センサー読み取り（一定間隔ごとに）
      if (now - s.lastSensorRead >= sensorInterval) {
        s.lastSensorRead = now;
        sensorUpdated = true;

        float distance = readDistance(s.sensorPin); // 距離取得
        float ignoreMin = getSensorIgnoreMin(i);   // そのセットの無視最小距離
        float ignoreMax = getSensorIgnoreMax(i);   // そのセットの無視最大距離

        // 距離ログ文字列を簡潔に修正
        distanceLog += "set" + String(i) + ": ";
        distanceLog += String(distance, 1) + "cm";
        if (i < SET_COUNT - 1) distanceLog += ", ";

        // 条件：設定した無視範囲以外で検知（かつ動作中でない場合）
        if ((distance < ignoreMin || distance > ignoreMax) && 
            !s.isServoMoving && !s.waitToClose) {
            
            // 前回の検知から1秒以内なら検知カウントを増やす
            if (now - s.lastDetectionTime < 1000) {
                s.detectionCount++;
            } else {
                // 1秒以上経過していたらカウントリセット
                s.detectionCount = 1;
            }
            s.lastDetectionTime = now;

            // DETECTION_THRESHOLD回連続で検知したら開く
            if (s.detectionCount >= DETECTION_THRESHOLD) {
                Serial.print("set");
                Serial.print(i);
                Serial.print(": Double detection at ");
                Serial.print(distance);
                Serial.println("cm → Open");

                s.targetAngle = getServoOpenAngle(i);  // 開ける
                s.isServoMoving = true;     // サーボ動作開始
                s.detectionCount = 0;       // カウントリセット
            }
        } else {
            // 検知しない場合はカウントをリセット
            if (now - s.lastDetectionTime >= 1000) {
                s.detectionCount = 0;
            }
        }
      }

      // サーボを少しずつ動かす処理（非ブロッキング）
      unsigned long interval = (s.mode == 1) ? servoIntervalSlow : servoIntervalNormal;

      if (s.isServoMoving && now - s.lastServoMove >= interval) {
        s.lastServoMove = now;

        if (s.currentAngle != s.targetAngle) {
          int step = (s.targetAngle > s.currentAngle) ? 1 : -1; // 方向を判定
          s.currentAngle += step;
          setServoAngle(i, s.currentAngle); // サーボを1度だけ更新
        } else {
          s.isServoMoving = false; // サーボ移動完了

          if (s.targetAngle == getServoOpenAngle(i)) {
            Serial.print("set"); Serial.print(i); Serial.println(": Door opened");
            s.openedTime = now;        // 開いた時間を記録
            s.waitToClose = true;      // 自動閉鎖の待機状態へ
          } else {
            Serial.print("set"); Serial.print(i); Serial.println(": Door closed");
          }
        }
      }

      // 一定時間後に自動で閉じる処理
      if (s.waitToClose && now - s.openedTime >= waitBeforeClose) {
        Serial.print("set"); Serial.print(i); Serial.println(": Auto-closing");

        s.targetAngle = getServoCloseAngle(i);        // 閉じる角度へ
        s.isServoMoving = true;    // サーボ移動開始
        s.waitToClose = false;     // 閉じる待機解除
        s.mode = 0;                // 通常モードへ戻す
      }
    }

    // センサー情報をシリアル出力（1ループに1回）
    if (sensorUpdated) {
      Serial.println(distanceLog);
    }
  }
}


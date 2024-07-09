//servo_pca_ar1.inoの進化系
//サーボをゆっくり動かす関数と早く動かす関数を用意
//おそらくpokiヘッド二号機用

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

#define SERVOMIN  150
#define SERVOMAX  400
#define SERVO_FREQ 50
#define SERVO4 4
#define SERVO5 5

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

int aTp(int angle) {
  return map(angle, 0, 180, SERVOMIN, SERVOMAX);
}

int pTa(int pulselen) {
  return map(pulselen, SERVOMIN, SERVOMAX, 0, 180);
}

int pulselen4 = aTp(90); // 初期位置を90度に設定
int pulselen5 = aTp(70); // 初期位置を70度に設定
char kioku;

void setup() {
  Serial.begin(115200);

  pwm.begin();
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(SERVO_FREQ);

  delay(1000);

  // サーボを初期位置に設定
  moveServos(90, 70);
}

void loop() {
  if (Serial.available() > 0) {
    char val = Serial.read();
    Serial.println(val);

    switch (val) {
      case 'r':
        moveServos(130, 50);
        break;
      case 'e':
        moveServos(90, 50);
        break;
      case 'w':
        moveServos(50, 50);
        break;
      case 'f':
        moveServos(130, 70);
        break;
      case 'd':
        moveServos(90, 70);
        break;
      case 's':
        moveServos(50, 70);
        break;

//左右
      case 'g':
        if (pTa(pulselen4) < 180) {
          pwm.setPWM(SERVO4, 0, pulselen4 + 50);
          pulselen4 = pulselen4 + 50;
        }
        break;
      case 'h':
        if (pTa(pulselen4) > 0) {
          pwm.setPWM(SERVO4, 0, pulselen4 - 50);
          pulselen4 = pulselen4 - 50;
        }
        break;

      case 't':
        moveServos(40, 30);
        moveServos(90, 70);
        moveServos(140, 30);
        moveServos(90, 70);
        break;

      case 'y':
        kioku = 'y';
        pwm.setPWM(SERVO4, 0, aTp(90));
        pwm.setPWM(SERVO5, 0, aTp(100));
        delay(500);
        pwm.setPWM(SERVO4, 0, aTp(90));
        pwm.setPWM(SERVO5, 0, aTp(70));
        delay(500);
        pwm.setPWM(SERVO4, 0, aTp(90));
        pwm.setPWM(SERVO5, 0, aTp(100));
        delay(500);
        pwm.setPWM(SERVO4, 0, aTp(90));
        pwm.setPWM(SERVO5, 0, aTp(70));
        delay(500);

        if (random(1, 3) == 1) {
          pwm.setPWM(SERVO4, 0, aTp(0));
          pwm.setPWM(SERVO5, 0, aTp(70));
          delay(2000);
          pulselen4 = aTp(0);
          pulselen5 = aTp(70);

          // シリアル受信まで待つ
          char val;
          do {
            while (!Serial.available());
            val = Serial.read();
            Serial.println(val);
          } while (val != 'g' && val != 'h');

          if (val == 'h') {
            moveServos(40, 30);
            moveServos(90, 70);
            moveServos(140, 30);
            moveServos(90, 70);
            kioku = 'p';
          } else if (val == 'g') {
            moveServos(40, 100);
            moveServos(140, 100);
            moveServos(40, 100);
            moveServos(140, 100);
            kioku = 'p';
          }

        } else {
          pwm.setPWM(SERVO4, 0, aTp(180));
          pwm.setPWM(SERVO5, 0, aTp(70));
          delay(1000);
          pulselen4 = aTp(180);
          pulselen5 = aTp(70);

          // シリアル受信まで待つ
          char val;
          do {
            while (!Serial.available());
            val = Serial.read();
            Serial.println(val);
          } while (val != 'g' && val != 'h');

          if (val == 'h') {
            pwm.setPWM(SERVO4, 0, aTp(90));
            pwm.setPWM(SERVO5, 0, aTp(70));
            delay(500);
            pulselen4 = aTp(90);
            pulselen5 = aTp(70);
            moveServos(40, 30);
            moveServos(90, 70);
            moveServos(140, 30);
            moveServos(90, 70);
            kioku = 'p';
          } else if (val == 'g') {
            pwm.setPWM(SERVO4, 0, aTp(90));
            pwm.setPWM(SERVO5, 0, aTp(70));
            delay(500);
            pulselen4 = aTp(90);
            pulselen5 = aTp(70);
            moveServos(40, 100);
            moveServos(140, 100);
            moveServos(40, 100);
            moveServos(140, 100);
            kioku = 'p';
          }
        }

        moveServos(90, 70);
        break;

      case 'b':
        moveServos(random(50, 130), random(50, 70)); // ランダムな位置に移動
        break;
    }  
    Serial.print("pulselen4: ");
    Serial.print(pTa(pulselen4));
    Serial.print(", pulselen5: ");
    Serial.println(pTa(pulselen5));
  }
}

void moveServos(int angleServo4, int angleServo5) {
  int moku4 = aTp(angleServo4);
  int moku5 = aTp(angleServo5);

  bool increasing4 = pulselen4 < moku4;
  bool increasing5 = pulselen5 < moku5;

  while (pulselen4 != moku4 || pulselen5 != moku5) {
    if (pulselen4 != moku4) {
      pulselen4 += increasing4 ? 1 : -1;
      pwm.setPWM(SERVO4, 0, pulselen4);
    }
    if (pulselen5 != moku5) {
      pulselen5 += increasing5 ? 1 : -1;
      pwm.setPWM(SERVO5, 0, pulselen5);
    }
    delay(10);
  }
}

void moveServos_fast(int angleServo4, int angleServo5) {
  int moku4 = aTp(angleServo4);
  int moku5 = aTp(angleServo5);

  bool increasing4 = pulselen4 < moku4;
  bool increasing5 = pulselen5 < moku5;

  while (pulselen4 != moku4 || pulselen5 != moku5) {
    if (pulselen4 != moku4) {
      pulselen4 += increasing4 ? 5 : -5;
      pwm.setPWM(SERVO4, 0, pulselen4);
    }
    if (pulselen5 != moku5) {
      pulselen5 += increasing5 ? 5 : -5;
      pwm.setPWM(SERVO5, 0, pulselen5);
    }
    delay(10);
  }
}

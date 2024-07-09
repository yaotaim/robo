//pcaを使ってサーボモーター制御　シリアル入力で動かす
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

#define SERVOMIN  150
#define SERVOMAX  400
#define SERVO_FREQ 50
#define SERVO4 4
#define SERVO5 5

byte val = 0;

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

void setup() {
  Serial.begin(115200);

  pwm.begin();
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(SERVO_FREQ);

  delay(10);
  pwm.setPWM(SERVO4, 0, aTp(90));
  pwm.setPWM(SERVO5, 0, aTp(90));

  delay(1000);
}

int aTp(int angle) {
  return map(angle, 0, 180, SERVOMIN, SERVOMAX);
}


void loop() {
  if (Serial.available() > 0) {
    val = Serial.read();

    Serial.println(char(val)); 

    if (val == 'w') {
      pwm.setPWM(SERVO4, 0, aTp(130));
      pwm.setPWM(SERVO5, 0, aTp(50));
      
    } else if (val == 'e') {
      pwm.setPWM(SERVO4, 0, aTp(90));
      pwm.setPWM(SERVO5, 0, aTp(50));

    } else if (val == 'r') {
      pwm.setPWM(SERVO4, 0, aTp(50));
      pwm.setPWM(SERVO5, 0, aTp(50));
  
    } else if (val == 's') {
      pwm.setPWM(SERVO4, 0, aTp(130));
      pwm.setPWM(SERVO5, 0, aTp(70));
 
    } else if (val == 'd') {
      pwm.setPWM(SERVO4, 0, aTp(90));
      pwm.setPWM(SERVO5, 0, aTp(70));

    } else if (val == 'f') {
      pwm.setPWM(SERVO4, 0, aTp(50));
      pwm.setPWM(SERVO5, 0, aTp(70));
    
    } else if (val == 't') {
      pwm.setPWM(SERVO4, 130, aTp(130));
      pwm.setPWM(SERVO5, 30, aTp(50));
      delay(1000);
      pwm.setPWM(SERVO4, 0, aTp(90));
      pwm.setPWM(SERVO5, 0, aTp(60));
      delay(1000);
      pwm.setPWM(SERVO4, 0, aTp(50));
      pwm.setPWM(SERVO5, 0, aTp(30));
      delay(1000);
      pwm.setPWM(SERVO4, 0, aTp(90));
      pwm.setPWM(SERVO5, 0, aTp(60));
      delay(1000);
    }
  }
}

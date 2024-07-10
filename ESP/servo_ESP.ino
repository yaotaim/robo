#include <ESP32Servo.h>

#define SP1 32
#define SP2 33

Servo myServo1;
Servo myServo2;

void setup() {
  myServo1.attach(SP1);
  myServo2.attach(SP2);
}

void loop() {
  myServo1.write(0);
  delay(2000);
  myServo1.write(90);
  delay(2000);
  myServo1.write(180);
  delay(2000);
  myServo1.write(90);
  delay(2000);
  /*
  myServo2.write(0);
  delay(2000);
  myServo2.write(90);
  delay(2000);
  myServo2.write(180);
  delay(2000);
  myServo2.write(90);
  delay(2000);
  */
}

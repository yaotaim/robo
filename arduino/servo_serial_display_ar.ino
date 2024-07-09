//シリアル入力よってサーボを動かす+displayモジュールに表示
#include <VarSpeedServo.h>
#include <LiquidCrystal.h>
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

byte val = 0;

VarSpeedServo myservo2;
VarSpeedServo myservo3;
int spd = 40;
bool han = false;

char kioku = '0';

void setup() {
  Serial.begin(9600);

  lcd.begin(16, 2);
  lcd.print("kawaiiiiiii");
  lcd.setCursor(0, 1);
  lcd.print("robot");

  myservo2.attach(2); 
  myservo3.attach(3);  
  myservo2.write(90, spd, han);
  myservo3.write(70, spd, han);
  delay(1000);
}

void loop() {
  if (Serial.available() > 0) {
    val = Serial.read();
    Serial.print("Received: ");
    Serial.println(char(val)); 

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Received: ");
    lcd.print(char(val));

    if (val == 'w' && kioku != 'w') {
      myservo2.write(130, spd, han);
      myservo3.write(50, spd, han);
      kioku = 'w';
    } else if (val == 'e' && kioku != 'e') {
      myservo2.write(90, spd, han);
      myservo3.write(50, spd, han);
      kioku = 'e';
    } else if (val == 'r' && kioku != 'r') {
      myservo2.write(50, spd, han);
      myservo3.write(50, spd, han);
      kioku = 'r';
    } else if (val == 's' && kioku != 's') {
      myservo2.write(130, spd, han);
      myservo3.write(70, spd, han);
      kioku = 's';
    } else if (val == 'd' && kioku != 'd') {
      myservo2.write(90, spd, han);
      myservo3.write(70, spd, han);
      kioku = 'd';
    } else if (val == 'f' && kioku != 'f') {
      myservo2.write(50, spd, han);
      myservo3.write(70, spd, han);
      kioku = 'f';
    } else if (val == 'x' && kioku != 'x') {
      myservo2.write(130, spd, han);
      myservo3.write(90, spd, han);
      kioku = 'x';
    } else if (val == 'c' && kioku != 'c') {
      myservo2.write(90, spd, han);
      myservo3.write(90, spd, han);
      kioku = 'c';
    } else if (val == 'v' && kioku != 'v') {
      myservo2.write(50, spd, han);
      myservo3.write(90, spd, han);
      kioku = 'v';
    } else if (val == 't' && kioku != 't') {
      myservo2.write(130, spd, true);
      myservo3.write(30, spd, true);
      delay(100);
      myservo2.write(90, spd, true);
      myservo3.write(60, spd, true);
      delay(100);
      myservo2.write(50, spd, true);
      myservo3.write(30, spd, true);
      delay(100);
      myservo2.write(90, spd, true);
      myservo3.write(60, spd, true);
      delay(100);

      kioku = 't';
    }
  }
}

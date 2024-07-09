//displayモジュール使ってみた

#include <LiquidCrystal.h>

LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

void setup() {
  Serial.begin(9600);

lcd.begin(16, 2);
lcd.print("kawaiiiiiii");
lcd.setCursor(0, 1);
lcd.print("robot");
}

void loop() {
  if (Serial.available() > 0) {
    char val = Serial.read();
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("mode: "); 
    lcd.print(val); 
  }
}


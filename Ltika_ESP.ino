//ESPでLチカする
#include <Arduino.h>

int_fast8_t _toggle = 0;

void setup() {
	Serial.begin(115200);
	pinMode(32, OUTPUT);
	digitalWrite(32, LOW);
}

void loop() {
	if(_toggle == 0) {
			Serial.println("点灯");
			digitalWrite(32, HIGH);	
			_toggle = 1;
	} else {
			Serial.println("消灯");
			digitalWrite(32, LOW);	
			_toggle = 0;
	}
	delay(100);
}

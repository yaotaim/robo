//arduinoでシャープの距離センサーを使う
void setup()
{
	Serial.begin(115200);
}

void loop()
{
	int value = analogRead(8);
	int distance = (6787/(value-3))-4;
	//50cm以下で反応
	if(distance <= 100){
		Serial.print(distance);
		Serial.println("cm");
	}
	else{
		Serial.println("not found");
	}
	delay(500);
}

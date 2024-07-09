//シリアル入力でLチカ
const int LED_PIN = 8; 
byte val = 0;
 
void setup(){
  Serial.begin(115200);      
  pinMode(LED_PIN, OUTPUT); 
  digitalWrite(LED_PIN, LOW);
}
 
void loop(){
 
  if(Serial.available()>0){  
      val = Serial.read();
    
      if(val == 'n') {
          Serial.println("点灯");
          digitalWrite(23, HIGH);  
      } else if (val == 'm'){
          Serial.println("消灯");
          digitalWrite(23, LOW);  
      }
    }
  }
}

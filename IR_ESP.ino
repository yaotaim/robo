//赤外線(IR)センサ使ってみた。近づいたらLED点灯
const int IR_SENSOR = 5;  // 赤外線センサ
const int LED = 12;     
byte lastSt = 0xFF;       
byte fixedSt = 0xFF;     
unsigned long smpltmr = 0;  
 
void setup() {
  pinMode(IR_SENSOR, INPUT);
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);
  Serial.begin(115200);
}
 
void loop() {
  if(millis() - smpltmr < 40) return;
  smpltmr = millis();
 
  byte st = digitalRead(IR_SENSOR);
  int cmp = (st == lastSt);
  lastSt = st;
   
  if(!cmp) return;
   
  if(st != fixedSt){
    fixedSt = st;
    st = (~st) & 0x01;
    Serial.print("Sensor:");
    Serial.println(st);
    digitalWrite(LED, st);  // LED制御
  }
}

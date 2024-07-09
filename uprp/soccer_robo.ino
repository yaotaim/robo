//多分動かなかった
#include <Servo.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position
int pas = 0;

#define MAX_PACKETSIZE 32    //Serial receive buffer
char buffUART[MAX_PACKETSIZE];
unsigned int buffUARTIndex = 0;
unsigned long preUARTTick = 0;
struct car_status{
  int speed;
  int angle;
  int direct;
};
int move_speed=100 ;

#define MAX_SPEED  250
#define MIN_SPEED  50
#define SPEED 255
#define TURN_SPEED  70
#define SLOW_TURN_SPEED  50
#define BACK_SPEED  60

int buttonState;
char old_status='0';
#define speedPinR 9   //  Front Wheel PWM pin connect Model-Y M_B ENA 
#define RightMotorDirPin1  22    //Front Right Motor direction pin 1 to Model-Y M_B IN1  (K1)
#define RightMotorDirPin2  24   //Front Right Motor direction pin 2 to Model-Y M_B IN2   (K1)                                 
#define LeftMotorDirPin1  26    //Front Left Motor direction pin 1 to Model-Y M_B IN3 (K3)
#define LeftMotorDirPin2  28   //Front Left Motor direction pin 2 to Model-Y M_B IN4 (K3)
#define speedPinL 10   //  Front Wheel PWM pin connect Model-Y M_B ENB

#define speedPinRB 11   //  Rear Wheel PWM pin connect Left Model-Y M_A ENA 
#define RightMotorDirPin1B  5    //Rear Right Motor direction pin 1 to Model-Y M_A IN1 ( K1)
#define RightMotorDirPin2B 6    //Rear Right Motor direction pin 2 to Model-Y M_A IN2 ( K1) 
#define LeftMotorDirPin1B 7    //Rear Left Motor direction pin 1 to Model-Y M_A IN3  (K3)
#define LeftMotorDirPin2B 8  //Rear Left Motor direction pin 2 to Model-Y M_A IN4 (K3)
#define speedPinLB 12    //  Rear Wheel PWM pin connect Model-Y M_A ENB

int car_direction = 1; // 1 means forward, 0 gear backward

/*motor control*/
void right_shift(int speed_fl_fwd,int speed_rl_bck ,int speed_rr_fwd,int speed_fr_bck) {
  FL_fwd(speed_fl_fwd); 
  RL_bck(speed_rl_bck); 
  RR_fwd(speed_rr_fwd);
  FR_bck(speed_fr_bck);
}
void left_shift(int speed_fl_bck,int speed_rl_fwd ,int speed_rr_bck,int speed_fr_fwd){
   FL_bck(speed_fl_bck);
   RL_fwd(speed_rl_fwd);
   RR_bck(speed_rr_bck);
   FR_fwd(speed_fr_fwd);
}
void go_advance(int speed){
   RL_fwd(speed);
   RR_fwd(speed);
   FR_fwd(speed);
   FL_fwd(speed); 
}
void go_back(int speed){
   RL_bck(speed);
   RR_bck(speed);
   FR_bck(speed);
   FL_bck(speed); 
}
void left_turn(int speed){
   RL_bck(speed);
   RR_fwd(speed);
   FR_fwd(speed);
   FL_bck(speed); 
}
void right_turn(int speed){
   RL_fwd(speed);
   RR_bck(speed);
   FR_bck(speed);
   FL_fwd(speed); 
}
void left_forward(int speed){
   RL_fwd(speed);
   RR_bck(0);
   FL_bck(0);
   FR_fwd(speed); 
}
void right_forward(int speed){
   RL_bck(0);
   RR_fwd(speed);
   FR_bck(0);
   FL_fwd(speed); 
}
void left_back(int speed){
   RL_fwd(0);
   RR_bck(speed);
   FR_fwd(0);
   FL_bck(speed); 
}
void right_back(int speed){
   RL_bck(speed);
   RR_fwd(0);
   FR_bck(speed);
   FL_fwd(0); 
}
void clockwise(int speed){
   RL_fwd(speed);
   RR_bck(speed);
   FR_bck(speed);
   FL_fwd(speed); 
}
void countclockwise(int speed){
   RL_bck(speed);
   RR_fwd(speed);
   FR_fwd(speed);
   FL_bck(speed); 
}
void FR_fwd(int speed)  //front-right wheel forward turn
{
  digitalWrite(RightMotorDirPin1,HIGH);
  digitalWrite(RightMotorDirPin2,LOW); 
  analogWrite(speedPinR,speed);
}
void FR_bck(int speed) // front-right wheel backward turn
{
  digitalWrite(RightMotorDirPin1,LOW);
  digitalWrite(RightMotorDirPin2,HIGH); 
  analogWrite(speedPinR,speed);
}
void FL_fwd(int speed) // front-left wheel forward turn
{
  digitalWrite(LeftMotorDirPin1,HIGH);
  digitalWrite(LeftMotorDirPin2,LOW);
  analogWrite(speedPinL,speed);
}
void FL_bck(int speed) // front-left wheel backward turn
{
  digitalWrite(LeftMotorDirPin1,LOW);
  digitalWrite(LeftMotorDirPin2,HIGH);
  analogWrite(speedPinL,speed);
}

void RR_fwd(int speed)  //rear-right wheel forward turn
{
  digitalWrite(RightMotorDirPin1B, HIGH);
  digitalWrite(RightMotorDirPin2B,LOW); 
  analogWrite(speedPinRB,speed);
}
void RR_bck(int speed)  //rear-right wheel backward turn
{
  digitalWrite(RightMotorDirPin1B, LOW);
  digitalWrite(RightMotorDirPin2B,HIGH); 
  analogWrite(speedPinRB,speed);
}
void RL_fwd(int speed)  //rear-left wheel forward turn
{
  digitalWrite(LeftMotorDirPin1B,HIGH);
  digitalWrite(LeftMotorDirPin2B,LOW);
  analogWrite(speedPinLB,speed);
}
void RL_bck(int speed)    //rear-left wheel backward turn
{
  digitalWrite(LeftMotorDirPin1B,LOW);
  digitalWrite(LeftMotorDirPin2B,HIGH);
  analogWrite(speedPinLB,speed);
}
 
 
void stop_stop()    //Stop
{
    analogWrite(speedPinLB,0);
 analogWrite(speedPinRB,0);
    analogWrite(speedPinL,0);
 analogWrite(speedPinR,0);
}


//Pins initialize
void init_GPIO()
{
  pinMode(RightMotorDirPin1, OUTPUT); 
  pinMode(RightMotorDirPin2, OUTPUT); 
  pinMode(speedPinL, OUTPUT);  
 
  pinMode(LeftMotorDirPin1, OUTPUT);
  pinMode(LeftMotorDirPin2, OUTPUT); 
  pinMode(speedPinR, OUTPUT);
     pinMode(RightMotorDirPin1B, OUTPUT); 
  pinMode(RightMotorDirPin2B, OUTPUT); 
  pinMode(speedPinLB, OUTPUT);  
 
  pinMode(LeftMotorDirPin1B, OUTPUT);
  pinMode(LeftMotorDirPin2B, OUTPUT); 
  pinMode(speedPinRB, OUTPUT);

}





void setup()
{
  init_GPIO();
  Serial1.begin(9600);//In order to fit the Bluetooth module's default baud rate, only 9600
  Serial1.begin(9600);
 
 
  stop_stop();

   myservo.attach(9);  // attaches the servo on pin 9 to the servo object
}

 

void loop(){
 do_Uart_Tick();
}

void do_Uart_Tick()
{

  char Uart_Date=0;
  if(Serial1.available()) 
  {
    size_t len = Serial1.available();
    uint8_t sbuf[len + 1];
    sbuf[len] = 0x00;
    Serial1.readBytes(sbuf, len);
    //parseUartPackage((char*)sbuf);
    memcpy(buffUART + buffUARTIndex, sbuf, len);//ensure that the serial port can read the entire frame of data
    buffUARTIndex += len;
    preUARTTick = millis();
    if(buffUARTIndex >= MAX_PACKETSIZE - 1) 
    {
      buffUARTIndex = MAX_PACKETSIZE - 2;
      preUARTTick = preUARTTick - 200;
    }
  }
  car_status cs;
  if(buffUARTIndex > 0 && (millis() - preUARTTick >= 100))//APP send flag to modify the obstacle avoidance parameters
  { //data ready
    buffUART[buffUARTIndex] = 0x00;
    Uart_Date=buffUART[0];
    cs=get_status(buffUART);
    car_direction=cs.angle;
    buffUARTIndex = 0;
  }
  move_speed=cs.speed;
   if (cs.speed>MAX_SPEED) 
  move_speed= MAX_SPEED;
   if (cs.speed<MIN_SPEED)
   move_speed= MIN_SPEED;

  switch (Uart_Date)    //serial control instructions
  {
    case 'w':  
    if(old_status=='0')
    go_advance(SPEED);
    old_status='w';
    delay(35);
    go_advance(SPEED);
    break;
    case 'a':left_shift(255,255,255,255);break;
    case 'd':right_shift(255,255,255,255);break;
    case 's':go_back(SPEED);break;
    case '1':left_turn(255);break;
    case '3':right_turn(255);break;
    case 'q':left_forward(255);break;
    case 'e':right_forward(255);break;
    case 'z':left_back(255);break;
    case 'c':right_back(255);break;
    case 'f':stop_stop();break;
    case 'r':clockwise(255);break;
    case 't':countclockwise(255);break;
    case 'n':for (pos = 0; pos <= 180; pos += 1) { 
               myservo.write(pos);                               
              };break;
    case 'm':for (pas = 180; pas >= 0; pas -= 1){ 
               myservo.write(pas);   
              } ;break;                              
    default:break;
  }
}

car_status get_status( char buffUART[])
{
  car_status cstatus;
  int index=2;
  if (buffUART[index]=='-'){
    cstatus.angle=-buffUART[index+1]+'0';
    index=index+3;
    
  } else {
   
    cstatus.angle=buffUART[index]-'0';
     index=index+2;
  }
  int currentvalue;
  int spd=0;
  while (buffUART[index]!=',')
  {
    currentvalue=buffUART[index]-'0';
    spd=spd*10+currentvalue;
    index++;
  }
  cstatus.speed=spd;
  index++;
  cstatus.direct=buffUART[index]-'0';
  return cstatus;
}

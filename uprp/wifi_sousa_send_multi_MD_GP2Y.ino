//webサーバーたて+モーターとセンサのマルチ処理+シリアル送る
//DCモーターの動きを試したい時はESP/DC_ESP.inoを試す

#include <WiFi.h>
#include <WebServer.h>
#include <ESP32Servo.h>

const char* ssid = "ASRcast-3870A4ED";
const char* password = "asciinew";

WebServer server(80);

// モーターAのピン
int ENA = 33;
int IN1 = 32;
int IN2 = 26;

// モーターBのピン
int IN3 = 27;
int IN4 = 14;
int ENB = 12;

const int freq = 30000;
const int pwmChannelA = 0;
const int pwmChannelB = 1;
const int resolution = 8;
int dutyCycle = 255;

const int voutPin = 35;
const int volt = 3.3;
const int ANALOG_MAX = 4096;
const int Threshold = 1000; //点灯する電圧値[mV]
const int sensa1_jyo=2;

TaskHandle_t thp[1];

void setup() {
  // シリアル初期化
  Serial.begin(115200);
  Serial2.begin(115200);
  //while(!Serial);
  
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENB, OUTPUT);

  ledcSetup(pwmChannelA, freq, resolution);
  ledcSetup(pwmChannelB, freq, resolution);

  ledcAttachPin(ENA, pwmChannelA);
  ledcAttachPin(ENB, pwmChannelB);

  //Serial.println("モーター制御の準備完了。m: 前進, n: 後退, b: 停止");

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  server.on("/", handleRoot);
  server.on("/MEN",men );
  server.on("/DOU",dou);
  server.on("/KOTE", kote);
  server.on("/FORWARD", forward);
  server.on("/BACKWARD", backward);
  server.on("/LEFT", left);
  server.on("/RIGHT", right);
  server.on("/STOP", stop);
  server.on("/SOUSA", sousa);
  server.on("/JIDOU", jidou);

  server.begin();
  Serial.println("HTTP server started");
  //xTaskCreatePinnedToCore(sensa, "sensa", 4096, NULL, 3, &thp[0], 0);
}

const char INDEX_HTML[] PROGMEM = R"rawliteral(

<!DOCTYPE HTML>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>KAWAROBO Control Interface</title>
  
  <style>
    *,
    ::before,                
    ::after {
      padding: 0;
      margin: 0;
      box-sizing: border-box;     
    }

    ul,
    ol {
      list-style: none;             /*リストの・を非表示にする*/
    }

    a {
      color: inherit;               /*親要素の文字色を継承*/
      text-decoration: none;        /*下線をなくす*/
      text-align: center;
    }

    html { 
      display: inline-block; 
      margin: 0 auto;
    }

    header {
      margin-top: 5px;
      margin-bottom: 5px;
    }

    h2 {
      margin-top: 0px;
      margin-bottom: 20px;
      line-height: 10px;
      margin-left: 0px;
    }
    p {
      text-align: center;
    }

    p3 {
      font-size: 12px;
      text-align: center;
    }

    h5 {
      font-size: 20px;
      text-align: center;
    }

    h4 {
      margin-top: 20px;
      font-size: 20px;
      text-align: center;
    }

    h4::after {
      content: '';
      display: block;
      width: 100px;
      height: 2px;
      background-color: #000000;
      margin: 0px auto 0;
    }

    body {
      margin: 0;
      padding: 5px;
    }
    .btn { 
      text-decoration: none; 
      font-size: 20px; 
      display: inline-block;
      width: 80px;
      line-height: 60px;
      border-radius: 5px;
      background-color: #668ad8; 
      color: #FFF; 
      border: none; 
      cursor: pointer;
      transition: background-color 0.3s ease;
    }
    .btn:hover {
      background-color: #627295;
    }
    .btn:active {
      background-color: #668ad8;
      box-shadow: 0px 1px #627295;
      transform: translateY(1px);
    }


    .control-group {
      text-align: center;
    }


    .chapter-list {
      width: 100%;
      max-width: 100%;
      margin: 0px auto 100px;
      display: grid;
      grid-template-columns: repeat(3, 1fr); /* Two columns */
      gap: 2px 2px; 
      justify-content: center;
    }

    .chapter-list li {
      background-color: rgba(128, 128, 128, 0.118);
      position: relative;
    }

    .botan-list {
      width: 100%;
      max-width: 100%;
      margin: 0px auto 1px;
      display: grid;
      grid-template-columns: repeat(3, 1fr); 
      gap: 2px 2px; 
      justify-content: center;
    }

    .botan-list2 {
      width: 100%;
      max-width: 100%;
      margin: 0px auto 20px;
      display: grid;
      grid-template-columns: repeat(2, 1fr); 
      gap: 2px 2px; 
      justify-content: center;
    }

    .botan-list li {
      background-color: rgba(128, 128, 128, 0.118);
      position: relative;
    }

    

  </style>
  
</head>

<body>
  <header>
    <h2>UPRP-ロボ剣-</h2> 
  </header>

  <ul class="chapter-list">
    <li>
      <ul class="botan-list">
        <li></li>
        <li>
          <div class="control-group">
            <a href="/FORWARD" class="btn">前</a>
          </div>
        </li>
        <li></li>
        <li>
          <div class="control-group">
            <a href="/LEFT" class="btn">左回</a>
          </div>
        </li>
        <li>
          <div class="control-group">
            <a href="/STOP" class="btn">止</a>
          </div>
        </li>
        <li>
          <div class="control-group">
            <a href="/RIGHT" class="btn">右回</a>
          </div>
        </li>
        <li></li>
        <li>
          <div class="control-group">
            <a href="/BACKWARD" class="btn">後</a>
          </div>
        </li>
        <li></li>
        
      </ul>
    </li>
    <li>
      <h4>モード</h4>
      <h5>%STATE1%</h5>
      <h4>POKIの状態</h4>
      <h5>%STATE2%</h5>
    </li>
    <li>
      <ul class="botan-list">
        <li>
          <div class="control-group">
            <a href="/MEN" class="btn">面</a>
          </div>
        </li>
        <li>
          <div class="control-group">
            <a href="/DOU" class="btn">胴</a>
          </div>
        </li>
        <li>
          <div class="control-group">
            <a href="/KOTE" class="btn">小手</a>
          </div>
        </li>
      </ul>
      <ul class="botan-list2">
        <li>
          <div class="control-group">
            <a href="/SOUSA" class="btn">操作</a>
          </div>
        </li>
        <li>
          <div class="control-group">
            <a href="/JIDOU" class="btn">自動</a>
          </div>
        </li>
      </ul>
      <ul class="botan-list">
        <li>
          <p3>スピード:</p3>
        </li>
        <li>
          <input type="range" min="0" max="100" step="1" value="1" id="iptJS">
        </li>
        <li>
          <span id="spnJS">0%</span>
        </li>

        <script>
          let ipt=document.getElementById("iptJS");
          let spn=document.getElementById("spnJS");
          let rangeValue=function(ipt,spn){
            return function(){
              spn.innerHTML=ipt.value+"%";
            }
          }
          ipt.addEventListener("input",rangeValue(ipt,spn));
        </script>
      </ul>
    </li>
  </ul>

</body>
</html>

)rawliteral";

String State1 = "未選択"; // 適切な初期状態に応じて初期化します
String State2 = "ハロー"; // 適切な初期状態に応じて初期化します

// HTMLページを提供する関数
void handleRoot() {
  String html = String(INDEX_HTML);
  html.replace("%STATE1%", State1); // %STATE% のプレースホルダーを現在の State で置き換えます
  html.replace("%STATE2%", State2); // %STATE% のプレースホルダーを現在の State で置き換えます
  server.send(200, "text/html", html);
}

void men() {
  Serial.println("面");
  Serial2.println("u");
  State2 = "面";
  handleRoot();
}

void dou() {
  Serial.println("胴");
  Serial2.println("i");
  State2 = "胴";
  handleRoot();
}

void kote() {
  Serial.println("小手");
  Serial2.println("o");
  State2 = "小手";
  handleRoot();
}

void forward() {
  Serial.println("前進");
  State2 = "前";
  // モーターA前進
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  ledcWrite(pwmChannelA, dutyCycle);
  // モーターB前進
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  ledcWrite(pwmChannelB, dutyCycle);
  handleRoot();
}

void backward() {
  Serial.println("後進");
  State2 = "後";
  // モーターA後退
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  ledcWrite(pwmChannelA, dutyCycle);
  // モーターB後退
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  ledcWrite(pwmChannelB, dutyCycle);
  handleRoot();
}

void left() {
  Serial.println("左回り");
  State2 = "左回";
  // モーターA前進
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  ledcWrite(pwmChannelA, dutyCycle);
  // モーターB後退
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  ledcWrite(pwmChannelB, dutyCycle);
  handleRoot();
}

void right() {
  Serial.println("右回り");
  State2 = "右回";
  // モーターA後退
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  ledcWrite(pwmChannelA, dutyCycle);
  // モーターB後退
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  ledcWrite(pwmChannelB, dutyCycle);
  handleRoot();
}

void stop() {
  Serial.println("停止");
  Serial2.println("q");
  State2 = "止";
  // モーターA停止
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  ledcWrite(pwmChannelA, 0);
  // モーターB停止
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  ledcWrite(pwmChannelB, 0);
  handleRoot();
}

void sousa() {
  Serial.println("操作モード");
  Serial2.println("t");
  State1 = "操作";
  handleRoot();
}

void jidou() {
  Serial.println("自動モード");
  Serial2.println("y");
  State1 = "自動";
  handleRoot();
}


void loop() {
  server.handleClient();
}

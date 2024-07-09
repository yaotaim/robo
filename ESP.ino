#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "ASRcast-3870A4ED";
const char* password = "asciinew";

WebServer server(80);

const char INDEX_HTML[] PROGMEM = R"rawliteral(
<!DOCTYPE HTML>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    html { font-family: Helvetica; display: inline-block; margin: 0px auto;text-align: center;} 
    .btn { 
      padding: 1px 1px; 
      text-decoration: none; 
      font-size: 20px; 
      margin: 1px;
      display: inline-block;
      width: 50px;
      border-radius: 5px;
      background-color: #668ad8; 
      color: #FFF; 
      border: none; 
      cursor: pointer;
    }
    .btn:hover {
      background-color: #627295;
    }
    .btn:active {
      background-color: #668ad8;
      box-shadow: 0px 1px #627295;
      transform: translateY(1px);
    }
    .controls {
      justify-content: center;
      align-items: center;
      flex-wrap: wrap;
    }
    .control-group {
      margin: 10px;
    }
    .led-control {
      margin-top: 20px;
    }
  </style>
</head>

<body>
  <p>かわいいロボット : %STATE%</p>

  <div class="controls">

    <div class="control-group">
      <a href="/FORWARD" class="btn">前</a>
    </div>

    <div class="control-group">
      <a href="/LEFT" class="btn">左回</a>
      <a href="/STOP" class="btn">止</a>
      <a href="/RIGHT" class="btn">右回</a>
    </div>

    <div class="control-group">
      <a href="/BACKWARD" class="btn">後</a>
    </div>

  </div>

  <div class="led-control">
    <a href="/F_LEFT" class="btn">左見</a>
    <a href="/F_MIDDLE" class="btn">正面</a>
    <a href="/F_RIGHT" class="btn">右見</a>
    <a href="/SOUSA" class="btn">操作</a>
    <a href="/JIDOU" class="btn">自動</a>
  </div>

</body>
</html>
)rawliteral";

// LEDのピン設定
String State = "ハロー"; // 適切な初期状態に応じて初期化します

// HTMLページを提供する関数
void handleRoot() {
  String html = String(INDEX_HTML);
  html.replace("%STATE%", State); // %STATE% のプレースホルダーを現在の State で置き換えます
  server.send(200, "text/html", html);
}

void f_left() {
  Serial.println("左見て");
  Serial2.println("u");
  State = "左見てる";
  handleRoot();
}

void f_middle() {
  Serial.println("正面見て");
  Serial2.println("i");
  State = "正面見てる";
  handleRoot();
}

void f_right() {
  Serial.println("右見て");
  Serial2.println("o");
  State = "右見てる";
  handleRoot();
}

void forward() {
  Serial.println("前進");
  State = "前";
  handleRoot();
}

void backward() {
  Serial.println("後進");
  State = "後";
  handleRoot();
}

void left() {
  Serial.println("左回り");
  State = "左回";
  handleRoot();
}

void right() {
  Serial.println("右回り");
  State = "右回";
  handleRoot();
}

void stop() {
  Serial.println("停止");
  Serial2.println("q");
  State = "止";
  handleRoot();
}

void sousa() {
  Serial.println("操作モード");
  Serial2.println("t");
  State = "操作";
  handleRoot();
}

void jidou() {
  Serial.println("自動モード");
  Serial2.println("y");
  State = "自動";
  handleRoot();
}

void setup() {
  Serial.begin(115200);
  Serial2.begin(115200);


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
  server.on("/F_LEFT",f_left );
  server.on("/F_MIDDLE",f_middle);
  server.on("/F_RIGHT", f_right);
  server.on("/FORWARD", forward);
  server.on("/BACKWARD", backward);
  server.on("/LEFT", left);
  server.on("/RIGHT", right);
  server.on("/STOP", stop);
  server.on("/SOUSA", sousa);
  server.on("/JIDOU", jidou);

  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}

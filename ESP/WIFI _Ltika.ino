//wifi接続してhtmlサーバーたてる+サーバー上からサーバー上からLチカ
//ESPでwebサーバ上からLチカ
#include <WiFi.h>
#include <WebServer.h>

// Wi-FiのSSIDとパスワードを設定
const char* ssid = "ASRcast-3870A4ED";
const char* password = "asciinew";

// Webサーバーのインスタンスを作成
WebServer server(80);

// HTMLコンテンツ
const char INDEX_HTML[] PROGMEM = R"rawliteral(
<!DOCTYPE HTML>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
      html { font-family: Helvetica; display: inline-block; margin: 0px auto;text-align: center;} 
      h1 {font-size:28px;} 
      .btn_on { padding:12px 30px; text-decoration:none; font-size:24px; background-color:
        #668ad8; color: #FFF; border-bottom: solid 4px #627295; border-radius: 2px;}
      .btn_on:active { -webkit-transform: translateY(0px); transform: translateY(0px);
        border-bottom: none;}
      .btn_off { background-color: #555555; border-bottom: solid 4px #333333;}
    </style>
  </head>
 
  <body><h1>Webサーバー</h1>
    <p>LEDの状態 : %STATE%</p>
    <p>（ 00.0℃, 00.0% ）</p>
    <p><a href="/ON"><button class="btn_on"> ON </button></a></p>
    <p><a href="/OFF"><button class="btn_on btn_off">OFF</button></a></p>
  </body>
</html>
)rawliteral";

// LEDのピン設定
const int LED_PIN = 4;
String ledState = "OFF";

// HTMLページを提供する関数
void handleRoot() {
  String html = INDEX_HTML;
  html.replace("%STATE%", ledState);
  server.send(200, "text/html", html);
}

// LEDをONにする関数
void handleLEDOn() {
  digitalWrite(LED_PIN, HIGH);
  ledState = "ON";
  handleRoot();
}

// LEDをOFFにする関数
void handleLEDOff() {
  digitalWrite(LED_PIN, LOW);
  ledState = "OFF";
  handleRoot();
}

void setup() {
  // シリアル通信を開始
  Serial.begin(115200);
  
  // LEDピンを出力に設定
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  // Wi-Fiに接続
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // ルートURLにアクセスがあったときのハンドラーを設定
  server.on("/", handleRoot);
  server.on("/ON", handleLEDOn);
  server.on("/OFF", handleLEDOff);

  // Webサーバーを開始
  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  // クライアントからのリクエストを処理
  server.handleClient();
}

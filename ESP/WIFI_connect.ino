//ESPでWIFI接続する
#include <WiFi.h>

const char *ssid="ASRcast-3870A4ED";          //  *** 書き換え必要 ***
const char *password="asciinew";    //  *** 書き換え必要（8文字以上）***

WiFiServer server(80);

void setup() {

  Serial.begin(115200);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("connecting");
  }
  Serial.println(WiFi.localIP());
  server.begin();
}

void loop() {
}

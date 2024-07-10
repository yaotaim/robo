//IRセンサーが正常か試す
//sRA-MD4-rakka-kai4とiikanzi(サーボとDCの並列処理~面でバック~)の合体



int usrf = 52;//落下防止用距離センサー右前
int uslf = 51;//落下防止用距離センサー左前
int uslb = 50;//落下防止用距離センサー左後ろ
int usrb = 53;//落下防止用距離センサー右後ろ


int osl  = 42;//敵感知用センサー左
int osr  = 44;//敵感知用センサー右
//int osb  = 41;//敵感知用センサー後ろ
int osrf = 43;//敵感知センサー右前

//const int ANALOG = 8;//敵感知用センサー前信号入力
//float Vcc = 5.0;//シャープ距離センサー関連
//float dist1;//シャープ距離センサー関連
//float osf;//シャープ距離センサー関連
 

byte val = 0;

void setup() {
  Serial.begin(115200);//シリアル通信
}


void loop() {
  //dist1 = Vcc*analogRead(ANALOG)/1023; //(5.0V*センサ数値/1023)1023は5V入力時の値
  //osf = 26.549*pow(dist1,-1.2091); //距離換算
  if (digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//もし落下防止用距離センサー全部異常なしなら
  //0がLOW,1がHIGH
    Serial.println("rakka seijyou");
    if(digitalRead(osl)==LOW && digitalRead(osr) == HIGH && digitalRead(osrf)==HIGH){//敵感知用センサー左反応=>左回転
      Serial.println("left teki");
    }else if(digitalRead(osl)==HIGH && digitalRead(osr) == LOW && digitalRead(osrf)==HIGH){//敵感知用センサー右反応=>右回転
      Serial.println("right teki");
    //}else if(digitalRead(osl)==HIGH && digitalRead(osr) == HIGH && digitalRead(osrf)==LOW){//敵感知用センサー左前反応=>左回転小
    //  Serial.println("left-forward teki");
    }else if(digitalRead(osl)==HIGH && digitalRead(osr) == HIGH && digitalRead(osrf)==LOW){//敵感知用センサー右前反応=>右回転小
      Serial.println("right-forward teki");
    //}else if(digitalRead(osl)==HIGH && digitalRead(osr) == HIGH && osf<10 && digitalRead(osb)==HIGH){//敵感知用センサー前反応=>面
    //  Serial.println("forward teki");
    

    //}else if(digitalRead(osl)==HIGH && digitalRead(osr) == HIGH && osf>10 && digitalRead(osb)==LOW){//敵感知用センサー前反応=>面　
    //  Serial.println("back teki");
    }


  }else if(digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == HIGH && digitalRead(usrb) == LOW){//落下防止センサー左後ろ反応=>右前
    Serial.println("lb ochisou");
  }else if(digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == HIGH){//落下防止センサー右後ろ反応=>左前
    Serial.println("rb ochisou");

  }else if(digitalRead(usrf)==LOW && digitalRead(uslf) == LOW && digitalRead(uslb) == HIGH && digitalRead(usrb) == HIGH){//落下防止センサー後ろ2つ反応=>前
    Serial.println("rblb ochisou");
  }else if(digitalRead(usrf)==HIGH && digitalRead(uslf) == LOW && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//落下防止センサー右前反応=>後ろ=>左回転
    Serial.println("rf ochisou");
  }else if(digitalRead(usrf)==LOW && digitalRead(uslf) == HIGH && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//落下防止センサー左前反応=>後ろ=>右回転
    Serial.println("lf ochisou");
  }else if(digitalRead(usrf)==HIGH && digitalRead(uslf) == HIGH && digitalRead(uslb) == LOW && digitalRead(usrb) == LOW){//落下防止センサー前2つ反応=>後ろ=>回転
    Serial.println("rf lf ochisou");   
  }else{//その他
    Serial.println("irei");
  }


  Serial.println("--------------------");
  Serial.println("usrf");
  Serial.println(digitalRead(usrf));
  Serial.println("uslf");
  Serial.println(digitalRead(uslf));
  Serial.println("uslb");
  Serial.println(digitalRead(uslb));
  Serial.println("usrb");
  Serial.println(digitalRead(usrb));
  Serial.println("osl");
  Serial.println(digitalRead(osl));
  Serial.println("osr");
  Serial.println(digitalRead(osr));
  Serial.println("osrf");
  Serial.println(digitalRead(osrf));

  //Serial.println("osb");
  //Serial.println(digitalRead(osb));
  //Serial.println("osf");
  //Serial.println(digitalRead(osf));
  //Serial.println(osf);
  Serial.println("------------------------");
  delay(1000);
}

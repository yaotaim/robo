import pyttsx3

def read_text(text):
    # エンジンの初期化
    engine = pyttsx3.init()

    # 読み上げ速度を設定
    engine.setProperty('rate', 150)

    # 音量を設定
    engine.setProperty('volume', 0.9)

    # 声を英語に変更
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)

    # テキストを読み上げる
    engine.say(text)

    # 読み上げを実行
    engine.runAndWait()

if __name__ == "__main__":
    # 読み上げたいテキスト
    text = "Hello! Reading English out loud with Python."
    read_text(text)

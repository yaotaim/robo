from threading import Lock
import requests
from playsound import playsound
import wave
import pyaudio
import time
import urllib.parse
import os

def playwav(file):
    # wavファイルの読み込み
    with wave.open(file, 'rb') as f:
        # PyAudioのインスタンスを生成
        p = pyaudio.PyAudio()

        # Streamを開く
        stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                        channels=f.getnchannels(),
                        rate=f.getframerate(),
                        output=True)

        # チャンクサイズを設定
        chunk_size = 1024

        # wavファイルを再生
        data = f.readframes(chunk_size)
        while data:
            stream.write(data)
            data = f.readframes(chunk_size)

        time.sleep(0.5)  # 0.5s待つ これがないと文末が途切れる

        # StreamとPyAudioインスタンスを終了
        stream.stop_stream()
        stream.close()
        p.terminate()

def voicebox_speech(text):
    mutex_lock = Lock()
    query = {
        'speaker': 1,
        'text': text
    }
    response = requests.post(
        'http://127.0.0.1:50021/audio_query?' + urllib.parse.urlencode(query))
    query = response.content
    headers = {'Content-Type': 'application/json'}
    response = requests.post(
        'http://127.0.0.1:50021/synthesis?speaker=1', data=query, headers=headers)
    with mutex_lock:
        with open('audio.wav', 'wb') as f:
            f.write(response.content)
        playwav("audio.wav")
        os.remove("audio.wav")
    return True

if __name__ == "__main__":
    while True:
        # ユーザー入力を取得
        user_input = input("話す内容を入力してください (終了するには'quit'と入力): ")
        if user_input.lower() == 'quit':
            print("終了します。")
            break
        voicebox_speech(user_input)

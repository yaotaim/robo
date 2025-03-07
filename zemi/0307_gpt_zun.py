from openai import OpenAI
import os
from threading import Lock
import requests
import wave
import pyaudio
import time
import urllib.parse

MODEL = "gpt-4o-mini"

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# chat.txt からシステムメッセージを読み込む
with open("chat.txt", "r", encoding="utf-8") as f:
    system_message = f.read().strip()

# ユーザーの入力を取得
user_input = input("You: ")

def playwav(file):
    """WAVファイルを再生する関数"""
    with wave.open(file, 'rb') as f:
        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                        channels=f.getnchannels(),
                        rate=f.getframerate(),
                        output=True)
        chunk_size = 1024

        data = f.readframes(chunk_size)
        while data:
            stream.write(data)
            data = f.readframes(chunk_size)

        time.sleep(0.5)  # 0.5s待つ これがないと文末が途切れる

        stream.stop_stream()
        stream.close()
        p.terminate()

def voicebox_speech(text):
    """Voicevox API を使って音声合成し、再生する関数"""
    mutex_lock = Lock()
    query = {
        'speaker': 1,
        'text': text
    }
    
    # 音声クエリを取得
    response = requests.post(
        'http://127.0.0.1:50021/audio_query?' + urllib.parse.urlencode(query))
    
    if response.status_code != 200:
        print("音声クエリの取得に失敗しました")
        return False

    query_json = response.json()  # JSONとして取得

    # 音声合成リクエストを送信
    headers = {'Content-Type': 'application/json'}
    response = requests.post(
        'http://127.0.0.1:50021/synthesis?speaker=1', json=query_json, headers=headers)
    
    if response.status_code != 200:
        print("音声合成に失敗しました")
        return False

    with mutex_lock:
        with open('audio.wav', 'wb') as f:
            f.write(response.content)
        playwav("audio.wav")
        os.remove("audio.wav")
    return True

# ChatGPT にメッセージを送信
try:
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_input}
        ]  # ここにカンマが抜けていたのを修正
    )

    # AIの応答を取得
    assistant_reply = completion.choices[0].message.content
    print("Assistant: " + assistant_reply)

    # 生成したAIの応答を音声で再生
    voicebox_speech(assistant_reply)

except Exception as e:
    print(f"エラーが発生しました: {e}")

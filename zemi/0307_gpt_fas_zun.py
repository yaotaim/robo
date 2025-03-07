import pyaudio
import wave
import numpy as np
from faster_whisper import WhisperModel
from openai import OpenAI
from threading import Lock
import requests
import time
import urllib.parse
import os

# OpenAI API設定
MODEL = "gpt-4o-mini"
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# 録音の設定
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
SILENCE_THRESHOLD = 600  # 無音のしきい値(音量)
SILENCE_DURATION = 20  # 無音と判定する持続時間(フレーム数)

# chat.txt からシステムメッセージを読み込む
with open("chat.txt", "r", encoding="utf-8") as f:
    system_message = f.read().strip()

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
        time.sleep(0.5)  # 文末が途切れないように少し待つ
        stream.stop_stream()
        stream.close()
        p.terminate()

def voicebox_speech(text):
    """Voicevox API を使って音声合成し、再生する関数"""
    mutex_lock = Lock()
    query = {'speaker': 1, 'text': text}
    
    # 音声クエリを取得
    response = requests.post('http://127.0.0.1:50021/audio_query?' + urllib.parse.urlencode(query))
    if response.status_code != 200:
        print("音声クエリの取得に失敗しました")
        return False

    query_json = response.json()
    
    # 音声合成リクエストを送信
    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://127.0.0.1:50021/synthesis?speaker=1', json=query_json, headers=headers)
    
    if response.status_code != 200:
        print("音声合成に失敗しました")
        return False

    with mutex_lock:
        with open('audio.wav', 'wb') as f:
            f.write(response.content)
        playwav("audio.wav")
        os.remove("audio.wav")
    return True

def record_audio(output_file="output.wav"):
    """音声を録音する関数"""
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    print("Recording started...")
    frames = []
    silence_frames = 0
    recording = False

    while True:
        data = stream.read(CHUNK)
        audio_data = np.frombuffer(data, dtype=np.int16)

        # 音声が無音かどうかを判定
        if np.abs(audio_data).mean() > SILENCE_THRESHOLD:
            if not recording:
                print("Voice detected, recording...")
                recording = True
            frames.append(data)
            silence_frames = 0
        else:
            if recording:
                silence_frames += 1
                if silence_frames > SILENCE_DURATION:
                    print("Silence detected, stopping...")
                    break
            frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # 録音結果を保存
    wf = wave.open(output_file, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print(f"Recording finished and saved as '{output_file}'")
    return output_file

def transcribe_and_respond(audio_file):
    """Whisper で音声をテキストに変換し、ChatGPT に送信し、Voicevox で音声合成"""
    model_size = "small"  # tiny, base, small, medium, large
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    segments, info = model.transcribe(audio_file, beam_size=5)
    print("Detected language:", info.language, "Probability:", info.language_probability)

    if info.language not in ["ja", "en"]:
        print("言語がサポートされていません")
        return

    # Whisper の出力を取得
    user_text = ''.join(segment.text for segment in segments)
    print("Transcribed Text:", user_text)

    # ChatGPT にメッセージを送信
    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_text}
            ]
        )

        # AIの応答を取得
        assistant_reply = completion.choices[0].message.content
        print("Assistant:", assistant_reply)

        # 生成したAIの応答を音声で再生
        voicebox_speech(assistant_reply)

    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    audio_file = record_audio()
    transcribe_and_respond(audio_file)

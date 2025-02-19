import requests
import sounddevice as sd
import numpy as np
import wave

VOICEVOX_URL = "http://127.0.0.1:50021"

def synthesize_speech(text, speaker=3):
    """VOICEVOXを使って音声合成する"""
    params = {"text": text, "speaker": speaker}
    response = requests.post(f"{VOICEVOX_URL}/audio_query", params=params)
    if response.status_code != 200:
        print("音声クエリの作成に失敗しました")
        return None

    query = response.json()
    
    response = requests.post(f"{VOICEVOX_URL}/synthesis", json=query, params=params)
    if response.status_code != 200:
        print("音声合成に失敗しました")
        return None

    return response.content

def play_audio(audio_data):
    """音声データを再生する"""
    with wave.open("output.wav", "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        wf.writeframes(audio_data)

    # 音声を再生
    with wave.open("output.wav", "rb") as wf:
        data = wf.readframes(wf.getnframes())
        audio = np.frombuffer(data, dtype=np.int16)
        sd.play(audio, samplerate=24000)
        sd.wait()

if __name__ == "__main__":
    while True:
        text = input("読み上げるテキストを入力 (qで終了): ")
        if text.lower() == "q":
            break
        audio_data = synthesize_speech(text)
        if audio_data:
            play_audio(audio_data)

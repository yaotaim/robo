import pyaudio
import wave
import numpy as np
from faster_whisper import WhisperModel
from playsound import playsound

from threading import Lock
import requests
import time
import urllib.parse
import os

# 録音の設定
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
SILENCE_THRESHOLD = 600  # 無音のしきい値(音量)
SILENCE_DURATION = 20  # 無音と判定する持続時間(フレーム数)

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


# 音声を録音する関数
def record_audio(output_file="output.wav"):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                        input=True, frames_per_buffer=CHUNK)

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

# Whisper で音声をテキストに変換し、特定の単語を判定
def transcribe_and_respond(audio_file):
    model_size = "small"  # tiny, base, small, medium, large
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    segments, info = model.transcribe(audio_file, beam_size=5)
    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    if info.language not in ["ja", "en"]:
        print("なにご？")
        return

    c_text = ''
    for segment in segments:
        print(segment.text)
        c_text += segment.text

    if 'よろしく' in c_text or '宜しく' in c_text:
        print('zun(ヨロシクオネガイシマス)')
        voice_input="よろしくおねがいします"
        voicebox_speech(voice_input)

    elif 'おはよう' in c_text:
        print('zun(ヨロシクオネガイシマス)')
        voice_input="よろしくおねがいします"
        voicebox_speech(voice_input)
    else:
        print('zun(ナンテイッタ？)')
        voice_input="なんていった？"
        voicebox_speech(voice_input)

if __name__ == "__main__":
    audio_file = record_audio()
    transcribe_and_respond(audio_file)
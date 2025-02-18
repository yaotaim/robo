import pyaudio
import wave
from faster_whisper import WhisperModel
from playsound import playsound
import numpy as np

# 録音の設定
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
SILENCE_THRESHOLD = 500  # 無音のしきい値(音量)
SILENCE_DURATION = 30  # 無音と判定する持続時間(フレーム数)

# 音声を録音する関数
def record_audio():
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
    wf = wave.open("output.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print("Recording finished and saved as 'output.wav'")

if __name__ == "__main__":
    record_audio()

# 録音データを WAV ファイルに保存
output_file = "output.wav"
with wave.open(output_file, 'wb') as wf:
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))

print(f"音声を {output_file} に保存しました。")

model_size = "small"#tiny base small medium (large)
model = WhisperModel(model_size, device="cpu", compute_type="int8")

segments, info = model.transcribe("output.wav", beam_size=5)

print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

c_text=''
for segment in segments:
    #print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
    print(segment.text)
    c_text+=segment.text

if 'よろしく'or'宜しく' in c_text:
    print('zun(ヨロシクオネガイシマス)')
    playsound("zun1.wav")
else:
    print('zun(ナンテイッタ？)')
    playsound("zun2.wav")

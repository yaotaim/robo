import pyaudio
import wave
import numpy as np

# 録音の設定
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
SILENCE_THRESHOLD = 600  # 無音のしきい値(音量)500
SILENCE_DURATION = 20  # 無音と判定する持続時間(フレーム数)15

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
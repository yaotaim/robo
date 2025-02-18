import pyaudio
import wave
import numpy as np
from faster_whisper import WhisperModel
from playsound import playsound

# 録音の設定
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
SILENCE_THRESHOLD = 600  # 無音のしきい値(音量)
SILENCE_DURATION = 20  # 無音と判定する持続時間(フレーム数)

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
        playsound("zun1.wav")
    else:
        print('zun(ナンテイッタ？)')
        playsound("zun2.wav")

if __name__ == "__main__":
    audio_file = record_audio()
    transcribe_and_respond(audio_file)

import pyaudio
import wave
from faster_whisper import WhisperModel
from playsound import playsound

# 録音パラメータ
fs = 44100            # サンプルレート（Hz）
duration = 5          # 録音時間（秒）
channels = 1          # モノラル（ステレオの場合は 2）
chunk = 1024          # 一度に読み込むフレーム数

print(f"録音開始...({duration}秒間)")

# PyAudio のインスタンスを生成
p = pyaudio.PyAudio()

# 録音用ストリームのオープン
stream = p.open(format=pyaudio.paInt16,
                channels=channels,
                rate=fs,
                input=True,
                frames_per_buffer=chunk)

frames = []

# 録音（duration 秒間、chunk 単位でデータを取得）
num_chunks = int(fs / chunk * duration)
for i in range(num_chunks):
    data = stream.read(chunk)
    frames.append(data)

print("録音終了")

# ストリームを停止・クローズ、PyAudio インスタンスを終了
stream.stop_stream()
stream.close()
p.terminate()

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

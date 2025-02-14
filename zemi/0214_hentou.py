import simpleaudio
from faster_whisper import WhisperModel

model_size = "medium"

# Run on GPU with FP16
#model = WhisperModel(model_size, device="cuda", compute_type="float16")
model = WhisperModel(model_size, device="cpu", compute_type="int8")

# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")

segments, info = model.transcribe("audio3.mp3", beam_size=5)

print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

for segment in segments:
    #print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
    print(segment.text)

if 'よろしく' in str(segment.text):
    wav_obj = simpleaudio.WaveObject.from_wave_file("zun1.wav")
    play_obj = wav_obj.play()
    play_obj.wait_done()
else:
    print('とくになし')



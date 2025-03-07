from openai import OpenAI
import os
from threading import Lock
import requests
from playsound import playsound
import wave
import pyaudio
import time
import urllib.parse

MODEL = "gpt-4o-mini"

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

with open("chat.txt", "r", encoding="utf-8") as f:
    system_message = f.read().strip()

user_input = input("You: ")

def playwav(file):
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

completion = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_input}
    ]
    voicebox_speech(user_input)
)

print("Assistant: " + completion.choices[0].message.content)

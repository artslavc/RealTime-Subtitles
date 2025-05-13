import pyaudio
from vosk import Model, KaldiRecognizer
import json
from googletrans import Translator
import threading

model = Model("full_path/vosk-model-small-en-us-0.15")
rec = KaldiRecognizer(model, 16000)

translator = Translator()

numbers = 1

# Настройка PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()


print("\nНачинаем распознавание...\n")

def translate(text):
    global numbers
    
    text = translator.translate(text, dest='ru')
    print(f'[{numbers}] * ' + text.text)
    numbers += 1

while True:
    data = stream.read(4000)
    if rec.AcceptWaveform(data):
        json_str = rec.Result()
        data = json.loads(json_str)
        text = data["text"]
        if text:
            threading.Thread(target=translate, args=(text,)).start()

import json, time, requests

import pyttsx3, pyaudio, vosk


WEATHER_API_KEY = "fb50eed1b9efe0e2f8660950a8e70f51"


class Speech:
    def __init__(self):
        self.speaker = 0
        self.tts = pyttsx3.init('sapi5')

    def set_voice(self, speaker):
        self.voices = self.tts.getProperty('voices')
        for count, voice in enumerate(self.voices):
            if count == 0:
                print('0')
                id = voice.id
            if speaker == count:
                id = voice.id
        return id

    def text2voice(self, speaker=0, text='Готов'):
        self.tts.setProperty('voice', self.set_voice(speaker))
        self.tts.say(text)
        self.tts.runAndWait()


class Recognize:
    def __init__(self):
        model = vosk.Model('vosk-model-small-ru-0.22')
        self.record = vosk.KaldiRecognizer(model, 16000)
        self.stream()

    def stream(self):
        pa = pyaudio.PyAudio()
        self.stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)


    def listen(self):
        while True:
            data = self.stream.read(4000, exception_on_overflow=False)
            if self.record.AcceptWaveform(data) and len(data) > 0:
                answer = json.loads(self.record.Result())
                if answer['text']:
                    yield answer['text']


def speak(text):
    speech = Speech()
    speech.text2voice(speaker=0, text=text)


def weather(city_name):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&lang=ru&units=metric&appid={WEATHER_API_KEY}"

    response = requests.get(url)
    data = response.json()

    return data["weather"][0]["description"]

def pressure(city_name):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&lang=ru&units=metric&appid={WEATHER_API_KEY}"

    response = requests.get(url)
    data = response.json()

    return data["main"]["pressure"]


def wind_speed(city_name):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&lang=ru&units=metric&appid={WEATHER_API_KEY}"

    response = requests.get(url)
    data = response.json()

    return data["wind"]["speed"]


def temp(city_name):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&lang=ru&units=metric&appid={WEATHER_API_KEY}"

    response = requests.get(url)
    data = response.json()

    return data["main"]["temp"]


def clouds(city_name):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&lang=ru&units=metric&appid={WEATHER_API_KEY}"

    response = requests.get(url)
    data = response.json()

    return data["clouds"]["all"]
    

if __name__ == '__main__':
    rec = Recognize()
    text_gen = rec.listen()
    rec.stream.stop_stream()
    speak('Вас приветствует погодный голосовой помощник!')
    time.sleep(0.2)
    speak('Погодные условия, какого города вас интересуют?')
    rec.stream.start_stream()
    for text in text_gen:
        time.sleep(0.5)
        if text:
            city_name = text
            print(city_name)
            speak('Что конкретно вас интересует?')
            time.sleep(0.5)
            for text_1 in text_gen:
                if text_1 == 'погодные условия':
                    weather = weather(city_name)
                    print(f'Погода в {city_name}: {weather}') 
                    speak(f'Погода в {city_name}: {weather}, что ещё нужно?') 
                    
                if text_1 == 'атмосферное давление':
                    pressure = pressure(city_name)
                    print(f'Атмосферное давление в {city_name}: {pressure} мм/p') 
                    speak(f'Атмосферное давление в {city_name} равняется {pressure} милиметров ртутного столба, что ещё нужно?') 
                    
                if text_1 == 'скорость ветра':
                    wind_speed = wind_speed(city_name)
                    print(f'Скорость ветра в {city_name}: {wind_speed} м/c') 
                    speak(f'Скорость ветра в {city_name} достигает {wind_speed} метров в секунду, что ещё нужно?') 

                if text_1 == 'температура воздуха':
                    temp = temp(city_name)
                    print(f'Температура воздуха в {city_name}: {temp} градусов цельсия') 
                    speak(f'Температура воздуха в {city_name}: {temp} градусов цельсия, что ещё нужно?') 

                if text_1 == 'облачность':
                    clouds = clouds(city_name)
                    print(f'Облачность в {city_name}: {clouds} %') 
                    speak(f'Облачность в {city_name} достигает {clouds} %, что ещё нужно?') 
                    
                if text_1 == 'сменить город': 
                    speak('Окей, какой город вас интересует?')
                    time.sleep(0.5) 
                    break

                elif text_1 == 'спасибо за помощь':
                    speak('Рада была помочь!')
                    time.sleep(0.5)
                    quit()

                else:
                    print(text_1)

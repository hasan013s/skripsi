# utils/sound_player.py

import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)  # kecepatan bicara

def speak(text):
    engine.say(text)
    engine.runAndWait()

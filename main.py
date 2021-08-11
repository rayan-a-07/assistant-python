import speech_recognition as sr    
import webbrowser
import time
import playsound
import os
import random
from gtts import gTTS
from datetime import datetime
from googletrans import Translator


translator = Translator()
joke_number = random.randint(1,4)
r = sr.Recognizer()

#translate to french function
def translate_to_french(text_src):
    translation = translator.translate(text_src, dest='fr', src='en')
    return translation.text

#translate to english function
def translate_to_english(text_src):
    translation = translator.translate(text_src, dest='en', src='fr')
    return translation.text

#joke_function
def joke_function(joke_number):
    joke_file = "/home/rayan/Documents/projets personnels/python/luna_speech_assistant/joke/blague-" + str(joke_number)
    joke_var = open(joke_file,'r')
    while True:
        joke_read = joke_var.readline()
        luna_speak(joke_read)
        if joke_read == "":
            break
    joke_var.close()

#input_function
def record_audio(ask = False):          
    with sr.Microphone() as source:
        if ask:
            luna_speak(ask)
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio, language = 'fr')
            #voice_date_en = r.recognize_google(audio, language = 'en') english output
        except sr.UnknownValueError:
            luna_speak('Désolé je ne vous ai pas compris')
        except sr.RequestError:
            luna_speak('Désolé je ne suis pas disponible pour le moment, veuillez réesayer plus tard')
        return voice_data

#audio_function
def luna_speak(audio_string):
    tts = gTTS(text=audio_string, lang='fr')
    audio_file = 'audio.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)

#en pronunciation
def luna_speak_en(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    audio_file = 'audio.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)    

now = datetime.now()
#output_function
def respond(voice_data):  
    nameCount = 0
    print(voice_data)
    if "comment t'appelles-tu" in voice_data:
        if nameCount > 1:
            luna_speak("Arrête de me demander plusieurs fois mon nom. Je t'ai déjà répondu")
        else: luna_speak("Je m'appelle Luna")
        nameCount+=1
    if "quel âge as-tu" in voice_data or "tu as quel âge" in voice_data:
        luna_speak("J'ai été créé le 27 juillet 2020")    
    if "il est quelle heure" in voice_data:
        luna_speak("Il est " + now.strftime("%H:%M:%S"))  
    if "raconte-moi une blague" in voice_data:
        luna_speak("d'accord, voici une blague")     
        joke_function(joke_number)
    if "quelle est la date d'aujourd'hui" in voice_data:
        month = translate_to_french(now.strftime("%B"))
        luna_speak(now.strftime("%d ") + month + now.strftime(" %Y"))
    if 'recherche' in voice_data:
        search = record_audio("Quelle recherche voulez-vous faire?")    
        url = 'https://google.com/search?q=' + search
        luna_speak("Voici ce que j'ai trouvé pour " + search)
        webbrowser.get().open(url)
    if 'cherche une localisation' in voice_data:
        location = record_audio("Quelle localisation voulez-vous chercher?")    
        url = 'https://google.nl/maps/place/' + location + '/&amp;'
        luna_speak("Voici la localisation que j'ai trouvé pour " + location)
        webbrowser.get().open(url)
    if "fais-moi l'accent anglais" in voice_data:
        luna_speak_en("Bonjour, je m'appelle Luna. Je suis l'assistant vocal de Rayan")    
    if "fais-moi une traduction en anglais" in voice_data:
        luna_translate_en = record_audio("Que voulez-vous traduire?")
        luna_speak("Voici la traduction de " + luna_translate_en + " en anglais")
        luna_speak_en(translate_to_english(luna_translate_en))
    if "est-ce que tu te rappelles de moi" in voice_data:
        luna_speak("Comment pourrais-je oublier mon créateur? Ce serait très égoïste de ma part!")
    if "qui t'a créé" in voice_data:
        luna_speak("Mon créateur s'appelle Rayan. C'est quelqu'un de très sympa, dont tout le monde devrait être fier d'avoir dans sa vie")    
    if 'bye' in voice_data or 'au revoir' in voice_data:
        exit()



time.sleep(0.1)        
#luna_speak('Que puis-je faire pour vous?')


while True:
    minute_annoucement = now.strftime("%M")
    secs_annoucement = now.strftime("%S")
    print(minute_annoucement)
    print(secs_annoucement)
    if minute_annoucement == 2 and secs_annoucement == 00:
        luna_speak("Il est " + now.strftime("%H:%M"))
    voice_data = record_audio()
    respond(voice_data)

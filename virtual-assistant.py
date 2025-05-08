import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import warnings
import calendar
import random
import wikipedia

from wmi import WMI
from pynput.keyboard import Key, Controller
from playsound import playsound
import subprocess


#ignore warnings
warnings.filterwarnings('ignore')

#records audio and returns a string
def record_audio():
    r = sr.Recognizer()

    #start recording mic
    with sr.Microphone() as source:
        print('Say something.')
        audio = r.listen(source)

    data = ''
    try:
        data = r.recognize_google(audio)
        print('You said: ' + data)
    except sr.UnknownValueError:
        print('Audio was not understandable.')
    except sr.RequestError as e:
        print('Request error: ' + e)

    return data



#creates audio from text string
def assistant_response(text):
    print(text)
    if os.path.exists('assistant_response.mp3'):
        os.remove('assistant_response.mp3')

    #lang is language
    myobj = gTTS(text= text, lang= 'en', slow= False)
    myobj.save('assistant_response.mp3')

    playsound('assistant_response.mp3')
    os.remove('assistant_response.mp3')



#returns true if text string is a wake word
def wake_word(text):
    WAKE_WORDS = ['fred']
    text = text.lower()

    for phrase in WAKE_WORDS:
        if phrase in text:
            return True

    return False



#get the current date
def get_date():
    now = datetime.datetime.now()
    weekday = calendar.day_name[now.weekday()]
    month_num = now.month
    day_num = now.day

    if 4 <= day_num <= 20 or 24 <= day_num <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day_num % 10 - 1]

    return 'Today is ' + weekday + ', ' + calendar.month_name[month_num] + ' the ' + str(day_num) + suffix + '.'



#returns the current time
def get_time():
    now = datetime.datetime.now()
    time = now.strftime("%H:%M %p")

    return 'It is ' + time + '.'



#returns today's weather
def get_weather():


    return ''



#answers a greeting if it reads a greeting
def greeting(text):
    GREETING_INPUTS = ['hello', 'hey']
    GREETING_RESPONSES = ['Howdy', 'Hey there']

    for word in text.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES) + '.'

    return ''



#gets person first and last name from text: ..... who is blah blah
def get_person(text):
    wordList = text.split()

    for i in range(0, len(wordList)):
        if i + 3 < len(wordList) and wordList[i].lower() == 'who' and wordList[i+1].lower() == 'is':
            return wordList[i+2] + ' ' + wordList[i+3]



#get sentences_num first lines of persons wiki page
def get_wiki(person, sentences_num):
    wiki = wikipedia.summary(person, sentences= sentences_num, auto_suggest=False)

    return wiki



#opens valorant and logs in
def open_game1():
    subprocess.Popen('cd C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Riot Games & VALORANT.lnk', shell= True)
    keyboard = Controller()
    f = WMI()
    flag = True

    while flag:
        for process in f.Win32_Process():
            if process.Name == 'RiotClientUx.exe':
                flag = False
                break

    keyboard.type('user')
    keyboard.press(Key.tab)
    keyboard.type('pass')
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

    return 'Opened.'


#the real program starts here
while True:
    text = record_audio()
    response = ''

    if wake_word(text):
        response = response + greeting(text)

        if 'date' in text:
            get_date = get_date()
            response = response + ' ' + get_date

        if 'time' in text:
            get_time = get_time()
            response = response + ' ' + get_time

        if 'morning' in text or 'weather' in text:
            get_weather = get_weather()
            response = response + ' ' + get_weather

        if 'open' in text and 'Game 1' in text:
            open_game1 = open_game1()
            response = response + ' ' + open_game1

        if 'who is' in text:
            person = get_person(text)
            wiki = get_wiki(person, 2)
            response = response + ' ' + wiki


        if response:
            assistant_response(response)



























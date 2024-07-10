import pyttsx3
import speech_recognition 
import requests
from bs4 import BeautifulSoup
import datetime
import re
import os
from pynput import keyboard
import pyautogui
import pygame
import pywhatkit as kit
from requests import get
import webbrowser
import cv2
import pyjokes
import time
import pygame.mixer as mixer
from plyer import notification
import speedtest






engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
rate = engine.setProperty("rate",170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source,0,4)

    try:
        print("Understanding..")
        query  = r.recognize_google(audio,language='en-in')
        print(f"You Said: {query}\n")
    except Exception as e:
        print("Say that again")
        return "None"
    return query
def get_user_input(prompt):
    speak(prompt)
    user_input = takeCommand()
    if user_input == "":
        user_input = input(f"{prompt}: ")
    return user_input
def get_weather(city):
    api_key = "7b3d80c179c0302279cb3b888ea2125c"  
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    
    response = requests.get(complete_url)
    data = response.json()
    
    if data["cod"] != "404":
        main = data["main"]
        wind = data["wind"]
        weather = data["weather"]
        temp = main["temp"]
        humidity = main["humidity"]
        wind_speed = wind["speed"]
        description = weather[0]["description"]
        rain_chance = "not available"

        if "rain" in data:
            rain_chance = data["rain"]

        weather_info = f"Temperature: {temp}°C, Humidity: {humidity}%, Wind Speed: {wind_speed} m/s, Description: {description}, Rain: {rain_chance}"
        return weather_info
    else:
        return "City Not Found"

def alarm(query):
    timehere = open("Alarmtext.txt","a")
    timehere.write(query)
    timehere.close()
    os.startfile("alarm.py")

def play_song(song_path):
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()

def handle_music_commands(songs, current_song_index):
    recognizer = speech_recognition.Recognizer()
    while True:
        try:
            print("Enter command (next, prev, stop) or say it:")
            with speech_recognition.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio).strip().lower()
                print(f"Voice command recognized: {command}")
        except speech_recognition.UnknownValueError:
            command = input("Voice not recognized. Please enter command (next, prev, stop): ").strip().lower()
        except speech_recognition.RequestError:
            command = input("Could not request results. Please enter command (next, prev, stop): ").strip().lower()
        except speech_recognition.WaitTimeoutError:
            command = input("Listening timed out. Please enter command (next, prev, stop): ").strip().lower()

        if command == "next":
            current_song_index = (current_song_index + 1) % len(songs)
        elif command == "prev":
            current_song_index = (current_song_index - 1) % len(songs)
        elif command == "stop":
            pygame.mixer.music.stop()
            break
        else:
            print("Invalid command.")
            continue
        
        song_path = os.path.join(music_direc, songs[current_song_index])
        play_song(song_path)
        print(f"Now playing: {songs[current_song_index]}")

if __name__ == "__main__":
    while True:
        query = takeCommand().lower()
        if "hello jarvis" in query:
            from GreetMe import greetMe
            greetMe()

            while True:
                query = takeCommand().lower()
                if "go to sleep" in query:
                    speak("Ok sir , You can me call anytime")
                    break 
                elif "hello" in query:
                    speak("Hello sir, how are you ?")
                elif "i am fine" in query:
                    speak("that's great, sir")
                elif "how are you" in query:
                    speak("Perfect, sir")
                elif "thank you" in query:
                    speak("you are welcome, sir")
                elif "google" in query:
                    from SearchNow import searchGoogle
                    searchGoogle(query)
                elif "youtube" in query:
                    from SearchNow import searchYoutube
                    searchYoutube(query)
                elif "wikipedia" in query:
                    from SearchNow import searchWikipedia
                    searchWikipedia(query)
                elif "temperature" in query or "weather" in query:
                    city_match = re.search(r"(in|of|at)\s+([a-zA-Z\s]+)", query)
                    if city_match:
                        city = city_match.group(2).strip()
                        try:
                            weather_info = get_weather(city)
                            speak(f"Current weather in {city} is {weather_info}")
                        except Exception as e:
                            speak(f"Sorry, I couldn't get the weather for {city}")
                    else:
                        speak("Please specify a city to get the weather information.")
                elif "the time" in query:
                    strTime = datetime.datetime.now().strftime("%H:%M")    
                    speak(f"Sir, the time is {strTime}")
                elif "open" in query:
                    from Dictapp import openappweb
                    openappweb(query)
                elif "close" in query:
                    from Dictapp import closeappweb
                    closeappweb(query)
                elif "set an alarm" in query:
                    print("input time example:- 10 and 10 and 10")
                    speak("Set the time")
                    a = input("Please tell the time :- ")
                    alarm(a)
                    speak("Done,sir")
                elif "pause" in query:
                    pyautogui.press("k")
                    speak("video paused")
                elif "play" in query:
                    pyautogui.press("k")
                    speak("video played")
                elif "mute" in query:
                    pyautogui.press("m")
                    speak("video muted")
                elif "volume up" in query:
                    from keyboard import volumeup
                    speak("Turning volume up,sir")
                    volumeup()
                elif "volume down" in query:
                    from keyboard import volumedown
                    speak("Turning volume down, sir")
                    volumedown()
                elif "remember that" in query:
                    rememberMessage = query.replace("remember that", "").replace("jarvis", "").strip()
                    speak(f"You told me to remember that {rememberMessage}")
                    with open("Remember.txt", "a") as file:
                        file.write(rememberMessage + "\n")
                elif "what do you remember" in query:
                    try:
                        with open("Remember.txt", "r") as file:
                            remembered = file.readlines()
                            if remembered:
                                speak("You told me to remember the following:")
                                for item in remembered:
                                    speak(item.strip())
                            else:
                                speak("I don't seem to remember anything.")
                    except FileNotFoundError:
                        speak("I don't seem to remember anything.")
                elif "news" in query:
                    from News import latestnews
                    latestnews()
                elif "calculate" in query:
                    from Calculate import WolfRamAlpha
                    from Calculate import Calc
                    query = query.replace("calculate","")
                    query = query.replace("jarvis","")
                    Calc(query)
                elif "whatsapp" in query:
                    from Whatsapp import sendMessage
                    sendMessage()
                elif "music" in query:
                    music_direc = "D:\\MI\\Ext"
                    songs = [song for song in os.listdir(music_direc) if song.endswith('.mp3')]
                    
                    if not songs:
                        print("No songs found in the directory.")
                    else:
                        pygame.mixer.init()
                        current_song_index = 0
                        play_song(os.path.join(music_direc, songs[current_song_index]))
                        print(f"Now playing: {songs[current_song_index]}")
                        
                        handle_music_commands(songs, current_song_index)
                        
                        pygame.mixer.quit() 
                elif "ip address"in query:
                    ip = get('https://api.ipify.org').text
                    speak(f"Your ip address is {ip}")
                elif "facebook" in query:
                    webbrowser.open("https://facebook.com")
                
                elif "instagram" in query:
                    webbrowser.open("https://instagram.com")
                
                elif "linkedin" in query:
                    webbrowser.open("https://linkedin.com")

                elif "stack overflow" in query:
                    webbrowser.open("https://www.stackoverflow.com")
                elif "open camera" in query:
                    cap  = cv2.VideoCapture(0)
                    while True:
                        ret, img = cap.read()
                        cv2.imshow('webcam ',img)
                        k = cv2.waitKey(50)
                        if k ==27:
                            break
                    cap.release()
                    cv2.destroyAllWindows()
                # elif "click my photo" in query:
                #     pyautogui.press("super")
                #     pyautogui.typewrite("camera")
                #     pyautogui.press("enter")
                #     pyautogui.sleep(2)
                #     speak("SMILE")
                #     pyautogui.press("enter")
                #to find a joke
                elif "tell me a joke" in query:
                    joke = pyjokes.get_joke()
                    speak(joke)
                
                elif "shutdown my laptop" in query:
                    os.system("shutdown /s /t 5")
                elif "restart my laptop" in query:
                    os.system("shutdown /r /t 5")
                
                elif 'switch the windows' in query:
                    pyautogui.keyDown("alt")
                    pyautogui.press("tab")
                    time.sleep(1)
                    pyautogui.keyup("alt")
                elif "schedule my day" in query:
                    tasks = [] #Empty list 
                    speak("Do you want to clear old tasks (Plz speak YES or NO)")
                    query = takeCommand().lower()
                    if "yes" in query:
                        file = open("tasks.txt","w")
                        file.write(f"")
                        file.close()
                        no_tasks = int(input("Enter the no. of tasks :- "))
                        i = 0
                        for i in range(no_tasks):
                            tasks.append(input("Enter the task :- "))
                            file = open("tasks.txt","a")
                            file.write(f"{i}. {tasks[i]}\n")
                            file.close()
                    elif "no" in query:
                        i = 0
                        no_tasks = int(input("Enter the no. of tasks :- "))
                        for i in range(no_tasks):
                            tasks.append(input("Enter the task :- "))
                            file = open("tasks.txt","a")
                            file.write(f"{i}. {tasks[i]}\n")
                            file.close()
                elif "show my schedule" in query:
                    file = open("tasks.txt","r")
                    content = file.read()
                    file.close()
                    mixer.init()
                    mixer.music.load("notification.mp3")
                    mixer.music.play()
                    notification.notify(
                        title = "My schedule :-",
                        message = content,
                        timeout = 15
                        )
                elif "internet speed" in query:
                    wifi  = speedtest.Speedtest()
                    upload_net = wifi.upload()/1048576         
                    download_net = wifi.download()/1048576
                    print("Wifi Upload Speed is", upload_net)
                    print("Wifi download speed is ",download_net)
                    speak(f"Wifi download speed is {download_net}")
                    speak(f"Wifi Upload speed is {upload_net}")
                elif "screenshot" in query:
                     import pyautogui 
                     im = pyautogui.screenshot()
                     im.save("ss.jpg")
                
                elif "sleep" in query:
                    speak("Thanks for using me sir...")
                    speak("Going to sleep")
                    exit()
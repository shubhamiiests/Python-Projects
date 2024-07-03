import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
import random
import pygame
import time
import requests
from requests import get
import wikipedia
import webbrowser
import pywhatkit as kit
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys
import pyjokes
import pyautogui


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[0].id)
engine.setProperty('voices',voices[len(voices) -1 ].id)

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=1, phrase_time_limit=5)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start")
            return ""
        except sr.UnknownValueError:
            print("Could not understand audio")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return ""
    return query

def get_user_input(prompt):
    speak(prompt)
    user_input = takecommand()
    if user_input == "":
        user_input = input(f"{prompt}: ")
    return user_input

def wish():
    hour = int(datetime.datetime.now().hour)
    tt= time.strftime("%I:%M %p")


    if hour>=0 and hour<=12:
        speak(f"Good Morning, its {tt}")
    elif hour>12 and hour<18:
        speak(f"Good Afternoon, its {tt}")
    else:
        speak(f"Good Evening, its {tt}")
    speak("I am Jarvis. Please tell me How can I help you Sir?")

def play_song(song_path):
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()

def handle_music_commands(songs, current_song_index):
    recognizer = sr.Recognizer()
    while True:
        try:
            print("Enter command (next, prev, stop) or say it:")
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio).strip().lower()
                print(f"Voice command recognized: {command}")
        except sr.UnknownValueError:
            command = input("Voice not recognized. Please enter command (next, prev, stop): ").strip().lower()
        except sr.RequestError:
            command = input("Could not request results. Please enter command (next, prev, stop): ").strip().lower()
        except sr.WaitTimeoutError:
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

def send_email(recipient, subject, body):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        # No need to enter email and password if already logged in Gmail
        # server.login("your_email", "your_password")
        server.sendmail("your_email", recipient, f"Subject: {subject}\n\n{body}")
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def set_alarm():
    speak("Please enter the hour for the alarm (24-hour format)")
    hour = takecommand()
    if hour == "":
        hour = input("Please type the hour for the alarm (24-hour format): ")
    hour = int(hour)

    speak("Please enter the minute for the alarm")
    minute = takecommand()
    if minute == "":
        minute = input("Please type the minute for the alarm: ")
    minute = int(minute)

    now = datetime.datetime.now()
    alarm_time = datetime.datetime(now.year, now.month, now.day, hour, minute)

    while True:
        now = datetime.datetime.now()
        if now >= alarm_time:
            speak("Alarm time reached!")
            music_dir = 'D:\\MI\\Ext'
            songs = [song for song in os.listdir(music_dir) if song.endswith('.mp3')]
            if songs:
                os.startfile(os.path.join(music_dir, songs[0]))
            else:
                speak("No music files found to play.")
            break

if __name__ == "__main__":
    #takecommand()
    #speak("this is Jarvis")
    wish()
    while True: #for running infinte times
    #if 1: for running only 1 time

        query = takecommand().lower()

        #logic building for task

        if "open notepad" in query:
            npath ="C:\\Windows\\notepad.exe"
            os.startfile(npath)
        elif "close notepad" in query:
            speak("okay sir,closing notepad")
            os.system("taskkill /f /im notepad.exe")
        
        elif "open chrome" in query:
            cpath ="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            os.startfile(cpath)
        elif "close chrome" in query:
            speak("okay sir,closing chrome")
            os.system("taskkill /f /im chrome.exe")
        
        elif "open edge" in query:
            epath = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
            os.startfile(epath)
        elif "close edge" in query:
            speak("okay sir,closing edge")
            os.system("taskkill /f /im msedge.exe")
        
        elif "open vs Code" in query:
            vpath = "C:\\Users\\skshu\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(vpath)
        elif "close vs code" in query:
            speak("okay sir,closing vs code")
            os.system("taskkill /f /im Code.exe")

        elif "open file explorer" in query:
            expath = "C:\\Windows\\explorer.exe"
            os.startfile(expath)
        elif "close explorer" in query:
            speak("okay sir,closing explorer")
            os.system("taskkill /f /im explorer.exe")
        
        elif "open command prompt" in query:
            os.system("start cmd")

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

        elif "play music" in query:
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
        
        elif "wikipedia" in query:
            speak("Searching wikipedia...")
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query, sentences = 3)
            speak("According to Wikipedia")
            speak(results)
            #print(results)
        
        elif "open youtube" in query:
            webbrowser.open("https://www.youtube.com")
        
        elif "open google" in query:
            speak("sir, what should i search on google")
            search = takecommand().lower()
            webbrowser.open(f"https://www.google.com/search?q={search}")

        elif "open facebook" in query:
            webbrowser.open("https://facebook.com")
        
        elif "open instagram" in query:
            webbrowser.open("https://instagram.com")
        
        elif "open linkedin" in query:
            webbrowser.open("https://linkedin.com")

        elif "open stack overflow" in query:
            webbrowser.open("https://www.stackoverflow.com") 
        
        if "send message" in query:
            speak("Sir, please provide the phone number")
            phone_number = takecommand()
            if phone_number == "None":
                phone_number = input("Please type the phone number: ")
        
            speak("What is the message?")
            message = takecommand()
            if message == "None":
                message = input("Please type the message: ")
            
            # Sanitize phone number (add country code if missing)
            if not phone_number.startswith("+91"):
                phone_number = f"+91{phone_number}"
            
            hour = int(input("Please enter the hour (24-hour format): "))
            minute = int(input("Please enter the minute: "))

            kit.sendwhatmsg(phone_number, message, hour, minute)

        elif "play song on youtube" in query:
            song = get_user_input("Sir, what song would you like to play on YouTube?")
            if song != "None":
                kit.playonyt(song)
        
        elif "send email" in query:
            recipient = get_user_input("To whom do you want to send the email?")
            if recipient != "None":
                subject = get_user_input("What is the subject of the email?")
                if subject != "None":
                    body = get_user_input("What message would you like to send?")
                    if body != "None":
                        send_email(recipient, subject, body)
        
        elif "set alarm" in query:
            set_alarm()
        
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
        
        elif "exit" in query:
            speak("Thanks for using me Sir, Have a Good Day.")
            sys.exit()
        
        
      


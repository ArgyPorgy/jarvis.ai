import json
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, PhotoImage
from tkinter import *
from PIL import Image, ImageTk
import pyttsx3
import webbrowser
import threading
import speech_recognition as sr
import openai
import pandas as pd
import requests
import random
import time
from autoYT import play
import sys
import tweepy
import os
import win32api
from takpic import take_picture
from web3 import Web3
from datetime import datetime
# import pywhatkit as wp
from plyer import notification
import winsound
from pymongo import MongoClient
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import ast
from cctv import cctv
from addtocart import add_to_wishlist
from aitrainer import biceps
import cv2
import mediapipe as mp
import numpy as np




start_time = time.time()
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)
listening_enabled = False


load_dotenv()
api_key = os.environ.get("WEATHER_API_KEY")
news_api_key = os.environ.get("news_api_key")
openAPI = os.getenv('openai_api_key')
openai.api_key=openAPI
food_data = pd.read_csv('food.csv')
def get_command(command): 
    if "assistant" in command:
        command = command.split("assistant")[1].strip()
    elif "jarvis" in command:
        command = command.split("jarvis")[1].strip()
    return command

def set_volume(volume):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume_interface = cast(interface, POINTER(IAudioEndpointVolume))
    volume_interface.SetMasterVolumeLevelScalar(volume, None)

def music(command):
    command = command.lower()
    if "play" in command:
        command = command.replace("play", '')
    engine.say("Fetching data")
    engine.runAndWait()
    change_border_color()
    output_text.insert(tk.END, "\nFetching Data...\n")
    # animate_border()
    # wp.playonyt(command)
    play(command)
    engine.say("Playing on your device")
    engine.runAndWait()

def start_listening():
    global listening_enabled
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        while listening_enabled:  # Check if listening is still enabled
            output_text.insert(tk.END, "Listening...\n")
            try:
                recognizer.pause_threshold= 1 #new 
                audio = recognizer.listen(source, timeout=10)
                command = recognizer.recognize_google(audio)
                output_text.insert(tk.END, f"You said: {command}\n")
                change_border_color()
                if 'assistant' in command.lower() or "jarvis" in command.lower():
                    # recognizer.pause_threshold= 1 #new 
                    change_border_color()
                    # engine.say("Hello!")
                    # engine.runAndWait()
                    command = get_command(command.lower())

                    if "can you hear" in command.lower():
                        engine.say("Yes i can hear you!")
                        engine.runAndWait()
                        output_text.insert(tk.END, "Yes i can hear you!\n")
                    elif "what can you do" in command or "what are your features" in command:
                        output_text.insert(tk.END,"these are all my features.")
                        engine.say("these are all my features.")
                        engine.runAndWait()
                        show_help()
                    elif "ip" in command.lower():
                        ip=ipadd()
                        engine.say(ip)
                        output_text.insert(tk.END, f"{ip}\n")
                        engine.runAndWait()
                    elif "who made you" in command.lower():
                        output_text.insert(tk.END, "I was made by the Team 'THE BOYS'. \nClick the contributors option in the menu tab for more info.\n")
                        change_background_image()
                        engine.say("I was made by the team THE BOYS")
                        engine.runAndWait()
                    
                    elif "reminder" in command.lower() or "alarm" in command.lower():
                        output_text.insert(tk.END, "Setting reminder...\n")
                        engine.say("Setting reminder")
                        engine.runAndWait()
                        # reminder(command.lower())
                        noti = threading.Thread(target=reminder, args=(command.lower(),))
                        noti.start()
                        start_listening()
                        noti.join()
                        # engine.runAndWait()
                    elif "location" in command.lower() or "where am i" in command.lower():
                        locationcurrent = get_location()
                        engine.say(locationcurrent)
                        output_text.insert(tk.END, f"{locationcurrent}\n")
                        webbrowser.open("https://www.google.com/maps/place/" + locationcurrent, new=1, autoraise=True)
                        engine.runAndWait()
                    elif "take a picture" in command.lower():
                        output_text.insert(tk.END, "Smile Please!\n")
                        engine.say("Say Cheese!")
                        engine.runAndWait()
                        take_picture()
                    elif "play" in command.lower() or "song" in command.lower():
                        music(command)
                    elif "volume" in command.lower():
                        try:
                            command = command.replace("volume", "")
                            if "full" in command.lower():
                                set_volume(1)
                            elif "mute" in command.lower():
                                set_volume(0)
                            else:
                                set_volume(int(command)/10)
                        except Exception:
                            output_text.insert(tk.END, "couldn't perform that operation")
                    elif command == "":
                        engine.say("Hello")
                        engine.runAndWait()
                        output_text.insert(tk.END, "Hello, nice to meet you!\n")
                    elif "shutdown" in command.lower():
                        engine.say("Shutting Down, Good bye !!")
                        engine.runAndWait()
                        output_text.insert(tk.END, "Shutting Down, Good bye !!\n")
                        shutdown()
                        engine.runAndWait()
                    elif "who" in command.lower() or "wikipedia" in command.lower() :
                        resp = searchWiki(command)
                        output_text.insert(tk.END, f"According to Wikipedia -> \n {resp}")
                        resp = "according to wikipedia, "+resp

                        engine.say(resp)
                        engine.runAndWait()
                    elif "news" in command.lower():
                        output_text.insert(tk.END, "Fetching news...\n")
                        engine.say("fetching news")
                        engine.runAndWait()
                        news(command.lower())
                    elif "schedule" in command.lower():
                        eventcalendar(command)   
                    elif "weather" in command.lower() or "temperature" in command.lower():
                        weather(command.lower())
                        engine.runAndWait()
                    elif "thank" in command.lower() or "thank you" in command.lower() or "thanks" in command.lower():
                        engine.say("I am glad to help you. Let me know if you want anything else.")
                        output_text.insert(tk.END, "Welcome...\n")
                        engine.runAndWait()
                    elif "connect cctv" in command.lower():
                        engine.say("Trying a connection...")
                        engine.runAndWait()
                        try:
                            cctv()
                            engine.say("successfuly connected")
                            engine.runAndWait()
                        except Exception as e:
                            engine.say("An error occurred!") 
                            engine.runAndWait()

                    elif "tweet" in command.lower():
                        while True:
                            # recognizer = sr.Recognizer()
                            engine.say("What do you want to tweet?\n")
                            engine.runAndWait()

                            with sr.Microphone() as sou:
                                recognizer.adjust_for_ambient_noise(sou)
                                output_text.insert(tk.END, "What do you want to tweet?")
                                
                                try:
                                    audio = recognizer.listen(sou, timeout=10)
                                    matter = recognizer.recognize_google(audio)
                                    output_text.insert(tk.END, f"Your message: {matter}\n")
                                    matter+=' @diversion2k24'
                                    tweet_py(matter)
                                    break

                                except sr.UnknownValueError:
                                    output_text.insert(tk.END, "Sorry, could not understand audio. Please say again: ")
                                    continue

                                except Exception as e:
                                    output_text.insert(tk.END, "Could not process the tweet! ")
                                    break
                            

                                


                        
                     
                        
                    elif "deactivate" in command.lower():
                        output_text.insert(tk.END, "Sayonara!\n")
                        engine.say("See you soon again! Sayonara...")
                        engine.runAndWait()
                        terminate()
                    elif "translate" in command.lower():
                        resp = translate(command)
                        output_text.insert(tk.END, resp)
                        engine.say(f"{resp}")
                        engine.runAndWait()

                    elif "calories" in command.lower():
                        food_item=command.lower()
                        food_items = [food.strip() for food in food_item.split('and')]
                        for food_item in food_items:
                                get_calories(food_item)
                        calculate_total_calories(food_items)


                    elif "joke" in command.lower():
                        joke = get_dad_joke()
                        output_text.insert(tk.END, joke)
                        engine.say(joke)
                        engine.runAndWait()

                    elif "biceps" in command.lower():
                        engine.say("Jarvis Gym mode activated..")
                        engine.say("Press 'q' to stop") 
                        engine.runAndWait()
                        output_text.insert(tk.END, "Press 'q' to stop \n")
                        biceps()
    
                        
                        


                        

                    elif "wishlist" in command.lower():
                        add_to_wishlist(command) 
                        engine.say("added to wishlist successfully")  
                        engine.runAndWait()

                    elif "study mode" in command.lower():
                        engine.say("initiating study mode")
                        # engine.runAndWait()
                        start_study_mode()
                    else:
                        resp = chat_gpt(command)
                        output_text.insert(tk.END, f"\n {resp}\n")
                        resp = "According to Chat GPT, "+ resp
                        engine.say(resp)
                        engine.runAndWait()
                    
            except sr.UnknownValueError:
                output_text.insert(tk.END, "Sorry, could not understand audio.\n")
                # engine.say("Sorry, could not understand audio.")
                # engine.runAndWait()
            except sr.WaitTimeoutError:
                handle_wait_timeout_error()

def handle_wait_timeout_error():
    global listening_enabled
    listening_enabled = False  # Set the flag to stop listening
    message = "Timeout. Please try pressing the Activate button again."
    output_text.insert(tk.END, message)
    engine.say(message)
    engine.runAndWait()
    terminate()

def terminate():
    global listening_enabled
    listening_enabled = False  # Set the flag to stop listening
    message = "Your assistant is deactivated successfully"
    output_text.insert(tk.END, "Deactivated...\n")
    engine.say(message)
    engine.runAndWait()

    terminate_button.pack_forget()
    activate_button.pack(pady=(10,10))

food_data = pd.read_csv('food.csv')

def get_calories(food_item):
    # Check if the food item is in the loaded CSV data
    if food_item.lower() in food_data['Food'].str.lower().values:
        # Retrieve the calories for the given food item
        calories = food_data.loc[food_data['Food'].str.lower() == food_item.lower(), 'Calories'].values[0]
        return calories
    else:
        return None
    
def searchWiki(query):
    import pywhatkit as wp
    result = wp.info(query, lines = 2, return_value=True)
    return result

def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle

def get_dad_joke():
    url = "https://icanhazdadjoke.com/"
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        joke_data = response.json()
        joke = joke_data["joke"]
        return joke
    else:
        return "Failed to retrieve dad joke."
        
def translate(command):
    tranProm = f"""
    I will provide you a text and translate it to me in english
    {command}
    """
    resp = chat_gpt(tranProm)
    return resp

SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Set OpenAI API key
load_dotenv()

# Get the OpenAI API key from the environment variables
openai_api_key = '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'

# Set the OpenAI API key
openai.api_key = openai_api_key

eventex = {
    'summary': 'Google I/O ',
    'location': '800 Howard St., San Francisco, CA 94103',
    'description': 'A chance to hear more about Google\'s developer products.',
    'start': {
        'dateTime': '2024-01-19T09:00:00+05:30',  # Corrected timezone offset
        'timeZone': 'Asia/Kolkata',
    },
    'end': {
        'dateTime': '2024-01-19T17:00:00+05:30',  # Corrected timezone offset
        'timeZone': 'Asia/Kolkata',
    },
    'recurrence': [
        'RRULE:FREQ=DAILY;COUNT=2'
    ],
    'attendees': [
        {'email': 'carghya10@gmail.com'},
    ],
    'reminders': {
        'useDefault': False,
        'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 10},
        ],
    },
}

# gpt_calendar_response = {}



def eventcalendar(command):
    global gpt_calendar_response
    engine.say("Can you tell me more about the event?")
    engine.runAndWait()
    output_text.insert(tk.END, "\nCan you tell me more about the event?\n")
    

    while True:
        user_input = command.lower()
        

        calendarprompt = f'''i want you to write me the details of the event using the following context : {user_input}. You must write the details in a similar format like it is written in {eventex} strictly. No matter what, stick to the original format given in {eventex}. Keep recurrence the same as given in {eventex}. If there is some context missing in {user_input}, keep those particular parts the same as {eventex}. Under any condition, DO NOT keep any value blank or change anything in the original format given in {eventex}.'''
        gpt_calendar_response = chat_gpt(calendarprompt)
        # print(gpt_calendar_response)
        aicalendar()
        engine.say("Your meeting is scheduled.")
        engine.runAndWait()
        output_text.insert(tk.END, "\nYour meeting is scheduled.\n")

def aicalendar():
    global gpt_calendar_response  # Declare as global
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)
        try:
            event = ast.literal_eval(gpt_calendar_response)
        except (ValueError, SyntaxError) as e:
            print(f"Error evaluating the dictionary: {e}")
            return
        print(event)
        event = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Event created: {event.get('htmlLink')}")

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        print("Getting the upcoming 10 events")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(start, event["summary"])

    except HttpError as error:
        print(f"An error occurred: {error}")


def change(t, extra):
    time_parts = t.split(':')    
        # Convert hours and minutes to minutes
    if len(time_parts) == 2:
        hours, minutes = map(int, time_parts)
        total_minutes = hours * 60 + minutes + extra
    # Convert hours, minutes, and seconds to minutes
    elif len(time_parts) == 3:
        hours, minutes, seconds = map(int, time_parts)
        total_minutes = hours * 60 + minutes + seconds / 60 + extra
    else:
        raise ValueError("Invalid time format")
    return total_minutes
def timdif(command):
    extra = 0
    if "a.m." in command:
        t = command.split("a.m.")[0].strip()
    elif 'p.m.' in command:
        t = command.split("p.m.")[0].strip()
        extra = 12 * 60
    else:
        t = command
    now = datetime.now()
    timestamp = now.strftime("%H:%M:%S")
    ctime = change(timestamp, 0)
    gtime = change(t, extra)
    min = gtime - ctime
    return min*60

def reminder(command):
    if "regarding" in command:
        matter = command.split("regarding")[1].strip()
        command = command.split("regarding")[0].strip()
    elif "for" in command:
        matter = command.split("for")[1].strip()
        command = command.split("for")[0].strip()
    else:
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            output_text.insert(tk.END, "Please tell me your event message: \n")
            # engine.say("Please tell me your event message")
            try:
                audio = recognizer.listen(source, timeout=10)
                matter = recognizer.recognize_google(audio)
                output_text.insert(tk.END, f"Your message: {matter}\n")
            except sr.UnknownValueError:
                output_text.insert(tk.END, "Sorry, could not understand audio.\n")
                return ""
            except sr.RequestError as e:
                print(
                    f"Could not request results from Google Speech Recognition service; {e}"
                )
                return ""
    t = timdif(command.split("at")[1].strip())
    time.sleep(t)
    
    notification.notify(title="REMINDER", message=matter, app_name="Notifier", app_icon="ico.ico", toast=True, timeout=20)
    i=0
    while(i==5):
        winsound.Beep(4000, 1000)
        i+=1


def news(command):
    categories = ["business", "entertainment", "health", "science", "sports", "technology"]
    category = "General"
    for i in categories:
        if i in command:
            category = i
            break
    category = category.capitalize()
    news_url = f"https://newsapi.org/v2/top-headlines?country=in&category={category}&apiKey={news_api_key}"
    try:
        response = requests.get(news_url)
        news_data = response.json()
        if news_data["status"] == "ok":
            articles = news_data["articles"]
            news_text = f"Here are the latest {category} headlines:\n\n"
            engine.say(news_text)
            engine.runAndWait()
            output_text.insert(tk.END, news_text)
            for index, article in enumerate(articles, start=1):
                if( index > 5):
                    break
                if({article['title']}=="Removed" or article['description'] is None):
                    index = index-1
                    continue
                else:
                    news_text = f"{index}. {article['title']}:\n{article['description']}\n\n"
                    output_text.insert(tk.END, news_text)
                    # print(news_data)
                    engine.say(f"News number{index} is {article['title']}")
                    engine.runAndWait()
        else:
            return f"Error fetching {category} news. Please try again later."
    except Exception as e:
        return f"An error occurred: {str(e)}"
def weather(command):
    city = extract_city_name(command)
    if city:
        weather_data = get_weather_data(city)
        engine.say(weather_data)  # Speak the weather details
        output_text.insert(tk.END, f"Weather in {city.capitalize()}: \n{weather_data}\n")
        engine.runAndWait()
    else:
        output_text.insert(tk.END, "Location not recognized.\n")
        engine.say("Location not recognized")

def extract_city_name(command):
    city = None
    if "in" in command:
        city = command.split("in")[1].strip()
    elif "of" in command:
        city = command.split("of")[1].strip()
    return city

def get_weather_data(city):
    base_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

    try:
        response = requests.get(base_url)
        data = response.json()

        temperature = data['main']['temp']
        # humidity = data['main']['humidity']
        # wind_speed = data['wind']['speed']
        weather_description = data['weather'][0]['description']

        result = (
            f"Temperature: {round(temperature - 273.15, 2)} °C\n"
            # f"Humidity: {humidity}%\n"
            # f"Wind Speed: {wind_speed} m/s\n"
            f"Description: {weather_description.capitalize()}"
        )
        return result

    except Exception as e:
        return f"Error fetching weather data: {e}"


def chat_gpt(prompt):
     response = openai.ChatCompletion.create(
         model="gpt-3.5-turbo",
         messages=[
             {"role": "user", "content": prompt}
         ]
     )

     chatgpt_response = response.choices[0].message['content']
     return chatgpt_response

def shutdown():
    if sys.platform.startswith('win'):
        # Windows shutdown command
        shutdown_command = "shutdown /s /t 1"
    elif sys.platform.startswith('linux') or sys.platform == 'darwin':
        # Linux shutdown command
        shutdown_command = "shutdown -h now"
    else:
        print("Unsupported operating system.")
        return False
    try:
        os.system(shutdown_command)
        return True
    except Exception as e:
        print(f"Error executing shutdown command: {e}\n")
        return False

def get_location():
    r = requests.get('https://get.geojs.io/')
    ip=requests.get('https://get.geojs.io/v1/ip.json')
    ipadd=ip.json()['ip']
    url='https://get.geojs.io/v1/ip/geo/'+ipadd+'.json'

    geoo_req= requests.get(url)
    geo_data = geoo_req.json()
    location=("Your location is " + geo_data['city']+","+geo_data['region']+","+geo_data['country'])
    return location

def ipadd():
    requests.get('https://get.geojs.io/')
    ip=requests.get('https://get.geojs.io/v1/ip.json')
    ipadd=ip.json()['ip']
    return ipadd

def ask_openai(question):
    # Generate a prompt for OpenAI based on the question
    prompt = f"Tell me the calories of {question}."

    # Use OpenAI API to generate a response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    chatgpt_response = response.choices[0].message['content']
    return chatgpt_response

'''def get_current_time_and_date():
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    current_date = now.strftime("%Y-%m-%d")
    return f"The current time is {current_time} and the date is {current_date}"
'''

def open_application(app_name):
    try:
        win32api.ShellExecute(0, "open", f"{app_name}.exe", None, None, 1)
        engine.say(f"{app_name} opened successfully.")
        engine.runAndWait()

    except:
        engine.say(f"{app_name} Not found in machine go for web version.")
        engine.runAndWait()
        open_web_version(app_name)

def open_web_version(app_name):
    try:
        base_url = "https://{app_name}.com/"
        app_url = base_url.format(app_name=app_name.lower())
        webbrowser.open(app_url)

        engine.say(f"{app_name} opened successfully.")
        engine.runAndWait()

    except Exception as e:
        print(f"An error occurred\n")

def calculate_total_calories(food_items):
    total_calories = 0

    for food_item in food_items:
        calories = get_calories(food_item)
        if calories is not None:
            total_calories += calories
            print(f"{food_item} has {calories} calories.")
        else:
            print(f"Sorry, {food_item} not found in the database.")

    print(f"\nTotal calories for all foods: {total_calories}")

    # Optionally, you can ask OpenAI for a summary or additional information
    question = "Tell me about the nutritional content of the foods."
    answer = ask_openai(question)
    print(f"\nOpenAI says: {answer}")    


#engine.say(message)
#engine.runAndWait()    

def activate_button():
    global listening_enabled
    listening_enabled = True  # Set the flag to start listening
    message = "Hey, your assistant is activated!"
    output_text.insert(tk.END, "Activated...\n")
    engine.say(message)
    engine.runAndWait()

    activate_button.pack_forget()
    terminate_button.pack(pady=(10, 10))
    listen_thread = threading.Thread(target=start_listening)
    listen_thread.start()
    
def restore_initial_image(new_bg_image):
    new_image = Image.open("jarvis.jpg")
    new_image = new_image.resize((750, 500), Image.BICUBIC)
    new_bg_image = ImageTk.PhotoImage(new_image)
    canvas.create_image(0, 0, anchor=tk.NW, image=new_bg_image)

def change_background_image():
    new_image = Image.open("us.png")
    new_image = new_image.resize((750, 500), Image.BICUBIC)
    new_bg_image = ImageTk.PhotoImage(new_image)
    canvas.create_image(0, 0, anchor=tk.NW, image=new_bg_image)
    # canvas.create_text(375, 20, text= "CREATORS OF JARVIS", fill="lightblue", font=("Algerian", 35, 'bold'))
    # canvas.pack(fill="both", expand=True)
    root.after(10000, lambda: restore_initial_image(new_bg_image))


def change_border_color():
    # Generate random RGB values for the border color
    border_color = "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    root.configure(borderwidth=2, highlightthickness=3, relief=tk.SOLID, highlightcolor=border_color)
    # Schedule the function to run again after a delay (e.g., 100 milliseconds)
    if (time.time() - start_time) < 1:
        root.after(500, change_border_color)
    

def show_contributors():
    messagebox.showinfo("Contributors", "Jarvis: The AI Voice Assistant is made by the team - 'The Boys'.\nThe contributors are as follows:\n 1. Arghya Chowdhury \n 2. Devjyoti Banerjee \n 3. Sayan Genri \n 4. Soham De")

def github_link():
    webbrowser.open("https://github.com/ArgyPorgy/test-jarvis.git")

def quit_button():
    root.destroy()

# Welcome message
def welcome_message():
    message = "Welcome! Use your mouth, not your finger! Tap the Activate button to start your personal assistant."
    engine.say(message)
    engine.runAndWait()

def show_help():
    help_window = tk.Toplevel()
    # Calculate the center position of the screen
    screen_width = help_window.winfo_screenwidth()
    screen_height = help_window.winfo_screenheight()
    x_position = (screen_width - 300) // 2  # Adjust the width as needed
    y_position = (screen_height - 300) // 2  # Adjust the height as needed
    help_window.configure(bg = 'lightblue')
    # Set window position and size
    help_window.geometry(f"300x300+{x_position}+{y_position}")
    # Customize the style of the window
    help_window.title("JARVIS - Help Box")
    help_label = scrolledtext.ScrolledText(help_window, wrap=tk.WORD, width=40, height=20, relief=tk.FLAT, bg = 'lightblue')
    help_label.pack(padx=10, pady=10)
    try:
        with open('help.txt', 'r') as file:
            content = file.read()
            help_label.delete('1.0', tk.END)  # Clear existing content
            help_label.insert(tk.END, content)  # Insert new content
    except FileNotFoundError:
        help_label.delete('1.0', tk.END)
        help_label.insert(tk.END, "File not found... ")

def study_mode_data():
    try:
        with open("study_info.json", "r") as file:
            study_data = json.load(file)

        study_data_window = tk.Toplevel(root)
        study_data_window.title("Study Data")
        study_data_window.configure(bg = 'lightblue')
        tree = ttk.Treeview(study_data_window, columns=("Index", "Subject", "Time", "Record"), show = 'headings')
        tree.heading("#1", text="Index")  # Add an index column
        tree.heading("#2", text="Subject")
        tree.heading("#3", text="Duration of study")
        tree.heading("#4", text="Recorded on")
        for index, (subject, time, record) in enumerate(zip(study_data["subject"], study_data["time"], study_data["record"]), start=1):
            tree.insert("", index, values=(index, subject, time, record))
             
        tree.pack(expand=True, fill=tk.BOTH)
        scrollbar = ttk.Scrollbar(study_data_window, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        # Pack the Treeview and Scrollbar
        tree.pack(side=tk.LEFT, fill=tk.Y)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        study_data_window.resizable(False, False)
    except Exception as e:
        print(f"Error reading file: {e}")

def get_gpt_help():
    if not get_gpt_help.has_run:
        get_gpt_help.has_run = True
        webbrowser.open("https://chat.openai.com/")
        chatgpt_button.pack_forget()
get_gpt_help.has_run = False

def start_study_mode():
    global study_mode_enabled, study_start_time
    new_image = Image.open("study.jpg")
    #new_image = Image.open("never.jpg")
    new_image = new_image.resize((750, 500), Image.BICUBIC)
    new_bg_image = ImageTk.PhotoImage(new_image)
    canvas.create_image(0, 0, anchor=tk.NW, image=new_bg_image)
    
    study_mode_enabled = True
    study_start_time = time.time()
    turn_off_study_button.pack(pady=(10, 10))
    chatgpt_button.pack(pady=(10,10))
    # Remove other widgets
    activate_button.pack_forget()
    terminate_button.pack_forget()
    quit_button.pack_forget()
    # output_text.pack_forget()
    
    dt.pack_forget()
    timer_label.pack(pady=(10,10))
    # Ask the user what to study
    engine.say("Welcome to Study Mode! What subject do you want to study?")
    engine.runAndWait()
    # Wait for user input
    subject = listen_and_get_subject()
    # Start the timer
    study_subject = subject
    start_timer(study_subject)

def listen_and_get_subject():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        output_text.insert(tk.END, "Listening for study subject...\n")
        try:
            audio = recognizer.listen(source, timeout=10)
            subject = recognizer.recognize_google(audio)
            output_text.insert(tk.END, f"Subject to study: {subject}\n")
            return subject
        except sr.UnknownValueError:
            output_text.insert(tk.END, "Sorry, could not understand the study subject.\n")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return ""

def start_timer(sub):
    global study_mode_enabled, study_start_time,subj
    subj=sub
    while study_mode_enabled:
        elapsed_time = time.time() - study_start_time
        timer_text = f"Study Mode for {sub} - {int(elapsed_time // 60)} min {int(elapsed_time % 60)} sec"
        timer_label.config(text=timer_text)
        root.update()
        time.sleep(1)

def get_calories(food_item):
    # Check if the food item is in the loaded CSV data
    if food_item.lower() in food_data['Food'].str.lower().values:
        # Retrieve the calories for the given food item
        calories = food_data.loc[food_data['Food'].str.lower() == food_item.lower(), 'Calories'].values[0]
        return calories
    else:
        return None
        

# def ask_openai(question):
#     # Generate a prompt for OpenAI based on the question
#     prompt = f"Tell me the calories of {question}."

#     # Use OpenAI API to generate a response
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "user", "content": prompt}
#         ]
#     )

    # chatgpt_response = response.choices[0].message['content']
    # return chatgpt_response

def calculate_total_calories(food_items):
    total_calories = 0

    for food_item in food_items:
        calories = get_calories(food_item)
        if calories is not None:
            total_calories += calories
            print(f"{food_item} has {calories} calories.")
            engine.say(f"{food_item} has {calories} calories.")
            engine.runAndWait()
        else:
            print(f"Sorry, {food_item} not found in the database.")
    engine.say(f"Total calories for all foods: {total_calories}")
    engine.runAndWait()
    Message = (f"Total calories for all foods: {total_calories}")
    output_text.insert(tk.END, Message)
    

    # Optionally, you can ask OpenAI for a summary or additional information
    # question = "Tell me about the nutritional content of the foods."
    # answer = ask_openai(question)
    # print(f"\nOpenAI says: {answer}")    


def turn_off_study_mode():
    global study_mode_enabled,subj
    study_mode_enabled = False
    # Reset the window to its original state
    # background_label.place_forget()
    turn_off_study_button.pack_forget()
    chatgpt_button.pack_forget()
    # activate_button.pack(pady=(10, 10))
    terminate_button.pack(pady=(10, 10))
    quit_button.pack(pady=10)
    output_text.pack(pady=10)
    # Remove the timer label
    timer_label.pack_forget()
    dt.pack(pady=(10, 10),  anchor=W)
    # Process the study time
    end_time = time.time()
    study_time = int(end_time - study_start_time)
    open("studymodedata.txt", "w").write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {subj} - Studied for {study_time // 60} minutes and {study_time % 60} seconds.")
    try:
        with open('study_info.json', 'r') as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        # If the file doesn't exist, initialize with empty lists
        existing_data = {"subject": [], "time": [], "record": []}

    # Append the new study record to the existing data
    existing_data["subject"].append(subj)
    existing_data["time"].append(f"{study_time//60} minutes and {study_time%60} seconds")
    existing_data["record"].append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Write the updated data back to the JSON file
    with open('study_info.json', 'w') as json_file:
        json.dump(existing_data, json_file, indent=2)

    engine.say(f"You studied for {study_time // 60} minutes and {study_time % 60} seconds.")
    engine.runAndWait()
def tweet_py(Message):
    try:
        consumer_key = os.getenv('consumer_key')
        consumer_secret = os.getenv('consumer_secret')
        access_token = os.getenv('access_token')
        access_token_secret = os.getenv('access_token_secret')
        barer_token = os.getenv('barer_token')
        client =tweepy.Client(barer_token,consumer_key,consumer_secret,access_token,access_token_secret)
        auth = tweepy.OAuthHandler(consumer_key,consumer_secret,access_token,access_token_secret)
        api = tweepy.API(auth)

        # Your tweet content
        
        tweet_content = Message
        

        client.create_tweet(text=tweet_content)
        output_text.insert(tk.END, "Successfully Tweeted")
        engine.say("your message has been Tweeted! ")
        engine.runAndWait()
    except:
        engine.say("Error")
        output_text.insert(tk.END, "An error occurred")
        engine.runAndWait()


def toggle_panel():
    target_x = 0 if slide_panel.winfo_x() < 0 else -155
    animate_slide(target_x)

def animate_slide(target_x):
    current_x = slide_panel.winfo_x()
    animation_speed= 9
    if current_x != target_x:
        if current_x < target_x:
            new_x = min(current_x + animation_speed, target_x)
        else:
            new_x = max(current_x - animation_speed, target_x)

        slide_panel.place(x=new_x, y=100)
        root.after(10, lambda: animate_slide(target_x))

button_style1 = {
    "width": 11,
    "height": 1,
    "bg": "#3498db",  # Background color
    "fg": "white",    # Text color
    "font": ("Helvetica", 11, "bold"),
    "relief": tk.SOLID,  # Relief style (flat appearance)
    "activebackground": "#2980b9",  # Background color when clicked
}
button_style2 = {
    # "width": 12,
    # "height": 1,
    "bg": "turquoise",  # Background color
    "fg": "black",    # Text color
    "font": ("Helvetica", 11, "bold"),
    "relief": tk.SOLID,  # Relief style (flat appearance)
    "activebackground": "darkblue",  # Background color when clicked
}

def isBlock(key):

    # Mumbai Matic network endpoint (QuickNode in this example)
    matic_mumbai_url = "https://rpc-mumbai.maticvigil.com/"
    w3 = Web3(Web3.HTTPProvider(matic_mumbai_url))

    # Replace the following variables with your actual contract address and ABI
    contract_address = "0xf5a01b2c617Ff413E2d821B943E5Bf690bda064B"

    
    with open('abi.json', 'r') as file:
        contract_abi = json.load(file)

    contract = w3.eth.contract(address=contract_address, abi=contract_abi)


    try:
        client = MongoClient("mongodb+srv://sohamde2004:sohamjgd@sohamcluster.imcgngv.mongodb.net/?retryWrites=true&w=majority")
        db = client.get_database("Razor_pay")
        records = db.Keys_DB
        ans = records.find_one({'testkey': key})
        if(ans == None):

        # Call the smart contract function to verify the product key
            result = contract.functions.verifyProductKey(key).call()

            if result:
            
                return True
            else:
                return False
        else:
            
            return True
    except Exception as e:
        print(f"Error during verification: {e}")
        return False
def isKeyPresent(key):
    client = MongoClient("mongodb+srv://sohamde2004:sohamjgd@sohamcluster.imcgngv.mongodb.net/?retryWrites=true&w=majority")
    db = client.get_database("keys_db")
    records = db.student_records
    ans = records.find_one({'testkey': key})
    if ans == None:
        return False
    else:
        return True

def insertKEY(key):
    client = MongoClient("mongodb+srv://sohamde2004:sohamjgd@sohamcluster.imcgngv.mongodb.net/?retryWrites=true&w=majority")
    db = client.get_database("keys_db")
    records = db.student_records


    # records.count_documents({})#counts the number of docus

    new_key = {
        "testkey":f"{key}",
        "valid":"true"
    }
    records.insert_one(new_key)


def verify_login():
    username = user.get()
    password = code.get()

    # Example: Check if the username and password match
    if isBlock(password):
        if(isKeyPresent(password) == False):
        # If login is successful, close the login window and open the main window
            insertKEY(password)
            
            value_to_add = "STATUS = VALIDATED"

            # Append the new value to the .env file
            with open(".env", "a") as env_file:
                env_file.write("\n" + value_to_add + "\n")
            login_window.destroy()
            open_main_window()
        else:
            messagebox.showerror("Login Failed" , "Product Key already used")    
    else:
        messagebox.showerror("Login Failed", "Invalid product key ")


def create_login_window():
    login = Tk()
    login.title("Login")
    login.configure(background='#192025', borderwidth=2, highlightthickness=3, relief=SOLID, highlightcolor="black")
    window_width = 500
    window_height = 500
    screen_width = login.winfo_screenwidth()
    screen_height = login.winfo_screenheight()
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    login.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    login.resizable(False, False)
    global user, code

    frame = Frame(login, width = 400, height=400, bg = 'lightblue') 
    frame.place(x = 50, y = 50)

    heading = Label(frame, text = 'PRODUCT KEY VERIFICATION',fg = 'black', bg = 'lightblue', font=('Algerian', 20, 'bold'))
    heading.place(x= 2, y = 30)

    def on_enter(e):
        user.delete(0, 'end')
    def on_leave(e):
        name = user.get()
        if name=="":
            user.insert(0, 'Username')
    user = Entry(frame, width=25, fg = 'black', border=0, bg = 'lightblue', font=('Courier', 12))
    user.place(x=30, y = 100)
    user.insert(12, 'Username')
    user.bind("<FocusIn>", on_enter)
    user.bind("<FocusOut>", on_leave)
    Frame(frame, width=300, height=2, bg = 'black').place(x=25, y=130)

    def on_enter(e):
        code.delete(0, 'end')
    def on_leave(e):
        pwd = code.get()
        if pwd=="":
            code.insert(0, 'Enter Product Key')
    code = Entry(frame, width=25, fg = 'black', border=0, bg = 'lightblue', font=('Courier', 12))
    code.place(x=30, y = 160)
    code.insert(12, 'Enter Product Key')
    code.bind("<FocusIn>", on_enter)
    code.bind("<FocusOut>", on_leave)
    Frame(frame, width=300, height=2, bg = 'black').place(x=25, y=190)

    Button(frame, width = 25, pady=10, text = "Validate Key", fg = 'white', border = 0, bg = '#57a1fa', font=('Microsoft Yahei UI Light', 13), cursor='hand2', command = verify_login).place(x = 70, y = 250)

    return login

def auto_scroll():
    output_text.yview(tk.SCROLL, 1, "units")
    root.after(1000, auto_scroll)
# Create the main window
def open_main_window():
    global root, output_text, timer_label, chatgpt_button, turn_off_study_button, terminate_button, activate_button, canvas, slide_panel, quit_button, dt
    root = tk.Tk()
    root.title("JARVIS - THE AI ASSISTANT")

    window_width = 750
    window_height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    root.configure(background='black', borderwidth=2, highlightthickness=3, relief=tk.SOLID, highlightcolor="lightblue")
    
    canvas = Canvas(root, bg = 'black', highlightthickness=0)
    background_image = Image.open("Untitled.png")
    background_image = background_image.resize((window_width, window_height), Image.BICUBIC)
    background_image = ImageTk.PhotoImage(background_image)
    canvas.create_image(0,0, image = background_image, anchor = NW)
    canvas.create_text(375, 20, text= "Use Mouth, not Fingers!!", fill="lightblue", font=("Algerian", 35, 'bold'))
    canvas.pack(fill="both", expand=True)

    slide_panel = tk.Frame(root, width=150, height=300, bg='blue', highlightthickness=2, highlightbackground='darkblue')
    slide_panel.pack_propagate(False)
    slide_panel.place(x=-155, y=100)

    label = tk.Label(slide_panel, text="---MENU BAR---", font=("Segoe UI", 14, "bold"), foreground="black", bg = 'blue')
    label.pack(pady=(10, 10))

    help = tk.Button(slide_panel, text="Help", command=show_help, **button_style1).pack(pady = 5)
    contributors = tk.Button(slide_panel, text="Contributors", command=show_contributors, **button_style1).pack(pady = 5)
    github = tk.Button(slide_panel, text="GitHub", command=github_link, **button_style1).pack(pady = 5)
    study_mode = tk.Button(slide_panel, text="Study Info", command=study_mode_data, **button_style1).pack(pady = 5)

    panel = tk.Frame(root, width=240, height=420, highlightthickness= 0, relief=tk.SOLID, highlightcolor='black', bg = 'black')
    panel.pack_propagate(False)
    panel.place(x=500, y=60)

    activate_button = tk.Button(panel, text="Activate", command=activate_button, **button_style2)
    activate_button.pack(pady = 5)

    output_text = scrolledtext.ScrolledText(panel, wrap=tk.WORD, width=26, height=10)
    output_text.configure(background="black", foreground="white", insertbackground="white", font=("Courier", 10))
    output_text.pack(pady=10)

    terminate_button = tk.Button(panel, text="Deactivate", command=terminate, **button_style2)
    # terminate_button.pack(pady=5)

    menu_panel = tk.Frame(panel, width=240, height=100, highlightthickness= 0, relief=tk.SOLID, highlightcolor='black', bg = 'black')
    menu_panel.pack_propagate(False)
    menu_panel.place(x=0, y=320)
    animate_button = tk.Button(menu_panel, text="Menu", command=toggle_panel, **button_style1)
    animate_button.pack(pady=5)
    quit_button = tk.Button(menu_panel, text="Quit", command=quit, **button_style1)
    quit_button.pack(pady = 5)

    chatgpt_button = tk.Button(panel, text="Get help from GPT", command=get_gpt_help, **button_style2)
    turn_off_study_button = tk.Button(panel, text="Turn Off Study Mode", command=turn_off_study_mode, **button_style2)
    
    root.resizable(False, False)

    timer_label = tk.Label(root, font=("Segoe UI", 14, "bold"), foreground="#3498db", bg = 'black')
    # timer_label.pack(pady=(10, 10))
    dt = tk.Label(root, font=("Segoe UI", 14, "bold"), foreground="#3498db", bg = 'black')
    dt.pack(pady=(10, 10), anchor=W)
    update_datetime()
    auto_scroll()
    root.after(100, welcome_message)
    root.mainloop()
def update_datetime():
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("\t %d-%m-%Y \t %I:%M:%S %p")
    dt.config(text=formatted_datetime)
    root.after(1000, update_datetime)
if os.environ.get("STATUS") == "VALIDATED":
    open_main_window()
else:
    login_window = create_login_window()
    login_window.mainloop()

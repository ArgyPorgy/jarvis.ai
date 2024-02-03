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
import sys
import os
import win32api
import wikipedia
from datetime import datetime

from dotenv import load_dotenv
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
def get_command(command): 
    if "assistant" in command:
        command = command.split("assistant")[1].strip()
    elif "jarvis" in command:
        command = command.split("jarvis")[1].strip()
    return command

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
                    elif "location" in command.lower() or "where i am" in command.lower():
                        locationcurrent = get_location()
                        engine.say(locationcurrent)
                        output_text.insert(tk.END, f"{locationcurrent}\n")
                        engine.runAndWait()
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
                        output_text.insert(tk.END, "According to Wikipedia -> ")
                        resp = "according to wikipedia, "+resp
                        engine.say(resp)
                        engine.runAndWait()
                    elif "news" in command.lower():
                        output_text.insert(tk.END, "Fetching news...\n")
                        engine.say("fetching news")
                        engine.runAndWait()
                        news(command.lower())
                    elif "weather" in command.lower() or "temperature" in command.lower():
                        weather(command.lower())
                        engine.runAndWait()
                    elif "thank" in command.lower() or "thank you" in command.lower() or "thanks" in command.lower():
                        engine.say("I am glad to help you. Let me know if you want anything else.")
                        output_text.insert(tk.END, "Welcome...\n")
                        engine.runAndWait()
                    elif "deactivate" in command.lower():
                        output_text.insert(tk.END, "Sayonara!\n")
                        engine.say("See you soon again! Sayonara...")
                        engine.runAndWait()
                        terminate()
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
    result = wp.info(query, lines = 2, return_value=True)
    return result

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
def show_help():
    messagebox.showinfo("Help", "This is a help message.")

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
    dt.pack(pady=(10, 10))
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
open_main_window()

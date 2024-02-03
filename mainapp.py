import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, PhotoImage
from tkinter import *
from PIL import Image, ImageTk
import pyttsx3
import webbrowser
import threading
import speech_recognition as sr
import random
import time

start_time = time.time()
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)
listening_enabled = False

def start_listening():
    global listening_enabled
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        while listening_enabled:  # Check if listening is still enabled
            output_text.insert(tk.END, "Listening...\n")
            try:
                isJarvis = ''
                with sr.Microphone() as sourceT:
                    recognizer.pause_threshold= 0.5 #new 
                    hotword = recognizer.listen(sourceT)
                    isJarvis = recognizer.recognize_google(hotword)
                    output_text.insert(tk.END, isJarvis)
                
                if 'assistant' in isJarvis.lower() or "jarvis" in isJarvis.lower():
                    # recognizer.pause_threshold= 1 #new 
                    # change_border_color()
                    output_text.insert(tk.END, "Hey\n")
                    engine.say("Hello! ")
                    # engine.runAndWait()
                     
                    audio = recognizer.listen(source, timeout=10)
                    command = recognizer.recognize_google(audio)
                    output_text.insert(tk.END, f"You said: {command}\n")

                    if "can you hear" in command.lower():
                        engine.say("Yes i can hear you!")
                        engine.runAndWait()
                        output_text.insert(tk.END, "Yes i can hear you!\n")
                    elif "who made you" in command.lower():
                        output_text.insert(tk.END, "I was made by the Team 'THE BOYS'. \nClick the contributors option in the menu tab for more info.\n")
                        change_background_image()
                        engine.say("I was made by the team THE BOYS")
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
    print("HElp showed")

def study_mode_data():
    print("Study mode enabled")

def get_gpt_help():
    if not get_gpt_help.has_run:
        get_gpt_help.has_run = True
        webbrowser.open("https://chat.openai.com/")
        chatgpt_button.pack_forget()
get_gpt_help.has_run = False

def turn_off_study_mode():
    print("Study mode disabled")

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
    global root, output_text, timer_label, chatgpt_button, turn_off_study_button, terminate_button, activate_button, canvas, slide_panel, quit_button
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

    timer_label = tk.Label(root, text="", font=("Segoe UI", 14, "bold"), foreground="#3498db", bg = 'black')
    timer_label.pack(pady=(10, 10))
    auto_scroll()
    root.after(100, welcome_message)
    root.mainloop()
open_main_window()

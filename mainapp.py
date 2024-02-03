import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from tkinter import *
import pyttsx3
import webbrowser
import threading

engine = pyttsx3.init()
engine.setProperty('rate', 150)

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

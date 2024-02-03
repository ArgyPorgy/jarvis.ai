import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pyttsx3

def terminate_button():
    message = "Your assistant is deactivate succesfully"
    engine.say(message)
    engine.runAndWait() 

def activate_button():
    message = "Hey your assistant is activate !! What can i do sir "
    engine.say(message)
    engine.runAndWait() 

def show_help():
    messagebox.showinfo("Help", "This is a help message.")

def show_contributors():
    messagebox.showinfo("Contributors", "Contributors to this application.")
def github():
    messagebox.showinfo("No link")


def quit_button():
    root.destroy()


# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 130)

# Welcome message
def welcome_message():
    message = "Welcome Niggas, Use your mouth, not your finger!, tap the activate for start your personal assistant"
    engine.say(message)
    engine.runAndWait()


# Create the main window
root = tk.Tk()
root.title("JARVIS")

# Set fixed window size
window_width = 400
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight() 
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Load and resize the background image
background_image = Image.open("jarvis.jpg")  # Replace "background.jpg" with your image file
background_image = background_image.resize((window_width, window_height), Image.BICUBIC)
background_image = ImageTk.PhotoImage(background_image)

# Create a label to hold the background image
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Style configuration
style = ttk.Style()

style.configure("TButton",
                padding=10,
                relief="flat",
                foreground="#000000",  # Button text color
                background="#808080",  # Button background color
                font=('Helvetica', 12, 'bold'),
                borderwidth=2,  # Border width
                bordercolor="#2c3e50",  # Border color
                highlightthickness=2,  # Thickness of focus highlight
                highlightbackground="#7f8c8d",  # Focus highlight color
                focuscolor="none",  # No focus color
                anchor="center",  # Text alignment
                width=15,  # Button width
                height=2,  # Button height
                underline=-1,  # Index of underlined character (-1 for none)
                wraplength=150,  # Wrap text after a certain width
                cursor="hand"  # Cursor style
                )


style.map("TButton",
          foreground=[('active', '#2980b9')],
          background=[('active', '#3498db')])

# Configure heading label style
style.configure("TLabel.Heading",
                font=('Segoe UI', 26, 'bold'),  # Updated font style
                foreground='#3498db',  # Updated heading text color
                shadowcolor='#2c3e50',  # Shadow color
                shadowoffset=(3, 3))  # Updated shadow offset

# Create heading label
heading_label = ttk.Label(root, text="Use mouth not finger!!", style="TLabel.Heading")
heading_label.pack(pady=(40, 30))

# Create buttons
activate_button = ttk.Button(root, text="Activate",command=activate_button , style="TButton")
terminate_button= ttk.Button(root, text="Terminate",command=terminate_button , style="TButton")
quit_button = ttk.Button(root, text="Quite", command=quit_button, style="TButton")

# Place buttons in the window
activate_button.pack(pady=(10, 40))
terminate_button.pack(pady=(10, 110))
quit_button.pack(pady=10)

# Create Menu Bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create Menu
menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Menu", menu=menu)

# Add Submenus
menu.add_command(label="Help", command=show_help)
menu.add_command(label="Contributors", command=show_contributors)
menu.add_command(label="Git-Hub", command=github)

root.after(100,welcome_message)
# Run the Tkinter event loop
root.mainloop()
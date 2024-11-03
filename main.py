import tkinter as tk
from tkinter import font
from tkinter import filedialog
import os
from cryptography.fernet import Fernet
from functions import *  # Ensure this is defined correctly

root = tk.Tk()
root.title("Faseeh Encrypts")
root.resizable(True, True)  # Allow window resizing

# Main variables:
enc = "Encrypt"
dec = "Decrypt"
no_action = "-"
action = no_action  # Shows at the action button and used to decide whether we need to encrypt or decrypt files.
info = "No file selected."  # Shown at the right of the screen.
filepath = None

ENCRYPTED_FILE_EXTENSION = '.enc'

# Functions:
def refresh_action_btn():
    action_btn.config(text=action)

def refresh_info_l():
    info_l.config(text=info)

def file_e_func():
    global filepath, action, info
    filepath = filedialog.askopenfilename()
    if filepath == "":
        action = no_action
        info = "No file selected."
    elif filepath.endswith(ENCRYPTED_FILE_EXTENSION):
        action = dec
        info = f"{os.path.basename(filepath)} is selected."
    elif filepath.endswith(".key"):
        action = no_action
        info = f"{os.path.basename(filepath)} is a key file. Cannot encrypt a key file."
    else:
        action = enc
        info = f"{os.path.basename(filepath)} is selected."
    refresh_action_btn()
    refresh_info_l()

def action_func():
    global filepath, action
    if filepath is None or action == no_action:
        return
    global info
    filename = os.path.basename(filepath)
    try:
        if action == enc:
            key, cipher_suite = generate_key_and_cipher_suite()
            path_to_key_file = filepath + '.key'
            create_key_file_and_write_key_to_it(path_to_key_file, key)
            encrypt_file(filepath, cipher_suite)
            add_extension(filepath, ENCRYPTED_FILE_EXTENSION)
            filepath += ENCRYPTED_FILE_EXTENSION
            action = dec
            refresh_action_btn()
            info = f"{filename} has been encrypted."
            refresh_info_l()
        elif action == dec:
            path_to_key_file = filepath[:-4] + '.key'
            key, cipher_suite = read_key_and_create_cipher_suite(path_to_key_file)
            decrypt_file(filepath, cipher_suite)
            os.rename(filepath, filepath[:-4])  # To remove the .enc extension.
            filepath = filepath[:-4]  # To remove the .enc extension.
            os.remove(path_to_key_file)
            action = enc
            refresh_action_btn()
            info = f"{filename} has been decrypted."
            refresh_info_l()
    except Exception as e:
        info = str(e)  # Display the error message
        refresh_info_l()

# UI variables:
scale_var = 1.0
pad1 = 4 * scale_var
pad2 = 2 * scale_var

# Font settings
custom_font = font.Font(size=int(10 * scale_var))
custom_font2 = font.Font(size=int(8 * scale_var))

# Function to resize text and buttons
def update_widgets():
    custom_font.config(size=int(10 * scale_var))
    custom_font2.config(size=int(8 * scale_var))

    # Keep the menu button heights consistent
    height = 2  # Fixed height for menu buttons
    scale_down.config(font=custom_font2, height=height)
    scale_up.config(font=custom_font2, height=height)
    help_button.config(font=custom_font2, height=height)
    action_btn.config(font=custom_font, height=int(2 * scale_var))
    file_e.config(font=custom_font, height=int(2 * scale_var))
    info_l.config(font=custom_font)

def scale_text(increment):
    global scale_var
    scale_var += increment
    scale_var = max(1, min(scale_var, 2.5))  # Clamping scale_var between 1 and 2.5
    update_widgets()

# Widgets:
menu = tk.Frame(root, bd=2, relief=tk.RAISED, padx=pad2)
menu.grid(row=0, column=0, columnspan=3, sticky='ew')

# Set a fixed height for the menu
menu_height = 30  # Adjust this value as needed
menu.config(height=menu_height)

menu_font = font.Font(size=8)
scale_down = tk.Button(menu, text="<<", relief=tk.FLAT, font=menu_font, command=lambda: scale_text(-0.25))
scale_down.grid(row=0, column=0, sticky='nsew')
scale_up = tk.Button(menu, text=">>", relief=tk.FLAT, font=menu_font, command=lambda: scale_text(0.25))
scale_up.grid(row=0, column=1, sticky='nsew')
help_button = tk.Button(menu, text="Help", relief=tk.FLAT, font=menu_font)
help_button.grid(row=0, column=2, sticky='nsew')

# Configure the grid to expand
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)

sel_f = tk.Label(root, text="Select the file to encrypt:", font=custom_font)
sel_f.grid(row=1, column=0, padx=pad1, pady=pad1, sticky='nsew')
file_e = tk.Button(root, text="File Explorer", padx=pad1, pady=pad1, command=file_e_func)
file_e.grid(row=1, column=1, padx=pad1, pady=pad1, sticky='nsew')

# Create the info label without wraplength first
info_l = tk.Label(root, text=info, font=custom_font, wraplength=0)
info_l.grid(row=1, column=2, rowspan=2, padx=pad1, pady=pad1, sticky='nsew')

def update_info_label():
    current_width = root.winfo_width() - (2 * pad1)  # Update width based on the current window size
    info_l.config(wraplength=current_width)

root.bind("<Configure>", lambda event: update_info_label())  # Update on resize

# Initialize the info label's wraplength correctly
update_info_label()

action_btn = tk.Button(root, text=action, padx=pad1, pady=pad1, font=custom_font, command=action_func)
action_btn.grid(row=2, column=0, columnspan=2, padx=pad1, pady=pad1, sticky='nsew')

# Run the main loop
root.mainloop()

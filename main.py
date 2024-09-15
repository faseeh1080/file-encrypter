import tkinter as tk
from tkinter import font
from tkinter import filedialog
import os
from cryptography.fernet import Fernet
from functions import *

root = tk.Tk()
root.title("Faseeh Encrypts")
root.resizable(False, False)

# Main variables:

enc = "Encrypt"
dec = "Decrypt"
no_action = "-"
action = no_action # Shows at the action button and used to decide whether we need to encrypt or decrypt files.
info = "No file selected." # Shown at the right of the screen.
filepath = None

ENCRYPTED_FILE_EXTENSION = '.enc'

# Functions:

def refresh_action_btn():
    action_btn.config(text=action)
def refresh_info_l():
    info_l.config(text=info)


def file_e_func():
    global filepath
    global action
    global info
    global info_l
    filepath = filedialog.askopenfilename()
    if filepath == "":
        action = no_action
        info = "No file selected."
    elif filepath.endswith(".enc"):
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
    global filepath
    global action
    if filepath == None or action == no_action:
        return
    global info
    global info_l
    filename = os.path.basename(filepath)
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
        try:
            path_to_key_file = filepath[:-4] + '.key'
            key, cipher_suite = read_key_and_create_cipher_suite(path_to_key_file)
            print(path_to_key_file)
        except:
            info = f"Unable to find the key file for {filename}."
            refresh_info_l()
            return
        decrypt_file(filepath, cipher_suite)
        os.rename(filepath, filepath[:-4]) # To remove the .enc extension.
        filepath = filepath[:-4] # To remove the .enc extension.
        os.remove(path_to_key_file)
        action = enc
        refresh_action_btn()
        info = f"{filename} has been decrypted."
        refresh_info_l()

# UI variables:

scale_var = 1
SCALE_MAXIMUM = 5
pad1 = 4 * scale_var
pad2 = 2 * scale_var
custom_font = font.Font(size=10 * scale_var)
custom_font2 = font.Font(size=8 * scale_var)

# Widgets:

menu = tk.Frame(root, bd=2, relief=tk.RAISED, padx=pad2)
menu.grid(row=0, column=0, columnspan=3, sticky='ew')
scale_down = tk.Button(menu, text="<<", relief=tk.FLAT, font=custom_font2)
scale_down.pack(side=tk.LEFT)
scale_up = tk.Button(menu, text=">>", relief=tk.FLAT, font=custom_font2)
scale_up.pack(side=tk.LEFT)
help = tk.Button(menu, text="Help", relief=tk.FLAT, font=custom_font2)
help.pack(side=tk.LEFT)

sel_f = tk.Label(root, text="Select the file to encrypt:", font=custom_font)
sel_f.grid(row=1, column=0, padx=pad1, pady=pad1)
file_e = tk.Button(root, text="File Explorer", padx=pad1, pady=pad1, command=file_e_func)
file_e.grid(row=1, column=1, padx=pad1, pady=pad1)

info_l_wraplength = 100 * scale_var
info_l_width = 16 * scale_var
info_l = tk.Label(root, text=info, font=custom_font, width=info_l_width, wraplength=info_l_wraplength)
info_l.grid(row=1, column=2, rowspan=2, padx=pad1, pady=pad1)

action_btn = tk.Button(root, text=action, padx=pad1, pady=pad1, font=custom_font, command=action_func)
action_btn.grid(row=2, column=0, columnspan=2, padx=pad1, pady=pad1, sticky='ew')

root.mainloop()
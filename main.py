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
action = enc # Shows at the action button and used to decide whether we need to encrypt or decrypt files.
info = "No file selected." # Shown at the right of the screen.
filepath = None

ENCRYPTED_FILE_EXTENSION = '.enc'

# Functions:

def refresh_path_entry(string):
    path_entry.delete(0, tk.END)
    path_entry.insert(tk.END, string)
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
    path_entry.delete(0, tk.END)
    path_entry.insert(tk.END, filepath)
    if filepath.endswith(".enc"):
        action = dec
    else:
        action = enc
    action_btn.config(text=action)
    info = f"{os.path.basename(filepath)} is selected."
    info_l.config(text=info)

def action_func():
    global filepath
    if filepath == None:
        return
    global info
    global info_l
    global action
    filename = os.path.basename(filepath)
    if action == enc:
        key, cipher_suite = generate_key_and_cipher_suite()
        path_to_key_file = filepath + '.key'
        create_key_file_and_write_key_to_it(path_to_key_file, key)
        encrypt_file(filepath, cipher_suite)
        add_extension(filepath, ENCRYPTED_FILE_EXTENSION)
        filepath += ENCRYPTED_FILE_EXTENSION
        refresh_path_entry(filepath)
        action = dec
        refresh_action_btn()
        info = f"{filename} has been encrypted."
        refresh_info_l()
        return
    if action == dec:
        try:
            path_to_key_file = filepath[:-4] + '.key'
            key, cipher_suite = read_key_and_create_cipher_suite(path_to_key_file)
            print(path_to_key_file)
        except:
            info = "Unable to find the key file."
            refresh_info_l()
            return
        decrypt_file(filepath, cipher_suite)
        os.rename(filepath, filepath[:-4]) # To remove the .enc extension.
        filepath = filepath[:-4] # To remove the .enc extension.
        os.remove(path_to_key_file)
        refresh_path_entry(filepath)
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
info_l.grid(row=1, column=2, rowspan=3, padx=pad1, pady=pad1)

path_entry = tk.Entry(root, font=custom_font)
path_entry.grid(row=2, column=0, columnspan=2, padx=pad1, pady=pad1, sticky="ew")

action_btn = tk.Button(root, text=action, padx=pad1, pady=pad1, font=custom_font, command=action_func)
action_btn.grid(row=3, column=0, columnspan=2, padx=pad1, pady=pad1, sticky='ew')

root.mainloop()
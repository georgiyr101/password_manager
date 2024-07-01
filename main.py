from cryptography.fernet import Fernet
import json
import os
import sys

KEY_FILE = 'key.key'

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)

def load_key():
    try:
        with open(KEY_FILE, 'rb') as key_file:
            return key_file.read()
    except FileNotFoundError:
        generate_key()
        return load_key()

key = load_key()
fernet = Fernet(key)

def encrypt_password(password: str):
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password

def decrypt_password(encrypted_password):
    try:
        decrypted_password = fernet.decrypt(encrypted_password).decode()
        return decrypted_password
    except :
        print("Error: Invalid token, decryption failed.")
        return None
def initialize_password_file():
    if not os.path.exists('passwords.json'):
        with open('passwords.json', 'w') as file:
            json.dump([], file)

def add_password(site, password):
    encrypted_password = encrypt_password(password)
    with open('passwords.json', 'r+') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = []
        data.append({"site": site, "password": encrypted_password.decode()})
        file.seek(0)
        json.dump(data, file)

def view_passwords():
    with open('passwords.json', 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = []
        passwords = ""
        for entry in data:
            decrypted_password = decrypt_password(entry["password"].encode())
            if decrypted_password is not None:
                passwords += f'Site: {entry["site"]}, Password: {decrypted_password}\n'
            else:
                passwords += f'Site: {entry["site"]}, Password: Error decrypting password.\n'
        return passwords

def delete_password(site):
    try:
        with open('passwords.json', 'r') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        data = []

    original_length = len(data)
    data = [entry for entry in data if entry["site"] != site]
    new_length = len(data)

    with open('passwords.json', 'w') as file:
        json.dump(data, file)

    return original_length != new_length







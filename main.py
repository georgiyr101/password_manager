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
        for entry in data:
            decrypted_password = decrypt_password(entry["password"].encode())
            if decrypted_password is not None:
                print(f'Site: {entry["site"]}, Password: {decrypted_password}')
            else:
                print(f'Site: {entry["site"]}, Password: Error decrypting password.')

def delete_password(site):
    with open('passwords.json', 'r+') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = []
        new_data = [entry for entry in data if entry["site"] != site]
        file.seek(0)
        file.truncate()  # очистка файла перед записью
        json.dump(new_data, file, indent=4)
        if len(data) == len(new_data):
            print(f'No password found for site: {site}')
        else:
            print(f'Password for site: {site} has been deleted.')

def main():
    initialize_password_file()
    while True:
        print('Choose option:')
        print('1 - View passwords')
        print('2 - Add password')
        print('3 - Delete password')
        print('4 - Exit')
        try:
            choice = int(input('print a number of option:'))
        except ValueError:
            print('Please, enter a number')

        if choice == 1:
            view_passwords()
        elif choice == 2:
            print('Enter the name of the site:')
            site = str(input())
            print('Enter the password')
            password = str(input())
            add_password(site,password)
        elif choice == 3:
            print('Enter the name of the site:')
            site = str(input())
            delete_password(site)
        elif choice == 4:
            sys.exit()
        else:
            print('There is no such option!')


if __name__ == "__main__":
    main()





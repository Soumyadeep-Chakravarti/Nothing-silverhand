#!/data/data/com.termux/files/usr/bin/python
import os
import subprocess
import getpass
import random
import string
import base64
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from flask import Flask, request, redirect, url_for, send_from_directory, render_template_string
from datetime import datetime
import sys

# Constants
DATA_FILE = '/sdcard/database_data.txt'
UPLOAD_FOLDER = "/storage/emulated/0/Cloud"
KEY_FILE = "key.json"

# ASCII Art
def display_ascii_art():
    print("""
  ___         _ ___           _ _ ___ _ 
 |   \\ ___ __| / __| ___ __  / / |_  ) |
 | |) / -_) _` \\__ \\/ -_) _| | | |/ /| |
 |___/\\___\\__,_|___/\\___\\__| |_|_/___|_|
""")

# Function to get device information
def get_device_info():
    username = subprocess.getoutput("whoami")

    return {
        "Device Code": username,
        "GitHub Link": "https://github.com/dedsec1121fk",
        "Bitcoin Wallet Address To Donate": "1Ae1kcqNTsFd5kfLT8shnwSU2HwoM11r5g"
    }

# Function to generate a random password
def generate_password():
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    digits = string.digits
    special_characters = string.punctuation
    
    first_char = random.choice(string.ascii_letters)
    last_char = random.choice(string.ascii_letters)
    
    while first_char == last_char:
        last_char = random.choice(string.ascii_letters)
    
    length = random.randint(6, 10)
    middle_chars = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(length))
    
    password = first_char + middle_chars + last_char
    password_list = list(password)
    random.shuffle(password_list)
    password = ''.join(password_list)
    
    return password

# Function to handle database operations
def add_data():
    data = input("Enter data to add: ")
    with open(DATA_FILE, 'a') as f:
        f.write(data + '\n')
    print("Data added successfully.")

def edit_data():
    if not os.path.exists(DATA_FILE):
        print("No data found to edit.")
        return
    
    with open(DATA_FILE, 'r') as f:
        lines = f.readlines()
    
    if not lines:
        print("The file is empty. Nothing to edit.")
        return
    
    print("Current data (edit as needed):\n")
    current_data = ''.join(lines)
    print(current_data)
    
    new_data = []
    print("Enter your edits (finish with a single line containing 'END'):")
    
    while True:
        line = input()
        if line == 'END':
            break
        new_data.append(line)
    
    with open(DATA_FILE, 'w') as f:
        f.write('\n'.join(new_data) + '\n')
    print("Data edited successfully.")

def search_data():
    search_term = input("Enter search term: ")
    with open(DATA_FILE, 'r') as f:
        matching_lines = [line.strip() for line in f if search_term in line]
    
    if not matching_lines:
        print("No matching data found.")
    else:
        print("Matching data:")
        for line in matching_lines:
            print(line)

def see_database():
    if not os.path.exists(DATA_FILE):
        print("No data found. The database is empty.")
        return
    
    with open(DATA_FILE, 'r') as f:
        data = f.read().strip()
    
    if not data:
        print("The database is empty.")
    else:
        print(data)

def database_menu():
    while True:
        print("\n")
        print("1) Add Data")
        print("2) Edit Data")
        print("3) Search Data")
        print("4) See Database")
        print("5) Return to Main Menu")
        print("\n")
        
        option = input("Choose an option: ")

        if option == '1':
            add_data()
        elif option == '2':
            edit_data()
        elif option == '3':
            search_data()
        elif option == '4':
            see_database()
        elif option == '5':
            break
        else:
            print("Invalid option. Please try again.")

# Local Cloud Storage
def install_packages():
    try:
        subprocess.run(["pip", "install", "--upgrade", "Flask"], check=True)
        with open('requirements.txt', 'w') as f:
            f.write('Flask\n')
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to install packages: {e}")

try:
    install_packages()
except ImportError:
    raise ImportError("Please install Flask using 'pip install Flask'.")

app = Flask(__name__)

def allowed_file(filename):
    return True  # Allow all file types

def get_files_by_extension():
    files_by_extension = {}
    for root, _, files in os.walk(UPLOAD_FOLDER):
        for file in files:
            extension = file.split('.')[-1].lower()
            if extension in files_by_extension:
                files_by_extension[extension].append(file)
            else:
                files_by_extension[extension] = [file]
    return files_by_extension

@app.route('/')
def index():
    files_by_extension = get_files_by_extension()
    return render_template_string("""
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>DedSec1121 Local Cloud Storage</title>
            <style>
                body {
                    background-color: black;
                    color: white;
                    font-family: Arial, sans-serif;
                }
                h1, h2 {
                    color: white;
                }
                a {
                    color: white;
                    text-decoration: none;
                }
                textarea {
                    width: 100%;
                    height: 300px;
                }
                input[type="submit"], input[type="file"], input[type="search"] {
                    margin-top: 10px;
                }
                ul {
                    list-style-type: none;
                    padding: 0;
                }
                li {
                    margin-bottom: 10px;
                }
            </style>
        </head>
        <body>
            <h1>DedSec1121 Local Cloud Storage</h1>
            <h2>Upload New File</h2>
            <form method=post enctype=multipart/form-data action="/upload">
                <input type=file name=file>
                <input type=submit value=Upload>
            </form>
            <h2>Files</h2>
            <ul>
                {% for extension, files in files_by_extension.items()|sort %}
                    <li>
                        <strong>{{ extension }}</strong>
                        <ul>
                            {% for file in files|sort %}
                                <li>
                                    <a href="{{ url_for('download_file', filename=file) }}">{{ file }}</a> |
                                    <a href="{{ url_for('delete_file', filename=file) }}">Delete</a>
                                </li>
                            {% endfor %}
                        </ul>
                    </li>
                {% endfor %}
            </ul>
        </body>
        </html>
        """, files_by_extension=files_by_extension)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return redirect(url_for('index'))
    else:
        return "File type not allowed", 400

@app.route('/delete/<filename>')
def delete_file(filename):
    try:
        os.remove(os.path.join(UPLOAD_FOLDER, filename))
        return redirect(url_for('index'))
    except Exception as e:
        return f"An error occurred while deleting the file: {str(e)}", 500

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/search', methods=['GET'])
def search_files():
    query = request.args.get('query', '').lower()
    matching_files = []

    for root, dirs, files in os.walk(UPLOAD_FOLDER):
        for file in files:
            if query in file.lower():
                matching_files.append(file)
                
    return render_template_string("""
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>DedSec1121 Local Cloud Storage</title>
            <style>
                body {
                    background-color: black;
                    color: white;
                    font-family: Arial, sans-serif;
                }
                h1, h2 {
                    color: white;
                }
                a {
                    color: white;
                    text-decoration: none;
                }
            </style>
        </head>
        <body>
            <h1>DedSec1121 Local Cloud Storage</h1>
            <h2>Search Results</h2>
            <ul>
                {% for file in matching_files %}
                    <li>
                        <a href="{{ url_for('download_file', filename=file) }}">{{ file }}</a> |
                        <a href="{{ url_for('delete_file', filename=file) }}">Delete</a>
                    </li>
                {% endfor %}
            </ul>
            <a href="/">Return to main menu</a>
        </body>
        </html>
        """, matching_files=matching_files)

def run_local_cloud():
    app.run(host="0.0.0.0", port=5000)

def show_device_info():
    info = get_device_info()
    print("\n")
    for key, value in info.items():
        print(f"{key}: {value}")
    print("\n")

# Main menu
def main_menu():
    display_ascii_art()
    show_device_info()
    
    while True:
        print("1) Database")
        print("2) Local Cloud Storage")
        print("3) Text Encryption/Decryption")
        print("4) Generate Password")
        print("5) Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            database_menu()
        elif choice == '2':
            run_local_cloud()
        elif choice == '3':
            print("Text Encryption/Decryption (Not implemented in this script)")
        elif choice == '4':
            password = generate_password()
            print("Generated password:", password)
        elif choice == '5':
            print("Psila,psila,ta maura ta mpere,den ta,den ta,den ta nikoun pote!\n2023 E' ESSO\nExiting the program.")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()


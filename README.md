# Script Overview

This Python script provides a set of utilities for managing local data and files using Termux on Android. It integrates features such as a simple file database, local cloud storage with Flask, and password generation. Below is a breakdown of its functionality and how to use it.

## Features

1. **Database Management**
   - **Add Data**: Append new data to a text file (`database_data.txt`).
   - **Edit Data**: Modify existing data in the text file.
   - **Search Data**: Search for specific terms within the text file.
   - **See Database**: Display the entire content of the text file.

2. **Local Cloud Storage**
   - **File Upload**: Upload files to a local directory (`/storage/emulated/0/Cloud`).
   - **File Download**: Download files from the local directory.
   - **File Deletion**: Delete files from the local directory.
   - **Search Files**: Search for files in the local directory by filename.

3. **Password Generation**
   - **Generate Password**: Create a random password with a mix of characters, digits, and special symbols.

4. **Device Information**
   - **Show Device Info**: Display device-related information and contact links.

## Usage Instructions

### 1. Setup

Ensure you have Python installed in Termux. You'll need the `Flask` package, which is installed automatically when the script runs. If Flask is missing, you can manually install it using:

```bash
pip install Flask
```

### 2. Running the Script

To run the script, use the following command in Termux:

```bash
python script.py
```

### 3. Main Menu Options

Upon running the script, you will see a menu with the following options:

1. **Database**
   - Choose this to manage the text file database (add, edit, search, or view data).

2. **Local Cloud Storage**
   - Starts a local web server allowing you to upload, download, delete, and search files.

3. **Text Encryption/Decryption**
   - This feature is currently not implemented.

4. **Generate Password**
   - Generates and displays a random password.

5. **Exit**
   - Exits the script.

### 4. Local Cloud Storage

When you select the Local Cloud Storage option, the script will start a Flask server on port 5000. You can access the interface via your web browser at `http://<your-device-ip>:5000`. The web interface allows you to:
- Upload files.
- View and manage existing files (download or delete).
- Search for files by name.

### 5. Notes

- Ensure the directories used in the script (`/sdcard` and `/storage/emulated/0/Cloud`) have appropriate read/write permissions.
- The `database_data.txt` file should be located at `/sdcard/database_data.txt`.
- The Flask server requires network permissions and will run on all network interfaces.

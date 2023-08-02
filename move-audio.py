import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import threading
from datetime import datetime
import subprocess
import webbrowser
import sys

def move_files(progress_var):
    try:
        config_file_path = "path_config.txt"
        with open(config_file_path, "r") as file:
            lines = file.readlines()
            source_path = lines[0].split(":", 1)[1].strip()
            destination_path = lines[1].split(":", 1)[1].strip()

        file_count = 0
        total_files = sum(len(files) for _, _, files in os.walk(source_path))
        log = []  # List to store the log entries

        for root, dirs, files in os.walk(source_path):
            for file in files:
                source_file = os.path.join(root, file)
                parent_directory = file.split("~")[0]  # Extracting dynamic folder name from filename

                if file.endswith(".mp3"):
                    relative_path_from_recordings = root.split("Recordings")[1].lstrip("\\")  # relative path from 'Recordings' directory
                    destination_subdirectories = os.path.join(destination_path, parent_directory, "Recordings", relative_path_from_recordings)
                elif file.endswith(".xml"):
                    relative_path_from_databases = root.split("Databases")[1].lstrip("\\")  # relative path from 'Databases' directory
                    destination_subdirectories = os.path.join(destination_path, parent_directory, "Databases", relative_path_from_databases)

                destination_file = os.path.join(destination_subdirectories, file)

                if not os.path.exists(destination_subdirectories):
                    os.makedirs(destination_subdirectories, exist_ok=True)

                if not os.path.exists(destination_file):
                    shutil.move(source_file, destination_file)
                    file_count += 1
                    progress = int((file_count / total_files) * 100)
                    progress_var.set(progress)
                    log_entry = f"Moved {source_file} to {destination_file}"
                else:
                    # Check if source file is different from the destination file
                    if os.path.getmtime(source_file) != os.path.getmtime(destination_file):
                        shutil.copy2(source_file, destination_file)
                        os.remove(source_file)
                        log_entry = f"Updated and removed source file {source_file} as it already exists in the destination"
                    else:
                        os.remove(source_file)
                        log_entry = f"Removed source file {source_file} as it already exists in the destination"
                log.append(log_entry)
                print(log_entry)

        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file_name = f"move_log_{current_time}.txt"
        log_file_path = os.path.join(os.path.dirname(config_file_path), log_file_name)
        save_log(log, log_file_path)

        print(f"Successfully moved {file_count} files from {source_path} to {destination_path}")
        print(f"Log saved to: {log_file_path}")

        # Remove empty subdirectories in the source path
        for root, dirs, files in os.walk(source_path, topdown=False):
            for directory in dirs:
                directory_path = os.path.join(root, directory)
                if directory not in ['Recordings', 'Databases'] and not os.listdir(directory_path):
                    os.rmdir(directory_path)
                    print(f"Removed empty directory: {directory_path}")

    except Exception as e:
        print(f"Error moving files: {str(e)}")

def save_log(log, log_file_path):
    with open(log_file_path, "w") as file:
        for log_entry in log:
            file.write(f"{log_entry}\n")

def select_source_path():
    source_path = filedialog.askdirectory()
    source_entry.delete(0, tk.END)
    source_entry.insert(0, source_path)

def select_destination_path():
    destination_path = filedialog.askdirectory()
    destination_entry.delete(0, tk.END)
    destination_entry.insert(0, destination_path)

def save_paths():
    source_path = source_entry.get()
    destination_path = destination_entry.get()
    with open("path_config.txt", "w") as file:
        file.write(f"Source Path: {source_path}\n")
        file.write(f"Destination Path: {destination_path}\n")
    print("Paths saved successfully.")

def execute_move():
    threading.Thread(target=move_files, args=(progress_var,)).start()

# Create GUI window
window = tk.Tk()
window.title("Move MP3 Files")
window.geometry("400x300")

# Source path selection
source_label = tk.Label(window, text="Source Path:")
source_label.pack()

source_frame = tk.Frame(window)
source_frame.pack()

source_entry = tk.Entry(source_frame, width=40)
source_entry.pack(side=tk.LEFT)

source_button = tk.Button(source_frame, text="Select", command=select_source_path)
source_button.pack(side=tk.LEFT)

# Destination path selection
destination_label = tk.Label(window, text="Destination Path:")
destination_label.pack()

destination_frame = tk.Frame(window)
destination_frame.pack()

destination_entry = tk.Entry(destination_frame, width=40)
destination_entry.pack(side=tk.LEFT)

destination_button = tk.Button(destination_frame, text="Select", command=select_destination_path)
destination_button.pack(side=tk.LEFT)

# Save paths button
save_button = tk.Button(window, text="Save Paths", command=save_paths)
save_button.pack()

# Progress bar
progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(window, length=300, mode="determinate", variable=progress_var)
progress_bar.pack(pady=10)

# Execute button
def execute_move():
    threading.Thread(target=move_files, args=(progress_var,)).start()

execute_button = tk.Button(window, text="Execute", command=execute_move)
execute_button.pack(pady=10)

# Open log button
def open_log():
    log_file_name = f"move_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    log_file_path = os.path.join(os.path.dirname(__file__), log_file_name)
    if os.path.exists(log_file_path):
        try:
            subprocess.Popen(['notepad.exe', log_file_path])
        except OSError:
            webbrowser.open(log_file_path)
    else:
        print("Log file not found.")

open_log_button = tk.Button(window, text="Open Log", command=open_log)
open_log_button.pack()

# Start GUI event loop
window.mainloop()

import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import threading
from datetime import datetime

def move_mp3_files(progress_var):
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
                if file.endswith(".mp3"):
                    source_file = os.path.join(root, file)
                    parent_directory = file.split("~")[0]
                    relative_path = os.path.relpath(root, source_path)
                    destination_subdirectories = os.path.join(destination_path, parent_directory, relative_path)
                    destination_file = os.path.join(destination_subdirectories, file)

                    if not os.path.exists(destination_subdirectories):
                        os.makedirs(destination_subdirectories, exist_ok=True)

                    if not os.path.exists(destination_file):
                        shutil.move(source_file, destination_file)
                        file_count += 1
                        progress = int((file_count / total_files) * 100)
                        progress_var.set(progress)
                        log_entry = f"Moved {source_file} to {destination_file}"
                        log.append(log_entry)
                        print(log_entry)
                    else:
                        log_entry = f"Destination file {destination_file} already exists. Skipped moving."
                        log.append(log_entry)
                        print(log_entry)

        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file_name = f"move_log_{current_time}.txt"
        log_file_path = os.path.join("D:\Projects\move-audio", log_file_name)
        save_log(log, log_file_path)

        print(f"Successfully moved {file_count} files from {source_path} to {destination_path}")
        print(f"Log saved to: {log_file_path}")

        # Remove empty subdirectories in the source path
        for root, dirs, files in os.walk(source_path, topdown=False):
            for directory in dirs:
                directory_path = os.path.join(root, directory)
                if not os.listdir(directory_path):
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
        file.write(f"Destination Path: {destination_path}")
    print("Paths saved successfully.")

def execute_move():
    threading.Thread(target=move_mp3_files, args=(progress_var,)).start()

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
execute_button = tk.Button(window, text="Execute", command=execute_move)
execute_button.pack(pady=10)

def open_log():
    log_file_name = f"move_log_{datetime.now().strftime('%Y-%m-%d')}.txt"
    log_file_path = os.path.join("D:\Projects\move-audio", log_file_name)
    if os.path.exists(log_file_path):
        os.startfile(log_file_path)
    else:
        print("Log file not found.")

# Open log button
open_log_button = tk.Button(window, text="Open Log", command=open_log)
open_log_button.pack()

# Start GUI event loop
window.mainloop()

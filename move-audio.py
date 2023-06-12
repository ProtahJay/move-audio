import os
import shutil

def copy_mp3_files(source_path, destination_path):
    try:
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
                        shutil.copy2(source_file, destination_file)
                        print(f"Copied {source_file} to {destination_file}")
                    else:
                        print(f"Destination file {destination_file} already exists. Skipped copying.")
        
        print(f"Successfully copied files from {source_path} to {destination_path}")
    except Exception as e:
        print(f"Error copying files: {str(e)}")

# Example usage
source_path = r"D:\move-audio\recorder\D\Recordings"
destination_path = r"D:\move-audio\storage\audiostore\Vericore\Intake\2023\Primary"

print(f"Source path: {source_path}")
print(f"Destination path: {destination_path}")

copy_mp3_files(source_path, destination_path)

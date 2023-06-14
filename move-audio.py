import os
import shutil

def move_mp3_files(source_path, destination_path):
    try:
        for root, dirs, files in os.walk(source_path):
             # Exclude specific directory
            if "Prelog" in dirs:
                dirs.remove("Prelog")
                
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
                        print(f"Moved {source_file} to {destination_file}")
                    else:
                        print(f"Destination file {destination_file} already exists. Skipped moving.")
        
        print(f"Successfully moved files from {source_path} to {destination_path}")

        # Remove empty subdirectories in the source path
        for root, dirs, files in os.walk(source_path, topdown=False):
            for directory in dirs:
                directory_path = os.path.join(root, directory)
                if not os.listdir(directory_path):
                    os.rmdir(directory_path)
                    print(f"Removed empty directory: {directory_path}")

    except Exception as e:
        print(f"Error moving files: {str(e)}")

# Example usage
source_path = r"D:\move-audio\recorder\D\Recordings"
destination_path = r"D:\move-audio\storage\audiostore\Vericore\Intake\2023\Primary"

print(f"Source path: {source_path}")
print(f"Destination path: {destination_path}")

move_mp3_files(source_path, destination_path)

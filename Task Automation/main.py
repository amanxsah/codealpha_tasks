import os
import shutil
import time

# Define the folder to be organized (change this to your folder path)
FOLDER_PATH = '/Users/aman/Documents/TEMPORARY FILE/Python'

# File categories (extensions) for organizing
FILE_CATEGORIES = {
    'Documents': ['.pdf', '.txt', '.docx', '.xlsx', '.pptx'],
    'Images': ['.jpeg', '.jpg', '.png', '.gif'],
    'Videos': ['.mp4', '.mkv', '.avi', '.mov'],
    'Audio': ['.mp3', '.wav', '.flac'],
    'Archives': ['.zip', '.tar', '.rar'],
    'Others': []
}

# Function to organize files based on their extension
def organize_files():
    # Check if the specified folder exists
    if not os.path.exists(FOLDER_PATH):
        print(f"Error: The directory {FOLDER_PATH} does not exist.")
        return

    # Go through each file in the directory
    for filename in os.listdir(FOLDER_PATH):
        file_path = os.path.join(FOLDER_PATH, filename)

        # Skip if it's a folder
        if os.path.isdir(file_path):
            continue

        # Get the file extension
        file_extension = os.path.splitext(filename)[1].lower()

        # Find the corresponding category for the file
        categorized = False
        for category, extensions in FILE_CATEGORIES.items():
            if file_extension in extensions:
                categorized = True
                category_folder = os.path.join(FOLDER_PATH, category)
                
                # Create the category folder if it doesn't exist
                if not os.path.exists(category_folder):
                    os.makedirs(category_folder)
                
                # Move the file to the appropriate category folder
                try:
                    shutil.move(file_path, os.path.join(category_folder, filename))
                    print(f"Moved {filename} to {category}")
                except Exception as e:
                    print(f"Error moving {filename}: {e}")
                break
        
        # If the file doesn't match any category, move it to 'Others'
        if not categorized:
            others_folder = os.path.join(FOLDER_PATH, 'Others')
            if not os.path.exists(others_folder):
                os.makedirs(others_folder)

            try:
                shutil.move(file_path, os.path.join(others_folder, filename))
                print(f"Moved {filename} to Others")
            except Exception as e:
                print(f"Error moving {filename}: {e}")


# Function to clean up empty folders (optional)
def clean_empty_folders():
    # Walk through the directory and clean empty folders
    for dirpath, dirnames, filenames in os.walk(FOLDER_PATH, topdown=False):
        for dirname in dirnames:
            folder_path = os.path.join(dirpath, dirname)
            if not os.listdir(folder_path):  # Check if folder is empty
                try:
                    os.rmdir(folder_path)
                    print(f"Removed empty folder: {folder_path}")
                except Exception as e:
                    print(f"Error removing folder {folder_path}: {e}")


# Function to log the task completion
def log_task():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    log_file = os.path.join(FOLDER_PATH, 'file_organizer_log.txt')
    with open(log_file, 'a') as f:
        f.write(f"Task completed at: {current_time}\n")

    print(f"Task log written to {log_file}")


# Main function to execute the file organization task
def main():
    print("Starting the file organization task...")

    # Organize files
    organize_files()

    # Clean up empty folders
    clean_empty_folders()

    # Log the task completion
    log_task()

    print("File organization completed!")


if __name__ == "__main__":
    main()

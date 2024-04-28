import os
import re
import shutil

def rename_directories(root_dir):
    """Function to rename directories."""
    for dir_name in os.listdir(root_dir):
        original_path = os.path.join(root_dir, dir_name)
        if os.path.isdir(original_path):
            # Extract chapter number using regular expression
            match = re.search(r'(chap|chuong)-(\d+)', dir_name)
            if match:
                chapter_number = match.group(2)
                new_name = f"chuong-{chapter_number}"
                new_path = os.path.join(root_dir, new_name)
                shutil.move(original_path, new_path)
                print(f"Renamed directory '{dir_name}' to '{new_name}'")

if __name__ == "__main__":
    root_directory = input("Enter the root directory path: ")
    rename_directories(root_directory)

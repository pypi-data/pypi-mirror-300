import os
import shutil


def delete_folder_and_contents(folder_path: str):
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        shutil.rmtree(folder_path)
        print(f"Successfully deleted the folder and all its contents: {folder_path}")
    else:
        print(f"The folder does not exist or is not a directory: {folder_path}")
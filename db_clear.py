# =========================
#  Module: Vector DB Clear
# =========================
import box
import yaml
import os

# Import config vars
with open('config/config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))

def delete_files_and_clear_content(folder_path, file_to_clear):
    try:
        # Get a list of all files in the folder
        files = os.listdir(folder_path)

        # Loop through the list and delete each file
        for file in files:
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"{file} deleted successfully.")
        
        print(f"All files in '{folder_path}' have been deleted.")
    except FileNotFoundError:
        print(f"Folder not found at path: {folder_path}")
    
    # Clear the contents of the specified file
    try:
        with open(file_to_clear, 'w') as clear_file:
            clear_file.truncate(0)
        print(f"Contents of '{file_to_clear}' cleared successfully.")
    except FileNotFoundError:
        print(f"{file_to_clear} not found.")

if __name__ == "__main__":
    folder_path = cfg.DB_FAISS_PATH
    file_to_clear = os.path.join(cfg.DATA_PATH, cfg.LOG_FILE)
    
    delete_files_and_clear_content(folder_path, file_to_clear)
import os
import time
import json
import shutil
from datetime import timedelta

def setup_log_file():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    log_dir = os.path.join(script_dir, 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_filename = f"clean_directories_{time.strftime('%Y-%m-%d')}.txt"
    log_file = os.path.join(log_dir, log_filename)
    
    return log_file

def load_config(local_config_file='config.json'):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, local_config_file)

    with open(config_file, 'r') as file:
        config = json.load(file)
    directories = {}
    for path, ttl_days in config["directories"].items():
        ttl = timedelta(days=ttl_days)
        if '*' in path:
            base_dir = path.rstrip('*')
            # Expand wildcard by getting all immediate subdirectories
            for subdir in next(os.walk(base_dir))[1]:
                directories[os.path.join(base_dir, subdir)] = ttl
        else:
            directories[path] = ttl
    return directories

def remove_old_files(directory, ttl):
    now = time.time()
    items_deleted = 0
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        # Check if it's a file or directory
        if os.path.isfile(file_path):
            file_mtime = os.path.getmtime(file_path)
            if now - file_mtime > ttl.total_seconds():
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
                items_deleted += 1
        elif os.path.isdir(file_path):
            # Optionally remove the directory if it's empty
            child_items_deleted = remove_old_files(file_path, ttl)
            items_deleted += child_items_deleted
            if not os.listdir(file_path):
                shutil.rmtree(file_path)
                print(f"Deleted directory: {file_path}")
                items_deleted += 1

    return items_deleted

def log(log_file, message):
    log_message = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}" if message != "" else ""
    
    print(log_message)

    with open(log_file, 'a') as f:
        f.write(log_message + '\n')

def log_deleted_items(log_file, items_deleted):
    if items_deleted > 0:
        log(log_file, f"{items_deleted} items deleted.")
    else:
        log(log_file, "No items deleted.")
    log(log_file, "")

def clean_directories(log_file, directories):
    log(log_file, f"Start cleaning directories.\n")
    for directory, ttl in directories.items():
        log(log_file, f"Checking directory: '{directory}'")
        if os.path.exists(directory):
            items_deleted = remove_old_files(directory, ttl)
            log(log_file, f"Checked directory: {directory}.")
            log_deleted_items(log_file, items_deleted)
        else:
            print(f"Directory {directory} does not exist")
    log(log_file, "")
    log(log_file, "")

def main():
    log_file = setup_log_file()
    directories = load_config()
    clean_directories(log_file, directories)

if __name__ == "__main__":
    main()

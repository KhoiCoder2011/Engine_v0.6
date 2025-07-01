import os
import shutil

def delete_cache(directory = "."):
    for root, dirs, _ in os.walk(directory):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                cache_path = os.path.join(root, dir_name)
                shutil.rmtree(cache_path)


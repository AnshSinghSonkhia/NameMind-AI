import os
from pathlib import Path

def safe_rename(original_path, new_name):
    """Rename file without overwriting"""
    parent = Path(original_path).parent
    ext = Path(original_path).suffix
    counter = 1
    
    while True:
        new_path = parent / f"{new_name}{ext}"
        if not new_path.exists():
            break
        new_path = parent / f"{new_name}_{counter}{ext}"
        counter += 1
    
    os.rename(original_path, new_path)
    return new_path
import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path
from content_extractor import extract_text, analyze_image
from filename_generator import generate_name
from utils import safe_rename

import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# from transformers.utils import HF_TIMEOUT
# HF_TIMEOUT = 600  # 10 minutes timeout (default is 10 seconds)

# def analyze_image(filepath):
#     classifier = pipeline("image-classification", 
#                           model="google/vit-base-patch16-224",
#                           device_map="auto",  # Use GPU if available
#                           timeout=600)  # 10 minutes
                          
def analyze_image(filepath):
    from transformers import pipeline
    try:
        classifier = pipeline(
            "image-classification", 
            model="google/vit-base-patch16-224", 
            timeout=600  # 10 minutes
        )
        results = classifier(filepath)
        return [result['label'] for result in results[:3]]  # Top 3 labels
    except Exception as e:
        print(f"Image analysis failed: {str(e)}")
        return []

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # self.title("AI File Renamer")
        self.title("NameMind AI - Let AI name your files")
        self.geometry("800x600")
        
        # Widgets
        self.btn_select = ttk.Button(self, text="Select Files", command=self.select_files)
        self.btn_select.pack(pady=10)
        
        self.progress = ttk.Progressbar(self, mode='determinate')
        self.progress.pack(fill='x', padx=20)
        
        self.log = tk.Text(self, wrap=tk.WORD)
        self.log.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.btn_start = ttk.Button(self, text="Start Renaming", command=self.start_process)
        self.btn_start.pack(pady=10)
        
        self.files = []
    
    def select_files(self):
        self.files = filedialog.askopenfilenames()
        self.log.insert(tk.END, f"Selected {len(self.files)} files\n")
    
    def start_process(self):
        self.progress['value'] = 0
        total = len(self.files)
        
        for idx, filepath in enumerate(self.files):
            try:
                # Analyze file
                text = extract_text(filepath)
                image_labels = []
                if filepath.lower().endswith(('.png', '.jpg', '.jpeg')):
                    image_labels = analyze_image(filepath)
                
                # Generate name
                new_name = generate_name(text, image_labels)
                new_path = safe_rename(filepath, new_name)
                
                # Update log
                self.log.insert(tk.END, 
                    f"Renamed: {Path(filepath).name} → {new_path.name}\n")
                
            except Exception as e:
                self.log.insert(tk.END, f"Error: {str(e)}\n")
            
            # Update progress
            self.progress['value'] = (idx + 1) / total * 100
            self.update_idletasks()

if __name__ == "__main__":
    app = App()
    app.mainloop()
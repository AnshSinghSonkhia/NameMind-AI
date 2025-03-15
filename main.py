import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from PIL import Image, ImageTk
from pathlib import Path
import sys
import os
from content_extractor import extract_text, analyze_image
from filename_generator import generate_name
from utils import safe_rename

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# from transformers.utils import HF_TIMEOUT
# HF_TIMEOUT = 600  # 10 minutes timeout (default is 10 seconds)

# def analyze_image(filepath):
#     classifier = pipeline("image-classification", 
#                           model="google/vit-base-patch16-224",
#                           device_map="auto",  # Use GPU if available
#                           timeout=600)  # 10 minutes
         
def resource_path(relative_path):
    """Get the absolute path to a resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


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

# class App(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         # self.title("AI File Renamer")
#         self.title("NameMind AI - Let AI name your files")
#         self.geometry("800x600")
        
#         # Widgets
#         self.btn_select = ttk.Button(self, text="Select Files", command=self.select_files)
#         self.btn_select.pack(pady=10)
        
#         self.progress = ttk.Progressbar(self, mode='determinate')
#         self.progress.pack(fill='x', padx=20)
        
#         self.log = tk.Text(self, wrap=tk.WORD)
#         self.log.pack(fill='both', expand=True, padx=20, pady=10)
        
#         self.btn_start = ttk.Button(self, text="Start Renaming", command=self.start_process)
#         self.btn_start.pack(pady=10)
        
#         self.files = []
    
#     def select_files(self):
#         self.files = filedialog.askopenfilenames()
#         self.log.insert(tk.END, f"Selected {len(self.files)} files\n")
    
#     def start_process(self):
#         self.progress['value'] = 0
#         total = len(self.files)
        
#         for idx, filepath in enumerate(self.files):
#             try:
#                 # Analyze file
#                 text = extract_text(filepath)
#                 image_labels = []
#                 if filepath.lower().endswith(('.png', '.jpg', '.jpeg')):
#                     image_labels = analyze_image(filepath)
                
#                 # Generate name
#                 new_name = generate_name(text, image_labels)
#                 new_path = safe_rename(filepath, new_name)
                
#                 # Update log
#                 self.log.insert(tk.END, 
#                     f"Renamed: {Path(filepath).name} → {new_path.name}\n")
                
#             except Exception as e:
#                 self.log.insert(tk.END, f"Error: {str(e)}\n")
            
#             # Update progress
#             self.progress['value'] = (idx + 1) / total * 100
#             self.update_idletasks()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NameMind AI")
        self.subtitle = tk.Label(
            self,
            text="Let AI name your files",
            font=("Helvetica", 16),
            bg="#2E3440",
            fg="#D8DEE9"  # Light text
        )
        self.subtitle.pack(pady=5)
        self.geometry("800x600")
        self.configure(bg="#2E3440")  # Dark background

        # Load logo
        # self.logo = Image.open("logo.png")  # Replace with your logo path
        logo_path = resource_path("logo.png")
        self.logo = Image.open(logo_path)
        self.logo = self.logo.resize((100, 100), Image.Resampling.LANCZOS)
        self.logo = ImageTk.PhotoImage(self.logo)

        # Create UI
        self.create_ui()

    def create_ui(self):
        # Header Frame
        header_frame = tk.Frame(self, bg="#2E3440")
        header_frame.pack(pady=20)

        # Logo
        logo_label = tk.Label(header_frame, image=self.logo, bg="#2E3440")
        logo_label.pack(side=tk.LEFT, padx=10)

        # App Name
        app_name = tk.Label(
            header_frame,
            text="NameMind AI",
            font=("Helvetica", 24, "bold"),
            bg="#2E3440",
            fg="#ECEFF4"  # Light text
        )
        app_name.pack(side=tk.LEFT)

        # File Selection Button
        self.btn_select = ttk.Button(
            self,
            text="Select Files",
            command=self.select_files,
            style="Accent.TButton"
        )
        self.btn_select.pack(pady=10)

        # Progress Bar
        self.progress = ttk.Progressbar(
            self,
            mode="determinate",
            length=600,
            style="Horizontal.TProgressbar"
        )
        self.progress.pack(pady=10)

        # Log/Preview Area
        self.log = scrolledtext.ScrolledText(
            self,
            wrap=tk.WORD,
            font=("Helvetica", 12),
            bg="#3B4252",  # Dark background
            fg="#ECEFF4",  # Light text
            height=10
        )
        self.log.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Start Button
        self.btn_start = ttk.Button(
            self,
            text="Start Renaming",
            command=self.start_process,
            style="Accent.TButton"
        )
        self.btn_start.pack(pady=10)

        # Configure Styles
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Modern theme
        self.style.configure("Accent.TButton", font=("Helvetica", 12), background="#5E81AC", foreground="white")  # Blue button
        self.style.map("Accent.TButton", background=[("active", "#81A1C1")])  # Hover effect
        self.style.configure("Horizontal.TProgressbar", thickness=20, background="#5E81AC")  # Blue progress bar

    def select_files(self):
        self.files = filedialog.askopenfilenames()
        self.log.insert(tk.END, f" 📁 Selected {len(self.files)} files\n\n")

    def start_process(self):
        self.progress["value"] = 0
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
                self.log.insert(tk.END, f" ✅ {Path(filepath).name} → {new_path.name}\n\n")
                
            except Exception as e:
                self.log.insert(tk.END, f" ❌ Error: {str(e)}\n\n")
            
            # Update progress
            self.progress["value"] = (idx + 1) / total * 100
            self.update_idletasks()

if __name__ == "__main__":
    app = App()
    app.mainloop()

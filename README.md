# NameMind AI

![▶️ Watch the Demo Video](https://github.com/AnshSinghSonkhia/NameMind-AI/blob/main/NameMindAI%20Product%20Demo%20(2).gif)


## Set Up Virtual Environment

> Create and activate virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

## Install Dependencies

> Install the required packages:

```powershell
pip install -r requirements.txt
```

```powershell
pip install torch transformers keybert pillow pytesseract PyPDF2 pdfplumber python-docx
```

## Run the Application

> Use the following command to run the application:

```powershell
python main.py
```

## Download tesseract

Install Tesseract OCR:

Download from `UB-Mannheim/tesseract`.
[UB-Mannheim/tesseract](https://github.com/tesseract-ocr/tesseract/releases/download/5.5.0/tesseract-ocr-w64-setup-5.5.0.20241111.exe)

Add Tesseract to your system PATH (e.g., C:\Program Files\Tesseract-OCR\tesseract.exe).

# Steps

Here's a step-by-step guide to package your AI Files Renamer (Namemind AI) as **standalone Windows software** that users can download and install without needing Python or technical setup:

---

### **Step 1: Finalize the Code**
Ensure your code:
- Uses **relative paths** (no hardcoded `C:\Program Files`)
- Handles errors gracefully
- Includes all dependencies in the project folder

---

### **Step 2: Create an Executable (.exe)**
Use **PyInstaller** to package the Python code into a standalone `.exe`:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Create a `build.spec` file:
   ```python
   # build.spec
   block_cipher = None

   a = Analysis(
       ['main.py'],
       pathex=[],
       binaries=[],
       datas=[
           ('utils.py', '.'),
           ('content_extractor.py', '.'),
           ('filename_generator.py', '.')
       ],
       hiddenimports=[
           'transformers.models.vit',
           'torch',
           'pytesseract',
           'docx',
           'pdfplumber'
       ],
       hookspath=[],
       hooksconfig={},
       runtime_hooks=[],
       excludes=[],
       win_no_prefer_redirects=False,
       win_private_assemblies=False,
       cipher=block_cipher,
       noarchive=False,
   )
   pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

   exe = EXE(
       pyz,
       a.scripts,
       a.binaries,
       a.zipfiles,
       a.datas,
       [],
       name='AI_Renamer',
       debug=False,
       bootloader_ignore_signals=False,
       strip=False,
       upx=True,
       upx_exclude=[],
       runtime_tmpdir=None,
       console=False,  # Set to True for debugging
       icon='icon.ico'  # Optional: Add an icon file
   )
   ```

3. Build the executable:
   ```bash
   pyinstaller build.spec
   ```

---

### **Step 3: Bundle Tesseract OCR**
1. Download the **portable Tesseract OCR** for Windows:
   - [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki) (choose the `zip` version)
   - Extract it to `AI_Renamer/tesseract/`

2. Modify your code to use the local Tesseract:
   ```python
   # content_extractor.py
   pytesseract.pytesseract.tesseract_cmd = os.path.join(
       os.path.dirname(__file__), 'tesseract', 'tesseract.exe'
   )
   ```

---

### **Step 4: Create an Installer**
Use **Inno Setup** to create a professional installer:

1. Download [Inno Setup](https://jrsoftware.org/isdl.php)

2. Create an installer script `AI_Renamer.iss`:
   ```iss
   [Setup]
   AppName=AI Renamer
   AppVersion=1.0
   DefaultDirName={pf}\AI Renamer
   OutputDir=.\Output
   OutputBaseFilename=AI_Renamer_Setup
   Compression=lzma2
   SolidCompression=yes
   SetupIconFile=icon.ico

   [Files]
   Source: "dist\AI_Renamer\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs
   Source: "tesseract\*"; DestDir: "{app}\tesseract"; Flags: ignoreversion recursesubdirs

   [Icons]
   Name: "{group}\AI Renamer"; Filename: "{app}\AI_Renamer.exe"
   Name: "{commondesktop}\AI Renamer"; Filename: "{app}\AI_Renamer.exe"

   [Run]
   Filename: "{app}\AI_Renamer.exe"; Description: "Launch AI Renamer"; Flags: postinstall nowait
   ```

3. Build the installer:
   - Open `AI_Renamer.iss` in Inno Setup
   - Click "Build" → Output will be in `Output/` folder

---

### **Step 5: Include AI Models**
Handle Hugging Face models (they’ll auto-download on first run):
```python
# filename_generator.py
from transformers import pipeline

def get_image_labels(image_path):
    try:
        # Models will auto-download to user's cache folder
        image_classifier = pipeline("image-classification", model="google/vit-base-patch16-224")
        result = image_classifier(image_path)
        return [item['label'] for item in result[:3]]
    except:
        return []
```

---

### **Step 6: Test the Software**
1. Test on a **fresh Windows machine** without Python installed
2. Verify:
   - OCR works with bundled Tesseract
   - AI models download automatically
   - Files are renamed correctly

---

### **Step 7: Distribute**
1. Upload to a file-sharing platform:
   - [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
   - Google Drive/Dropbox
   - [SourceForge](https://sourceforge.net/)

2. Create a download page with:
   - Installer file (`AI_Renamer_Setup.exe`)
   - System requirements:
     ```
     - Windows 10/11
     - 4GB RAM (8GB recommended)
     - 500MB free disk space
     ```
   - Instructions for use

---

### Step 9: Package as EXE
Install PyInstaller if not done:

```powershell
pip install pyinstaller
```
Create executable:

```powershell
pyinstaller --onefile --windowed --icon=icon.ico main.py
```

The EXE will be in dist/ folder

---

### **Optional Enhancements**
1. **Code Signing**:
   - Sign your `.exe` with a certificate to avoid "Unknown Publisher" warnings
   - Providers: [Sectigo](https://www.sectigo.com/), [DigiCert](https://www.digicert.com/)

2. **Auto-Updates**:
   Use `requests` to check for new versions:
   ```python
   import requests
   def check_update():
       try:
           response = requests.get("https://api.yourdomain.com/version")
           return response.json()['latest_version']
       except:
           return None
   ```

3. **Custom Branding**:
   - Add a splash screen
   - Include a custom icon (`icon.ico`)

---

### **Final Folder Structure**
```
AI_Renamer/
├── dist/                   # PyInstaller output
├── tesseract/              # Bundled OCR engine
├── main.py                 # Main application
├── content_extractor.py
├── filename_generator.py
├── utils.py
├── build.spec
├── AI_Renamer.iss          # Inno Setup script
└── icon.ico               # Application icon
```

---

This approach ensures users get a **single-click installer** with all dependencies included. They won’t need Python or technical knowledge to use your AI Renamer! 🚀

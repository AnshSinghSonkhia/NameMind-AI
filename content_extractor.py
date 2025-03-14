import os
import sys
from PIL import Image
import pytesseract
import pdfplumber
import docx

def get_tesseract_path():
    """Get Tesseract path dynamically for both dev and production"""
    if getattr(sys, 'frozen', False):  # Running as bundled exe
        base_path = os.path.dirname(sys.executable)
    else:  # Running as script
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, "tesseract", "tesseract.exe")

# Set Tesseract path dynamically
pytesseract.pytesseract.tesseract_cmd = get_tesseract_path()

def extract_text(filepath):
    """Extract text from various file formats"""
    text = ""
    try:
        if filepath.lower().endswith(('.png', '.jpg', '.jpeg')):
            with Image.open(filepath) as img:
                text = pytesseract.image_to_string(img)
        elif filepath.lower().endswith('.pdf'):
            with pdfplumber.open(filepath) as pdf:
                text = " ".join([page.extract_text() or "" for page in pdf.pages])
        elif filepath.lower().endswith('.docx'):
            doc = docx.Document(filepath)
            text = " ".join([para.text for para in doc.paragraphs])
        elif filepath.lower().endswith(('.txt', '.py', '.js', '.html', '.css', '.md')):
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
    except Exception as e:
        print(f"Error extracting text: {str(e)}")
    return text.strip()

def analyze_image(filepath):
    """Analyze image content using AI"""
    from transformers import pipeline
    try:
        classifier = pipeline(
            "image-classification", 
            model="google/vit-base-patch16-224",
            timeout=600  # 10 minute timeout
        )
        results = classifier(filepath)
        return [result['label'] for result in results[:3]]  # Top 3 labels
    except Exception as e:
        print(f"Image analysis failed: {str(e)}")
        return []
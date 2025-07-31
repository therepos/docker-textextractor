import fitz
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
import os

def extract_text(path: str) -> str:
    ext = os.path.splitext(path)[-1].lower()
    if ext == ".pdf":
        return extract_from_pdf(path)
    elif ext in [".jpg", ".jpeg", ".png"]:
        return extract_from_image(path)
    else:
        return "Unsupported file type"

def extract_from_pdf(path: str) -> str:
    doc = fitz.open(path)
    text = "\n".join(page.get_text() for page in doc)
    if text.strip():
        return text.strip()
    images = convert_from_path(path)
    return "\n".join(pytesseract.image_to_string(img) for img in images)

def extract_from_image(path: str) -> str:
    img = Image.open(path)
    return pytesseract.image_to_string(img)

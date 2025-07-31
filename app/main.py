from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
import os
from app.extract import extract_text
from app.utils import save_file, generate_uid

app = FastAPI()
UPLOAD_DIR = "uploads"
EXPORT_DIR = "exports"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"message": "Text Extractor API", "version": "1.0"}

@app.post("/extract_and_download/")
async def extract_and_download(file: UploadFile = File(...)):
    uid = generate_uid()
    input_path = save_file(file, UPLOAD_DIR)
    text = extract_text(input_path)
    
    output_path = os.path.join(EXPORT_DIR, f"{uid}.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    return FileResponse(output_path, media_type="text/plain", filename=f"{uid}.txt")

@app.get("/export/{uid}")
def export_file(uid: str):
    path = os.path.join(EXPORT_DIR, f"{uid}.txt")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path, media_type="text/plain", filename=f"{uid}.txt")

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
from app.extract import extract_text

app = FastAPI()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"message": "Text Extractor is running."}

@app.post("/extract/")
async def extract(file: UploadFile = File(...)):
    input_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save uploaded file
    with open(input_path, "wb") as f:
        f.write(await file.read())

    try:
        # Extract text
        text = extract_text(input_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")

    # Write to a text file in same dir
    txt_path = os.path.splitext(input_path)[0] + ".txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)

    return FileResponse(txt_path, media_type="text/plain", filename=os.path.basename(txt_path))

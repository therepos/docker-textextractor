import os
import uuid
import shutil

def generate_uid() -> str:
    return uuid.uuid4().hex[:12]

def save_file(uploaded_file, dest_folder: str) -> str:
    os.makedirs(dest_folder, exist_ok=True)
    file_path = os.path.join(dest_folder, uploaded_file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)
    return file_path
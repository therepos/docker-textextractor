FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY app/ ./app
COPY app/requirements.txt .

RUN pip install --no-cache-dir -r app/requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.10-slim

WORKDIR /app

# Install system dependencies required by pyzbar, opencv, and easyocr
RUN apt-get update && apt-get install -y \
    libzbar0 \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to leverage Docker caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Start the FastAPI application
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}

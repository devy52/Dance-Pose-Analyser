FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1 \
    libavcodec-extra \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install "uvicorn[standard]"

# ↓↓↓ THIS IS THE IMPORTANT FIX ↓↓↓
RUN mkdir -p app/model && \
    wget -q https://storage.googleapis.com/mediapipe-models/pose_landmarker/heavy/float/pose_landmarker_heavy.task \
    -O app/model/pose_landmarker_heavy.task

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]

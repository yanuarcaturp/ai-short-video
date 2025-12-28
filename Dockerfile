FROM python:3.10-slim

# Install ffmpeg & yt-dlp
RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    pip install yt-dlp && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]


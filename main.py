from fastapi import FastAPI
from pydantic import BaseModel
import subprocess, uuid, os

app = FastAPI()

class VideoRequest(BaseModel):
    url: str
    duration: int = 30

@app.get("/")
def home():
    return {"status": "AI Short Video Backend Running"}

@app.post("/clip")
def clip_video(data: VideoRequest):
    os.makedirs("videos", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    video_path = f"videos/{uuid.uuid4()}.mp4"
    output_path = f"outputs/{uuid.uuid4()}.mp4"

    # Download video (YouTube / TikTok)
    subprocess.run([
        "yt-dlp",
        "-f", "mp4",
        "-o", video_path,
        data.url
    ], check=True)

    # Convert to short video
    subprocess.run([
        "ffmpeg", "-y",
        "-i", video_path,
        "-t", str(data.duration),
        "-vf", "scale=720:1280",
        output_path
    ], check=True)

    return {"output": output_path}
  
if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
    

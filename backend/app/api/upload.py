from fastapi import APIRouter, UploadFile, HTTPException
from app.tasks.video_tasks import process_video
import uuid
import os
import shutil

router = APIRouter()

# Define storage paths (relative to backend root)
VIDEO_DIR = "storage/videos"
os.makedirs(VIDEO_DIR, exist_ok=True)

@router.post("/upload")
async def upload_video(file: UploadFile):
    video_id = str(uuid.uuid4())
    video_filename = f"{video_id}.mp4" 
    video_path = os.path.join(VIDEO_DIR, video_filename)

    try:
        # Save uploaded file to disk
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save video file: {str(e)}")
    
    # Trigger async task with the absolute path or relative path
    # We use relative path here as worker is in same root
    process_video.delay(video_id, video_path)

    return {
        "video_id": video_id,
        "status": "processing started"
    }

from pydantic import BaseModel
from fastapi.responses import JSONResponse

class YouTubeURL(BaseModel):
    url: str

@router.post("/upload-url")
async def process_youtube_url(payload: YouTubeURL):
    """
    Downloads and processes a YouTube video from URL.
    """
    try:
        from app.services.youtube import download_audio_from_youtube
        
        # 1. Download (Video + Audio)
        # Note: blocking download for MVP simplicity
        result = download_audio_from_youtube(payload.url)
        
        video_id = result['video_id']
        file_path = result['file_path']
        
        # 2. Trigger standard processing
        process_video.delay(video_id, file_path)
        
        return {
            "video_id": video_id, 
            "status": "processing", 
            "message": f"YouTube video '{result['title']}' downloading/processing started"
        }
        
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

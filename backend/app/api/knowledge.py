from fastapi import APIRouter, HTTPException
import os
import json
from app.models.knowledge_schema import VideoKnowledge
from pydantic import BaseModel
from app.services.vector_db import get_vector_service

class IndexRequest(BaseModel):
    video_id: str
    chunks: list[dict]

router = APIRouter()

@router.get("/knowledge/{video_id}")
async def get_video_knowledge(video_id: str):
    """
    Retrieves the structured knowledge for a specific video.
    """
    # Construct path to knowledge file
    knowledge_path = f"storage/knowledge/{video_id}.json"
    
    if not os.path.exists(knowledge_path):
        raise HTTPException(status_code=404, detail="Knowledge not found. Video might still be processing.")
    
    try:
        with open(knowledge_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading knowledge file: {str(e)}")

@router.get("/knowledge")
async def list_videos():
    """
    Lists all processed videos with their metadata.
    """
    knowledge_dir = "storage/knowledge"
    if not os.path.exists(knowledge_dir):
        return []

    videos = []
    try:
        for filename in os.listdir(knowledge_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(knowledge_dir, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Extract summary metadata
                    videos.append({
                        "video_id": data.get("video_id"),
                        "title": f"Video {data.get('video_id')[:8]}...", # Fallback title
                        "subject": data.get("subject", "General"),
                        "difficulty": data.get("difficulty", "Intermediate"),
                        "topic_count": len(data.get("theory", [])),
                        "formula_count": len(data.get("formulas", []))
                    })
        return videos
    except Exception as e:
        print(f"Error listing videos: {e}")
        return []

@router.post("/knowledge/index")
async def index_knowledge(request: IndexRequest):
    """
    Internal endpoint to index chunks into Vector DB.
    This avoids multi-process locking issues by centralizing writes.
    """
    try:
        service = get_vector_service()
        service.upsert_chunks(request.video_id, request.chunks)
        return {"status": "success"}
    except Exception as e:
        print(f"Indexing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.chat_service import ask_video

router = APIRouter()

class ChatRequest(BaseModel):
    question: str
    video_id: str

@router.post("/chat")
async def chat_with_video(request: ChatRequest):
    """
    Asks a question to the video brain.
    """
    response = ask_video(request.video_id, request.question)
    
    if "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])
        
    return response

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api import upload, knowledge, chat
import os

app = FastAPI(title="VidSage API")

# Ensure storage directory exists
os.makedirs("storage", exist_ok=True)

# Mount static files
app.mount("/files", StaticFiles(directory="storage"), name="storage")

@app.on_event("startup")
async def startup_event():
    # Initialize VectorDB on startup
    from app.services.vector_db import get_vector_service
    get_vector_service()

app.include_router(upload.router, prefix="/api")
app.include_router(knowledge.router, prefix="/api")
app.include_router(chat.router, prefix="/api")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Backend running", "service": "VidSage API"}

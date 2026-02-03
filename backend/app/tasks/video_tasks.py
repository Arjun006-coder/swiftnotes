from app.core.celery_app import celery_app
from app.services.audio import extract_audio
from app.services.transcription import transcribe_audio
from app.services.chunking import chunk_segments
from app.services.knowledge_extractor import extract_knowledge
from app.services.knowledge_merger import merge_knowledge
import os
import json
import requests

@celery_app.task
def process_video(video_id: str, video_path: str):
    print(f"[{video_id}] Starting pipeline for {video_path}")
    
    # Define paths
    audio_path = f"storage/audio/{video_id}.wav"
    transcript_path = f"storage/transcripts/{video_id}.json"
    chunks_path = f"storage/chunks/{video_id}.json"
    knowledge_path = f"storage/knowledge/{video_id}.json"

    try:
        # 1. Extract Audio
        print(f"[{video_id}] Extracting audio...")
        extract_audio(video_path, audio_path)

        # 2. Transcribe
        print(f"[{video_id}] Transcribing...")
        segments = transcribe_audio(audio_path)

        # 3. Save Raw Transcript
        print(f"[{video_id}] Saving transcript...")
        os.makedirs(os.path.dirname(transcript_path), exist_ok=True)
        with open(transcript_path, "w", encoding="utf-8") as f:
            json.dump(segments, f, ensure_ascii=False, indent=2)

        # 4. Chunking
        print(f"[{video_id}] Chunking...")
        chunks = chunk_segments(segments)
        
        # 5. Save Chunks
        os.makedirs(os.path.dirname(chunks_path), exist_ok=True)
        with open(chunks_path, "w", encoding="utf-8") as f:
            json.dump(chunks, f, ensure_ascii=False, indent=2)

        # 6. Knowledge Extraction (Phase 4)
        print(f"[{video_id}] Extracting knowledge from {len(chunks)} chunks...")
        chunk_knowledge_list = []
        for i, chunk in enumerate(chunks):
            print(f"[{video_id}] Processing chunk {i+1}/{len(chunks)}")
            k_data = extract_knowledge(chunk["text"], chunk_id=i)
            chunk_knowledge_list.append(k_data)

        # 7. Merge & Normalize
        print(f"[{video_id}] Merging knowledge...")
        final_knowledge = merge_knowledge(chunk_knowledge_list, video_id)

        # 8. Save Knowledge Graph
        os.makedirs(os.path.dirname(knowledge_path), exist_ok=True)
        with open(knowledge_path, "w", encoding="utf-8") as f:
            json.dump(final_knowledge, f, ensure_ascii=False, indent=2)

        # 9. Index Knowledge (Vector DB)
        # 9. Index Knowledge (Vector DB)
        print(f"[{video_id}] Indexing knowledge via Internal API...")
        
        # Flatten knowledge for indexing
        chunks_to_index = []
        
        # Index Theory
        for item in final_knowledge.get("theory", []):
            text = f"Theory: {item['title']}\n{item['explanation']}"
            chunks_to_index.append({"text": text, "type": "theory"})
            
        # Index Formulas
        for item in final_knowledge.get("formulas", []):
            text = f"Formula: {item['name']}\nEquation: {item['equation']}\nUsage: {item['usage']}"
            chunks_to_index.append({"text": text, "type": "formula"})
            
        # Index Examples
        for item in final_knowledge.get("examples", []):
            text = f"Example: {item['problem']}\nSolution: {item['solution']}"
            chunks_to_index.append({"text": text, "type": "example"})
            
        # Send to API
        if chunks_to_index:
            try:
                response = requests.post(
                    "http://localhost:8000/api/knowledge/index",
                    json={"video_id": video_id, "chunks": chunks_to_index}
                )
                response.raise_for_status()
                print(f"[{video_id}] Indexing successful (API).")
            except Exception as e:
                print(f"[{video_id}] Indexing (API) failed: {e}")
                # We don't fail the whole pipeline if indexing fails, but we should log it.
                # Or maybe we SHOULD fail? Let's treat it as non-critical for now so user gets transcript.
                pass

        print(f"[{video_id}] Pipeline completed successfully.")
        return {
            "video_id": video_id,
            "status": "completed",
            "chunks_count": len(chunks),
            "knowledge_items": len(final_knowledge.get("theory", []))
        }

    except Exception as e:
        print(f"[{video_id}] Pipeline failed: {e}")
        return {
            "video_id": video_id,
            "status": "failed",
            "error": str(e)
        }

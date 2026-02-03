import json
import os
from app.services.llm_factory import get_llm_service
from app.models.knowledge_schema import ChunkKnowledge

# Load prompt once
PROMPT_PATH = os.path.join(os.path.dirname(__file__), "../prompts/knowledge_extraction.txt")
with open(PROMPT_PATH, "r") as f:
    KNOWLEDGE_PROMPT = f.read()

def extract_knowledge(chunk_text: str, chunk_id: int) -> dict:
    """
    Extracts structured knowledge from a single text chunk using the configured LLM.
    Returns a dict matching ChunkKnowledge schema.
    """
    llm = get_llm_service()
    
    # Format prompt
    # Use replace() instead of format() because the prompt contains 
    # JSON curly braces {} which confuse str.format()
    final_prompt = KNOWLEDGE_PROMPT.replace("{text}", chunk_text)
    
    try:
        # Call LLM
        response_json_str = llm.generate(prompt=final_prompt, temperature=0.2)
        
        # Parse JSON
        data = json.loads(response_json_str)
        
        # Validate against schema (optional but recommended)
        # We perform soft validation here to ensure structure exists
        # In a strict environment, we'd use ChunkKnowledge(**data)
        
        return {
            "chunk_id": chunk_id,
            "theory": data.get("theory", []),
            "formulas": data.get("formulas", []),
            "examples": data.get("examples", []),
            "key_points": data.get("key_points", [])
        }
    except Exception as e:
        print(f"Error extracting knowledge for chunk {chunk_id}: {e}")
        # Return empty structure on failure to keep pipeline moving
        return {
            "chunk_id": chunk_id,
            "theory": [],
            "formulas": [],
            "examples": [],
            "key_points": [] 
        }

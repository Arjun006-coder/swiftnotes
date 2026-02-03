from typing import List, Dict
from app.models.knowledge_schema import VideoKnowledge, ChunkKnowledge, TheoryPoint, Formula

def merge_knowledge(chunks_data: List[dict], video_id: str) -> dict:
    """
    Merges knowledge from multiple chunks into a single coherent structure.
    Deduplicates theory and formulas.
    """
    merged_theory: Dict[str, TheoryPoint] = {}
    merged_formulas: Dict[str, Formula] = {}
    all_examples = []
    cheat_sheet_candidates = []

    for chunk in chunks_data:
        # 1. Merge Theory (Deduplicate by title)
        for item in chunk.get("theory", []):
            title = item["title"].strip()
            # Simple dedupe: if title exists, maybe append explanation or skip
            # For now, we skip if already present to avoid noise
            if title.lower() not in merged_theory:
                merged_theory[title.lower()] = item

        # 2. Merge Formulas (Deduplicate by name)
        for item in chunk.get("formulas", []):
            name = item["name"].strip()
            if name.lower() not in merged_formulas:
                merged_formulas[name.lower()] = item

        # 3. Collect Examples (Keep all, they are usually unique)
        if "examples" in chunk:
            all_examples.extend(chunk["examples"])

        # 4. Collect Practical Scenarios
        if "practical" in chunk:
             # Add to examples or keep separate? Let's keep separate in the final object 
             # but we need to update VideoKnowledge schema too (implicitly handled by dict)
             # Wait, VideoKnowledge is a Pydantic model effectively in types.ts too.
             # I need to ensure the backend dict reflects `VideoKnowledge` structure if I validated it.
             # `knowledge_merger` returns a dict, but `knowledge.py` might validate it?
             # Let's check `VideoKnowledge` in schema first.
             pass 

        # 5. Collect Key Points for Cheat Sheet
        if "key_points" in chunk:
            cheat_sheet_candidates.extend(chunk["key_points"])

    # Collect all practicals (simple aggregation)
    all_practical = []
    for chunk in chunks_data:
        if "practical" in chunk:
            all_practical.extend(chunk["practical"])

    # Format result
    final_output = {
        "video_id": video_id,
        "difficulty": "Intermediate", # Placeholder logic
        "subject": "General",        # Placeholder logic
        "chunks": chunks_data,       # Keep original chunk references
        "theory": list(merged_theory.values()),
        "formulas": list(merged_formulas.values()),
        "examples": all_examples,
        "practical": all_practical,
        "cheat_sheet": cheat_sheet_candidates[:20] # Limit to top 20 points
    }

    return final_output

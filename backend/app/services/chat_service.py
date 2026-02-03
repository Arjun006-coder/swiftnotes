import json
import os
from app.services.llm_factory import get_llm_service
from app.services.vector_db import get_vector_service

# Hybrid Prompt: Prioritize Context > General Knowledge
CHAT_PROMPT = """You are a helpful AI tutor assistant.
Your goal is to answer the user's question.

Video Context:
{retrieved_context}

User Question:
{user_question}

Instructions:
1. **PRIORITY**: Check the "Video Context" first. If the answer is there (e.g., a specific definition given in the video), use it and mention "According to the video...".
2. **FALLBACK**: If the video context is missing or irrelevant, use your own General Knowledge to answer helpfuly.
3. **CLARITY**: If answering from General Knowledge, briefly mention that this extra info wasn't found in the video.
"""

def search_rag(question: str, video_id: str) -> str:
    """
    Semantic search using Vector DB.
    Returns best matches or empty string.
    """
    try:
        vector_service = get_vector_service()
        
        # Lower threshold to catch loose relevance, but don't block
        results = vector_service.search(
            query=question, 
            limit=5, 
            score_threshold=0.2 
        )
        
        # Filter by video_id
        relevant_texts = []
        for hit in results:
            if hit['video_id'] == video_id:
                relevant_texts.append(f"[{hit['type'].upper()}] {hit['text']}")

        if not relevant_texts:
            return ""
            
        return "\n\n".join(relevant_texts)
    except Exception as e:
        print(f"Vector Search Error: {e}")
        return "" # Fallback to empty context on error

def ask_video(video_id: str, question: str):
    """
    Orchestrates the Q&A process.
    """
    # 1. Retrieve (RAG) - No Hard Rule anymore
    context = search_rag(question, video_id)
    
    if not context:
        context = "No specific relevant segments found in the video. Please answer using General Knowledge."

    # 2. Generate
    llm = get_llm_service()
    final_prompt = CHAT_PROMPT.format(retrieved_context=context, user_question=question)
    
    try:
        # Increase temperature slightly for better general answers
        answer = llm.generate(final_prompt, temperature=0.4)
        sources = context[:500] + "..." if context and "No specific relevant" not in context else "General Knowledge"
        return {"answer": answer, "sources": sources}
    except Exception as e:
        return {"error": f"LLM Generation failed: {str(e)}"}
    except Exception as e:
        return {"error": f"LLM Generation failed: {str(e)}"}

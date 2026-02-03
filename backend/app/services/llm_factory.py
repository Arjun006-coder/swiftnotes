import os
import json
from typing import Any, Dict

class MockLLM:
    """
    A dummy LLM for testing without API keys.
    Returns static academic-looking data.
    """
    def generate(self, prompt: str, temperature: float = 0.2) -> str:
        # Heuristic: If prompt mentions "JSON", return the mock extraction structure
        if "JSON" in prompt or "schema" in prompt:
             return json.dumps({
                "theory": [
                    {"title": "Mock Concept A", "explanation": "This is a simulated explanation of concept A from the video."},
                    {"title": "Mock Concept B", "explanation": "This is a simulated explanation of concept B."}
                ],
                "formulas": [
                    {"name": "Mock Formula", "expression": "E = mc^2", "explanation": "Energy equals mass times speed of light squared."}
                ],
                "examples": [
                    {"question": "What is 2+2?", "solution": "4"}
                ],
                "key_points": ["Key point 1", "Key point 2"]
            })
        
        # Otherwise, assume it's a Chat request
        return "This is a mock answer from VidSage. I found relevant info in the notes regarding 'Mock Concept A'. The answer is 42."

import requests

class OllamaLLM:
    """
    Local Ollama implementation.
    Assumes Ollama is running on localhost:11434.
    """
    def __init__(self, model="llama3:8b"):
        self.model = model
        self.api_url = "http://localhost:11434/api/generate"

    def generate(self, prompt: str, temperature: float = 0.2) -> str:
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "temperature": temperature,
                "format": "json" if "JSON" in prompt else None 
            }
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            
            # Ollama returns 'response' field in the JSON body
            return response.json().get("response", "")
        except Exception as e:
            print(f"Ollama Error: {e}")
            return f"Error generating response from Ollama: {str(e)}"

class OpenAILLM:
    """
    Real OpenAI implementation.
    Requires OPENAI_API_KEY environment variable.
    """
    def __init__(self):
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        except ImportError:
            raise ImportError("openai package not installed. Run 'pip install openai'")
        except Exception as e:
             print(f"OpenAI Init Error: {e}")
             self.client = None

    def generate(self, prompt: str, temperature: float = 0.2) -> str:
        if not self.client:
             raise RuntimeError("OpenAI client not initialized.")
        
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content

def get_llm_service():
    """
    Factory to return the appropriate LLM service.
    Prioritize: OpenAI Key -> Ollama Local -> Mock Fallback
    """
    # Check for OpenAI Key first
    if os.getenv("OPENAI_API_KEY"):
        print("Using Cloud LLM: OpenAI")
        return OpenAILLM()
    
    # Check if Ollama is running (simple ping)
    try:
        requests.get("http://localhost:11434/")
        print("Using Local LLM: Ollama (llama3:8b)")
        return OllamaLLM(model="llama3:8b")
    except:
        print("WARNING: OpenAI Key missing AND Ollama not detected. Using MockLLM.")
        return MockLLM()

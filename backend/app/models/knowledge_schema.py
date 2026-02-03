from typing import List, Optional
from pydantic import BaseModel

class TheoryPoint(BaseModel):
    title: str
    explanation: str

class Formula(BaseModel):
    name: str
    expression: str
    explanation: Optional[str] = None

class Example(BaseModel):
    question: str
    solution: str

class PracticalScenario(BaseModel):
    description: str
    code_snippet: Optional[str] = None
    usage: str

class ChunkKnowledge(BaseModel):
    # We might not strictly need chunk_id in the LLM output, 
    # but it's good for the merger to know source.
    # Identifying it as Optional for LLM generation flexibility.
    theory: List[TheoryPoint]
    formulas: List[Formula]
    examples: List[Example]
    practical: List[PracticalScenario]
    key_points: List[str]

class VideoKnowledge(BaseModel):
    video_id: str
    subject: Optional[str] = None
    difficulty: Optional[str] = None
    chunks: List[ChunkKnowledge]
    practical: List[PracticalScenario] = []
    cheat_sheet: List[str]

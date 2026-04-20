from typing import List, Optional
from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str
    name: Optional[str] = None


class LLMRequest(BaseModel):
    messages: List[Message]
    temperature: float = 0.7
    stream: bool = True
    max_tokens: Optional[int] = None


class LLMResponse(BaseModel):
    success: bool
    content: str
    thought: Optional[str] = None
    error: Optional[str] = None

from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    role: str
    content: str

class ChatCreateRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    session_id: str
    history: List[Message]

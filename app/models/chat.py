from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Message(BaseModel):
    """Simple message model"""
    text: str
    is_user: bool
    timestamp: Optional[str] = None

class ChatHistory(BaseModel):
    """Simple chat history model"""
    role: str
    parts: List[dict]

class ChatRequest(BaseModel):
    """Simple chat request"""
    message: str
    session_id: Optional[str] = None
    history: Optional[List[Message]] = []

class ChatResponse(BaseModel):
    """Simple chat response"""
    message: str
    session_id: Optional[str] = None
    timestamp: str = datetime.now().isoformat()
    is_data_loaded: bool = True

class InitializeRequest(BaseModel):
    """Simple initialize request"""
    session_id: Optional[str] = None

class InitializeResponse(BaseModel):
    """Simple initialize response"""
    success: bool
    message: str
    session_id: Optional[str] = None

class ChatbotConfig(BaseModel):
    """Simple chatbot config"""
    name: str
    description: str

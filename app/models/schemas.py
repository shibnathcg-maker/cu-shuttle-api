from pydantic import BaseModel
from typing import Any, Optional

class StandardResponse(BaseModel):
    status: str
    message: str
    data: Any = None
    error: Optional[str] = None

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
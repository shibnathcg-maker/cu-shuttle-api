# app/routers/chat.py
from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.services.chat_service import chat_service

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        print(f"📨 Chat request: {req.message}")
        reply = await chat_service.get_response(req.message)
        print("✅ Groq replied successfully")
        return ChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat service error: {str(e)}")
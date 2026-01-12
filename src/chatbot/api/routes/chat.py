from fastapi import APIRouter, HTTPException
from ..schemas import ChatCreateRequest, ChatResponse
from ..services.chat_manager import ChatManager


router = APIRouter()
chat_manager = ChatManager()

@router.post("/chat/create", response_model=ChatResponse)
def create_chat(request: ChatCreateRequest):
    history = chat_manager.create_chat(request.session_id, request.message)
    return {"session_id": request.session_id, "history": history}

@router.get("/chat/{session_id}", response_model=ChatResponse)
def get_chat(session_id: str):
    history = chat_manager.get_chat(session_id)
    if not history:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"session_id": session_id, "history": history}

@router.delete("/chat/{session_id}")
def delete_chat(session_id: str):
    success = chat_manager.delete_chat(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"message": "Chat deleted successfully"}

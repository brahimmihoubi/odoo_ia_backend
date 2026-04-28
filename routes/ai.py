from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from services.deps import get_current_user

router = APIRouter()

class ChatMessage(BaseModel):
    message: str
    context: Optional[dict] = None

@router.post("/chat")
def chat(req: ChatMessage, user=Depends(get_current_user)):
    return {
        "reply": f"AI Assistant received: {req.message}. (This is a mock placeholder response. Real LLM integration required.)"
    }

class ReportRequest(BaseModel):
    type: str
    params: Optional[dict] = None

@router.post("/generate-report")
def generate_report(req: ReportRequest, user=Depends(get_current_user)):
    return {
        "report": f"Generated AI report of type: {req.type}",
        "content": "This is a placeholder AI-generated report summary."
    }

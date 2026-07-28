from fastapi import APIRouter
from app.services.gemini_service import ask_ai

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


@router.get("/")
def ai_home():
    return {"message": "MeetMind AI is ready!"}


@router.post("/chat")
def chat(message: str):
    reply = ask_ai(message)
    return {
        "user": message,
        "ai": reply
    }
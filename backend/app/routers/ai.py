from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.gemini_service import ask_ai
from app import crud

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


@router.get("/")
def home():
    return {"message": "MeetMind AI is ready!"}


@router.post("/chat")
def chat(
    meeting_id: int,
    message: str,
    db: Session = Depends(get_db)
):
    reply = ask_ai(message)

    crud.save_conversation(
        db=db,
        meeting_id=meeting_id,
        user_message=message,
        ai_response=reply
    )

    return {
        "user": message,
        "ai": reply
    }
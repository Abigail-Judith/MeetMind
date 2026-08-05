from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud
from app.services.gemini_service import ask_ai

router = APIRouter(
    prefix="/summary",
    tags=["Summary"]
)


@router.post("/{meeting_id}")
def generate_summary(
    meeting_id: int,
    db: Session = Depends(get_db)
):
    history = crud.build_chat_history(db, meeting_id)

    prompt = f"""
You are MeetMind, an AI meeting assistant.

Analyze the following meeting conversation and generate a structured summary.

Return the summary using exactly these sections:

## Overview

## Key Discussion Points

## Decisions Made

## Action Items
(Write "None" if there are no action items.)

## Next Steps
(Write "None" if nothing was discussed.)

Meeting Conversation:

{history}
"""

    summary = ask_ai(prompt)

    return {
        "meeting_id": meeting_id,
        "summary": summary
    }
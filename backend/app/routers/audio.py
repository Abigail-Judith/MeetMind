import os
import uuid

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Transcript
from app.services.whisper_service import transcribe_audio


router = APIRouter(
    prefix="/audio",
    tags=["Audio"]
)


@router.post("/upload/{meeting_id}")
async def upload_audio(
    meeting_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        os.makedirs("uploads/audio", exist_ok=True)

        filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join("uploads/audio", filename)

        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        transcript_text = transcribe_audio(file_path)

        transcript = Transcript(
            meeting_id=meeting_id,
            transcript=transcript_text
        )

        db.add(transcript)
        db.commit()
        db.refresh(transcript)

        os.remove(file_path)

        return {
            "message": "Audio transcribed successfully",
            "meeting_id": meeting_id,
            "transcript": transcript_text
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
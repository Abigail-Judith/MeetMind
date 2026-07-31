from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db
from app.security import get_current_user

router = APIRouter(tags=["Meetings"])


@router.post("/meetings", response_model=schemas.MeetingResponse)
def create_meeting(
    meeting: schemas.MeetingCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.create_meeting(db, meeting, current_user.id)

@router.get(
    "/meetings/{meeting_id}/history",
    response_model=list[schemas.ConversationResponse]
)
def get_history(
    meeting_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_conversations(db, meeting_id)
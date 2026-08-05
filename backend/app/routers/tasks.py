from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud
from app.services.task_service import extract_tasks

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post("/extract/{meeting_id}")
def extract_meeting_tasks(
    meeting_id: int,
    db: Session = Depends(get_db)
):
    history = crud.build_chat_history(
        db=db,
        meeting_id=meeting_id
    )

    tasks = extract_tasks(history)

    for task in tasks:
        crud.save_task(
            db=db,
            meeting_id=meeting_id,
            person=task["person"],
            task=task["task"],
            deadline=task["deadline"]
        )

    return {
        "meeting_id": meeting_id,
        "tasks": tasks
    }
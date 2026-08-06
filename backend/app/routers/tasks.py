from fastapi import APIRouter, Depends, HTTPException
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

@router.get("/{meeting_id}")
def get_tasks(
    meeting_id: int,
    db: Session = Depends(get_db)
):
    tasks = crud.get_tasks(db, meeting_id)

    return tasks

@router.patch("/{task_id}/complete")
def complete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = crud.complete_task(db, task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    deleted = crud.delete_task(db, task_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "message": "Task deleted successfully"
    }
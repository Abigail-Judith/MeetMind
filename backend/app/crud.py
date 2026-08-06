from sqlalchemy.orm import Session
from app import models, schemas
from app.security import hash_password, verify_password
MAX_HISTORY = 10

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user

def create_meeting(db: Session, meeting: schemas.MeetingCreate, owner_id: int):
    db_meeting = models.Meeting(
        title=meeting.title,
        description=meeting.description,
        meeting_time=meeting.meeting_time,
        owner_id=owner_id
    )

    db.add(db_meeting)
    db.commit()
    db.refresh(db_meeting)

    return db_meeting

def save_conversation(
    db,
    meeting_id,
    user_message,
    ai_response
):
    conversation = models.Conversation(
        meeting_id=meeting_id,
        user_message=user_message,
        ai_response=ai_response
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation

def get_conversations(db, meeting_id):
    return (
        db.query(models.Conversation)
        .filter(models.Conversation.meeting_id == meeting_id)
        .order_by(models.Conversation.created_at.asc())
        .all()
    )

def build_chat_history(db, meeting_id):
    conversations = (
        db.query(models.Conversation)
        .filter(models.Conversation.meeting_id == meeting_id)
        .order_by(models.Conversation.created_at.desc())
        .limit(MAX_HISTORY)
        .all()
    )

    conversations.reverse()

    history = ""

    for conv in conversations:
        history += f"User: {conv.user_message}\n"
        history += f"AI: {conv.ai_response}\n\n"

    return history

def save_task(
    db,
    meeting_id,
    person,
    task,
    deadline
):
    new_task = models.Task(
        meeting_id=meeting_id,
        person=person,
        task=task,
        deadline=deadline
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

def get_tasks(db, meeting_id):
    return (
        db.query(models.Task)
        .filter(models.Task.meeting_id == meeting_id)
        .order_by(models.Task.created_at.asc())
        .all()
    )

def complete_task(db, task_id):
    task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id)
        .first()
    )

    if task:
        task.status = "Completed"
        db.commit()
        db.refresh(task)

    return task

def delete_task(db, task_id):
    task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id)
        .first()
    )

    if not task:
        return None

    db.delete(task)
    db.commit()

    return True
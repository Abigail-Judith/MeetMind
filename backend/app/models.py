from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime, UTC

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    meeting_time = Column(String)

    owner_id = Column(Integer, ForeignKey("users.id"))

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)

    meeting_id = Column(
        Integer,
        ForeignKey("meetings.id")
    )

    user_message = Column(String)

    ai_response = Column(String)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC)
    )

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    meeting_id = Column(
        Integer,
        ForeignKey("meetings.id")
    )

    person = Column(String)

    task = Column(String)

    deadline = Column(String)

    status = Column(
        String,
        default="Pending"
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC)
    )

class Transcript(Base):
    __tablename__ = "transcripts"

    id = Column(Integer, primary_key=True, index=True)

    meeting_id = Column(
        Integer,
        ForeignKey("meetings.id")
    )

    transcript = Column(String)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC)
    )
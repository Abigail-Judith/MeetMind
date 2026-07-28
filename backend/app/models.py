from sqlalchemy import Column, Integer, String, ForeignKey

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
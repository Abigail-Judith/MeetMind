from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class MeetingCreate(BaseModel):
    title: str
    description: str
    meeting_time: str


class MeetingResponse(BaseModel):
    id: int
    title: str
    description: str
    meeting_time: str
    owner_id: int

    class Config:
        from_attributes = True

class ConversationCreate(BaseModel):
    meeting_id: int
    user_message: str


class ConversationResponse(BaseModel):
    id: int
    meeting_id: int
    user_message: str
    ai_response: str
    created_at: datetime

    class Config:
        from_attributes = True
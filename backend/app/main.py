from fastapi import FastAPI

from app.database import Base, engine
from app.routers import auth, meetings
from app.routers import ai, summary
from app.routers import tasks
from app import models
from app.routers import audio
from app.routers import documents

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MeetMind API")


app.include_router(auth.router)
app.include_router(meetings.router)
app.include_router(ai.router)
app.include_router(summary.router)
app.include_router(tasks.router)
app.include_router(audio.router)
app.include_router(documents.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to MeetMind AI 🚀"
    }
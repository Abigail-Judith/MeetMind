from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import auth, meetings
from app.routers import ai, summary
from app.routers import tasks
from app import models
from app.routers import audio
from app.routers import documents
from app.routers import rag

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MeetMind API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(meetings.router)
app.include_router(ai.router)
app.include_router(summary.router)
app.include_router(tasks.router)
app.include_router(audio.router)
app.include_router(documents.router)
app.include_router(rag.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to MeetMind AI 🚀"
    }
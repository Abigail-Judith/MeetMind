from fastapi import FastAPI

from app.database import Base, engine
from app.routers import auth, meetings
from app.routers import ai

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MeetMind API")


app.include_router(auth.router)
app.include_router(meetings.router)
app.include_router(ai.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to MeetMind AI 🚀"
    }
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app import crud, models, schemas
from app.database import Base, engine, get_db
from app.security import create_access_token, get_current_user

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to MeetMind AI 🚀"}


@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = crud.authenticate_user(
        db,
        form_data.username,
        form_data.password
    )

    if not db_user:
        return {"message": "Invalid email or password"}

    token = create_access_token({"sub": db_user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.get("/profile", response_model=schemas.UserResponse)
def profile(current_user=Depends(get_current_user)):
    return current_user
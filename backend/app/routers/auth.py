from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db
from app.security import create_access_token, get_current_user

router = APIRouter(tags=["Authentication"])


@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    db_user = crud.authenticate_user(
        db,
        form_data.username,
        form_data.password,
    )

    if not db_user:
        return {"message": "Invalid email or password"}

    token = create_access_token({"sub": db_user.email})

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.get("/profile", response_model=schemas.UserResponse)
def profile(current_user: models.User = Depends(get_current_user)):
    return current_user
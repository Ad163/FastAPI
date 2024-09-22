from fastapi import APIRouter, Depends, Path, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ..models import Todo, User
from ..database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user
from passlib.context import CryptContext



router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Admin Not found"}},
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[User, Depends(get_current_user)]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/", status_code=status.HTTP_200_OK)
async def read_root(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return db.query(User).filter(User.id == user.id).first()


# Changing of password
class ChangePassword(BaseModel):
    old_password: str
    new_password: str = Field(min_length=8)
    confirm_password: str = Field(min_length=8)


@router.put("/change-password", status_code=status.HTTP_200_OK)
async def change_password(user: user_dependency, db: db_dependency, change_password: ChangePassword):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if not pwd_context.verify(change_password.old_password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    if change_password.new_password != change_password.confirm_password:
        raise HTTPException(status_code=401, detail="Password does not match")
    user.hashed_password = pwd_context.hash(change_password.new_password)
    db.commit()
    return {"message": "Password changed successfully"}

# Changing of email
class ChangeEmail(BaseModel):
    email: str


@router.put("/change-email", status_code=status.HTTP_200_OK)
async def change_email(user: user_dependency, db: db_dependency, change_email: ChangeEmail):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user_email = db.query(User).filter(User.id == user.id).first()
    user_email.email = change_email.email
    db.commit()
    return {"message": "email change successfully"}


# Changing of phone number
class ChangePhoneNumber(BaseModel):
    phone_number: str


@router.put("/change-phone-number", status_code=status.HTTP_200_OK)
async def change_phone_number(user: user_dependency, db: db_dependency, change_phone_number: ChangePhoneNumber):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user_model = db.query(User).filter(User.id == user.id).first()
    user_model.phone_number = change_phone_number.phone_number
    db.commit()
    return {"message": "Phone number changed successfully"}


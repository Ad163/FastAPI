from fastapi import APIRouter, Depends, Path, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ..models import Todo, User
from ..database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
from pydantic import BaseModel, Field
# import models
from .auth import get_current_user



router = APIRouter(
    prefix="/admin",
    tags=["admin"],
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


@router.get("/", status_code=status.HTTP_200_OK)
async def read_root(db: db_dependency, user: user_dependency):
    if user is None or user.role != "admin":
        raise HTTPException(status_code=401, detail="Authentication failed")
    users = db.query(User).all()
    return users

@router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def read_item(user: user_dependency, db: db_dependency, user_id: int = Path(gt=0)):
    if user is None or user.role != "admin":
        raise HTTPException(status_code=401, detail="Authentication failed")
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None or user.role != "admin":
        raise HTTPException(status_code=401, detail="Authentication failed")
    
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}
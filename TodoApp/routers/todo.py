from fastapi import APIRouter, Depends, Path, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ..models import Todo, User
from ..database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
from pydantic import BaseModel, Field
# from models import Todo
# import models
from .auth import get_current_user



router = APIRouter(
    prefix="/api",
    tags=["todos"],
    responses={404: {"description": "Not found"}},
)



class Request(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    priority: int = Field(ge=1, le=5)
    completed: bool
    user_id: int


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[User, Depends(get_current_user)]

# @router.get("/", status_code=status.HTTP_200_OK)
# async def read_root(db: db_dependency, user: user_dependency):
#     return db.query(Todo).filter(Todo.user_id == user.id).all()

@router.get("/", status_code=status.HTTP_200_OK)
async def read_root(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    todos = db.query(Todo).filter(Todo.user_id == user.id).all()
    return todos


@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def read_item(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    todo = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.user_id == user.id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_item(todo: Request, db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
  
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        priority=todo.priority,
        completed=todo.completed,
        user_id = todo.user_id

    )


    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.put("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_item(db: db_dependency, user: user_dependency, todo: Request, todo_id: int = Path(ge=1)):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    db_todo = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.user_id == user.id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db_todo.title = todo.title
    db_todo.description = todo.description
    db_todo.priority = todo.priority
    db_todo.completed = todo.completed
    db_todo.user_id = todo.user_id
    db.commit()
    return db_todo


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(db: db_dependency, user:user_dependency, todo_id: int = Path(ge=1)):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    db_todo = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.user_id == user.id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return db_todo



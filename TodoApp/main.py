from fastapi import FastAPI, Depends, Path, HTTPException, status
from .models import Base, Todo
from .database import engine, SessionLocal
from .routers import auth, todo, admin, user
from typing import Annotated
from sqlalchemy.orm import Session
from .routers.todo import get_db


app = FastAPI()

@app.get("/health")
def health():
    return {"status": "Healthy Service"}


@app.get("/", status_code=status.HTTP_200_OK)
async def read_root(db: Annotated[Session, Depends(get_db)]):
    todos = db.query(Todo).all()
    return todos


Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todo.router)
app.include_router(admin.router)
app.include_router(user.router)

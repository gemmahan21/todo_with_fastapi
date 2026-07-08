from fastapi import APIRouter, Depends

from typing import List

from app.database import connect_db
from app.schemas import TodoSchema, TodoRequestSchema
from app.models import User
from app.security import get_current_user

from sqlalchemy.orm import Session

from app.repositories.todo_repository import TodoRepository


router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)

@router.get("/", response_model=List[TodoSchema])
def get_todos(db: Session = Depends(connect_db)):
    todo_repository = TodoRepository(db)

    return todo_repository.find_all()

@router.post("/", response_model=TodoSchema, status_code=201)
def create_todo(todo: TodoRequestSchema, db: Session = Depends(connect_db), author: User = Depends(get_current_user)):
    todo_repository = TodoRepository(db)

    new_todo = todo_repository.create_todo(todo, author_id=author.id)
    return new_todo


@router.get("/{id}", response_model=TodoSchema)
def read_todo(id: int, q: str | None = None, db: Session = Depends(connect_db)):
    todo_repository = TodoRepository(db)

    todo = todo_repository.find_by_id(id)
    return todo

@router.patch("/{id}", response_model=TodoSchema)
def update_todo(id: int, todo: TodoRequestSchema, db: Session = Depends(connect_db), author: User = Depends(get_current_user)):
    todo_repository = TodoRepository(db)
    found = todo_repository.update_todo(id, todo, author_id=author.id)
    
    return found


@router.delete("/{id}")
def delete_todo(id: int, db: Session = Depends(connect_db), author: User = Depends(get_current_user)):
    todo_repository = TodoRepository(db)
    todo_repository.delete_todo(id, author_id=author.id)
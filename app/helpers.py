from fastapi import HTTPException

from app.models import Todo, User
from sqlalchemy.orm import Session

def find_todo(id: int, db: Session):
    todo = db.query(Todo).filter(Todo.id == id).first()

    if todo is None:
        raise HTTPException(
            status_code=404,
            detail="Todo not found."
        )

    return todo

def match_author(todo: Todo, author: User):
    if todo.author_id != author.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission."
        )
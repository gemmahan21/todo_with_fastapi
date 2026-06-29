from fastapi import HTTPException

from app.models import Todo
from sqlalchemy.orm import Session

def find_todo(id: int, db: Session):
    todo = db.query(Todo).filter(Todo.id == id).first()

    if todo is None:
        raise HTTPException(
            status_code=404,
            detail="Todo not found."
        )

    return todo
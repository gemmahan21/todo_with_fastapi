from fastapi import FastAPI, Depends
from typing import List

from app.database import Base, engine, connect_db
from app.schemas import (
    TodoSchema,
    TodoRequestSchema
)
from app.helpers import find_todo

from app.models import Todo
from sqlalchemy.orm import Session

# db table create
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "ToDo List API!"}

@app.get("/todos", response_model=List[TodoSchema])
def get_todos(db: Session = Depends(connect_db)):
    todos = db.query(Todo).order_by(Todo.id).all()
    return todos

@app.post("/todos", response_model=TodoRequestSchema, status_code=201)
def create_todo(todo: TodoRequestSchema, db: Session = Depends(connect_db)):
    new_todo = Todo(
        text=todo.text,
        completed=todo.completed
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo


@app.get("/todos/{id}", response_model=TodoSchema)
def read_todo(id: int, q: str | None = None, db: Session = Depends(connect_db)):
    todo = find_todo(id, db)
    
    return todo


@app.patch("/todos/{id}", response_model=TodoSchema)
def update_todo(id: int, todo: TodoRequestSchema, db: Session = Depends(connect_db)):
    found = find_todo(id, db)

    found.text = todo.text
    found.completed = todo.completed

    db.commit()
    db.refresh(found)
    
    return found


@app.delete("/todos/{id}")
def delete_todo(id: int, db: Session = Depends(connect_db)):
    todo = find_todo(id, db)

    db.delete(todo)
    db.commit()

    return {
        "message" : "Todo deleted",
        "deleted_todo_id" : todo.id
    }
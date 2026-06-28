from fastapi import FastAPI, Depends
from typing import List

from app.database import todos, get_next_id, connect_db
from app.schemas import (
    TodoSchema,
    TodoRequestSchema
)
from app.helpers import find_todo

from app.models import Todo
from sqlalchemy.orm import Session

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "ToDo List API!"}

@app.get("/todos", response_model=List[TodoSchema])
def get_todos(db: Session = Depends(connect_db)):
    todos = db.query(Todo).order_by(Todo.id).all()
    return todos

@app.post("/todos", response_model=TodoRequestSchema, status_code=201)
def create_todo(todo: TodoRequestSchema):
    global next_id
    
    new_todo = TodoSchema(
        id=next_id,
        text=todo.text,
        completed=todo.completed
    )

    todos.append(new_todo)
    next_id += 1

    return new_todo


@app.get("/todos/{id}", response_model=TodoSchema)
def read_todo(id: int, q: str | None = None):
    todo = find_todo(id)
    return todo


@app.patch("/todos/{id}", response_model=TodoSchema)
def update_todo(id: int, todo: TodoRequestSchema):
    found = find_todo(id)

    found.text = todo.text
    found.completed = todo.completed
    
    return found


@app.delete("/todos/{id}")
def delete_todo(id: int):
    todo = find_todo(id)

    todos.remove(todo)

    return {
        "message" : "Todo deleted",
        "deleted_todo_id" : todo.id
    }
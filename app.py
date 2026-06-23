from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import List

app = FastAPI()

class TodoShcema(BaseModel):
    id: int
    text: str
    completed: bool
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TodoRequestShcema(BaseModel):
    text: str
    completed: bool = False

todos: List[TodoShcema] = []
next_id = 1

def find_todo(id: int):
    for todo in todos:
        if todo.id == id:
            return todo
    raise HTTPException(status_code=404, detail="Todo Not Found.")

@app.get("/")
def read_root():
    return {"message": "ToDo List API!"}

@app.get("/todos", response_model=List[TodoShcema])
def get_todos():
    return todos

@app.post("/todos", response_model=TodoRequestShcema, status_code=201)
def create_todo(todo: TodoRequestShcema):
    global next_id
    
    new_todo = TodoShcema(
        id=next_id,
        text=todo.text,
        completed=todo.completed
    )

    todos.append(new_todo)
    next_id += 1

    return new_todo


@app.get("/todos/{id}", response_model=TodoShcema)
def read_todo(id: int, q: str | None = None):
    todo = find_todo(id)
    return todo


@app.patch("/todos/{id}", response_model=TodoShcema)
def update_todo(id: int, todo: TodoRequestShcema):
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
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import Todo
from app.schemas import TodoRequestSchema

class TodoRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_all(self):
        return self.db.query(Todo).order_by(Todo.id).all()
    
    def find_by_id(self, id: int):
        todo = self.db.query(Todo).filter(Todo.id == id).first()

        if todo is None:
            raise HTTPException(
                status_code=404,
                detail="Todo not found."
            )

        return todo
    
    def create_todo(self, todo: TodoRequestSchema, author_id: int):
        new_todo = Todo(
            text=todo.text,
            completed=todo.completed,
            author_id=author_id
        )

        self.db.add(new_todo)
        self.db.commit()
        self.db.refresh(new_todo)

        return new_todo
    
    def update_todo(self, id: int, todo: TodoRequestSchema, author_id: int):
        found = self.find_by_id(id)

        if found.author_id != author_id:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission."
            )

        found.text = todo.text
        found.completed = todo.completed

        self.db.commit()
        self.db.refresh(found)
        
        return found
    
    def delete_todo(self, id: int, author_id: int):
        todo = self.find_by_id(id)

        if todo.author_id != author_id:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission."
            )

        self.db.delete(todo)
        self.db.commit()

        return {
            "message" : "Todo deleted",
            "deleted_todo_id" : todo.id
        }
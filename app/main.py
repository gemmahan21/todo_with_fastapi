from fastapi import FastAPI, Depends, HTTPException
from typing import List

from app.database import Base, engine, connect_db
from app.schemas import (
    TodoSchema,
    TodoRequestSchema,
    UserSchema,
    UserRegisterSchema,
    UserWithTodoSchema,
    UserLoginSchema,
    TokenSchema
)
from app.security import (
    create_access_token,
    get_current_user,
    hashed_password,
    verify_password
)
from app.helpers import find_todo, match_author

from app.models import Todo, User
from sqlalchemy.orm import Session

# db table create
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "ToDo Lists!"}


@app.get("/todos", response_model=List[TodoSchema])
def get_todos(db: Session = Depends(connect_db)):
    todos = db.query(Todo).order_by(Todo.id).all()
    return todos

@app.post("/todos", response_model=TodoSchema, status_code=201)
def create_todo(todo: TodoRequestSchema, db: Session = Depends(connect_db), author: User = Depends(get_current_user)):
    new_todo = Todo(
        text=todo.text,
        completed=todo.completed,
        author_id=author.id
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
def update_todo(id: int, todo: TodoRequestSchema, db: Session = Depends(connect_db), author: User = Depends(get_current_user)):
    found = find_todo(id, db)

    match_author(found, author)

    found.text = todo.text
    found.completed = todo.completed

    db.commit()
    db.refresh(found)
    
    return found


@app.delete("/todos/{id}")
def delete_todo(id: int, db: Session = Depends(connect_db), author: User = Depends(get_current_user)):
    todo = find_todo(id, db)

    match_author(todo, author)

    db.delete(todo)
    db.commit()

    return {
        "message" : "Todo deleted",
        "deleted_todo_id" : todo.id
    }

@app.post("/users", response_model=UserSchema, status_code=201)
def rigster_user(user: UserRegisterSchema, db: Session = Depends(connect_db)):
    existed_user = db.query(User).filter(User.email == user.email).first()

    if existed_user is not None:
        raise HTTPException(status_code=400)
    
    join_user = User(
        username = user.username,
        email = user.email,
        password = hashed_password(user.password)
    )

    db.add(join_user)
    db.commit()
    db.refresh(join_user)

    return join_user

@app.post("/signin", response_model=TokenSchema)
def login(user: UserLoginSchema, db: Session = Depends(connect_db)):
    existed = db.query(User).filter(User.email == user.email).first()

    if existed is None:
        raise HTTPException(
            status_code=401,
            detail="Not Found user info.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if not verify_password(user.password, existed.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    acccess_token = create_access_token(data={"sub": existed.email})

    return { "access_token": acccess_token }


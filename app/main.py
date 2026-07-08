from fastapi import FastAPI

from app.database import Base, engine
from app.routers import todos, auth


# db table create
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Todo Lists"
)


@app.get("/")
def read_root():
    return {"message": "ToDo Lists!"}

app.include_router(todos.router)
app.include_router(auth.router)
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from typing import List
from app.schemas import TodoSchema

from app.config import get_settings


settings = get_settings()

engine = create_engine(settings.db_url)

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)

class Base(DeclarativeBase):
    pass

def connect_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

# temp list
todos: List[TodoSchema] = []

_next_id = 1


def get_next_id() -> int:
    global _next_id

    current_id = _next_id
    _next_id += 1

    return current_id
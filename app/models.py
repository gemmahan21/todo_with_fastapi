from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )
    username: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )
    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    todos: Mapped[list["Todo"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan"
    )


class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )
    text: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    author: Mapped["User"] = relationship(
        back_populates="todos"
    )
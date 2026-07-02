from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict

class TodoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    text: str
    completed: bool
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    author_id: int

class TodoRequestSchema(BaseModel):
    text: str
    completed: bool = False


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str

class UserRegisterSchema(BaseModel):
    username: str
    email: str
    password: str

class UserLoginSchema(BaseModel):
    email: str
    password: str

class UserWithTodoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    todos: list[TodoSchema] = Field(default_factory=list)


class TokenSchema(BaseModel):
    access_token: str
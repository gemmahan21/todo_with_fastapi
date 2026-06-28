from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict

class TodoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    text: str
    completed: bool
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TodoRequestSchema(BaseModel):
    text: str
    completed: bool = False

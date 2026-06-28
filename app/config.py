from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pathlib import Path

class Settings(BaseSettings):
    db_url: str = "postgresql://gemma:smart1234@localhost:5432/todos"


@lru_cache
def get_settings():
    return Settings()
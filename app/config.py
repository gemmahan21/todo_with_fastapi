from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    PORT: int
    DB_URL: str
    SECRET_KEY: str
    TOKEN_EXPIRE: int


@lru_cache
def get_settings():
    return Settings()

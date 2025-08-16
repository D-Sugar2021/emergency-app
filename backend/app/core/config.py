from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, PostgresDsn
from typing import Optional

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # For testing purposes, we can use an in-memory SQLite database
    TESTING: bool = True
    DATABASE_URL: Optional[PostgresDsn] = None

    # Celery settings
    CELERY_BROKER_URL: str = "filesystem:///app/backend/celery/broker"
    CELERY_RESULT_BACKEND: str = "file:///app/backend/celery/results"

    class Config:
        env_file = Path(__file__).parent.parent.parent / "app.env"

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        if self.TESTING:
            return "sqlite+aiosqlite:///memory:"
        return self.DATABASE_URL


settings = Settings()

import os

import redis
from dotenv import load_dotenv
from pathlib import Path

from pydantic.v1 import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    PROJECT_NAME: str = "Passwords manager"

    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    # DATABASE_URL: str | None = "sqlite:///./user_manager.sqlite3"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

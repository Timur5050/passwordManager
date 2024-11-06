import os
from dotenv import load_dotenv
from pathlib import Path

from pydantic.v1 import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class AuthJWT(BaseSettings):
    private_key_path: Path = BASE_DIR / "UserManager" / "certs" / "private.pem"
    public_key_path: Path = BASE_DIR / "UserManager" / "certs" / "public.pem"
    algorithm: str = "RS256"
    access_token_exp_minutes: int = 15
    refresh_token_exp_minutes: int = 60 * 24


class Settings(BaseSettings):
    PROJECT_NAME: str = "Users manager"

    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "tdd")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    # DATABASE_URL: str | None = "sqlite:///./user_manager.sqlite3"
    ASYNC_DATABASE_URL: str | None = "sqlite+aiosqlite:///./user_manager.sqlite3"
    auth_jwt: AuthJWT = AuthJWT()

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

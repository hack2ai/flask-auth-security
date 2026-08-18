import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent

# Load variables from .env
load_dotenv(BASE_DIR / ".env")


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")

    if not SECRET_KEY:
        raise RuntimeError(
            "SECRET_KEY environment variable must be configured."
        )

    DATABASE = os.environ.get(
        "DATABASE_PATH",
        str(BASE_DIR / "database" / "users.db")
    )

    # Session security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"


    # 30-minute session lifetime
    PERMANENT_SESSION_LIFETIME = 1800

    # CSRF protection
    WTF_CSRF_ENABLED = True

    # Maximum request body size: 1 MB
    MAX_CONTENT_LENGTH = 1024 * 1024

    # Never use Flask debug mode for production
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = False

    SESSION_COOKIE_SECURE = False
    WTF_CSRF_ENABLED = True

    DATABASE = str(
        BASE_DIR / "database" / "test_users.db"
    )

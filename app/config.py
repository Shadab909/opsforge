import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    SECRET_KEY = os.environ.get("OPSFORGE_SECRET_KEY", "opsforge-local-secret-key-2026")
    BASE_DIR = BASE_DIR
    PROCESSED_DIR = BASE_DIR / "processed"
    USER_DATA_DIR = BASE_DIR / "user_data"
    KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"
    PORT = int(os.environ.get("PORT", 5000))
    HOST = os.environ.get("HOST", "127.0.0.1")
    DEBUG = True
    TURSO_DATABASE_URL = os.environ.get("TURSO_DATABASE_URL", "")
    TURSO_AUTH_TOKEN = os.environ.get("TURSO_AUTH_TOKEN", "")


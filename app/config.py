import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = BASE_DIR / "app"
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"
UPLOADS_DIR = BASE_DIR / "uploads"

# Ensure uploads directory exists
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# Database
DATABASE_PATH = BASE_DIR / "gramsetu.db"

# Security & JWT
SECRET_KEY = os.getenv("GRAMSETU_SECRET_KEY", "gramsetu_sih_hackathon_super_secret_jwt_key_2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# Max upload size: 5MB
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}

# AI and App Details
APP_NAME = "GramSetu"
APP_TAGLINE = "One Voice, One Photo, One Connected Village."
APP_VERSION = "1.0.0-SIH-Prototype"

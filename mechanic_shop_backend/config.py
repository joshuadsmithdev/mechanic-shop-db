# mechanic_shop_backend/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env (if running locally)
load_dotenv()

class Config:
    # Secret key for sessions or JWTs
    SECRET_KEY = os.getenv("JWT_SECRET", "dev-secret")

    # SQLAlchemy configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Render provides DATABASE_URL for PostgreSQL
    # SQLAlchemy expects the URL to start with "postgresql://"
    database_url = os.getenv("DATABASE_URL")

    if database_url and database_url.startswith("postgres://"):
        # Render sometimes gives old-style URLs, fix them for SQLAlchemy
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    # --- Minimal fix: use ABSOLUTE path for local SQLite in ./instance/dev.db ---
    _here = os.path.dirname(__file__)                         # .../mechanic_shop_backend
    _project_root = os.path.abspath(os.path.join(_here, ".."))  # repo root
    _instance_dir = os.path.join(_project_root, "instance")
    os.makedirs(_instance_dir, exist_ok=True)                   # ensure folder exists
    _db_path = os.path.join(_instance_dir, "dev.db")

    SQLALCHEMY_DATABASE_URI = database_url or f"sqlite:///{_db_path}"

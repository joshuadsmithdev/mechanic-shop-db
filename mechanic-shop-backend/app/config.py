# app/config.py
import os
from dotenv import load_dotenv
load_dotenv()  # fine for local projects

def _build_mysql_uri():
    user = os.getenv("DB_USER")
    pwd  = os.getenv("DB_PASS")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT")          # may be empty/None
    name = os.getenv("DB_NAME")

    # If required pieces are missing, return None so we can fall back
    if not (user and pwd and name):
        return None

    auth = f"{user}:{pwd}@"               # user & pwd guaranteed above
    hostport = f"{host}:{port}" if port else host
    return f"mysql+mysqlconnector://{auth}{hostport}/{name}"

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_dev_secret")

    # 1) Prefer a full URL if provided (works for sqlite/mysql/postgres)
    # 2) Else try to compose a MySQL URL from parts (only if complete)
    # 3) Else fall back to local sqlite so dev “just works”
    SQLALCHEMY_DATABASE_URI = (
        os.getenv("DATABASE_URL")
        or _build_mysql_uri()
        or "sqlite:///dev.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

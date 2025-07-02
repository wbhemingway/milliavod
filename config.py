import os
from pathlib import Path

from dotenv import load_dotenv

basedir = Path(__file__).resolve().parent

dotenv_path = basedir / ".env"
load_dotenv(dotenv_path)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")

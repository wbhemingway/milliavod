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
    OAUTH2_PROVIDERS = {
        # Google OAuth 2.0 documentation
        # https://developers.google.com/identity/protocols/oauth2/web-server#httprest
        'google': {
            'client_id': os.environ.get('GOOGLE_CLIENT_ID'),
            'client_secret': os.environ.get('GOOGLE_CLIENT_SECRET'),
            'authorize_url': 'https://accounts.google.com/o/oauth2/auth',
            'token_url': 'https://accounts.google.com/o/oauth2/token',
            'userinfo': {
                'url': 'https://www.googleapis.com/oauth2/v3/userinfo',
                'email': lambda json: json['email']
            },
            'scopes': ['https://www.googleapis.com/auth/userinfo.email']
        }
    }

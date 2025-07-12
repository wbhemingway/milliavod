from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "main.index"
login.login_message = "Please log in to access this"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.errors import errors as errors_bp

    app.register_blueprint(errors_bp)

    from app.auth import auth as auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.admin import admin as admin_bp

    app.register_blueprint(admin_bp, url_prefix="/admin")

    from app.main import main as main_bp

    app.register_blueprint(main_bp)

    return app


# from app import models  # noqa: E402, F401

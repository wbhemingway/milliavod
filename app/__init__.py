import logging
import os
from logging.handlers import RotatingFileHandler

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

    from app.cli import bp as cli_bp

    app.register_blueprint(cli_bp)

    if not app.debug and not app.testing:
        if not os.path.exists("logs"):
            os.mkdir("logs")
        file_handler = RotatingFileHandler(
            "logs/microblog.log", maxBytes=10240, backupCount=10
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s " "[in %(pathname)s:%(lineno)d]"
            )
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("milliavod startup")

    return app


# from app import models  # noqa: E402, F401

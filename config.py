"""Flask config."""
from os import environ, path

from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))


class Config:
    """Flask configuration variables."""

    # General Config
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_ENV = environ.get("FLASK_ENV")
    # FLASK_APP = "application.py"
    # FLASK_ENV = "development"
    SECRET_KEY = environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    # Assets
    # LESS_BIN = environ.get("LESS_BIN")
    # ASSETS_DEBUG = environ.get("ASSETS_DEBUG")
    # LESS_RUN_IN_DEBUG = environ.get("LESS_RUN_IN_DEBUG")

    # Static Assets
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    # COMPRESSOR_DEBUG = environ.get("COMPRESSOR_DEBUG")
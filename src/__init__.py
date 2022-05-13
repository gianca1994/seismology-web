import os

from dotenv import load_dotenv
from flask import Flask
from flask_breadcrumbs import Breadcrumbs
from flask_login import LoginManager

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    load_dotenv()

    app.config["API_URL"] = os.getenv("API_URL")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 100
    Breadcrumbs(app=app)
    login_manager.init_app(app)

    return app

import os

from dotenv import load_dotenv
from flask import Flask
from flask_breadcrumbs import Breadcrumbs
from flask_login import LoginManager
from flask_wtf import CSRFProtect

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    load_dotenv()

    app.config["API_URL"] = os.getenv("API_URL")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 10
    csrf = CSRFProtect(app)
    csrf.init_app(app)
    app.config["SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    Breadcrumbs(app=app)
    login_manager.init_app(app)

    from .routes import main, verified_seism, unverified_seism, user, sensor
    app.register_blueprint(main.main)
    app.register_blueprint(verified_seism.verified_seism)
    app.register_blueprint(unverified_seism.unverified_seism)
    app.register_blueprint(user.user)
    app.register_blueprint(sensor.sensor)

    return app

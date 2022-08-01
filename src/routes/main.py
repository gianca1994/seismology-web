import requests
import json
from flask import Blueprint, redirect, url_for, current_app, make_response, flash
from flask_breadcrumbs import register_breadcrumb
from flask_login import login_user, logout_user

from .auth import User
from ..forms.login import LoginForm

main = Blueprint("main", __name__, url_prefix="/")


@main.route("/")
@register_breadcrumb(main, "breadcrumbs.", "Home")
def index():
    return redirect(url_for("verified_seism.index"))


@main.route("/login", methods=["POST"])
def login():
    loginForm = LoginForm()

    if loginForm.is_submitted():
        data = json.dumps({
            "email": loginForm.email.data,
            "password": loginForm.password.data
        })

        response = requests.request(
            "POST",
            current_app.config["API_URL"] + "/auth/login",
            headers={'Content-Type': 'application/json'},
            data=data
        )

        if response.status_code == 200:
            user_data = json.loads(response.text)
            user = User(
                id=user_data.get("id"),
                email=user_data.get("email"),
                role=user_data.get("role")
            )
            login_user(user)
            req = make_response(redirect(url_for("main.index")))
            req.set_cookie("access_token", user_data.get("access_token"), httponly=True)
            return req
        else:
            flash("Usuario o contraseña incorrecta", "danger")
    return redirect(url_for("main.index"))


@main.route("/logout")
def logout():
    req = make_response(redirect(url_for("main.index")))
    req.set_cookie("access_token", "", httponly=True)
    logout_user()
    return req

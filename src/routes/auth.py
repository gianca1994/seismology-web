from functools import wraps

import jwt
from flask import flash, redirect, request, url_for
from flask_login import UserMixin, current_user
from .. import login_manager


class User(UserMixin):
    def __init__(self, id, email, role):
        self.id = id
        self.email = email
        self.role = role


@login_manager.request_loader
def load_user(request):
    if "access_token" in request.cookies:
        try:
            decoded = jwt.decode(request.cookies["access_token"], verify=False)
            user_data = decoded["user_claims"]
            user = User(user_data["id"], user_data["email"], user_data["admin"])
            return user
        except jwt.exceptions.InvalidTokenError:
            print("Invalid Token.")
        except jwt.exceptions.DecodeError:
            print("DecodeError.")
    return None


@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("Debe iniciar sesión para continuar.", "warning")
    return redirect(url_for("main.index"))


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kws):
        if not current_user.admin:
            flash("Acceso restringido a administradores.", "warning")
            return redirect(url_for("main.index"))
        return fn(*args, **kws)

    return wrapper

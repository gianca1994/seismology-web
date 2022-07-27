import json

from flask import Blueprint, flash, redirect, render_template, url_for, request
from flask_breadcrumbs import register_breadcrumb
from flask_login import login_required

from ..forms.user import UserCreateForm, UserEditForm
from ..utilities.functions import sendRequest
from .auth import admin_required

user = Blueprint("user", __name__, url_prefix="/users")
auth = Blueprint("auth", __name__, url_prefix="/auth")


@user.route("/")
@login_required
@admin_required
@register_breadcrumb(user, ".", "Users")
def index():
    data = {}
    if "page" in request.args:
        data["page"] = request.args.get("page", "")
    else:
        if "page" in data:
            del data["page"]
    r = sendRequest(method="get", url="/users", data=json.dumps(data), auth=True)

    if r.status_code == 200:
        users = json.loads(r.text)["Users"]
        title = "Users List"
        return render_template(
            "users.html",
            title=title,
            users=users,
        )
    else:
        return redirect(url_for("user.index"))


@user.route("/view/<int:id>")
@login_required
@admin_required
@register_breadcrumb(user, ".view", "View")
def view(id):
    r = sendRequest(method="get", url="/users/" + str(id), auth=True)
    if r.status_code == 404:
        flash("User not found", "danger")
        return redirect(url_for("user.index"))
    user = json.loads(r.text)
    title = "User View"
    return render_template(
        "user_view.html",
        title=title,
        user=user
    )


@auth.route("/create", methods=["GET", "POST"])
@login_required
@admin_required
@register_breadcrumb(user, ".create", "Create User")
def create():
    form = UserCreateForm()
    if form.validate_on_submit():
        user = {
            "email": form.email.data,
            "password": form.password.data,
            "firstname": form.first_name.data,
            "lastname": form.last_name.data,
            "role": form.role.data
        }
        data = json.dumps(user)
        sendRequest(method="post", url="/auth/register", data=data, auth=True)
        return redirect(url_for("user.index"))

    return render_template(
        "user_create.html",
        form=form
    )


@user.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
@register_breadcrumb(user, ".edit", "Edit User")
def edit(id):
    form = UserEditForm()
    if not form.is_submitted():
        r = sendRequest(method="get", url="/users/" + str(id), auth=True)
        if r.status_code == 404:
            flash("User not found", "danger")
            return redirect(url_for("user.index"))

        user = json.loads(r.text)
        form.email.data = user["email"]
        form.first_name.data = user["firstname"]
        form.last_name.data = user["lastname"]
        form.role.data = user["role"]

    if form.validate_on_submit():
        user = {
            "email": form.email.data,
            "firstname": form.first_name.data,
            "lastname": form.last_name.data,
            "role": form.role.data
        }
        data = json.dumps(user)
        r = sendRequest(method="put", url="/users/" + str(id), data=data, auth=True)
        flash("User edited", "success")
        return redirect(url_for("user.index"))
    return render_template(
        "user_edit.html",
        form=form,
        id=id
    )


@user.route("/delete/<int:id>")
@login_required
@admin_required
def delete(id):
    r = sendRequest(method="delete", url="/users/" + str(id), auth=True)
    flash("User deleted", "danger")
    return redirect(url_for("user.index"))
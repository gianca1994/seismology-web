from flask import Blueprint, redirect, url_for
from flask_breadcrumbs import register_breadcrumb

main = Blueprint("main", __name__, url_prefix="/")


@main.route("/")
@register_breadcrumb(main, "breadcrumbs.", "Home")
def index():
    return "hello world"

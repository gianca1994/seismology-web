import json

from flask import current_app, flash, redirect, request, url_for
import requests
from werkzeug.routing import RequestRedirect


def sendRequest(method, url, auth=False, data=None):
    headers = {"content-type": "application/json"}

    if auth:
        headers["authorization"] = "Bearer " + request.cookies['access_token']

    if method.lower() == "get":
        response = requests.get(current_app.config["API_URL"] + url, headers=headers, data=data)

    if method.lower() == "post":
        response = requests.post(current_app.config["API_URL"] + url, headers=headers, data=data)

    if method.lower() == "put":
        response = requests.put(current_app.config["API_URL"] + url, headers=headers, data=data)

    if method.lower() == "delete":
        response = requests.delete(current_app.config["API_URL"] + url, headers=headers)

    if response.status_code == 401 or response.status_code == 422:
        flash("Authorization token not valid. Please log in again", "warning")
        raise RequestRedirect(url_for("main.logout"))

    return response

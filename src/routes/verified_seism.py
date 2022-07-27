import csv
import io
import json

from flask import (
    Blueprint,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_breadcrumbs import register_breadcrumb

from ..forms.login import LoginForm
from ..forms.seism import SeismFilterForm
from ..utilities.functions import sendRequest

verified_seism = Blueprint("verified_seism", __name__, url_prefix="/verified-seisms")


@verified_seism.route("/")
@register_breadcrumb(verified_seism, ".", "Verified Seisms")
def index():
    loginForm = LoginForm()
    filter = SeismFilterForm(request.args, meta={"csrf": False})

    r = sendRequest(method="get", url="/sensors-info")
    filter.sensorId.choices = [(int(sensor["id"]), sensor["name"]) for sensor in json.loads(r.text)["sensors"]]
    filter.sensorId.choices.insert(0, [0, "All"])
    data = {}

    if filter.validate():
        if filter.from_datetime.data and filter.to_datetime.data:
            if filter.from_datetime.data == filter.to_datetime.data:
                data["datetime"] = filter.to_datetime.data.strftime("%Y-%m-%d %H:%M")
        if filter.from_datetime.data is not None:
            data["from_datetime"] = filter.from_datetime.data.strftime("%Y-%m-%d %H:%M")
        if filter.to_datetime.data is not None:
            data["to_datetime"] = filter.to_datetime.data.strftime("%Y-%m-%d %H:%M")

        if filter.sensorId.data is not None and filter.sensorId.data != 0:
            data["sensorId"] = filter.sensorId.data

        if filter.depth_min.data is not None:
            data["depth_min"] = filter.depth_min.data
        if filter.depth_max.data is not None:
            data["depth_max"] = filter.depth_max.data

        if filter.magnitude_min.data is not None:
            data["magnitude_min"] = filter.magnitude_min.data
        if filter.magnitude_max.data is not None:
            data["magnitude_max"] = filter.magnitude_max.data

    if "sort_by" in request.args:
        data["sort_by"] = request.args.get("sort_by", "")

    if "download" in request.args:
        if request.args.get("download", "") == "Download":
            code, page, list_seisms = 200, 1, []

            while code == 200:
                data["page"] = page
                r = sendRequest(method="get", url="/verified-seisms", data=json.dumps(data))
                code = r.status_code
                if code == 200:
                    for seism in json.loads(r.text)["Verified-seisms"]:
                        element = {
                            "datetime": seism["datetime"],
                            "depth": seism["depth"],
                            "magnitude": seism["magnitude"],
                            "latitude": seism["latitude"],
                            "longitude": seism["longitude"],
                            "sensor.name": seism["sensor"]["name"],
                        }
                        list_seisms.append(element)
                page += 1

            si = io.StringIO()
            fc = csv.DictWriter(si, fieldnames=list_seisms[0].keys())
            fc.writeheader()
            fc.writerows(list_seisms)

            output = make_response(si.getvalue())
            output.headers["Content-Disposition"] = "attachment; filename=seisms.csv"
            output.headers["Content-type"] = "text/csv"
            return output

    if "page" in request.args:
        data["page"] = request.args.get("page", "")
    else:
        if "page" in data:
            del data["page"]

    r = sendRequest(method="get", url="/verified-seisms", data=json.dumps(data))

    if r.status_code == 200:
        verified_seisms = json.loads(r.text)["Verified-seisms"]

        pagination = {
            "total": json.loads(r.text)["total"],
            "pages": json.loads(r.text)["pages"],
            "current_page": json.loads(r.text)["page"]
        }
        title = "Verified Seisms List"
        return render_template(
            "verified_seisms.html",
            title=title,
            verified_seisms=verified_seisms,
            loginForm=loginForm,
            filter=filter,
            pagination=pagination,
        )
    else:
        flash("Error de filtrado", "danger")
        return redirect(url_for("verified_seism.index"))


@verified_seism.route("/view/<int:id>")
@register_breadcrumb(verified_seism, ".view", "View")
def view(id):
    r = sendRequest(method="get", url="/verified-seisms/" + str(id))

    if r.status_code == 404:
        return redirect(url_for("verified_seism.index"))

    verified_seism = json.loads(r.text)
    title = "Verified Seism View"
    loginForm = LoginForm()
    return render_template(
        "verified_seism_view.html",
        title=title,
        verified_seism=verified_seism,
        loginForm=loginForm,
    )

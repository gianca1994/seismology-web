from flask_wtf import FlaskForm
from wtforms import (BooleanField, FloatField, IntegerField, SelectField, SubmitField, validators)
from wtforms.fields.html5 import DateTimeLocalField as DateTimeField


class UnverifiedSeismEditForm(FlaskForm):
    depth = IntegerField(label="Depth", validators=[
        validators.DataRequired(
            message="This field should be an integer")
    ])

    magnitude = FloatField(label="Magnitude", validators=[
        validators.DataRequired(
            message="This field should be a decimal value")
    ])

    verified = BooleanField(label="Verified")

    submit = SubmitField(label="Send")


class SeismFilterForm(FlaskForm):
    from_datetime = DateTimeField(
        label="From Datetime",
        format="%Y-%m-%dT%H:%M",
        validators=[validators.optional()]
    )

    to_datetime = DateTimeField(
        label="To Datetime",
        format="%Y-%m-%dT%H:%M",
        validators=[validators.optional()]
    )

    depth_min = IntegerField(label="Depth Min", validators=[validators.optional()])
    depth_max = IntegerField(label="Depth Max", validators=[validators.optional()])
    magnitude_min = FloatField(label="Magnitude Min", validators=[validators.optional()])
    magnitude_max = FloatField(label="Magnitude Max", validators=[validators.optional()])
    sensorId = SelectField(label="Sensor Associated", validators=[validators.optional()], coerce=int)

    submit = SubmitField(label="Filter")
    download = SubmitField(label="Download")

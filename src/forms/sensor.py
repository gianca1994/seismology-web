from flask_wtf import FlaskForm
from wtforms import validators
from wtforms import BooleanField, IntegerField, SelectField, StringField, SubmitField


class SensorCreateForm(FlaskForm):
    name = StringField(label="Name", validators=[
        validators.DataRequired(message="This field is required")
    ])

    ip = StringField(label="Ip", validators=[
        validators.DataRequired(
            message="This field is required")
    ])

    port = IntegerField(label="Port", validators=[
        validators.InputRequired(
            message="This field is required")
    ])

    status = BooleanField(label="Status")
    active = BooleanField(label="Active")

    submit = SubmitField(label="Send")


class SensorEditForm(FlaskForm):
    name = StringField(label="Name", validators=[
        validators.DataRequired(message="This field is required")
    ])

    ip = StringField(label="Ip", validators=[
        validators.DataRequired(message="This field is required")
    ])

    port = IntegerField(label="Port", validators=[
        validators.InputRequired(message="This field is required")
    ])

    status = BooleanField(label="Status")
    active = BooleanField(label="Active")

    userId = SelectField(label="User Associated", validators=[
        validators.InputRequired(message="This field is required")
    ], coerce=int)

    submit = SubmitField(label="Send")


class SensorFilterForm(FlaskForm):
    name = StringField(label="Name", validators=[validators.optional()])
    status = BooleanField(label="Status", validators=[validators.optional()])
    active = BooleanField(label="Active", validators=[validators.optional()])
    userId = SelectField("Users", [validators.optional()], coerce=int)
    submit = SubmitField(label="Filter")

from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, validators
from wtforms.fields.html5 import EmailField


class LoginForm(FlaskForm):
    email = EmailField("E-mail", [
        validators.Required(message="E-mail is require"),
        validators.Email(message="Format not valid")
    ])

    password = PasswordField("Password", [
        validators.Required()
    ])

    submit = SubmitField("Login")

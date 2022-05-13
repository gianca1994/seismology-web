from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, validators, TextField
from wtforms.fields.html5 import EmailField


class UserCreateForm(FlaskForm):
    email = EmailField("E-mail", [
        validators.Required(message="E-mail is require"),
        validators.Email(message="Format not valid")
    ])

    password = PasswordField("Password", [
        validators.Required(),
        validators.EqualTo("confirm", message="Passwords dont match")
    ])

    confirm = PasswordField("Repeat Password")
    first_name = TextField("FirstName", validators.Required(message="First Name is require"))
    last_name = TextField("LastName", validators.Required(message="Last Name is require"))
    submit = SubmitField("Send")


class UserEditForm(FlaskForm):
    email = EmailField("E-mail", [
        validators.Required(message="E-mail is require"),
        validators.Email(message="Format not valid")
    ])

    submit = SubmitField("Send")

from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, validators, TextField, SelectField
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
    first_name = TextField("FirstName", [validators.Required(message="First Name is required")])
    last_name = TextField("LastName", [validators.Required(message="Last Name is required")])
    role = SelectField(label="Role", validators=[validators.optional()], coerce=str, choices=['standard', 'admin'])

    submit = SubmitField("Send")


class UserEditForm(FlaskForm):
    email = EmailField("E-mail", [
        validators.Required(message="E-mail is require"),
        validators.Email(message="Format not valid")
    ])
    first_name = TextField("FirstName", [validators.Required(message="First Name is required")])
    last_name = TextField("LastName", [validators.Required(message="Last Name is required")])

    role = SelectField(label="Role", validators=[validators.optional()], coerce=str, choices=['standard', 'admin'])

    submit = SubmitField("Send")

from wtforms import Form, StringField, PasswordField, validators
from wtforms.fields.html5 import EmailField

class RegistrationForm(Form):
    name = StringField("Full Name", [validators.Length(min=4, max=30), validators.DataRequired()])
    username = StringField("Username", [validators.Length(min=4, max=30), validators.DataRequired()])
    email = EmailField("Email", [validators.Email(), validators.DataRequired()])
    password = PasswordField("Password", [validators.Length(min=5), validators.DataRequired(), validators.EqualTo("confirm", message="Passwords must match.")])
    confirm = PasswordField("Confirm Password")

    
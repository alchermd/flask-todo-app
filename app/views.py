from flask import render_template, request
from app.forms import RegistrationForm
from app import app

@app.route("/")
def index():
    return render_template("home.html", title="Home")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        pass
    return render_template("register.html", title="Register", form=form)
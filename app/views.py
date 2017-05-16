from flask import render_template, request, flash, redirect, url_for
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from app.forms import RegistrationForm
from app import app

# MySQL connection.
mysql = MySQL(app)

@app.route("/")
def index():
    return render_template("home.html", title="Home")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        # Get user data from form.
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create a cursor and insert user into the database.
        curr = mysql.connection.cursor()
        curr.execute("INSERT INTO users(name, username, email, password) VALUES(%s, %s, %s, %s)", (name, username, email, password))

        # Close connection.
        mysql.connection.commit()
        curr.close()

        # Redirect the user.
        flash("Account created!", "success")    
        return redirect(url_for("login"))
        
    return render_template("register.html", title="Register", form=form)
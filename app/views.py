from flask import render_template, request, flash, redirect, url_for, session
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

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Get user data from form
        username = request.form['username']
        plain_pw = request.form['password']
        
        # Create a cursor and query the database.
        curr = mysql.connection.cursor()
        result = curr.execute("SELECT * FROM users WHERE username=%s", (username,))

        # Check for match.
        if result:
            # Save user data from query result.
            user_data = curr.fetchone()
            hashed_pw = user_data['password']

            # Validate password
            if sha256_crypt.verify(plain_pw, hashed_pw):
                # Save user session.
                session['logged_in'] = True
                session['username'] = user_data['username']
                
                # Redirect to dashboard.
                flash("Login success.", "success")
                return redirect(url_for("dashboard"))

        return render_template("login.html", title="Login", err="Invalid credentials.")

    return render_template("login.html", title="Login")
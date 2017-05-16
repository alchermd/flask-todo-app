from flask import render_template, request, flash, redirect, url_for, session
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from app.forms import RegistrationForm, TaskForm
from app import app

# MySQL connection.
mysql = MySQL(app)

# Route for the index page or home page.
@app.route("/")
def index():
    return render_template("home.html", title="Home")

# Route for the registration page.
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

# Route for the login page.
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

# Route for the logout page.
@app.route("/logout")
def logout():
    # Clear the user session then redirect them to login page.
    session.clear()
    flash("You are now logged out.", "info")
    return redirect(url_for("login"))

# Route for the user dashboard.
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        pass

    # Create a cursor and query the database.
    curr = mysql.connection.cursor()
    curr.execute("SELECT * FROM tasks WHERE author=%s", (session['username'],))
    tasks = curr.fetchall()

    # Close the connection before rendering.
    curr.close()

    return render_template("dashboard.html", title="Dashboard", tasks=tasks)

# Route for the add task page.
@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    form = TaskForm(request.form)

    if request.method == "POST" and form.validate():
        # Get task information
        author = session['username']
        description = form.description.data
        status = form.status.data

        # Create a cursor and query the database.
        curr = mysql.connection.cursor()
        curr.execute("INSERT INTO tasks(author, description, status) VALUES(%s, %s, %s)", (author, description, status))
        
        # Commit and close connection.
        mysql.connection.commit()
        curr.close()

        # Flash and redirect back to dashboard.
        flash("Task added.", "success")
        return redirect(url_for("dashboard"))
        
    return render_template("add_task.html", title="Add Task", form=form)
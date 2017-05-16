from functools import wraps
from flask import flash, redirect, url_for, session
from app import views

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Please login to continue.", "danger")
            return redirect(url_for("login"))
    return decorated_function
import sqlite3
import re
import requests

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required


# Configure application
app = Flask(__name__)
app.debug = True
app.secret_key = "supersecretkey"

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():

    return render_template("index.html")

@app.route("/login", methods = ["GET","POST"])
def login():

    if request.method == "GET":
    
        return render_template("login.html")
    
    elif request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username is None or password is None:
            flash("Invalid username or password")
            return render_template("login.html")
        
        if len(username) == 0 or len(password) == 0:
            flash("Invalid username or password")
            return render_template("login.html")
        
        url = "https://dummyjson.com/auth/login"

        headers = {"Content-Type": "application/json"}

        payload = {"username":username,"password":password}

        authResponse = requests.post(
            url=url,
            headers=headers,
            json=payload,
            verify=False
        )

        if not authResponse.ok:

            flash("Invalid username or password")
            return redirect('/login')
        
        authResponseJSON = authResponse.json()

        session["first_name"] = authResponseJSON["firstName"]
        session["last_name"] = authResponseJSON["lastName"]
        session["profile_pic_url"] = authResponseJSON["image"]
        session["user_id"]  = authResponseJSON["id"]
        
        return redirect("/")
    
@app.route("/logout",methods=["POST"])
@login_required
def logout():

    session.clear()
    return redirect("/")
import sqlite3
import re
import requests
from helpers import login_required

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

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

    firstName = session["first_name"]
    lastName = session["last_name"]
    return render_template("index.html",firstName,lastName)

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

        dbResponse = requests.post(
            method = "POST",
            url=url,
            headers=headers,
            json=payload,
            verify=False
        )

        app.logger.debug(dbResponse)

        session["first_name"] = dbResponse["firstName"]
        session["last_name"] = dbResponse["lastName"]
        session["profile_pic_url"] = dbResponse["image"]
        session["user_id"]  =dbResponse["id"]

        return redirect("index.html")


if __name__ == "__main__":
    app.run(debug=True)
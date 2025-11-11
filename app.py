import sqlite3

from flask import Flask, flash, redirect, render_template, request, session,g
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


DATABASE = "app.db"

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop("db", None)
    if db is not None:
        db.close()



@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods = ["GET","POST"])
def login():

    if request.method == "GET":
    
        return render_template("login.html")
    
    elif request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        app.logger.debug('username:')
        app.logger.debug(username)
        app.logger.debug('password')
        app.logger.debug(password)
        if username is None or password is None:
            flash("Invalid username or password")
            return render_template("login.html")
        
        flash("ela re")
        return render_template("login.html")
    



if __name__ == "__main__":
    app.run(debug=True)
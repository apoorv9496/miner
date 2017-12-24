from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from flask import Flask
from flask_jsglue import JSGlue

from helper import send_mail, code_gen

# configure application
app = Flask(__name__)
jsglue = JSGlue(app)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

code = 906572
code_reg = 906572

@app.route("/")
def index():

    #clear any running session if tab was closed
    session.clear()

    rows = db.execute("SELECT COUNT(username) as users FROM miner")

    return render_template("index.html", total_registered=rows[0]["users"])

@app.route("/login", methods=["GET", "POST"])
def login():

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return 0 #"username field cannot be blank"

        # ensure password was submitted
        elif not request.form.get("password"):
            return 1 #"password field cannot be blank"

        # query database for username
        rows = db.execute("SELECT * FROM authority WHERE name = :name", name=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return 2 #"password doesn't match"

        global code
        code = send_mail(rows[0]["email"])

        return render_template("code.html")
    else:
        return render_template("index.html")

@app.route("/code_verify", methods=["GET", "POST"])
def code_verify():

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return redirect(url_for("index"))

        # ensure password was submitted
        elif not request.form.get("password"):
            return redirect(url_for("index"))

        # ensure code was submitted
        elif not request.form.get("code_verify"):
            return redirect(url_for("index"))

        global code
        if(str(request.form.get("code_verify")) != str(code)):
            return redirect(url_for("index"))

        # query database for username
        rows = db.execute("SELECT * FROM miner WHERE username = :name", name=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return redirect(url_for("index"))

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        return render_template("miner.html")

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("index.html")

@app.route("/logout")
#@login_required
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return render_template("login.html")

        # ensure email was submitted
        if not request.form.get("email"):
            return render_template("login.html")

        # ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html")

        # ensure re-password was submitted
        elif not request.form.get("re-password"):
            return render_template("login.html")

        global code_reg
        code_reg = send_mail(request.form.get("email"))

        #insert into database the details of the new user
        #rows = db.execute("INSERT INTO miner (user, hash) VALUES(:username, :hash_val)", username=request.form.get("username"), hash_val=pwd_context.hash(request.form.get("password")))

        #if not rows:
        #    return render_template("login.html")

        return render_template("code_reg.html")

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/code_verify_reg", methods=["GET", "POST"])
def code_verify_reg():

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return render_template("login.html")

        # ensure email was submitted
        if not request.form.get("email"):
            return render_template("login.html")

        # ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html")

        # ensure re-password was submitted
        elif not request.form.get("re-password"):
            return render_template("login.html")

        # ensure code was submitted
        elif not request.form.get("code_verify_reg"):
            return render_template("login.html")

        global code
        if(str(request.form.get("code_verify_reg")) != str(code)):
            return redirect(url_for("index"))

        #insert into database the details of the new user
        rows = db.execute("INSERT INTO miner (username, email, hash) VALUES(:username, :email, :hash_val)", username=request.form.get("username"), hash_val=pwd_context.hash(request.form.get("password")), email=request.form.get("email"))

        if not rows:
            return render_template("login.html")

        return render_template("login.html")

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
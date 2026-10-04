from flask import Flask, make_response, render_template, request

import db

app = Flask(__name__)
app.cli.add_command(db.init_db_command)


def render_page(template, title, **context):
    if request.headers.get("HX-Request"):
        html = render_template("fragment.html", page=template, title=title, **context)
    else:
        html = render_template("base.html", page=template, title=title, **context)
    response = make_response(html)
    response.headers["Vary"] = "HX-Request"
    return response


@app.route("/")
def index():
    return render_page("partials/home.html", "Home")


@app.route("/add")
def add():
    return render_page("partials/add.html", "Add")


@app.route("/calendar")
def calendar():
    return render_page("partials/calendar.html", "Calendar")


@app.route("/account")
def account():
    return render_page("partials/account.html", "Account")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_page("partials/register.html", "Register")
    email = request.form["email"].strip().lower()
    password = request.form["password"]
    confirm = request.form["confirm"]
    error = None
    if not email or not password:
        error = "Please enter an email and a password."
    elif len(password) < 8:
        error = "Your password needs at least 8 characters."
    elif password != confirm:
        error = "The passwords don't match."
    if error:
        return render_page("partials/register.html", "Register", error=error, email=email)
    return render_page("partials/register.html", "Register", message="Your details are valid.")

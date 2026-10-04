from flask import Flask, make_response, render_template, request
from flask_login import LoginManager, UserMixin, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

import db

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-to-a-long-random-string"
app.cli.add_command(db.init_db_command)

login_manager = LoginManager(app)


class User(UserMixin):
    def __init__(self, row):
        self.id = row["id"]
        self.email = row["email"]
        self.first_name = row["first_name"]
        self.last_name = row["last_name"]


@login_manager.user_loader
def load_user(user_id):
    conn = db.get_db()
    row = conn.execute(
        "SELECT id, email, first_name, last_name FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()
    conn.close()
    if row is None:
        return None
    return User(row)


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
    conn = db.get_db()
    existing = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
    if existing is not None:
        conn.close()
        return render_page("partials/register.html", "Register",
                           error="That email is already registered.", email=email)
    conn.execute(
        "INSERT INTO users (email, password_hash) VALUES (?, ?)",
        (email, generate_password_hash(password)),
    )
    conn.commit()
    conn.close()
    return render_page("partials/register.html", "Register", message="Account created.")

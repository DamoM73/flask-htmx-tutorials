from flask import Flask, make_response, render_template, request
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

import assessment_service
import db
import user_service

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-to-a-long-random-string"
app.cli.add_command(db.init_db_command)

login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return user_service.get_user(int(user_id))


def render_page(template, title, push_url=None, **context):
    if request.headers.get("HX-Request"):
        html = render_template("fragment.html", page=template, title=title, **context)
    else:
        html = render_template("base.html", page=template, title=title, **context)
    response = make_response(html)
    response.headers["Vary"] = "HX-Request"
    if push_url:
        response.headers["HX-Push-Url"] = push_url
    return response


@app.route("/")
def index():
    return render_page("partials/home.html", "Home")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "GET":
        return render_page("partials/add.html", "Add", values={})
    values = {
        "subject": request.form["subject"].strip(),
        "details": request.form["details"].strip(),
        "start_date": request.form["start_date"],
        "due_date": request.form["due_date"],
    }
    error = None
    if not values["subject"] or not values["details"]:
        error = "Please enter a subject and details."
    elif not values["start_date"] or not values["due_date"]:
        error = "Please choose a start date and a due date."
    elif values["due_date"] < values["start_date"]:
        error = "The due date can't be before the start date."
    if error:
        return render_page("partials/add.html", "Add", error=error, values=values)
    assessment_service.add_assessment(current_user.id, values["subject"], values["details"],
                                      values["start_date"], values["due_date"])
    return render_page("partials/add.html", "Add", values={}, message="Assessment saved.")


@app.route("/calendar")
@login_required
def calendar():
    return render_page("partials/calendar.html", "Calendar")


@app.route("/account")
@login_required
def account():
    return render_page("partials/account.html", "Account", user=current_user)


@app.route("/account/details", methods=["GET", "POST"])
@login_required
def set_details():
    if request.method == "GET":
        return render_page("partials/set_details.html", "Account", values=current_user)
    first_name = request.form["first_name"].strip()
    last_name = request.form["last_name"].strip()
    if not first_name or not last_name:
        return render_page("partials/set_details.html", "Account", values=request.form,
                           error="Please enter your first and last name.")
    user_service.update_details(current_user.id, first_name, last_name)
    user = user_service.get_user(current_user.id)
    return render_page("partials/account.html", "Account", push_url="/account", user=user)


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
    if user_service.email_taken(email):
        return render_page("partials/register.html", "Register",
                           error="That email is already registered.", email=email)
    user_service.create_user(email, password)
    login_user(user_service.check_login(email, password))
    return render_page("partials/set_details.html", "Account", push_url="/account/details",
                       values=current_user)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_page("partials/login.html", "Login")
    email = request.form["email"].strip().lower()
    password = request.form["password"]
    user = user_service.check_login(email, password)
    if user is None:
        return render_page("partials/login.html", "Login",
                           error="Incorrect email or password.", email=email)
    login_user(user)
    return render_page("partials/home.html", "Home", push_url="/")


@app.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return render_page("partials/login.html", "Login", push_url="/login")

from datetime import date

from flask import Flask, abort, make_response, render_template, request
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


@app.template_filter("au_date")
def au_date(iso_date):
    return date.fromisoformat(iso_date).strftime("%d/%m/%Y")


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


def validate_assessment(form):
    values = {
        "subject": form["subject"].strip(),
        "details": form["details"].strip(),
        "start_date": form["start_date"],
        "due_date": form["due_date"],
    }
    if not values["subject"] or not values["details"]:
        return values, "Please enter a subject and details."
    if not values["start_date"] or not values["due_date"]:
        return values, "Please choose a start date and a due date."
    if values["due_date"] < values["start_date"]:
        return values, "The due date can't be before the start date."
    return values, None


@app.route("/")
def index():
    if current_user.is_authenticated:
        return home()
    return render_page("partials/login.html", "Login")


@app.route("/home")
@login_required
def home():
    assessments = assessment_service.get_assessments(current_user.id)
    return render_page("partials/home.html", "Home", push_url="/home", assessments=assessments)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "GET":
        return render_page("partials/add.html", "Add", values={})
    values, error = validate_assessment(request.form)
    if error:
        return render_page("partials/add.html", "Add", error=error, values=values)
    assessment_service.add_assessment(current_user.id, values["subject"], values["details"],
                                      values["start_date"], values["due_date"])
    return render_page("partials/add.html", "Add", values={}, message="Assessment saved.")


@app.route("/assessments/<int:assessment_id>")
@login_required
def assessment_card(assessment_id):
    assessment = assessment_service.get_assessment(assessment_id, current_user.id)
    if assessment is None:
        abort(404)
    return render_template("partials/assessment_card.html", assessment=assessment)


@app.route("/assessments/<int:assessment_id>/complete", methods=["POST"])
@login_required
def complete(assessment_id):
    if assessment_service.get_assessment(assessment_id, current_user.id) is None:
        abort(404)
    assessment_service.set_completed(assessment_id, current_user.id, 1)
    return ""


@app.route("/assessments/<int:assessment_id>/edit", methods=["GET", "POST"])
@login_required
def edit(assessment_id):
    assessment = assessment_service.get_assessment(assessment_id, current_user.id)
    if assessment is None:
        abort(404)
    if request.method == "GET":
        return render_template("partials/edit_form.html", assessment=assessment,
                               values=assessment)
    values, error = validate_assessment(request.form)
    completed = 1 if "completed" in request.form else 0
    if error:
        return render_template("partials/edit_form.html", assessment=assessment,
                               values=values, error=error)
    assessment_service.update_assessment(assessment_id, current_user.id, values["subject"],
                                         values["details"], values["start_date"],
                                         values["due_date"], completed)
    if completed:
        return ""
    assessment = assessment_service.get_assessment(assessment_id, current_user.id)
    return render_template("partials/assessment_card.html", assessment=assessment)


@app.route("/calendar")
@login_required
def calendar():
    chart = assessment_service.get_chart(current_user.id)
    return render_page("partials/calendar.html", "Calendar", chart=chart)


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
    return home()


@app.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return render_page("partials/login.html", "Login", push_url="/login")

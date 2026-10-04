from flask import Flask, make_response, render_template, request

app = Flask(__name__)


def render_page(template, title):
    if request.headers.get("HX-Request"):
        html = render_template(template)
    else:
        html = render_template("base.html", page=template, title=title)
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

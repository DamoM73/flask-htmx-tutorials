from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("base.html", page="partials/home.html", title="Home")


@app.route("/add")
def add():
    return render_template("base.html", page="partials/add.html", title="Add")


@app.route("/calendar")
def calendar():
    return render_template("base.html", page="partials/calendar.html", title="Calendar")


@app.route("/account")
def account():
    return render_template("base.html", page="partials/account.html", title="Account")

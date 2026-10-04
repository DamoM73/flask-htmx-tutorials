from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>StudyM8</h1><p>Your study planner</p>"

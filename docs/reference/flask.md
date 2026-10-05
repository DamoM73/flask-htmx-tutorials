# Flask

!!! learn "On this page we will learn"
    - how routes connect addresses to Python functions
    - how to read form data and send templates back
    - which Flask and Flask-Login tools StudyM8 uses

**Flask** is a Python library that turns Python functions into a web server. We wrote our first Flask app in [First Flask App](../shell/01_first_flask_app.md).

## Commands

| Command | Does |
| :-- | :-- |
| `flask run --debug` | starts the server at `http://127.0.0.1:5000`, restarting whenever we save |
| `flask init-db` | our own command: creates the database from ***schema.sql*** (deletes all data) |
| `flask shell` | a Python prompt that can use our app's files |
| ++ctrl+c++ | stops the server |

## Routes

```python
@app.route("/assessments/<int:assessment_id>/edit", methods=["GET", "POST"])
@login_required
def edit(assessment_id):
    ...
```

| Part | Means |
| :-- | :-- |
| `@app.route("/address")` | run the function below when this address is requested |
| `methods=["GET", "POST"]` | the request methods the route accepts (GET only, if left out) |
| `<int:assessment_id>` | a whole number in the address, passed to the function |
| `@login_required` | only logged-in users can use the route; goes **below** `@app.route` |

## Requests

| Code | Gives |
| :-- | :-- |
| `request.method` | `"GET"` or `"POST"` |
| `request.form["email"]` | the value of the form input named `email` |
| `"completed" in request.form` | whether a checkbox was ticked |
| `request.headers.get("HX-Request")` | the `HX-Request` header, or `None` |

## Responses

| Code | Sends |
| :-- | :-- |
| `return "text"` | the text or HTML in the string |
| `render_template("file.html", name=value)` | a template from the ***templates*** folder, with values for Jinja |
| `make_response(html)` | a response object, so we can add headers |
| `response.headers["HX-Push-Url"] = "/home"` | adds a header to the response |
| `abort(404)` | stops and sends a 404 Not Found error |
| `url_for("static", filename="style.css")` | the address of a file in the ***static*** folder |

## Request lifecycle

| Code | Runs |
| :-- | :-- |
| `@app.before_request` | before every request |
| `@app.after_request` | after every request, with the response |
| `app.teardown_appcontext(close_db)` | when each request finishes, even after an error |
| `g` | an object for storing values during one request |
| `@app.template_filter("au_date")` | registers a Jinja filter |

## Flask-Login

| Code | Does |
| :-- | :-- |
| `LoginManager(app)` | connects Flask-Login to the app |
| `login_manager.login_view = "login"` | where to send visitors who aren't logged in |
| `@login_manager.user_loader` | the function that loads a user from the `id` in the session cookie |
| `class User(UserMixin)` | a user class with the properties Flask-Login needs |
| `login_user(user)` | logs a user in |
| `logout_user()` | logs the current user out |
| `current_user` | the logged-in user, in Python and in templates |
| `current_user.is_authenticated` | `True` if someone is logged in |

## Password hashing (Werkzeug)

| Code | Does |
| :-- | :-- |
| `generate_password_hash(password)` | makes a salted hash of a password |
| `check_password_hash(hash, password)` | `True` if the password matches the hash |

## Documentation

Documentation is the official guide written by the people who made the code library, and we can use it to look up every function, including ones that aren't covered on this page.

- [Flask documentation](https://flask.palletsprojects.com/)
- [Flask-Login documentation](https://flask-login.readthedocs.io/)
- [Werkzeug password hashing](https://werkzeug.palletsprojects.com/en/stable/utils/#module-werkzeug.security)

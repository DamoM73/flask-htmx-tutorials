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

## More for your own website

### Public pages and member pages

A community website has two audiences: members, and people who want to learn about or join the group. Leave `@login_required` off public pages (home, news, events, contact) and add it to member-only pages. A template can show extra parts to members:

```html+jinja
{% if current_user.is_authenticated %}
<a href="/events/{{ event.id }}/rsvp" role="button">I'm going</a>
{% else %}
<p><a href="/login">Log in</a> to RSVP.</p>
{% endif %}
```

### Admins and roles

Only organisers should post news or delete events. Give the users table an `is_admin` column (see [SQL](sql.md#adding-a-column-to-an-existing-table)), load it in the `User` class (`self.is_admin = row["is_admin"]`, and add `is_admin` to the `SELECT` in `get_user`), then make a decorator that only lets admins through:

```python
from functools import wraps


def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return view(*args, **kwargs)
    return wrapped
```

Use it in place of `@login_required`:

```python
@app.route("/news/add", methods=["GET", "POST"])
@admin_required
def add_news():
    ...
```

- `@wraps(view)` → keeps the original function's name, which Flask uses for the route
- `@login_required` → visitors who aren't logged in are sent to the login page first
- `abort(403)` → sends **403 Forbidden**: logged in, but not allowed

Make the first admin in the Flask shell:

```text
>>> import db
>>> conn = db.get_db()
>>> conn.execute("UPDATE users SET is_admin = 1 WHERE email = ?", ("you@example.org",))
>>> conn.commit()
```

In templates, show admin buttons with `{% if current_user.is_authenticated and current_user.is_admin %}`. Hiding a button isn't enough on its own; the route must also use `@admin_required`.

### Deleting

```python
@app.route("/events/<int:event_id>", methods=["DELETE"])
@admin_required
def delete_event(event_id):
    if not event_service.delete_event(event_id):
        abort(404)
    return ""
```

The button that sends the request uses `hx-delete` and `hx-confirm` (see [HTMX](htmx.md#deleting-with-a-confirmation)).

### Query strings

Values after a `?` in an address, like `/events?team=u12&month=03`, are a **query string**. Filters, searches and page numbers usually use them, because they don't change anything on the server.

```python
team = request.args.get("team", "")
page = request.args.get("page", 1, type=int)
```

- `request.args.get("team", "")` → the value, or `""` if it isn't there
- `type=int` → turns the value into a number, or uses the default if it isn't a number

### File uploads

Admins may want to add images to news posts. The form needs `enctype="multipart/form-data"` so the file is sent:

```html
<form hx-post="/news/add" hx-target="#content" enctype="multipart/form-data">
    <label>
        Image
        <input type="file" name="image" accept="image/*">
    </label>
    ...
</form>
```

```python
import uuid
from pathlib import Path

from werkzeug.utils import secure_filename

UPLOAD_FOLDER = Path(__file__).parent / "static" / "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024


def save_image(file):
    if file is None or file.filename == "":
        return None
    extension = file.filename.rsplit(".", 1)[-1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        return None
    filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
    file.save(UPLOAD_FOLDER / filename)
    return filename
```

In the route, `filename = save_image(request.files.get("image"))`, then save `filename` in the news row. Show it with `url_for('static', filename='uploads/' + news.image)`.

- create the ***static/uploads*** folder first
- `request.files` → uploaded files, by input name
- `ALLOWED_EXTENSIONS` → only accept image files, so nobody can upload a program
- `secure_filename` → removes characters that could be used to save the file somewhere dangerous
- `uuid.uuid4().hex` → a random string at the start, so two files called ***photo.jpg*** don't overwrite each other
- `MAX_CONTENT_LENGTH` → refuses uploads bigger than 5 MB

### Redirects and flash messages

StudyM8 always sends back a page after a form. Many Flask sites instead **redirect** after a POST, so refreshing the page doesn't submit the form again:

```python
from flask import flash, redirect, url_for

flash("Event saved.")
return redirect(url_for("events"))
```

- `redirect(...)` → tells the browser to load a different address
- `url_for("events")` → the address of the `events` view function
- `flash("...")` → stores a message to show on the next page

Show flashed messages in ***base.html*** and ***fragment.html***, just above `{% include page %}`:

```html+jinja
{% for message in get_flashed_messages() %}
<p class="success">{{ message }}</p>
{% endfor %}
```

With HTMX requests, StudyM8's `render_page(..., push_url=...)` already does the same job as a redirect. To make HTMX load a completely new page instead, send an `HX-Redirect` header: `response.headers["HX-Redirect"] = url_for("events")`.

### Error pages

```python
@app.errorhandler(404)
def not_found(error):
    return render_page("partials/not_found.html", "Not Found"), 404
```

Returning a tuple sends the page with the status code. Write ***not_found.html*** with a friendly message and a link back to the home page. Do the same for `403`.

!!! tip "HTMX and error pages"
    HTMX doesn't swap 4xx and 5xx responses into the page, so an HTMX request that gets a 404 seems to do nothing. Normal page loads show the error page as expected. To swap 404 pages too, add this to the `htmx-config` meta tag: `"responseHandling": [{"code": "204", "swap": false}, {"code": "[23]..", "swap": true}, {"code": "404", "swap": true}, {"code": "[45]..", "swap": false, "error": true}]`.

### A contact form without email

Sending email needs a mail server, which is beyond this course. Instead, save messages in a table and show them on an admin-only page:

```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL,
    sent_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);
```

The contact route validates and `INSERT`s, just like the Add page in StudyM8. Also show the group's email address and phone number with `mailto:` and `tel:` links (see [HTML](html.md#contact-links)).

### Working with dates and times in Python

```python
from datetime import date, datetime

today = date.today()
starts = datetime.fromisoformat("2026-03-14T09:00")
if starts.date() < today:
    error = "That event is in the past."
```

`fromisoformat` turns the text from a `datetime-local` input into a `datetime`, so we can compare it.

### Running the website on our laptop

Our website runs on our own laptop. `flask run` starts a small web server, and the browser connects to it at `http://127.0.0.1:5000`. The address `127.0.0.1` means "this computer", so the site only works on the laptop that's running it. That's all we need to build, test and present the website.

1. Open the project folder in VS Code and activate the virtual environment.
2. Run `flask run --debug`. Debug mode restarts the server when we save a file and shows a detailed error page when something goes wrong.
3. Open `http://127.0.0.1:5000` in the browser.
4. Press ++ctrl+c++ in the terminal to stop the server.

To check how the site looks on a phone, open the browser's device toolbar (++f12++, then the phone and tablet icon) and choose a phone size.

#### A clean demo database

Before testing or presenting, reset the database so it has the same sample content every time:

```text
flask init-db
flask seed-db
```

`init-db` deletes everything and creates empty tables, then `seed-db` fills them from ***seed.sql*** (see [Sample data](sql.md#sample-data)).

#### Letting other people try it

Because the site only runs on our laptop, testers and our teacher use it on our laptop:

- **Usability testing**: hand the laptop to the tester, in class or at home, and watch them (see [Usability testing](test_plans.md#usability-testing)).
- **Presenting**: run the site on our laptop and show it on the classroom screen.
- **Evidence**: take screenshots and short screen recordings of the site working, including the phone view in the device toolbar.

!!! warning "Keep it safe"
    Use made-up names and details in the sample data, never real members' personal information. Keep `SECRET_KEY` out of anything we share, and set it to a long random string.

## Documentation

Documentation is the official guide written by the people who made the code library, and we can use it to look up every function, including ones that aren't covered on this page.

- [Flask documentation](https://flask.palletsprojects.com/)
- [Flask-Login documentation](https://flask-login.readthedocs.io/)
- [Werkzeug password hashing](https://werkzeug.palletsprojects.com/en/stable/utils/#module-werkzeug.security)
- [Flask file uploads](https://flask.palletsprojects.com/en/stable/patterns/fileuploads/)
- [The Flask development server](https://flask.palletsprojects.com/en/stable/server/)

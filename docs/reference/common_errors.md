# Common Errors

!!! learn "On this page we will learn"
    - how to read a Python error message
    - what the errors we're most likely to see in StudyM8 mean
    - how to fix each one

## Reading an error

When our code crashes, Flask shows an error page in the browser, and the terminal shows a **traceback**: the list of code that was running when the error happened. Tracebacks can be long, but the important parts are:

- the **last line** → the type of error and a message saying what went wrong
- the lines that mention **our files** (like ***app.py***) → where in our code it happened

Lines that mention files inside ***.venv*** are Flask's own code, so we can usually skip them.

## Starting the server

### ImportError when running flask { #import-error }

``` { .text .error linenums="1" }
Error: While importing 'app', an ImportError was raised:

Traceback (most recent call last):
  File "C:\Users\student\Documents\studym8\app.py", line 5, in <module>
    from flask_login import LoginManager, current_user, login_required, login_user, logout_user
ModuleNotFoundError: No module named 'flask_login'
```

- **line 1** → Flask couldn't load ***app.py***.
- **lines 4–5** → the line of ***app.py*** that imports Flask-Login.
- **line 6** → Python can't find the `flask_login` library.

**Fix:** the virtual environment isn't active, or the library isn't installed. Check the terminal prompt starts with `(.venv)` (see [Setting Up](../start/setup.md#create-a-virtual-environment)), then run `pip install flask flask-login plotly pandas`.

## Templates

### TemplateNotFound { #template-not-found }

``` { .text .error linenums="1" }
  File "C:\Users\student\Documents\studym8\app.py", line 8, in index
    return render_template("index.html")
jinja2.exceptions.TemplateNotFound: index.html
```

- **lines 1–2** → the line of our code that asked for the template.
- **line 3** → Flask couldn't find a template with that name.

**Fix:** check the ***templates*** folder is spelt correctly and sits next to ***app.py***, and that the file name (including any folder, like `partials/`) matches exactly.

### Missing endif { #missing-endif }

``` { .text .error linenums="1" }
jinja2.exceptions.TemplateSyntaxError: Unexpected end of template. Jinja was looking for the following tags: 'elif' or 'else' or 'endif'. The innermost block that needs to be closed is 'if'.
```

- **line 1** → an `{% if %}` was never closed.

**Fix:** add `{% endif %}`. The same error appears with `for` and `endfor`.

### 'values' is undefined { #values-is-undefined }

``` { .text .error linenums="1" }
jinja2.exceptions.UndefinedError: 'values' is undefined
```

- **line 1** → the template used `values.something`, but the route didn't send `values`.

**Fix:** send the variable from every `render_page` or `render_template` call that uses this template, even if it's empty: `values={}`.

### BuildError { #build-error }

``` { .text .error linenums="1" }
werkzeug.routing.exceptions.BuildError: Could not build url for endpoint 'statc' with values ['filename']. Did you mean 'static' instead?
```

- **line 1** → `url_for` was given a name that isn't a route or `static`. Flask suggests what we probably meant.

**Fix:** correct the spelling in `url_for(...)`.

## Requests

### 405 Method Not Allowed { #method-not-allowed }

The browser shows **Method Not Allowed: The method is not allowed for the requested URL.**

**Fix:** a form sent a POST to a route that only accepts GET. Add `methods=["GET", "POST"]` to the route's `@app.route`.

### 400 Bad Request { #bad-request }

The browser shows **Bad Request: The browser (or proxy) sent a request that this server could not understand.**

**Fix:** the code asked for `request.form["name"]`, but the form has no input with that `name`. Check the spelling matches in the template and in ***app.py***.

### 404 Not Found { #not-found }

The browser shows **Not Found**.

**Fix:** check the address is right. For an assessment, our code sends a 404 on purpose when the assessment doesn't belong to the logged-in user.

## Users

### 'AnonymousUserMixin' object has no attribute 'id' { #anonymous-user }

``` { .text .error linenums="1" }
AttributeError: 'AnonymousUserMixin' object has no attribute 'id'
```

- **line 1** → the code used `current_user.id`, but nobody is logged in, so `current_user` is an anonymous user with no `id`.

**Fix:** add `@login_required` below the route's `@app.route`. See [Prevent Unauthorised Access](../assessments/22_unauthorised_access.md).

## Database

### no such table { #no-such-table }

``` { .text .error linenums="1" }
sqlite3.OperationalError: no such table: users
```

- **line 1** → the database doesn't have that table.

**Fix:** stop the server and run `flask init-db`. Run it again after changing ***schema.sql*** (this deletes all data).

### UNIQUE constraint failed { #unique-constraint }

``` { .text .error linenums="1" }
sqlite3.IntegrityError: UNIQUE constraint failed: users.email
```

- **line 1** → an `INSERT` tried to add a second row with the same email.

**Fix:** check for an existing row before inserting, like `email_taken` does.

### FOREIGN KEY constraint failed { #foreign-key-constraint }

``` { .text .error linenums="1" }
sqlite3.IntegrityError: FOREIGN KEY constraint failed
```

- **line 1** → a row's `user_id` doesn't match any user. Usually the database was recreated while someone was still logged in.

**Fix:** log out, register again, and try again.

### Cannot operate on a closed database { #closed-database }

``` { .text .error linenums="1" }
sqlite3.ProgrammingError: Cannot operate on a closed database.
```

- **line 1** → code used a database connection after it was closed.

**Fix:** after [One Connection per Request](../optimisation/31_fewer_connections.md), remove every `conn.close()` from ***user_service.py*** and ***assessment_service.py***.

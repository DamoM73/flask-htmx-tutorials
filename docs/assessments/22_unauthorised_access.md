# 22. Prevent Unauthorised Access

!!! learn "In this lesson we will learn"
    - why hiding links doesn't protect a page
    - how `@login_required` protects a route
    - how Flask-Login sends visitors to the login page
    - why every query must check who owns the data

## Introduction

In [Account Link Visibility](../users/12_link_visibility.md) we hid the Add, Calendar and Account links from logged-out visitors. But anyone can still type `/add` into the address bar. Worse, if a logged-out visitor submits the Add form, our code tries to use `current_user.id`, which an anonymous user doesn't have, and the server crashes.

So the server itself needs to refuse these pages to anyone who isn't logged in. Flask-Login has a decorator for this: `@login_required`. If someone who isn't logged in asks for a route with this decorator, Flask-Login sends them to the login page instead.

!!! primm "PRIMM"
    1. **Predict** what will happen if you log out and type `http://127.0.0.1:5000/add` into the address bar.
    2. **Run** it to find out. Then fill in the form and click Save.
    3. Time to **investigate**. Look at the terminal. What type of error was raised? Why?

## Protect the routes

Go back to ***app.py*** and change the highlighted code at the top of the file.

```python linenums="1" hl_lines="2 13" title="app.py"
--8<-- "examples/assessments/22_unauthorised_access/step01/app.py:1:13"
```

??? note "Code explanation"
    - **line 2** → also imports `login_required` from Flask-Login.
    - **line 13** → tells Flask-Login which view function shows the login page, so it knows where to send visitors who aren't logged in.

Now add `@login_required` below the `@app.route` line of each route that needs a logged-in user. Start with `add`:

```python linenums="38" hl_lines="2" title="app.py"
--8<-- "examples/assessments/22_unauthorised_access/step01/app.py:38:40"
```

??? note "Code explanation"
    - **line 39** → only lets logged-in users use the `add` route. The decorator must go **below** `@app.route`.

Then do the same for `calendar`, `account` and `set_details`:

```python linenums="63" hl_lines="2 8 14" title="app.py"
--8<-- "examples/assessments/22_unauthorised_access/step01/app.py:63:77"
```

??? note "Code explanation"
    - **line 64** → protects the `calendar` route.
    - **line 70** → protects the `account` route.
    - **line 76** → protects the `set_details` route.

!!! primm "PRIMM"
    1. **Predict** what will happen now when you log out and type `http://127.0.0.1:5000/add` into the address bar.
    2. **Run** it to find out. Look at the address bar after the page loads.
    3. Time to **investigate**. What does `?next=%2Fadd` at the end of the address mean? (Hint: `%2F` is how a `/` is written inside an address.)

!!! tip "Why below @app.route?"
    Decorators wrap the function below them, from the bottom up. `@login_required` wraps `add` first, so the login check runs before our code. Then `@app.route` connects the wrapped function to the address. If the order were swapped, Flask would connect the unprotected function, and the check would never run.

## Who owns the data?

Logging in proves **who** someone is. It doesn't decide **what** they're allowed to see. Each assessment belongs to one user, so whenever we read or change an assessment, our SQL must check that it belongs to the logged-in user:

- reading assessments → `WHERE user_id = ?`
- reading or changing one assessment → `WHERE id = ? AND user_id = ?`

If we forgot the `user_id` check, a logged-in user could change the number in an address like `/assessments/7/edit` and see or edit someone else's assessment. We'll use these checks in every assessment query from the next lesson on.

!!! warning "Never trust the address"
    Users can type any address and send any form data. The server must check, on every request, that the user is logged in **and** that the data they're asking for is theirs.

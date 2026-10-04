# 11. Log In and Log Out

!!! learn "In this lesson we will learn"
    - how websites remember who's logged in with sessions and cookies
    - how to set up Flask-Login and a `User` class
    - how to check a password against its hash
    - how to log users in and out

## Introduction

Users can register, but they can't log in yet. Logging in raises a tricky problem: HTTP has no memory. Every request is separate, so the server doesn't know that the request for the Home page came from the same person who logged in a moment ago.

Websites solve this with a **session**. When we log in, the server gives the browser a **cookie**: a small piece of data the browser stores and sends back with every request to that website. The cookie holds our user's `id`, and it's **signed** with a secret key, so nobody can change it to pretend to be someone else.

**Flask-Login** is a library that handles all of this for us. We just need to tell it:

1. how to describe a user → a `User` class
2. how to load a user from the database using the `id` in the cookie → a **user loader** function
3. when to log a user in or out → `login_user` and `logout_user`

## Set up Flask-Login

Go back to ***app.py*** and change the highlighted code below.

```python linenums="1" hl_lines="2-3 8 11 14-19 22-32" title="app.py"
--8<-- "examples/users/11_login_logout/step01/app.py:1:32"
```

??? note "Code explanation"
    - **line 2** → imports the parts of Flask-Login we need.
    - **line 3** → also imports `check_password_hash`, which checks a password against a saved hash.
    - **line 8** → sets the app's **secret key**, which Flask uses to sign the session cookie. On a real website this would be a long random string kept out of the code.
    - **line 11** → creates a `LoginManager`, which connects Flask-Login to our app.
    - **line 14** → defines a `User` class. Inheriting from `UserMixin` gives it the properties Flask-Login expects, such as `is_authenticated`.
    - **line 15** → the constructor takes a row from the users table.
    - **lines 16–19** → copy the row's columns into the user object's attributes.
    - **line 22** → a decorator that tells Flask-Login to use the function below to load users.
    - **line 23** → defines `load_user`. Flask-Login calls it on every request, with the `id` from the session cookie.
    - **line 24** → opens a connection to the database.
    - **lines 25–28** → selects the user with that `id`, without the password hash, which we don't need here.
    - **line 29** → closes the connection.
    - **line 30** → checks whether no user was found (for example, if the database was recreated)…
    - **line 31** → …if so, returns `None`, so Flask-Login treats the visitor as logged out.
    - **line 32** → otherwise, returns a `User` object made from the row.

## The login form

Create a new file, add the code below and save it as ***login.html*** in the ***templates/partials*** folder.

```html+jinja linenums="1" title="templates/partials/login.html"
--8<-- "examples/users/11_login_logout/step02/templates/partials/login.html"
```

??? note "Code explanation"
    - **lines 1–2** → open the card and show the heading.
    - **line 3** → opens the form, which posts to `/login` and swaps the response into `<main>`.
    - **lines 4–7** → the email input, filled with the email the user typed if there was an error.
    - **lines 8–11** → the password input.
    - **lines 12–14** → show the error message, if there is one.
    - **line 15** → the Login button.
    - **lines 16–17** → close the form and the card.

## The login and logout routes

When a user logs in, we want to take them to the Home page, and change the address bar to `/`. Because the form's request went to `/login`, HTMX doesn't know the address should change. The server can tell it, by sending an `HX-Push-Url` header in the response.

Go back to ***app.py*** and change the highlighted code in `render_page`.

```python linenums="35" hl_lines="1 8-9" title="app.py"
--8<-- "examples/users/11_login_logout/step03/app.py:35:44"
```

??? note "Code explanation"
    - **line 35** → adds a `push_url` parameter. Its default is `None`, so routes that don't need it can leave it out.
    - **line 42** → checks whether a `push_url` was given…
    - **line 43** → …if so, adds an `HX-Push-Url` header, which tells HTMX to change the address bar to that address.

Then add the two new routes to the bottom of ***app.py***.

```python linenums="98" hl_lines="1-14 17-20" title="app.py"
--8<-- "examples/users/11_login_logout/step03/app.py:98:117"
```

??? note "Code explanation"
    - **line 98** → creates the `/login` route for GET and POST requests.
    - **line 99** → defines the `login` view function.
    - **line 100** → checks whether the request is a GET…
    - **line 101** → …if so, shows the empty login form.
    - **line 102** → gets the email from the form, without spaces and in lower case.
    - **line 103** → gets the password from the form.
    - **line 104** → opens a connection to the database.
    - **line 105** → finds the user with this email. `*` selects every column, including the password hash.
    - **line 106** → closes the connection.
    - **line 107** → checks whether no user was found, or the password doesn't match the saved hash…
    - **lines 108–109** → …if so, shows the form again with an error.
    - **line 110** → otherwise, logs the user in. Flask-Login puts the user's `id` in the session cookie.
    - **line 111** → shows the Home page and changes the address bar to `/`.
    - **line 114** → creates the `/logout` route, which only accepts POST.
    - **line 115** → defines the `logout` view function.
    - **line 116** → logs the user out, removing their `id` from the session cookie.
    - **line 117** → shows the login form and changes the address bar to `/login`.

!!! tip "Why doesn't the error say which one was wrong?"
    The error says "Incorrect email or password" whether the email or the password was wrong. If it said "No account with that email", an attacker could use the login form to find out who has an account.

!!! tip "Why is logout a POST?"
    A GET request should only ever fetch something. Logging out changes something (the session), so it uses POST. It also means a simple link or image on another website can't log our users out.

## The menu links

Open ***templates/nav.html***, add the highlighted code below and save it.

```html+jinja linenums="1" hl_lines="10 12" title="templates/nav.html"
--8<-- "examples/users/11_login_logout/step04/templates/nav.html"
```

??? note "Code explanation"
    - **line 10** → adds a Logout link. `hx-post="/logout"` sends a POST request to `/logout`. The response goes into `<main>`, because the link is inside the list that sets `hx-target`.
    - **line 12** → adds a Login link, marked as current when the title is `"Login"`.

!!! primm "PRIMM"
    1. **Predict** what will happen when you log in with the account you registered last lesson. What will happen with the wrong password?
    2. **Run** the code. Try logging in with a wrong password, then with the right one. Then click Logout.
    3. Time to **investigate**. Open the developer tools (++f12++) and click **Application**, then **Cookies** and `http://127.0.0.1:5000`. Log in and out while you watch. What happens to the cookie called `session`?

## Log in after registering

It would be annoying to register and then have to log in straight away. Let's log new users in as soon as their account is created.

Go back to ***app.py*** and change the highlighted code at the end of the `register` function.

```python linenums="82" hl_lines="13 15-16" title="app.py"
--8<-- "examples/users/11_login_logout/step05/app.py:82:97"
```

??? note "Code explanation"
    - **line 94** → selects the new user's row, now that it's been saved.
    - **line 96** → logs the new user in.
    - **line 97** → shows the Home page and changes the address bar to `/`.

The register form no longer needs to show a success message. Open ***templates/partials/register.html*** and delete the three lines that show the message:

```html+jinja
        {% if message %}
        <p class="success">{{ message }}</p>
        {% endif %}
```

!!! primm "PRIMM"
    1. **Predict** what you'll see after registering a new account.
    2. **Run** the code by registering another account.
    3. Time to **investigate**. Look at the menu after you've logged in. Which links don't make sense for a logged-in user? Which links don't make sense for someone who isn't logged in?

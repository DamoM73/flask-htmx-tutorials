# 10. Register

!!! learn "In this lesson we will learn"
    - how to build an HTML form with labels and inputs
    - how a form sends data to Flask with a POST request
    - how to validate form data on the server
    - how to hash a password and save a new user to the database

## Introduction

Before anyone can log in, they need an account. In this lesson we'll build the Register page.

Let's think about what happens when someone registers:

| Input | Process | Output |
| :-- | :-- | :-- |
| email, password and confirm password, typed into a form | check every field has a value, the password is long enough and both passwords match | an error message if anything is wrong |
| | check the email isn't already registered | an error message if it is |
| | hash the password and save the new user in the users table | a message saying the account was created |

So we need:

1. a form → ***templates/partials/register.html***
2. a Register link in the menu → ***templates/nav.html***
3. a route that shows the form and processes it → ***app.py***

## The form

A **form** collects information from the user and sends it to the server. Each piece of information is typed into an **input**, and each input has a **label** that says what to type.

Create a new file, add the code below and save it as ***register.html*** in the ***templates/partials*** folder.

```html+jinja linenums="1" title="templates/partials/register.html"
--8<-- "examples/users/10_register/step01/templates/partials/register.html"
```

??? note "Code explanation"
    - **line 1** → opens an `<article>`, so Pico draws the form in a card.
    - **line 2** → the page heading.
    - **line 3** → opens the `<form>`. When the form is submitted, `hx-post="/register"` sends its data to the `/register` route as a POST request, and `hx-target="#content"` swaps the response into `<main>`.
    - **lines 4–7** → a label with an email input inside it. `type="email"` tells the browser to expect an email address. `name="email"` is the name Flask uses to find the value. `required` stops the browser sending the form while the input is empty.
    - **lines 8–11** → the password input. `type="password"` hides what's typed.
    - **lines 12–15** → a second password input, so users type their password twice.
    - **line 16** → the button that submits the form.
    - **lines 17–18** → close the form and the card.

!!! tip "Labels"
    Putting an input inside its `<label>` connects them. Clicking the label puts the cursor in the input, and screen readers read the label out when the input is selected. Pico also uses the label to lay out the form.

## The Register link

Open ***templates/nav.html***, add the highlighted code below and save it.

```html+jinja linenums="1" hl_lines="10" title="templates/nav.html"
--8<-- "examples/users/10_register/step02/templates/nav.html"
```

??? note "Code explanation"
    - **line 10** → adds a Register link to the menu, marked as current when the title is `"Register"`.

## The register route

The register route has two jobs:

- a GET request (clicking the Register link) → show the empty form
- a POST request (submitting the form) → check the data and respond

Our route also needs to send extra values, like an error message, to the templates. So we'll let `render_page` accept any number of extra values, and pass them all on.

Go back to ***app.py*** and change the highlighted code below.

```python linenums="1" hl_lines="9 11 13" title="app.py"
--8<-- "examples/users/10_register/step03/app.py:1:16"
```

??? note "Code explanation"
    - **line 9** → adds `**context` to `render_page`. The two stars collect any extra **keyword arguments** (like `error="..."`) into a dictionary called `context`.
    - **line 11** → `**context` passes every value in the dictionary on to the fragment template.
    - **line 13** → passes the same values on to the full page template.

Now add the route to the bottom of ***app.py***.

```python linenums="39" hl_lines="1-17" title="app.py"
--8<-- "examples/users/10_register/step03/app.py:39:55"
```

??? note "Code explanation"
    - **line 39** → creates the `/register` route. `methods=["GET", "POST"]` lets it accept both kinds of request; by default, a route only accepts GET.
    - **line 40** → defines the `register` view function.
    - **line 41** → checks whether the request is a GET…
    - **line 42** → …if so, shows the empty form and finishes.
    - **line 43** → gets the email from the submitted form. `.strip()` removes spaces from each end and `.lower()` makes it lower case, so `Sam@School.com ` and `sam@school.com` count as the same email.
    - **lines 44–45** → get the two passwords from the form.
    - **line 46** → starts with no error.
    - **line 47** → checks whether the email or password is empty…
    - **line 48** → …if so, sets an error message.
    - **line 49** → otherwise, checks whether the password is shorter than 8 characters…
    - **line 50** → …if so, sets an error message.
    - **line 51** → otherwise, checks whether the two passwords are different…
    - **line 52** → …if so, sets an error message.
    - **line 53** → checks whether there's an error…
    - **line 54** → …if so, shows the form again with the error message and the email the user typed.
    - **line 55** → otherwise, shows the form with a message saying the details are valid. We'll save the user here soon.

!!! tip "Never trust the browser"
    The `required` attribute stops the browser sending empty inputs, so why check again on the server? Because anyone can change the HTML in their browser, or send a request without using our form at all. The server must always **validate** (check) every piece of data it receives.

## Show the messages

Our route sends `error`, `email` and `message` to the template, but the template doesn't use them yet.

Open ***templates/partials/register.html***, change the highlighted code below and save it.

```html+jinja linenums="1" hl_lines="6 16-21" title="templates/partials/register.html"
--8<-- "examples/users/10_register/step04/templates/partials/register.html"
```

??? note "Code explanation"
    - **line 6** → fills the email input with the email the user typed, so they don't have to type it again after an error. When `email` hasn't been sent, Jinja shows nothing.
    - **line 16** → checks whether an error was sent…
    - **line 17** → …if so, shows it in a paragraph with the class `error`.
    - **line 18** → ends the `if`.
    - **lines 19–21** → show the message, if one was sent, in a paragraph with the class `success`.

Now let's colour the messages. Open ***static/style.css***, add the highlighted code below and save it.

```css linenums="1" hl_lines="6-8 10-12" title="static/style.css"
--8<-- "examples/users/10_register/step05/static/style.css"
```

??? note "Code explanation"
    - **line 6** → a selector for every element with the class `error`. A dot means "class".
    - **line 7** → sets the text colour to Pico's colour for deleted text, which is red.
    - **line 8** → ends the styles for `.error`.
    - **lines 10–12** → give elements with the class `success` Pico's colour for inserted text, which is green.

!!! primm "PRIMM"
    1. **Predict** what will happen if you submit the form with a password of `cat`.
    2. **Run** the code. Click Register and try these, one at a time: a short password, two passwords that don't match, then valid details.
    3. Time to **investigate**. Remove the `required` from the email input in the browser: right-click the input, choose **Inspect**, double-click `required` and delete it. Now submit the form with no email. Which line of ***app.py*** caught the problem?

## Save the user

Now we can save valid users to the database. We need to:

1. check no one has already registered with that email
2. **hash** the password
3. `INSERT` the new user into the users table

A **hash** is a scrambled version of a password, made by a one-way calculation. It's easy to turn a password into a hash, but impossible to turn a hash back into the password. When a user logs in, we hash the password they type and check it matches the saved hash.

Go back to ***app.py*** and add the highlighted code below at the top.

```python linenums="1" hl_lines="2" title="app.py"
--8<-- "examples/users/10_register/step06/app.py:1:4"
```

??? note "Code explanation"
    - **line 2** → imports `generate_password_hash` from Werkzeug, a library that comes with Flask.

Then change the highlighted code at the end of the `register` function.

```python linenums="54" hl_lines="3-15" title="app.py"
--8<-- "examples/users/10_register/step06/app.py:54:68"
```

??? note "Code explanation"
    - **line 56** → opens a connection to the database.
    - **line 57** → looks for a user with this email. `.fetchone()` gets the first row found, or `None` if there are no rows.
    - **line 58** → checks whether a user was found…
    - **line 59** → …if so, closes the connection…
    - **lines 60–61** → …and shows the form again with an error. The line is split in two because it's long; Python joins lines that are inside brackets.
    - **lines 62–65** → inserts the new user, with their email and the hash of their password. The two `?` placeholders are filled from the tuple on line 64.
    - **line 66** → saves the new row.
    - **line 67** → closes the connection.
    - **line 68** → shows the form with a message saying the account was created.

!!! warning "Did we create the database?"
    If we skipped `flask init-db` in the last lesson, submitting the form shows an error page, and the terminal shows a long error ending like this:

    ``` { .text .error linenums="1" }
      File "C:\Users\student\Documents\studym8\app.py", line 57, in register
        existing = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
    sqlite3.OperationalError: no such table: users
    ```

    - **line 1** → the error happened on line 57 of ***app.py***, in the `register` function.
    - **line 2** → the line that caused it: the `SELECT` that looks for the email.
    - **line 3** → an `OperationalError` from SQLite: there's no users table to look in.

    Stop the server, run `flask init-db`, then start the server again.

!!! primm "PRIMM"
    1. **Predict** what will happen if you register the same email twice.
    2. **Run** the code. Register a new account, then try to register the same email again, this time with capital letters.
    3. Time to **investigate**. Stop the server and open the Flask shell. Use `SELECT` to look at your user's `password_hash`. Then register a second user with the **same** password and compare their hashes. Why are they different?

!!! tip "Why are the hashes different?"
    Werkzeug adds a random **salt** to each password before hashing it, and saves the salt at the start of the hash. Two users with the same password get different hashes, so an attacker can't tell they share a password. When checking a password, Werkzeug reads the salt back out of the saved hash.

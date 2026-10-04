# 13. Account Page

!!! learn "In this lesson we will learn"
    - how to send the logged-in user to a template
    - how to show an object's attributes with Jinja
    - how `or` gives a default value when something is empty

## Introduction

Now that users can log in, the Account page can show their details. If we look back at the [design](../start/design.md#account-and-set-details), the Account page shows the user's email, first name and last name.

So let's think about this:

1. The logged-in user is `current_user`, a `User` object with `email`, `first_name` and `last_name` attributes.
2. The account route will send that object to the template as `user`.
3. The template will show each attribute in the card.

!!! tip "Why send user?"
    Templates can already use `current_user`, so why send it as `user`? In [Set Details Code](15_set_details_code.md) we'll show the Account page straight after changing the user's name. At that moment `current_user` still holds the old name, so we'll need to send a fresh copy of the user instead. Using `user` in the template means it works both ways.

## The account template

Open ***templates/partials/account.html***, replace its code with the code below and save it.

```html+jinja linenums="1" title="templates/partials/account.html"
--8<-- "examples/account/13_account_page/step01/templates/partials/account.html"
```

??? note "Code explanation"
    - **line 1** → opens the card.
    - **line 2** → the page heading.
    - **line 3** → shows the user's email. `{{ user.email }}` gets the `email` attribute of the `user` object, just like `user.email` in Python.
    - **line 4** → shows the user's first name. A new user hasn't set their name yet, so `first_name` is `None`. `or ""` shows an empty string instead of the word "None".
    - **line 5** → shows the user's last name, in the same way.
    - **line 6** → closes the card.

## The account route

Go back to ***app.py*** and change the highlighted code below at the top of the file.

```python linenums="1" hl_lines="2" title="app.py"
--8<-- "examples/account/13_account_page/step02/app.py:1:3"
```

??? note "Code explanation"
    - **line 2** → also imports `current_user` from Flask-Login, so our Python code can use it.

Then change the highlighted code in the `account` function.

```python linenums="62" hl_lines="3" title="app.py"
--8<-- "examples/account/13_account_page/step02/app.py:62:64"
```

??? note "Code explanation"
    - **line 64** → sends the logged-in user to the template as `user`.

!!! primm "PRIMM"
    1. **Predict** what the Account page will show for the account you're logged in with.
    2. **Run** the code by logging in and clicking Account.
    3. Time to **investigate**. Remove `or ""` from line 4 of ***account.html*** and refresh. What changes? Why? Put it back when you're done.
    4. Now **modify** the template so the email is shown last.

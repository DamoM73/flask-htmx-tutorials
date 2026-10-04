# 15. Set Details Code

!!! learn "In this lesson we will learn"
    - how to validate the set details form
    - how to change a row in the database with `UPDATE`
    - why `current_user` can be out of date straight after a change

## Introduction

Our Set Details form doesn't save anything yet. When the user clicks Save, we need to:

| Input | Process | Output |
| :-- | :-- | :-- |
| first name and last name, typed into the form | check both names have a value | an error message if either is empty |
| | `UPDATE` the user's row in the users table | |
| | load the user again from the database | the Account page, showing the new names |

## Show errors

Open ***templates/partials/set_details.html***, add the highlighted code below and save it.

```html+jinja linenums="1" hl_lines="12-14" title="templates/partials/set_details.html"
--8<-- "examples/account/15_set_details_code/step01/templates/partials/set_details.html"
```

??? note "Code explanation"
    - **lines 12–14** → show the error message, if there is one, using the `error` class we made in [Register](../users/10_register.md#show-the-messages).

## Save the names

Go back to ***app.py*** and change the highlighted code in the `set_details` function.

```python linenums="67" hl_lines="3-18" title="app.py"
--8<-- "examples/account/15_set_details_code/step02/app.py:67:84"
```

??? note "Code explanation"
    - **line 69** → checks whether the request is a GET…
    - **line 70** → …if so, shows the form and finishes.
    - **lines 71–72** → get the first and last names from the form, without spaces at each end.
    - **line 73** → checks whether either name is empty…
    - **lines 74–75** → …if so, shows the form again with an error. `values=request.form` fills the inputs with what the user typed, so they don't have to type it again.
    - **line 76** → opens a connection to the database.
    - **lines 77–80** → updates the logged-in user's row. `SET` lists the columns to change and their new values. `WHERE id = ?` makes sure only this user's row changes.
    - **line 81** → saves the change.
    - **line 82** → closes the connection.
    - **line 83** → loads the user again from the database, using the same `load_user` function Flask-Login uses.
    - **line 84** → shows the Account page with the fresh copy of the user, and changes the address bar to `/account`.

!!! warning "Always use WHERE with UPDATE"
    Without `WHERE id = ?`, the `UPDATE` would change **every** user's name to the names in the form. Always check an `UPDATE` (or `DELETE`) has a `WHERE`.

!!! primm "PRIMM"
    1. **Predict** what you'll see after typing your names and clicking Save. What if one name is empty?
    2. **Run** the code by going to `http://127.0.0.1:5000/account/details` and trying both.
    3. Time to **investigate**. Change line 84 to send `user=current_user` instead of `user=user`, then save a new name. What does the Account page show? Click Account in the menu. What does it show now? Why? Change line 84 back when you're done.

!!! tip "Why was current_user out of date?"
    Flask-Login loads `current_user` from the database once, at the start of each request. Our `UPDATE` happens later in the same request, so `current_user` still holds the old names. Loading the user again gets the new names. On the next request, Flask-Login loads the user again and `current_user` is up to date.

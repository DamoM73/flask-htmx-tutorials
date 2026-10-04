# 16. User Service Module

!!! learn "In this lesson we will learn"
    - why we split a program into modules
    - how to move our user database code into its own module
    - how to refactor without changing what a program does

## Introduction

Look through ***app.py***. It now does lots of different jobs: setting up the app, building pages, handling forms, and opening database connections to run SQL. It's over 120 lines long and getting hard to find things in.

Programmers keep big programs manageable by splitting them into **modules**, where each module has one job. We already did this with ***db.py***, which handles the database connection. Now we'll make a module for everything to do with users in the database: ***user_service.py***.

So let's think about which jobs move:

- the `User` class → ***user_service.py***
- loading a user by `id` → `get_user`
- checking whether an email is taken → `email_taken`
- saving a new user → `create_user`
- checking an email and password → `check_login`
- saving a user's names → `update_details`
- reading forms and building pages → stays in ***app.py***

Changing how code is organised without changing what it does is called **refactoring**. When we finish, StudyM8 should work exactly as it does now.

## The user service module

Create a new file, add the code below and save it as ***user_service.py*** in the ***studym8*** folder.

```python linenums="1" title="user_service.py"
--8<-- "examples/account/16_user_service/step01/user_service.py"
```

??? note "Code explanation"
    - **line 1** → imports `UserMixin` for the `User` class.
    - **line 2** → imports the password hashing functions.
    - **line 4** → imports `get_db` from our ***db.py*** module.
    - **lines 7–12** → the `User` class, moved from ***app.py***.
    - **line 15** → defines `get_user`, which finds a user by their `id`.
    - **lines 16–21** → open a connection, select the user and close the connection.
    - **lines 22–24** → return `None` if no user was found, otherwise a `User` object.
    - **line 27** → defines `email_taken`, which checks whether an email is already registered.
    - **lines 28–30** → open a connection, look for the email and close the connection.
    - **line 31** → returns `True` if a row was found and `False` if not.
    - **line 34** → defines `create_user`, which saves a new user.
    - **lines 35–41** → insert the email and password hash, save the change and close the connection.
    - **line 44** → defines `check_login`, which returns the user if the email and password are right.
    - **lines 45–47** → find the user with this email.
    - **lines 48–49** → return `None` if there's no user with that email.
    - **lines 50–51** → return `None` if the password doesn't match the hash.
    - **line 52** → otherwise, returns a `User` object.
    - **line 55** → defines `update_details`, which saves a user's names.
    - **lines 56–62** → update the user's row, save the change and close the connection.

## Use the module in app.py

Now ***app.py*** can call these functions instead of running SQL itself.

Go back to ***app.py***. Delete the `User` class, then change the code so it matches the code below. The highlighted lines are new or changed.

```python linenums="1" hl_lines="2 5 16 60-61 81 84-85 95-96 99" title="app.py"
--8<-- "examples/account/16_user_service/step02/app.py"
```

??? note "Code explanation"
    - **line 2** → removes `UserMixin` from the import, because the `User` class is now in ***user_service.py***.
    - **line 5** → imports our new ***user_service.py*** module. The Werkzeug import has gone, because ***app.py*** no longer hashes passwords.
    - **line 16** → `load_user` now asks `user_service` for the user. The `id` in the session cookie is text, so `int()` turns it into a number.
    - **line 60** → saves the names using `user_service`.
    - **line 61** → loads the fresh copy of the user using `user_service`.
    - **line 81** → checks whether the email is taken using `user_service`.
    - **lines 82–83** → show the error, as before.
    - **line 84** → saves the new user using `user_service`.
    - **line 85** → gets the new user with `check_login` and logs them in.
    - **line 95** → checks the email and password using `user_service`, which returns the user or `None`.
    - **line 96** → checks whether the login failed.
    - **line 99** → logs the user in.

Notice that ***app.py*** has no SQL in it at all now. It just asks `user_service` for what it needs.

!!! primm "PRIMM"
    1. **Predict** what will be different about StudyM8 after the refactor.
    2. **Run** the code. Register a new account, log out, log in, and change your name, to check everything still works.
    3. Time to **investigate**. Count the lines in ***app.py*** before and after. Which functions in ***app.py*** got shorter? Which file would you open to change how passwords are checked?

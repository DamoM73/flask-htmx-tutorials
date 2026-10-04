# 9. Connecting Flask to SQLite

!!! learn "In this lesson we will learn"
    - how to connect to an SQLite database from Python
    - how to add our own command to the `flask` command
    - how to create the database from our schema file
    - how to run SQL from the Flask shell

## Introduction

We have a schema, but no database yet. In this lesson we'll write a small **module** (a Python file that other files import) to handle our database connection. It will do two jobs:

1. open a connection to the database whenever our code needs one → `get_db`
2. create the database from ***schema.sql*** when we type a command in the terminal → `flask init-db`

## The database module

Create a new file, add the code below and save it as ***db.py*** in the ***studym8*** folder.

```python linenums="1" title="db.py"
--8<-- "examples/users/09_flask_sqlite/step01/db.py"
```

??? note "Code explanation"
    - **line 1** → imports `sqlite3`, the Python library for SQLite databases.
    - **line 2** → imports `Path`, which works with file and folder paths.
    - **line 4** → imports `click`, the library Flask uses to make terminal commands. It was installed with Flask.
    - **line 6** → works out the path of the database file, ***studym8.db***, in the same folder as ***db.py***. `__file__` is the path of the current file and `.parent` is its folder.
    - **line 7** → works out the path of ***schema.sql*** in the same way.
    - **line 10** → defines `get_db`, which opens a connection to the database.
    - **line 11** → connects to the database file. If the file doesn't exist yet, SQLite creates an empty one.
    - **line 12** → sets `row_factory` so each row comes back as a `sqlite3.Row`. This lets us get a column's value by its name, like a dictionary: `row["email"]`.
    - **line 13** → returns the connection.
    - **line 16** → a decorator that turns the function below into a terminal command called `init-db`.
    - **line 17** → defines the function that runs when we type the command.
    - **line 18** → opens a connection to the database.
    - **line 19** → reads ***schema.sql*** and runs all the SQL in it.
    - **line 20** → closes the connection. We should always close a connection when we've finished with it.
    - **line 21** → prints a message in the terminal so we know it worked.

## Add the command to Flask

Our app doesn't know about the `init-db` command yet. We need to import ***db.py*** and add the command to the app.

Go back to ***app.py*** and add the highlighted code below.

```python linenums="1" hl_lines="3 6" title="app.py"
--8<-- "examples/users/09_flask_sqlite/step02/app.py:1:7"
```

??? note "Code explanation"
    - **line 3** → imports our ***db.py*** module.
    - **line 6** → adds the `init-db` command from ***db.py*** to our app's commands.

## Create the database

The server needs to stop while we run a different command. Click in the terminal, press ++ctrl+c++ to stop the server, then type:

```text
flask init-db
```

The terminal shows:

```text
Database created.
```

A new file called ***studym8.db*** appears in the ***studym8*** folder. That's our database.

!!! warning "init-db deletes everything"
    Line 1 of ***schema.sql*** deletes the users table before creating it. Every time we run `flask init-db`, all the users in the database are deleted. That's handy while we're building StudyM8, but we need to be careful once we have data we want to keep.

## Try some SQL

Let's put some data into the database and read it back. Flask has a **shell**: a Python prompt where we can type code that uses our app's files.

In the terminal, type:

```text
flask shell
```

The prompt changes to `>>>`. Type each line below after the `>>>`, pressing ++enter++ after each one. The lines without `>>>` are what Python shows back.

```text
>>> import db
>>> conn = db.get_db()
>>> conn.execute("INSERT INTO users (email, password_hash) VALUES (?, ?)", ("test@school.com", "abc"))
<sqlite3.Cursor object at 0x7f58b56daac0>
>>> conn.commit()
>>> rows = conn.execute("SELECT id, email FROM users").fetchall()
>>> rows
[<sqlite3.Row object at 0x7f58b530cc40>]
>>> rows[0]["email"]
'test@school.com'
>>> rows[0]["id"]
1
```

- `conn.execute(...)` → runs an SQL statement. Each `?` is a **placeholder**, filled in with the values from the tuple that follows.
- `conn.commit()` → saves the changes. Until we commit, an `INSERT` hasn't really been saved.
- `.fetchall()` → gets all the rows the `SELECT` found, as a list.
- `rows[0]["email"]` → the `email` column of the first row.

!!! tip "Why placeholders?"
    We could build SQL by joining strings together, like `"... WHERE email = '" + email + "'"`. But if a user typed SQL into a form, it would become part of our statement and could change or delete our data. This attack is called **SQL injection**. Placeholders keep the user's values separate from the SQL, so they can never be run as SQL. We'll **always** use placeholders.

Now let's try to break a constraint. Type:

```text
>>> conn.execute("INSERT INTO users (email, password_hash) VALUES (?, ?)", ("test@school.com", "xyz"))
```

Python shows this error:

``` { .text .error linenums="1" }
Traceback (most recent call last):
  File "<console>", line 1, in <module>
sqlite3.IntegrityError: UNIQUE constraint failed: users.email
```

- **line 1** → the start of the error report.
- **line 2** → the error came from the line we typed into the shell (the console).
- **line 3** → an `IntegrityError` means a constraint was broken. The `UNIQUE` constraint on the `email` column stopped a second user with the same email.

Type `exit()` to leave the shell. Then run `flask init-db` again to clear out the test user, and start the server again with `flask run --debug`.

!!! primm "PRIMM"
    1. **Predict** what `rows` will hold if you insert two different users and then run the `SELECT` again.
    2. **Run** it in the Flask shell to check.
    3. Time to **investigate**. What happens if you insert a user, don't call `conn.commit()`, and then type `exit()`? Start the shell again and `SELECT` the users to find out.
    4. Now **modify** the `SELECT` so it only finds the user with a particular email. (Hint: use `WHERE` and a `?` placeholder.)

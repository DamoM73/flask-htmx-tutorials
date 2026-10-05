# 31. One Connection per Request

!!! learn "In this lesson we will learn"
    - why opening a connection for every query is wasteful
    - how to share one connection across a request with Flask's `g` object
    - how a teardown function closes the connection when the request ends

## Introduction

Every function in our service modules opens its own database connection and closes it again. So a request that makes three queries opens three connections. Opening a connection means finding the database file, opening it and setting it up, every time.

A better plan:

1. the first time a request needs the database, open a connection and keep it in `g`
2. any more queries in the same request reuse the connection from `g`
3. when the request finishes, close the connection

Remember from [Optimisation](29_optimisation.md#time-each-request) that `g` holds values for one request, then is thrown away. That makes it the perfect place to keep a connection.

## Share the connection

Open ***db.py***, change the highlighted code below and save it.

```python linenums="1" hl_lines="5 12-17 20-23 33-35" title="db.py"
--8<-- "examples/optimisation/31_fewer_connections/step01/db.py"
```

??? note "Code explanation"
    - **line 5** → imports `g` from Flask.
    - **line 12** → checks whether this request has a connection yet…
    - **line 13** → …if not, prints our message…
    - **line 14** → …opens a connection and stores it in `g` as `db`…
    - **lines 15–16** → …and sets it up as before.
    - **line 17** → returns the request's connection, new or reused.
    - **line 20** → defines `close_db`, which will run when each request finishes. Flask passes it any error that happened, which we don't need.
    - **line 21** → takes the connection out of `g`. `g.pop("db", None)` gives `None` if there wasn't one.
    - **line 22** → checks whether there was a connection…
    - **line 23** → …if so, closes it.
    - **line 33** → defines `init_app`, which connects ***db.py*** to our app.
    - **line 34** → tells Flask to run `close_db` when each request is torn down (finished).
    - **line 35** → adds the `init-db` command, which ***app.py*** used to do itself.

Notice `init_db_command` no longer closes its connection. `close_db` does that now.

## Connect db.py to the app

Go back to ***app.py*** and change the highlighted code below.

```python linenums="11" hl_lines="3" title="app.py"
--8<-- "examples/optimisation/31_fewer_connections/step02/app.py:11:15"
```

??? note "Code explanation"
    - **line 13** → calls `init_app`, which sets up the teardown and the `init-db` command.

## Stop closing connections early

Our service functions still close the connection after each query. Now that the connection is shared, closing it would break the next query in the same request.

Open ***user_service.py*** and delete every line that says:

```python
    conn.close()
```

Then do the same in ***assessment_service.py***. There are five in ***user_service.py*** and five in ***assessment_service.py***.

!!! warning "Cannot operate on a closed database"
    If you miss one, a request that makes more than one query will crash with `sqlite3.ProgrammingError: Cannot operate on a closed database.` Search each file for `close` (++ctrl+f++) to check you've got them all.

!!! primm "PRIMM"
    1. **Predict** how many connections each request will open now.
    2. **Run** StudyM8 and repeat the steps from [Optimisation](29_optimisation.md#count-database-connections). Compare the terminal with last time.
    3. Time to **investigate**. Comment out line 34 of ***db.py*** (put a `#` in front), restart the server and use StudyM8 for a while. Nothing seems wrong, so why does closing connections matter? (Hint: think about thousands of requests.) Put the line back when you're done.

# 18. Assessments Table

!!! learn "In this lesson we will learn"
    - how to link two tables with a foreign key
    - how SQLite stores dates and true/false values
    - how to give a column a default value
    - how to turn on foreign key checking in SQLite

## Introduction

Users can register and log in. Now we need somewhere to store their assessments. If we look back at the [assessments table in our design](../start/design.md#assessments-table), each assessment has a subject, details, a start date, a due date and whether it's completed.

But there's an important extra column: `user_id`. StudyM8 has lots of users, and each one should only see their own assessments. So every assessment needs to record which user it belongs to.

## Foreign keys

The `user_id` column holds the `id` of a row in the users table. A column that refers to the primary key of another table is called a **foreign key**. It links the two tables together:

| assessments.id | user_id | subject | → | users.id | email |
| :-- | :-- | :-- | :-- | :-- | :-- |
| 1 | 2 | Maths | → | 2 | alex@school.com |
| 2 | 1 | English | → | 1 | sam@school.com |
| 3 | 2 | Science | → | 2 | alex@school.com |

Alex (user 2) owns assessments 1 and 3, and Sam (user 1) owns assessment 2. One user can have many assessments, but each assessment belongs to one user. This is called a **one-to-many relationship**.

A foreign key can also be a constraint: the database refuses to save an assessment whose `user_id` doesn't match a real user.

## Dates and true/false in SQLite

SQLite doesn't have a date type or a true/false type, so:

- dates are stored as `TEXT` in the form `YYYY-MM-DD`, for example `2026-10-12`. This is the same form HTML date inputs use. Because the year comes first, sorting the text also sorts the dates in order.
- completed is stored as an `INTEGER`: `0` for not completed and `1` for completed.

## Add the table to the schema

Open ***schema.sql***, add the highlighted code below and save it.

```sql linenums="1" hl_lines="1 12-21" title="schema.sql"
--8<-- "examples/assessments/18_assessments_table/step01/schema.sql"
```

??? note "Code explanation"
    - **line 1** → deletes the assessments table if it exists. It must be deleted before the users table, because the assessments point to the users.
    - **line 12** → starts creating the `assessments` table.
    - **line 13** → the primary key, numbered automatically.
    - **line 14** → the `id` of the user who owns the assessment. It can't be empty.
    - **lines 15–16** → the subject and details, which can't be empty.
    - **lines 17–18** → the start and due dates, stored as text.
    - **line 19** → whether the assessment is completed. `DEFAULT 0` means a new assessment is not completed unless we say otherwise.
    - **line 20** → makes `user_id` a foreign key that must match an `id` in the users table.
    - **line 21** → closes the list of columns.

## Turn on foreign keys

For historical reasons, SQLite doesn't check foreign keys unless we ask it to, every time we connect.

Open ***db.py***, add the highlighted code below and save it.

```python linenums="10" hl_lines="4" title="db.py"
--8<-- "examples/assessments/18_assessments_table/step02/db.py:10:14"
```

??? note "Code explanation"
    - **line 13** → turns on foreign key checking for this connection. A `PRAGMA` is a special SQLite command that changes a setting.

## Recreate the database

Stop the server, then run:

```text
flask init-db
```

!!! warning "This deletes your users"
    `flask init-db` deletes every table and creates them again, so all the accounts you've registered are gone. You'll need to register again.

Now let's check the foreign key works. Start the Flask shell with `flask shell`, then try to add an assessment for user 99, who doesn't exist:

```text
>>> import db
>>> conn = db.get_db()
>>> conn.execute("INSERT INTO assessments (user_id, subject, details, start_date, due_date) VALUES (?, ?, ?, ?, ?)", (99, "Maths", "Algebra test", "2026-10-12", "2026-10-12"))
```

Python shows this error:

``` { .text .error linenums="1" }
Traceback (most recent call last):
  File "<console>", line 1, in <module>
sqlite3.IntegrityError: FOREIGN KEY constraint failed
```

- **line 1** → the start of the error report.
- **line 2** → the error came from the line we typed into the shell.
- **line 3** → the foreign key constraint stopped an assessment being saved for a user who doesn't exist.

Type `exit()` to leave the shell, then start the server again with `flask run --debug`.

!!! primm "PRIMM"
    1. **Predict** what would happen if you registered a user (who would be user 1), then ran the same `INSERT` with `user_id` 1.
    2. **Run** it: register an account in the browser, then try the `INSERT` in the Flask shell with `1` instead of `99`. Remember to `conn.commit()`.
    3. Time to **investigate**. `SELECT * FROM assessments` in the shell. What value does `completed` have, even though the `INSERT` didn't mention it? Which line of ***schema.sql*** set it?

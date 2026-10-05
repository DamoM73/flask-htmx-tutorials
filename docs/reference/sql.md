# SQL

!!! learn "On this page we will learn"
    - how to create tables with columns, types and constraints
    - how to insert, select, update and delete rows
    - how to run SQL safely from Python with placeholders

**SQL** (Structured Query Language) is the language we use to talk to a database. StudyM8 uses **SQLite**, which keeps the whole database in one file. We first met SQL in [Databases and SQL](../users/08_databases_sql.md).

## Creating tables

```sql
CREATE TABLE assessments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    completed INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

| Part | Means |
| :-- | :-- |
| `INTEGER`, `TEXT` | the column's data type: whole numbers or text |
| `PRIMARY KEY` | the column that uniquely identifies each row |
| `AUTOINCREMENT` | SQLite numbers new rows for us |
| `NOT NULL` | the column must have a value |
| `UNIQUE` | no two rows can have the same value |
| `DEFAULT 0` | the value used if an `INSERT` doesn't give one |
| `FOREIGN KEY ... REFERENCES` | the column must match a primary key in another table |
| `DROP TABLE IF EXISTS` | delete a table, and all its rows, if it exists |

SQLite stores dates as text (`YYYY-MM-DD`) and true/false as `0` or `1`. See [Assessments Table](../assessments/18_assessments_table.md).

## The four statements

### INSERT: add a row

```sql
INSERT INTO users (email, password_hash) VALUES ('sam@school.com', 'abc')
```

### SELECT: read rows

```sql
SELECT id, subject, due_date
FROM assessments
WHERE user_id = 1 AND completed = 0
ORDER BY due_date
```

- `SELECT *` → every column
- `WHERE` → only rows that match; join conditions with `AND` or `OR`
- `ORDER BY due_date` → sort, smallest first; add `DESC` for largest first

### UPDATE: change rows

```sql
UPDATE users SET first_name = 'Sam', last_name = 'Lee' WHERE id = 1
```

### DELETE: remove rows

```sql
DELETE FROM assessments WHERE id = 3
```

!!! warning "Always use WHERE"
    `UPDATE` and `DELETE` without `WHERE` change or remove **every** row in the table.

## Running SQL from Python

```python
conn = get_db()
row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
conn.execute("UPDATE users SET first_name = ? WHERE id = ?", (first_name, user_id))
conn.commit()
```

| Code | Does |
| :-- | :-- |
| `conn.execute(sql, values)` | runs a statement; each `?` is filled from the tuple of values |
| `.fetchone()` | the first row found, or `None` |
| `.fetchall()` | every row found, as a list |
| `row["email"]` | a column's value, by name |
| `conn.commit()` | saves changes; without it, an `INSERT`, `UPDATE` or `DELETE` is lost |
| `cursor.rowcount` | how many rows the last `UPDATE` or `DELETE` changed |

!!! warning "Always use placeholders"
    Never build SQL by joining strings with user input. A user could type SQL into a form and change our statement, an attack called **SQL injection**. `?` placeholders keep values separate from the SQL. See [Connecting Flask to SQLite](../users/09_flask_sqlite.md#try-some-sql).

## More for your own website

The examples below use tables a community group website might have:

```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    starts_at TEXT NOT NULL,
    location TEXT,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories (id)
);

CREATE TABLE news (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    image TEXT,
    posted_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);
```

`DEFAULT (datetime('now', 'localtime'))` fills in the date and time when a row is inserted, so our code doesn't have to.

### Deleting rows

```python
cursor = conn.execute("DELETE FROM events WHERE id = ?", (event_id,))
conn.commit()
deleted = cursor.rowcount == 1
```

If another table points to the row with a foreign key (for example, RSVPs for the event), SQLite refuses with `FOREIGN KEY constraint failed`. Either delete the linked rows first, or add `ON DELETE CASCADE` to the foreign key so SQLite deletes them for us:

```sql
FOREIGN KEY (event_id) REFERENCES events (id) ON DELETE CASCADE
```

### Dates with times

Store dates with times as text in the form `YYYY-MM-DDTHH:MM`, which is exactly what `<input type="datetime-local">` sends. Text in this form sorts in time order.

SQLite has functions for working with these values:

| Function | Gives |
| :-- | :-- |
| `date('now', 'localtime')` | today's date, `YYYY-MM-DD` |
| `datetime('now', 'localtime')` | the date and time now, `YYYY-MM-DD HH:MM:SS` |
| `date(starts_at)` | just the date part of a value |
| `strftime('%m', starts_at)` | just the month, `03` |
| `date('now', 'localtime', '+7 days')` | the date a week from today |

Without `'localtime'`, SQLite uses UTC time, which is 10 hours behind Queensland.

### Upcoming events only

```sql
SELECT id, title, starts_at, location
FROM events
WHERE date(starts_at) >= date('now', 'localtime')
ORDER BY starts_at
```

Events in a particular month:

```python
conn.execute("SELECT * FROM events WHERE strftime('%m', starts_at) = ? ORDER BY starts_at", (month,))
```

### The newest first, and LIMIT

```sql
SELECT id, title, posted_at FROM news ORDER BY posted_at DESC LIMIT 5
```

- `DESC` → sorts from largest to smallest, so the newest post comes first
- `LIMIT 5` → only the first 5 rows, for a "Latest news" section
- `LIMIT 10 OFFSET 20` → skip 20 rows, then take 10; used for "Load more" pages

### Joining tables

A **join** combines rows from two tables that are linked by a foreign key:

```sql
SELECT events.title, events.starts_at, categories.name AS category
FROM events
JOIN categories ON events.category_id = categories.id
ORDER BY events.starts_at
```

- `JOIN categories ON ...` → for each event, find the category whose `id` matches the event's `category_id`
- `events.title` → when two tables have columns with the same name, put the table name in front
- `AS category` → gives the column a new name in the results, so we can use `row["category"]`

A plain `JOIN` leaves out events with no matching category. `LEFT JOIN` keeps them, with `None` for the category.

### Many-to-many: a linking table

A member can RSVP to many events, and an event can have many members attending. This is a **many-to-many relationship**, and it needs a third table that links the other two:

```sql
CREATE TABLE rsvps (
    user_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    PRIMARY KEY (user_id, event_id),
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events (id) ON DELETE CASCADE
);
```

`PRIMARY KEY (user_id, event_id)` makes the pair unique, so a member can't RSVP to the same event twice.

### Counting and grouping

```sql
SELECT events.id, events.title, COUNT(rsvps.user_id) AS attending
FROM events
LEFT JOIN rsvps ON rsvps.event_id = events.id
GROUP BY events.id
ORDER BY events.starts_at
```

- `COUNT(...)` → how many rows there are; other **aggregate functions** are `SUM`, `AVG`, `MIN` and `MAX`
- `GROUP BY events.id` → count separately for each event
- `LEFT JOIN` → keeps events that nobody has RSVP'd to yet, with a count of 0

### Searching

`LIKE` finds text that matches a pattern. `%` matches any characters:

```python
pattern = f"%{search}%"
conn.execute("SELECT * FROM news WHERE title LIKE ? OR body LIKE ?", (pattern, pattern))
```

`LIKE` ignores upper and lower case for English letters. Still use `?` placeholders for the search text.

### Adding a column to an existing table

```sql
ALTER TABLE users ADD COLUMN is_admin INTEGER NOT NULL DEFAULT 0
```

This keeps the existing rows. Also add the column to ***schema.sql***, so it's there next time the database is created.

### Sample data

A **seed** file fills the database with sample content, so we can test and demonstrate the site without typing everything in each time. Make a file called ***seed.sql***:

```sql
INSERT INTO categories (name) VALUES ('Training'), ('Games'), ('Social');
INSERT INTO events (title, starts_at, location, category_id) VALUES
    ('Under 12s training', '2026-03-10T17:30', 'Bayside Oval', 1),
    ('Round 1 vs Wynnum', '2026-03-14T09:00', 'Wynnum Park', 2);
```

Run it with a command like `init-db` in ***db.py***:

```python
SEED = Path(__file__).parent / "seed.sql"


@click.command("seed-db")
def seed_db_command():
    conn = get_db()
    conn.executescript(SEED.read_text())
    conn.commit()
    click.echo("Sample data added.")
```

Add `app.cli.add_command(seed_db_command)` to `init_app`, then run `flask seed-db` after `flask init-db`.

## Documentation

Documentation is the official guide written by the people who made the code library, and we can use it to look up every statement and option, including ones that aren't covered on this page.

- [SQLite SQL reference](https://www.sqlite.org/lang.html)
- [Python sqlite3 documentation](https://docs.python.org/3/library/sqlite3.html)

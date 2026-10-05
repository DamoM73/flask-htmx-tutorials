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

## Documentation

Documentation is the official guide written by the people who made the code library, and we can use it to look up every statement and option, including ones that aren't covered on this page.

- [SQLite SQL reference](https://www.sqlite.org/lang.html)
- [Python sqlite3 documentation](https://docs.python.org/3/library/sqlite3.html)

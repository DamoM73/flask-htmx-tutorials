# 8. Databases and SQL

!!! learn "In this lesson we will learn"
    - what a database is and how it organises data into tables
    - what primary keys, data types and constraints are
    - what SQL is and the four statements we'll use most
    - how to write a schema file that creates our users table

## Introduction

Right now StudyM8 forgets everything as soon as we stop the server. To keep track of users and their assessments, we need somewhere permanent to store our data: a **database**.

A database is an organised collection of data that a program can search, add to and change. We'll use **SQLite**, a database that keeps everything in a single file. SQLite comes built into Python, so there's nothing extra to install.

## Tables, rows and columns

A database stores data in **tables**. A table looks a lot like a spreadsheet:

- each **column** is one piece of information we store, such as an email address
- each **row** is one record, such as one user

Here's what our users table might look like with two users in it:

| id | email | password_hash | first_name | last_name |
| :-- | :-- | :-- | :-- | :-- |
| 1 | sam@school.com | scrypt:32768:8:1$u3d7… | Sam | Lee |
| 2 | alex@school.com | scrypt:32768:8:1$oih8… | Alex | Nguyen |

### Primary keys

Every row needs a way to tell it apart from every other row. Two users could have the same name, so we give each row a unique number called a **primary key**. In our users table the primary key is the `id` column. SQLite can number the rows for us automatically: 1, 2, 3 and so on.

### Data types

Each column holds one **data type**. SQLite has a small set of types, and we'll use two:

| Type | Holds | Example |
| :-- | :-- | :-- |
| `INTEGER` | whole numbers | `1` |
| `TEXT` | words and characters | `'sam@school.com'` |

### Constraints

A **constraint** is a rule the database enforces on a column. If our code tries to break the rule, the database refuses and raises an error. We'll use three:

- `UNIQUE` → no two rows can have the same value, so two users can't register the same email
- `NOT NULL` → the column must have a value; it can't be left empty
- `PRIMARY KEY` → the column is the unique identifier for each row

## SQL

We talk to the database using **SQL** (Structured Query Language). SQL statements read almost like English sentences. These are the four statements we'll use most:

| Statement | Does | Example |
| :-- | :-- | :-- |
| `INSERT` | adds a row | `INSERT INTO users (email, password_hash) VALUES ('sam@school.com', 'abc')` |
| `SELECT` | reads rows | `SELECT email FROM users WHERE id = 1` |
| `UPDATE` | changes rows | `UPDATE users SET first_name = 'Sam' WHERE id = 1` |
| `DELETE` | removes rows | `DELETE FROM users WHERE id = 1` |

Notice the `WHERE` part. It picks which rows the statement works on. Without a `WHERE`, `UPDATE` and `DELETE` change **every** row in the table, so we need to be careful.

!!! tip "Capital letters"
    SQL doesn't care about capital letters, but we write SQL keywords like `SELECT` and `WHERE` in capitals so they stand out from table and column names.

## The schema file

Before we can store any data, we need to create the table. The design of a database (its tables, columns, types and constraints) is called its **schema**. We'll write our schema as SQL in its own file, so we can create the database again whenever we need to.

Create a new file, add the code below and save it as ***schema.sql*** in the ***studym8*** folder.

```sql linenums="1" title="schema.sql"
--8<-- "examples/users/08_databases_sql/step01/schema.sql"
```

??? note "Code explanation"
    - **line 1** → deletes the users table if it already exists, so we always start with a fresh, empty table. This also deletes all the data in it.
    - **line 3** → starts creating a table called `users`. The columns are listed inside the brackets, separated by commas.
    - **line 4** → the `id` column: a whole number that's the table's primary key. `AUTOINCREMENT` means SQLite gives each new row the next number.
    - **line 5** → the `email` column: text that must be unique and can't be empty.
    - **line 6** → the `password_hash` column: text that can't be empty. We'll store a scrambled version of the password here, never the password itself.
    - **lines 7–8** → the `first_name` and `last_name` columns. They can be empty, because users set their names after they register.
    - **line 9** → closes the list of columns. The semicolon ends the SQL statement.

Compare the schema with the [users table in our design](../start/design.md#users-table). Every column in the design is in the schema.

!!! primm "PRIMM"
    1. **Predict** what would happen if two users tried to register with the same email address.
    2. We can't **run** this file yet. In the next lesson we'll use Python to run it and create the database.
    3. Time to **investigate**. Why do you think `first_name` doesn't have `NOT NULL`, but `email` does?
    4. Now **modify** your thinking. If StudyM8 also stored each user's year level, what would the column look like? Write the line, but don't add it to ***schema.sql***.

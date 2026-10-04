# 24. Home Page Code

!!! learn "In this lesson we will learn"
    - how to select a user's rows in order with `ORDER BY`
    - how to write a Jinja filter to format dates
    - how the `/` route can show different pages to different visitors

## Introduction

Our Home page shows sample data. Now let's load the real assessments from the database. We need to:

1. select the logged-in user's assessments, with the soonest due date first → `get_assessments` in ***assessment_service.py***
2. send them to the Home page → the `home` route in ***app.py***
3. show the dates the Australian way (`12/10/2026` rather than `2026-10-12`) → a Jinja **filter**

We'll also tidy up the `/` route. A logged-in user should see their Home page, and anyone else should see the login form.

## Get the assessments

Open ***assessment_service.py***, add the highlighted code below to the bottom and save it.

```python linenums="13" hl_lines="3-13" title="assessment_service.py"
--8<-- "examples/assessments/24_home_code/step01/assessment_service.py:13:25"
```

??? note "Code explanation"
    - **line 15** → defines `get_assessments`, which takes a user's `id`.
    - **line 16** → opens a connection to the database.
    - **lines 17–23** → selects the user's assessments. `WHERE user_id = ?` only finds this user's rows, and `ORDER BY due_date` sorts them with the earliest due date first. `.fetchall()` returns every row found, as a list.
    - **line 24** → closes the connection.
    - **line 25** → returns the list of rows.

## Use the real data

Go back to ***app.py*** and add the highlighted import at the top.

```python linenums="1" hl_lines="1" title="app.py"
--8<-- "examples/assessments/24_home_code/step02/app.py:1:4"
```

??? note "Code explanation"
    - **line 1** → imports the `date` class from Python's `datetime` library.

Now add the highlighted filter below the `load_user` function.

```python linenums="19" hl_lines="5-7" title="app.py"
--8<-- "examples/assessments/24_home_code/step02/app.py:19:25"
```

??? note "Code explanation"
    - **line 23** → registers the function below as a Jinja filter called `au_date`. A **filter** changes a value as it's shown in a template.
    - **line 24** → defines the filter function, which takes a date in the form `YYYY-MM-DD`.
    - **line 25** → turns the text into a `date` object, then formats it as day/month/year.

Next, change the highlighted code in the `index` and `home` functions.

```python linenums="40" hl_lines="3-5 11" title="app.py"
--8<-- "examples/assessments/24_home_code/step02/app.py:40:51"
```

??? note "Code explanation"
    - **line 42** → checks whether a user is logged in…
    - **line 43** → …if so, shows their Home page.
    - **line 44** → otherwise, shows the login form.
    - **line 50** → gets the logged-in user's assessments from the database, in place of the sample data.

Finally, after logging in, users should see their Home page. Change the highlighted code at the end of the `login` function.

```python linenums="141" hl_lines="2" title="app.py"
--8<-- "examples/assessments/24_home_code/step02/app.py:141:142"
```

??? note "Code explanation"
    - **line 142** → shows the Home page by calling the `home` function, which also sets the address bar to `/home`.

## Format the dates

Open ***templates/partials/assessment_card.html***, change the highlighted code below and save it.

```html+jinja linenums="1" hl_lines="6" title="templates/partials/assessment_card.html"
--8<-- "examples/assessments/24_home_code/step03/templates/partials/assessment_card.html"
```

??? note "Code explanation"
    - **line 6** → passes each date through the `au_date` filter. The `|` symbol sends the value on the left into the filter on the right.

!!! primm "PRIMM"
    1. **Predict** the order your assessments will appear in on the Home page.
    2. **Run** the code. Add three assessments with different due dates, in any order, then click Home.
    3. Time to **investigate**. Log out, then register a new account. What's on the new user's Home page? Why?
    4. Now **modify** the SQL so the assessments are sorted by subject instead. Change it back when you're done.

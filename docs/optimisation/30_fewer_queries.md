# 30. Fewer Database Queries

!!! learn "In this lesson we will learn"
    - how to spot database queries a route doesn't need
    - how `rowcount` tells us how many rows an `UPDATE` changed
    - how to reuse data we already have instead of asking the database again

## Introduction

In the last lesson, the terminal showed that completing, editing and changing names each open more connections than they need. Each connection is a separate request to the database, called a **query**. Let's look at each route and work out which queries it doesn't need.

| Route | Queries now | The one we can remove |
| :-- | :-- | :-- |
| complete | `SELECT` the assessment to check it's the user's, then `UPDATE` it | the `SELECT`: the `UPDATE` already checks `user_id`, so it can tell us whether it found the assessment |
| edit | `SELECT` to check ownership, `UPDATE`, then `SELECT` again to build the card | the second `SELECT`: we already have the new details from the form |
| set details | `UPDATE` the names, then `SELECT` the user again | the `SELECT`: we already have the new names from the form |

(Each route also has one query from Flask-Login loading the user at the start of the request. We'll keep that one.)

## Complete with one query

When SQLite runs an `UPDATE`, it records how many rows it changed, in the cursor's `rowcount`. Our `UPDATE` has `WHERE id = ? AND user_id = ?`, so:

- `rowcount` is `1` → the assessment exists and belongs to this user, and it's been updated
- `rowcount` is `0` → no assessment matched, so it doesn't exist or it isn't this user's

Open ***assessment_service.py***, change the highlighted code in `set_completed` and save it.

```python linenums="43" hl_lines="3 9" title="assessment_service.py"
--8<-- "examples/optimisation/30_fewer_queries/step01/assessment_service.py:43:51"
```

??? note "Code explanation"
    - **line 45** → keeps the **cursor** that `execute` returns. A cursor holds information about the statement that just ran.
    - **line 51** → returns `True` if exactly one row was updated, and `False` if none were.

Now go back to ***app.py*** and change the highlighted code in the `complete` function.

```python linenums="105" hl_lines="4" title="app.py"
--8<-- "examples/optimisation/30_fewer_queries/step02/app.py:105:110"
```

??? note "Code explanation"
    - **line 108** → completes the assessment. If `set_completed` returns `False`, no assessment matched, so we send a 404 error. The separate `SELECT` has gone.

## Edit without reloading the assessment

Change the highlighted code at the end of the `edit` function.

```python linenums="127" hl_lines="6-7" title="app.py"
--8<-- "examples/optimisation/30_fewer_queries/step02/app.py:127:133"
```

??? note "Code explanation"
    - **line 132** → adds the assessment's `id` to the `values` dictionary, which already holds the new subject, details and dates from the form.
    - **line 133** → builds the card from `values`, instead of loading the assessment from the database again.

## Set details without reloading the user

Change the highlighted code at the end of the `set_details` function.

```python linenums="159" hl_lines="2-4" title="app.py"
--8<-- "examples/optimisation/30_fewer_queries/step02/app.py:159:162"
```

??? note "Code explanation"
    - **lines 160–161** → update the names on `current_user`, so it's no longer out of date.
    - **line 162** → shows the Account page with `current_user`, instead of loading the user from the database again.

!!! primm "PRIMM"
    1. **Predict** how many connections completing, editing and changing names will open now.
    2. **Run** StudyM8 and check the terminal.
    3. Time to **investigate**. Log in as a different user and try to complete one of the first user's assessments with `htmx.ajax("POST", "/assessments/1/complete", {swap: "none"})` in the **Console**. Does the 404 still work? Which line makes that happen now?

!!! tip "Is it worth it?"
    Each query we removed only saves about a millisecond on our computer. But a popular website handles thousands of requests every second, often with the database on a different computer. There, every query adds network time too, and removing one from every request can make a big difference.

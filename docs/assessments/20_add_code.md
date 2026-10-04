# 20. Add Page Code

!!! learn "In this lesson we will learn"
    - how to collect form data into a dictionary
    - how to validate dates by comparing them as text
    - how to save an assessment that belongs to the logged-in user
    - how to clear a form after a successful save

## Introduction

Now let's make the Save button work. When the form is submitted, we need to:

| Input | Process | Output |
| :-- | :-- | :-- |
| subject, details, start date and due date | check the subject and details aren't empty | an error, and the form refilled with what was typed |
| | check both dates were chosen | an error, and the form refilled |
| | check the due date isn't before the start date | an error, and the form refilled |
| | `INSERT` the assessment, with the logged-in user's `id` | an empty form and a "saved" message |

Clearing the form after saving means users can add their next assessment straight away.

## Show messages

Open ***templates/partials/add.html***, add the highlighted code below and save it.

```html+jinja linenums="1" hl_lines="22-27" title="templates/partials/add.html"
--8<-- "examples/assessments/20_add_code/step01/templates/partials/add.html"
```

??? note "Code explanation"
    - **lines 22–24** → show the error message, if there is one.
    - **lines 25–27** → show the success message, if there is one.

## Save the assessment

Go back to ***app.py*** and change the highlighted code in the `add` function.

```python linenums="36" hl_lines="3-29" title="app.py"
--8<-- "examples/assessments/20_add_code/step02/app.py:36:64"
```

??? note "Code explanation"
    - **line 38** → checks whether the request is a GET…
    - **line 39** → …if so, shows the empty form.
    - **lines 40–45** → collects the form data into a dictionary called `values`, removing spaces from the ends of the subject and details. Keeping the values together makes it easy to send them all back to the form.
    - **line 46** → starts with no error.
    - **line 47** → checks whether the subject or details are empty…
    - **line 48** → …if so, sets an error.
    - **line 49** → otherwise, checks whether either date is missing…
    - **line 50** → …if so, sets an error.
    - **line 51** → otherwise, checks whether the due date comes before the start date. Dates in the form `YYYY-MM-DD` compare correctly as text, because the year comes first, then the month, then the day…
    - **line 52** → …if so, sets an error.
    - **line 53** → checks whether there's an error…
    - **line 54** → …if so, shows the form again with the error and the values the user typed.
    - **line 55** → opens a connection to the database.
    - **lines 56–61** → inserts the assessment. The SQL is in triple quotes so it can go over two lines. The first value is `current_user.id`, so the assessment belongs to the logged-in user.
    - **line 62** → saves the change.
    - **line 63** → closes the connection.
    - **line 64** → shows an empty form with a message saying the assessment was saved.

!!! primm "PRIMM"
    1. **Predict** what will happen if you choose a due date before the start date.
    2. **Run** the code. Try saving with an empty subject, with no dates, and with the dates the wrong way round. Then save a real assessment.
    3. Time to **investigate**. Stop the server, open the Flask shell and `SELECT * FROM assessments`. Can you find your assessment? What is its `user_id`? Log in as a different user, add an assessment, and check again.
    4. Now **modify** the code so the subject can't be longer than 30 characters. (Hint: `len()`.)

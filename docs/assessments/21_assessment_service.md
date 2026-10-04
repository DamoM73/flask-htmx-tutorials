# 21. Assessment Service Module

!!! learn "In this lesson we will learn"
    - how to start a second service module
    - how to move SQL out of a route and into a function

## Introduction

In [User Service Module](../account/16_user_service.md) we moved all the users table code into ***user_service.py***. Now that we're working with the assessments table, let's do the same thing from the start, with a module called ***assessment_service.py***.

Right now the only assessment SQL is the `INSERT` in the `add` route. We'll move it into a function called `add_assessment`. As we build the rest of StudyM8, every new piece of assessment SQL will go into this module.

## The assessment service module

Create a new file, add the code below and save it as ***assessment_service.py*** in the ***studym8*** folder.

```python linenums="1" title="assessment_service.py"
--8<-- "examples/assessments/21_assessment_service/step01/assessment_service.py"
```

??? note "Code explanation"
    - **line 1** → imports `get_db` from our ***db.py*** module.
    - **line 4** → defines `add_assessment`, which takes the user's `id` and the assessment's details.
    - **line 5** → opens a connection to the database.
    - **lines 6–10** → inserts the assessment for that user.
    - **line 11** → saves the change.
    - **line 12** → closes the connection.

## Use the module in app.py

Go back to ***app.py*** and add the highlighted import at the top.

```python linenums="1" hl_lines="4" title="app.py"
--8<-- "examples/assessments/21_assessment_service/step02/app.py:1:6"
```

??? note "Code explanation"
    - **line 4** → imports our new ***assessment_service.py*** module.

Then replace the database code in the `add` function with the highlighted code below.

```python linenums="53" hl_lines="4-5" title="app.py"
--8<-- "examples/assessments/21_assessment_service/step02/app.py:53:58"
```

??? note "Code explanation"
    - **lines 56–57** → saves the assessment using `assessment_service`, passing the logged-in user's `id` and the values from the form.

!!! primm "PRIMM"
    1. **Predict** whether the Add page will behave any differently.
    2. **Run** the code by adding another assessment.
    3. Time to **investigate**. Notice that `add_assessment` takes the user's `id` as a parameter, rather than using `current_user` itself. Why might that be a good idea? (Think about which module knows about logged-in users.)

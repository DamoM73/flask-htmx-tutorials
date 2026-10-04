# 26. Edit Assessments

!!! learn "In this lesson we will learn"
    - how to swap a card for an edit form, and back again
    - how to send part of a page without the page shell
    - how to refactor repeated code into a function (the DRY principle)
    - how a checkbox is sent with a form

## Introduction

Users make mistakes, and due dates change. If we look back at the [design](../start/design.md#edit), clicking **Edit** on a card turns that card into a form. **Save** turns it back into a card with the new details, and **Cancel** turns it back without changing anything.

So let's think about this:

| User action | Request | Response |
| :-- | :-- | :-- |
| clicks Edit | GET `/assessments/<id>/edit` | the edit form, swapped in place of the card |
| clicks Cancel | GET `/assessments/<id>` | the card, swapped in place of the form |
| clicks Save with a mistake | POST `/assessments/<id>/edit` | the edit form again, with an error |
| clicks Save with valid details | POST `/assessments/<id>/edit` | the updated card, or nothing if it was marked completed |

All of these responses are just one card or one form, not a whole page, so they don't need the page shell or a new title.

## The Edit button

Open ***templates/partials/assessment_card.html***, add the highlighted code below and save it.

```html+jinja linenums="1" hl_lines="14-16" title="templates/partials/assessment_card.html"
--8<-- "examples/assessments/26_edit/step01/templates/partials/assessment_card.html"
```

??? note "Code explanation"
    - **line 14** → a button with Pico's `secondary` class, which gives it a grey colour.
    - **line 15** → when clicked, asks for this assessment's edit form.
    - **line 16** → swaps the form in place of the whole card.

## The edit form

Create a new file, add the code below and save it as ***edit_form.html*** in the ***templates/partials*** folder.

```html+jinja linenums="1" title="templates/partials/edit_form.html"
--8<-- "examples/assessments/26_edit/step02/templates/partials/edit_form.html"
```

??? note "Code explanation"
    - **line 1** → the form sits in an `<article>`, so it looks like a card and `closest article` can find it.
    - **line 2** → opens the form. It posts to the edit route, and swaps the response in place of this whole card.
    - **lines 3–10** → the subject and details inputs, filled from `values`.
    - **lines 11–20** → the start and due dates, side by side.
    - **lines 21–24** → a Completed checkbox, so users can also complete an assessment while editing it.
    - **lines 25–27** → show the error message, if there is one.
    - **line 28** → a grid, so the two buttons sit side by side.
    - **line 29** → the Save button, which submits the form.
    - **line 30** → the Cancel button. `type="button"` stops it submitting the form.
    - **lines 31–32** → when clicked, asks for this assessment's card and swaps it in place of the form.
    - **lines 33–35** → close the grid, the form and the card.

## Don't repeat yourself

The edit route needs to check the subject, details and dates, exactly like the add route does. We could copy the checks, but then if we ever changed a rule, we'd have to remember to change it in two places.

Programmers call this the **DRY principle**: Don't Repeat Yourself. When the same code is needed in two places, we move it into a function and call the function from both.

Go back to ***app.py*** and add the highlighted function above the `index` function.

```python linenums="38" hl_lines="3-16" title="app.py"
--8<-- "examples/assessments/26_edit/step03/app.py:38:53"
```

??? note "Code explanation"
    - **line 40** → defines `validate_assessment`, which takes the submitted form.
    - **lines 41–46** → collects the form data into the `values` dictionary.
    - **line 47** → checks whether the subject or details are empty…
    - **line 48** → …if so, returns the values and an error message. Returning ends the function, so no more checks run.
    - **lines 49–50** → return an error if either date is missing.
    - **lines 51–52** → return an error if the due date is before the start date.
    - **line 53** → if every check passed, returns the values and `None` for the error.

Now replace the checks in the `add` function with a call to the new function.

```python linenums="70" hl_lines="6" title="app.py"
--8<-- "examples/assessments/26_edit/step03/app.py:70:80"
```

??? note "Code explanation"
    - **line 75** → calls `validate_assessment`. It returns two values, which Python **unpacks** into `values` and `error`.

## Update in the database

Open ***assessment_service.py***, add the highlighted code below to the bottom and save it.

```python linenums="48" hl_lines="3-12" title="assessment_service.py"
--8<-- "examples/assessments/26_edit/step04/assessment_service.py:48:59"
```

??? note "Code explanation"
    - **line 50** → defines `update_assessment`, which takes the assessment's `id`, the user's `id` and the new details.
    - **line 51** → opens a connection.
    - **lines 52–57** → updates every column of the assessment, but only if it belongs to this user.
    - **line 58** → saves the change.
    - **line 59** → closes the connection.

## The edit routes

Go back to ***app.py*** and add the highlighted routes around the `complete` route.

```python linenums="81" hl_lines="3-9 21-41" title="app.py"
--8<-- "examples/assessments/26_edit/step05/app.py:81:121"
```

??? note "Code explanation"
    - **line 83** → creates a route that shows one assessment's card.
    - **line 84** → only logged-in users can use it.
    - **line 85** → defines the `assessment_card` view function.
    - **line 86** → gets the assessment, if it belongs to this user.
    - **lines 87–88** → send a 404 error if it doesn't.
    - **line 89** → sends just the card. We use `render_template` rather than `render_page`, because this is one card, not a page.
    - **line 101** → creates the edit route for GET and POST requests.
    - **line 102** → only logged-in users can use it.
    - **line 103** → defines the `edit` view function.
    - **line 104** → gets the assessment, if it belongs to this user.
    - **lines 105–106** → send a 404 error if it doesn't.
    - **line 107** → checks whether the request is a GET…
    - **lines 108–109** → …if so, sends the edit form, filled with the assessment's current details.
    - **line 110** → checks the submitted details using our new function.
    - **line 111** → a checkbox is only sent with a form when it's ticked, so `completed` is `1` if `"completed"` is in the form and `0` if it isn't.
    - **line 112** → checks whether there's an error…
    - **lines 113–114** → …if so, sends the edit form again, with what the user typed and the error.
    - **lines 115–117** → saves the new details.
    - **line 118** → checks whether the assessment was marked completed…
    - **line 119** → …if so, returns nothing, so the card disappears from the Home page.
    - **line 120** → otherwise, gets the updated assessment from the database.
    - **line 121** → sends the updated card.

!!! primm "PRIMM"
    1. **Predict** what will happen when you click Edit, change the details and click Save. What will Cancel do?
    2. **Run** the code. Try Edit then Cancel, Edit with the due date before the start date, Edit with new details, and Edit with Completed ticked.
    3. Time to **investigate**. Open two cards' edit forms at the same time. Does saving one affect the other? Why not?
    4. Now **modify** the Add page so the subject can't be longer than 30 characters, by changing `validate_assessment`. Check the rule works on the Edit form too, without changing anything else.

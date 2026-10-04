# 25. Complete Assessments

!!! learn "In this lesson we will learn"
    - how a checkbox can send a request with HTMX
    - how `hx-target="closest article"` and `hx-swap="outerHTML"` replace one card
    - how to return a 404 error for data that isn't the user's
    - how to filter out completed assessments with SQL

## Introduction

When a user finishes an assessment, they'll tick **Completed** on its card. The card should disappear from the Home page straight away, without reloading the page.

So let's think about this:

1. The checkbox sends a POST request to `/assessments/<id>/complete`, where `<id>` is the assessment's `id`.
2. The server checks the assessment belongs to the logged-in user, then sets `completed` to `1`.
3. The server sends back an empty response.
4. HTMX swaps the empty response in place of the **whole card**, so the card disappears.

## The checkbox

Open ***templates/partials/assessment_card.html***, add the highlighted code below and save it.

```html+jinja linenums="1" hl_lines="7-14" title="templates/partials/assessment_card.html"
--8<-- "examples/assessments/25_complete/step01/templates/partials/assessment_card.html"
```

??? note "Code explanation"
    - **line 7** → adds a footer to the card, with a class we'll style soon.
    - **line 8** → opens the label for the checkbox.
    - **line 9** → a checkbox input.
    - **line 10** → when the checkbox is clicked, sends a POST request to the complete route for this assessment.
    - **line 11** → `hx-target="closest article"` targets the nearest `<article>` around the checkbox, which is this card. `hx-swap="outerHTML"` replaces the whole card, not just what's inside it.
    - **line 12** → the label's text.
    - **lines 13–14** → close the label and the footer.

## Complete in the database

Open ***assessment_service.py***, add the highlighted code below to the bottom and save it.

```python linenums="26" hl_lines="3-12 15-22" title="assessment_service.py"
--8<-- "examples/assessments/25_complete/step02/assessment_service.py:26:47"
```

??? note "Code explanation"
    - **line 28** → defines `get_assessment`, which finds one assessment.
    - **line 29** → opens a connection to the database.
    - **lines 30–35** → selects the assessment, but only if it belongs to this user. `.fetchone()` returns the row, or `None` if there isn't one.
    - **line 36** → closes the connection.
    - **line 37** → returns the row, or `None`.
    - **line 40** → defines `set_completed`, which changes an assessment's `completed` value.
    - **line 41** → opens a connection.
    - **lines 42–45** → updates the assessment, again only if it belongs to this user.
    - **line 46** → saves the change.
    - **line 47** → closes the connection.

## The complete route

Go back to ***app.py*** and change the highlighted import at the top.

```python linenums="1" hl_lines="3" title="app.py"
--8<-- "examples/assessments/25_complete/step03/app.py:1:4"
```

??? note "Code explanation"
    - **line 3** → also imports `abort`, which stops a request and sends back an error.

Then add the complete route above the `calendar` route.

```python linenums="77" hl_lines="3-9" title="app.py"
--8<-- "examples/assessments/25_complete/step03/app.py:77:85"
```

??? note "Code explanation"
    - **line 79** → creates a route with a **variable** in its address. `<int:assessment_id>` matches a whole number, which Flask passes to the function as `assessment_id`.
    - **line 80** → only logged-in users can use it.
    - **line 81** → defines the `complete` view function.
    - **line 82** → checks whether the assessment doesn't exist or isn't this user's…
    - **line 83** → …if so, sends a `404 Not Found` error.
    - **line 84** → marks the assessment as completed.
    - **line 85** → returns an empty response, which HTMX swaps in place of the card.

!!! primm "PRIMM"
    1. **Predict** what will happen when you tick an assessment's Completed checkbox. What will you see if you then refresh the page?
    2. **Run** the code to check your predictions.
    3. Time to **investigate**. The card disappeared, but came back when you refreshed. Why? Look at the SQL in `get_assessments`.

## Show only outstanding assessments

The Home page should only list assessments that are still to do. Open ***assessment_service.py***, change the highlighted code in `get_assessments` and save it.

```python linenums="15" hl_lines="6" title="assessment_service.py"
--8<-- "examples/assessments/25_complete/step04/assessment_service.py:15:25"
```

??? note "Code explanation"
    - **line 20** → adds a second condition. `AND completed = 0` only finds assessments that haven't been completed.

## Tidy the card footer

Open ***static/style.css***, add the highlighted code below and save it.

```css linenums="1" hl_lines="14-18 20-22" title="static/style.css"
--8<-- "examples/assessments/25_complete/step05/static/style.css"
```

??? note "Code explanation"
    - **line 14** → a selector for elements with the class `card-footer`.
    - **line 15** → lays out the footer's contents in a row, using **flexbox**.
    - **line 16** → pushes the first item to the left and the last item to the right.
    - **line 17** → lines the items up vertically in the middle.
    - **line 18** → ends the styles for `.card-footer`.
    - **lines 20–22** → remove the space Pico puts under buttons, for buttons in a card footer. We'll add an Edit button there in the next lesson.

!!! primm "PRIMM"
    1. **Predict** what you'll see when you complete an assessment and refresh the page now.
    2. **Run** the code to check.
    3. Time to **investigate**. Find the `id` of one of your assessments in the Flask shell. Log in as a different user, open the developer tools **Console** tab, and type `htmx.ajax("POST", "/assessments/1/complete", {swap: "none"})`, using that `id` in place of `1`. Look at the terminal. What status code did the server send? Which line of ***app.py*** decided that?

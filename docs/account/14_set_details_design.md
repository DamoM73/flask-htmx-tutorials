# 14. Set Details Design

!!! learn "In this lesson we will learn"
    - how to fill a form's inputs with values that are already saved
    - how placeholders guide users
    - how to add a route for a new page

## Introduction

New users don't have a first or last name yet. The **Set Details** page lets them add their names, or change them later. In this lesson we'll build the page. In the next lesson we'll make the Save button work.

The page needs:

- a text input for the first name, already filled with the saved first name (if there is one)
- a text input for the last name, filled in the same way
- a Save button

## The set details form

Create a new file, add the code below and save it as ***set_details.html*** in the ***templates/partials*** folder.

```html+jinja linenums="1" title="templates/partials/set_details.html"
--8<-- "examples/account/14_set_details_design/step01/templates/partials/set_details.html"
```

??? note "Code explanation"
    - **lines 1–2** → open the card and show the heading.
    - **line 3** → opens the form, which posts to `/account/details` and swaps the response into `<main>`.
    - **line 4** → opens the label for the first name.
    - **line 5** → the label's text.
    - **line 6** → a text input named `first_name`. `value` fills it with the `first_name` from `values`, or nothing if there isn't one. `placeholder` shows grey hint text while the input is empty.
    - **line 7** → closes the label.
    - **lines 8–11** → the last name label and input, built the same way.
    - **line 12** → the Save button.
    - **lines 13–14** → close the form and the card.

!!! tip "Quotes inside quotes"
    The `value` attribute is already inside double quotes, so the empty string inside the Jinja code uses single quotes: `value="{{ values.first_name or '' }}"`. Jinja runs before the browser sees the HTML, so the browser only ever sees the finished value.

## The set details route

Go back to ***app.py*** and add the highlighted code below the `account` function.

```python linenums="62" hl_lines="6-8" title="app.py"
--8<-- "examples/account/14_set_details_design/step02/app.py:62:69"
```

??? note "Code explanation"
    - **line 67** → creates the `/account/details` route for GET and POST requests.
    - **line 68** → defines the `set_details` view function.
    - **line 69** → shows the Set Details form, using the logged-in user as `values`, so the inputs show the saved names. The title is `"Account"`, so the Account link stays highlighted in the menu.

!!! tip "Why call it values?"
    The form fills its inputs from `values`. Right now `values` is the logged-in user, so the inputs show the saved names. In the next lesson, when the user makes a mistake, we'll send what they typed as `values` instead, so they don't lose it.

There's no link to the Set Details page yet. We'll add one in [Account Navigation](17_account_navigation.md).

!!! primm "PRIMM"
    1. **Predict** what you'll see at `http://127.0.0.1:5000/account/details`.
    2. **Run** the code by typing the address into the browser while you're logged in.
    3. Time to **investigate**. Type a name and click Save. What happens? Why?
    4. Now **modify** the placeholders so they give an example name, such as `e.g. Sam`.

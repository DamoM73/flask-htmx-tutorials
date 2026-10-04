# 19. Add Page Design

!!! learn "In this lesson we will learn"
    - how to use text areas and date inputs in a form
    - how Pico's grid lays out elements side by side
    - how to fill a form from a dictionary of values

## Introduction

The Add page is where users record a new assessment. If we look back at the [design](../start/design.md#add), the form needs:

- a subject → a text input
- the details → a **text area**, which can hold several lines of text
- a start date and a due date → **date inputs**, side by side
- a Save button

Just like the Set Details form, the inputs will be filled from a `values` dictionary. When the page first loads, `values` will be empty, so the form is empty. In the next lesson, if the user makes a mistake, we'll send back what they typed.

## The add form

Open ***templates/partials/add.html***, replace its code with the code below and save it.

```html+jinja linenums="1" title="templates/partials/add.html"
--8<-- "examples/assessments/19_add_design/step01/templates/partials/add.html"
```

??? note "Code explanation"
    - **lines 1–2** → open the card and show the heading.
    - **line 3** → opens the form, which posts to `/add` and swaps the response into `<main>`.
    - **lines 4–7** → the subject label and text input, filled from `values.subject`.
    - **line 8** → opens the details label.
    - **line 9** → the label's text.
    - **line 10** → a `<textarea>` for the details. Unlike an input, a text area has a closing tag, and its value goes between the tags rather than in a `value` attribute.
    - **line 11** → closes the label.
    - **line 12** → opens a `<div>` with Pico's `grid` class, which places each element inside it side by side in equal columns. On narrow screens, Pico stacks them instead.
    - **lines 13–16** → the start date label and input. `type="date"` shows a date picker. Whatever format the user's computer displays, the value sent to the server is always `YYYY-MM-DD`.
    - **lines 17–20** → the due date label and input.
    - **line 21** → closes the grid.
    - **line 22** → the Save button.
    - **lines 23–24** → close the form and the card.

!!! tip "A div"
    A `<div>` is an element with no meaning of its own. We use it to group other elements so we can lay them out or style them together, like the two dates here.

## The add route

The add route needs to accept POST requests (for the form) and send an empty `values` dictionary.

Go back to ***app.py*** and change the highlighted code in the `add` function.

```python linenums="36" hl_lines="1 3" title="app.py"
--8<-- "examples/assessments/19_add_design/step02/app.py:36:38"
```

??? note "Code explanation"
    - **line 36** → lets the `/add` route accept GET and POST requests.
    - **line 38** → sends an empty dictionary as `values`. Jinja shows nothing for `values.subject` when the dictionary has no `subject` key, so the form is empty.

!!! primm "PRIMM"
    1. **Predict** what the Add page will look like.
    2. **Run** the code by logging in and clicking Add. Click in a date input.
    3. Time to **investigate**. Make the browser window narrow. What happens to the two dates? Then change line 38 to send `values={"subject": "Maths"}` and refresh. What changes? Change it back when you're done.

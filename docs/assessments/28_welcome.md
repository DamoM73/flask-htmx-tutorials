# 28. Welcome Page

!!! learn "In this lesson we will learn"
    - what a landing page is for
    - how to lay out features with Pico's grid
    - how to show logged-out visitors a welcome page

## Introduction

Right now, a visitor who isn't logged in sees the login form. That doesn't tell them what StudyM8 is or why they'd want it. Most websites greet new visitors with a **landing page**: it explains what the website does and has a clear **call to action**, a button that invites them to sign up.

If we look back at the [design](../start/design.md#welcome), the Welcome page has:

- a heading and a sentence that explains StudyM8
- three features, side by side
- a Register now button

## The Welcome page

Create a new file, add the code below and save it as ***welcome.html*** in the ***templates/partials*** folder.

```html+jinja linenums="1" title="templates/partials/welcome.html"
--8<-- "examples/assessments/28_welcome/step01/templates/partials/welcome.html"
```

??? note "Code explanation"
    - **line 1** → opens the card.
    - **lines 2–5** → the card's header, with the main heading and a sentence explaining StudyM8.
    - **line 6** → opens a grid, which puts the three features side by side.
    - **lines 7–10** → the first feature: a small heading and a sentence.
    - **lines 11–14** → the second feature.
    - **lines 15–18** → the third feature.
    - **line 19** → closes the grid.
    - **line 20** → opens the card's footer.
    - **line 21** → the call to action: a button that loads the Register page.
    - **lines 22–23** → close the footer and the card.

## Show it to visitors

Go back to ***app.py*** and change the highlighted code in the `index` function.

```python linenums="56" hl_lines="5" title="app.py"
--8<-- "examples/assessments/28_welcome/step02/app.py:56:60"
```

??? note "Code explanation"
    - **line 60** → shows the Welcome page to visitors who aren't logged in.

Users who log out should also see the Welcome page. Change the highlighted code in the `logout` function.

```python linenums="191" hl_lines="4" title="app.py"
--8<-- "examples/assessments/28_welcome/step02/app.py:191:194"
```

??? note "Code explanation"
    - **line 194** → shows the Welcome page and sets the address bar to `/`.

!!! primm "PRIMM"
    1. **Predict** what you'll see when you log out.
    2. **Run** the code. Log out, then click Register now.
    3. Time to **investigate**. Make the browser window narrow. What happens to the three features?
    4. Now **modify** the Welcome page to add a fourth feature. Does the grid still fit?

StudyM8 now has every feature from the design. In the next section we'll make it faster.

# 23. Home Page Design

!!! learn "In this lesson we will learn"
    - how to make a template for one item and reuse it
    - how to repeat HTML with a Jinja `{% for %}` loop
    - what a for loop's `{% else %}` does in Jinja
    - how to test a template with sample data

## Introduction

The Home page lists all of the user's outstanding assessments. If we look back at the [design](../start/design.md#home), each assessment is shown as a card.

So let's think about this:

1. Every card looks the same, just with different data → one template for one card: ***assessment_card.html***.
2. The Home page needs one card for each assessment → a Jinja `{% for %}` loop that includes the card template.
3. Later, we'll need to send a single card on its own (when an assessment is edited), so keeping the card in its own template will pay off.

In this lesson we'll build the templates and test them with some sample data. In the next lesson we'll load the real assessments from the database.

## The card template

Create a new file, add the code below and save it as ***assessment_card.html*** in the ***templates/partials*** folder.

```html+jinja linenums="1" title="templates/partials/assessment_card.html"
--8<-- "examples/assessments/23_home_design/step01/templates/partials/assessment_card.html"
```

??? note "Code explanation"
    - **line 1** → opens the card.
    - **lines 2–4** → the card's header, showing the subject in bold.
    - **line 5** → the details.
    - **line 6** → the start and due dates in small text.
    - **line 7** → closes the card.

## The Home page template

Open ***templates/partials/home.html***, change the highlighted code below and save it.

```html+jinja linenums="1" hl_lines="2-6" title="templates/partials/home.html"
--8<-- "examples/assessments/23_home_design/step02/templates/partials/home.html"
```

??? note "Code explanation"
    - **line 2** → starts a loop over the `assessments` list. Each time around the loop, `assessment` is the next item, just like a Python `for` loop.
    - **line 3** → includes the card template. The included template can use the loop's `assessment` variable.
    - **line 4** → `{% else %}` on a Jinja `for` loop runs when the list is empty.
    - **line 5** → a message with a link to the Add page, shown when there are no assessments.
    - **line 6** → ends the loop.

## The home route

Our Home page has been the `/` route. From now on, the Home page will have its own address, `/home`, and only logged-in users can see it.

Go back to ***app.py*** and change the highlighted code below.

```python linenums="33" hl_lines="3 6-13" title="app.py"
--8<-- "examples/assessments/23_home_design/step03/app.py:33:45"
```

??? note "Code explanation"
    - **line 35** → the `/` route now just runs the `home` function.
    - **line 38** → creates the `/home` route.
    - **line 39** → only logged-in users can see it.
    - **line 40** → defines the `home` view function.
    - **lines 41–44** → a list of two sample assessments, each a dictionary. Jinja's `assessment.subject` works with dictionary keys as well as attributes.
    - **line 45** → shows the Home page with the sample assessments, and sets the address bar to `/home`.

Finally, the Home link in the menu needs to go to `/home`. Open ***templates/nav.html***, change the highlighted code below and save it.

```html+jinja linenums="1" hl_lines="7" title="templates/nav.html"
--8<-- "examples/assessments/23_home_design/step03/templates/nav.html"
```

??? note "Code explanation"
    - **line 7** → the Home link now goes to `/home`.

!!! primm "PRIMM"
    1. **Predict** what the Home page will show.
    2. **Run** the code by logging in and clicking Home.
    3. Time to **investigate**. Change line 41 to `assessments = []` and refresh. What do you see now? Which line of ***home.html*** made that happen? Change it back when you're done.
    4. Now **modify** the sample data to add a third assessment.

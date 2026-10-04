# 4. Styling with Pico

!!! learn "In this lesson we will learn"
    - what CSS is and how a page loads a stylesheet
    - how Pico CSS styles plain HTML without extra code
    - how to lay out a menu bar with `<header>`, `<nav>` and lists
    - how to make a card with the `<article>` element

## Introduction

Our pages work, but they look very plain. That's because we've only written HTML, which describes the content of a page. To change how a page looks, we need **CSS** (Cascading Style Sheets).

Writing CSS for a whole website takes a long time, so we'll use **Pico CSS**. Pico is a ready-made stylesheet that styles plain HTML elements. If we use the right HTML elements, Pico makes them look good without us writing any CSS at all.

!!! tip "Semantic HTML"
    HTML elements that describe what their content *is* are called **semantic** elements. `<nav>` says "this is navigation", `<main>` says "this is the main content" and `<article>` says "this is a self-contained piece of content". Pico uses these meanings to decide how each part should look. Semantic HTML also helps screen readers describe the page to people with vision impairments.

## Load Pico

Open ***templates/base.html***, change the highlighted code below and save it.

```html+jinja linenums="1" hl_lines="5 7 10-23" title="templates/base.html"
--8<-- "examples/shell/04_pico/step01/templates/base.html"
```

??? note "Code explanation"
    - **line 5** → tells phones and tablets to fit the page to their screen width, so Pico can adjust the layout for small screens.
    - **line 7** → loads the Pico stylesheet from the internet. The `<link>` element connects the page to another file; `rel="stylesheet"` says the file is CSS and `href` is its address.
    - **line 10** → opens a `<header>` element for the top of the page. Pico's `container` **class** keeps the content centred with space on each side.
    - **line 11** → opens the `<nav>`. Pico lays out each list inside a `<nav>` in a row.
    - **lines 12–14** → the first list, holding the StudyM8 name as a bold link back to the Home page. Pico puts the first list on the left.
    - **line 15** → opens the second list, which Pico puts on the right.
    - **lines 16–19** → each menu link is now inside a list item (`<li>`).
    - **lines 20–21** → close the second list and the `<nav>`.
    - **line 22** → closes the `<header>`.
    - **line 23** → gives `<main>` the `container` class, so the page content lines up with the menu.

!!! primm "PRIMM"
    1. **Predict** how the page will look once Pico is loaded.
    2. **Run** the code by refreshing the browser.
    3. Time to **investigate**. Make the browser window very narrow, then wide again. What does Pico do? Change your computer between light and dark mode (or check the page on a phone). What happens?

## Cards

StudyM8 will show each assessment in a **card**: a box that groups related information. In Pico, an `<article>` element is drawn as a card. An `<article>` can have its own `<header>` and `<footer>`, which Pico shades slightly differently.

We don't have a database yet, so let's make one card with some made-up data to see how it looks.

Open ***templates/partials/home.html***, change the highlighted code below and save it.

```html+jinja linenums="1" hl_lines="2-10" title="templates/partials/home.html"
--8<-- "examples/shell/04_pico/step02/templates/partials/home.html"
```

??? note "Code explanation"
    - **line 2** → opens an `<article>`, which Pico draws as a card.
    - **lines 3–5** → the card's header, holding the subject in bold.
    - **line 6** → the assessment details.
    - **lines 7–9** → the card's footer, holding the due date in small text.
    - **line 10** → closes the `<article>`.

!!! primm "PRIMM"
    1. **Predict** what the Home page will look like.
    2. **Run** the code by refreshing the browser.
    3. Time to **investigate**. What does `<strong>` do? What does `<small>` do?
    4. Now **modify** the code to add a second card for an English essay due on 20/10/2026.

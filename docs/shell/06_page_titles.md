# 6. Page Titles

!!! learn "In this lesson we will learn"
    - why the browser tab stops changing when HTMX swaps content
    - how HTMX updates the title from a `<title>` element in the response
    - how to build a fragment template that wraps each partial

## Introduction

Let's check something. Refresh the browser on the Home page, then click Calendar and look at the browser tab. It still says **Home | StudyM8**.

When we refresh, Flask sends the whole page, including the `<title>` in the `<head>`. But when we click a link, HTMX only swaps the content of `<main>`. The `<head>` is never replaced, so the title never changes.

The good news is that HTMX has a solution built in: if a response contains a `<title>` element, HTMX uses it to update the browser tab. So all we need to do is send a `<title>` with each partial.

We could add a `<title>` to the top of every partial, but then the full page would have a `<title>` inside `<main>` as well as in the `<head>`. Instead, let's make one small template that wraps any partial with a title. We'll call it a **fragment**.

## The fragment template

Create a new file, add the code below and save it as ***fragment.html*** in the ***templates*** folder.

```html+jinja linenums="1" title="templates/fragment.html"
--8<-- "examples/shell/06_page_titles/step01/templates/fragment.html"
```

??? note "Code explanation"
    - **line 1** → a `<title>` element using the page's title. HTMX finds it in the response and updates the browser tab.
    - **line 2** → includes the partial named in `page`, just like ***base.html*** does.

## Send the fragment

Now Flask needs to send the fragment, instead of the bare partial, to HTMX requests.

Go back to ***app.py*** and change the highlighted code below.

```python linenums="1" hl_lines="8" title="app.py"
--8<-- "examples/shell/06_page_titles/step02/app.py"
```

??? note "Code explanation"
    - **line 8** → builds ***fragment.html*** for HTMX requests, passing in the partial's file name and the title.

!!! primm "PRIMM"
    1. **Predict** what the browser tab will show as you click each menu link.
    2. **Run** the code by refreshing the browser and clicking each link.
    3. Time to **investigate**. Use the **Network** tab in the developer tools to look at the response when you click a link. Where is the `<title>`?
    4. Now **modify** the code so the Home page's tab says **My Assessments | StudyM8**. Which file did you change? Change it back when you're done, because we'll use the title for something else in the next lesson.

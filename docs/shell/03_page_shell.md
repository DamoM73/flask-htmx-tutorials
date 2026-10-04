# 3. The Page Shell

!!! learn "In this lesson we will learn"
    - why our pages should share one template for the parts that repeat
    - how to make links with the `<a>` element
    - how to use Jinja's `{% include %}` to put one template inside another
    - how to add more routes to our Flask app

## Introduction

StudyM8 has several pages: Home, Add, Calendar and Account. If we look back at the [design](../start/design.md#pages), every page has the same menu at the top. Only the part underneath the menu changes.

We could copy the menu into every page's template, but then every time we change the menu we'd have to change every template. That's a lot of repeated code, and it's easy to miss one.

So let's think about this:

1. The parts that are the same on every page (the `<head>` and the menu) go in one template → the **page shell**.
2. The part that's different on each page goes in its own small template → a **partial**.
3. When a browser asks for a page, Flask builds the page shell and drops the right partial into it.

## The page shell

Create a new file, add the code below and save it as ***base.html*** in the ***templates*** folder.

```html+jinja linenums="1" title="templates/base.html"
--8<-- "examples/shell/03_page_shell/step01/templates/base.html"
```

??? note "Code explanation"
    - **lines 1–6** → the start of the HTML document, just like ***index.html***. The browser tab shows the page's title.
    - **line 7** → opens the `<body>`.
    - **line 8** → opens a `<nav>` element, which holds the website's main navigation links.
    - **lines 9–12** → one link for each page. The `<a>` element makes a link, and its `href` attribute is the address the link goes to.
    - **line 13** → closes the `<nav>`.
    - **line 14** → opens a `<main>` element, which holds the main content of the page.
    - **line 15** → a Jinja **include** tag. It finds the template named in the `page` variable and puts its HTML here.
    - **line 16** → closes the `<main>`.
    - **lines 17–18** → close the `<body>` and the `<html>`.

!!! tip "Two kinds of Jinja brackets"
    Jinja uses two kinds of brackets:

    - `{{ }}` → shows a value, for example `{{ title }}`
    - `{% %}` → does something, for example `{% include page %}`

## The partials

Each page now needs its own partial. Partials aren't full HTML documents; they only hold the content for their part of the page.

Create a new folder called ***partials*** inside the ***templates*** folder. Then create these four files in the ***partials*** folder.

```html+jinja linenums="1" title="templates/partials/home.html"
--8<-- "examples/shell/03_page_shell/step02/templates/partials/home.html"
```

??? note "Code explanation"
    - **line 1** → the Home page's heading.
    - **line 2** → a placeholder paragraph. We'll replace it with the user's assessments later.

```html+jinja linenums="1" title="templates/partials/add.html"
--8<-- "examples/shell/03_page_shell/step02/templates/partials/add.html"
```

??? note "Code explanation"
    - **lines 1–2** → the Add page's heading and a placeholder paragraph.

```html+jinja linenums="1" title="templates/partials/calendar.html"
--8<-- "examples/shell/03_page_shell/step02/templates/partials/calendar.html"
```

??? note "Code explanation"
    - **lines 1–2** → the Calendar page's heading and a placeholder paragraph.

```html+jinja linenums="1" title="templates/partials/account.html"
--8<-- "examples/shell/03_page_shell/step02/templates/partials/account.html"
```

??? note "Code explanation"
    - **lines 1–2** → the Account page's heading and a placeholder paragraph.

## The routes

Now Flask needs a route for each page. Each route builds ***base.html*** and tells it which partial to include.

Go back to ***app.py*** and change the highlighted code below.

```python linenums="1" hl_lines="8 11-13 16-18 21-23" title="app.py"
--8<-- "examples/shell/03_page_shell/step03/app.py"
```

??? note "Code explanation"
    - **line 8** → builds ***base.html***, setting `page` to the Home partial and `title` to `"Home"`.
    - **line 11** → creates a route for the `/add` address.
    - **line 12** → defines the `add` view function.
    - **line 13** → builds ***base.html*** with the Add partial.
    - **lines 16–18** → the `/calendar` route, which builds ***base.html*** with the Calendar partial.
    - **lines 21–23** → the `/account` route, which builds ***base.html*** with the Account partial.

We don't need ***index.html*** any more, so delete it from the ***templates*** folder. Our ***studym8*** folder should now look like this:

```text
studym8/
    .venv/
    templates/
        partials/
            account.html
            add.html
            calendar.html
            home.html
        base.html
    app.py
```

!!! primm "PRIMM"
    1. **Predict** what you'll see when you click each link in the menu.
    2. **Run** the code by refreshing the browser, then click each link.
    3. Time to **investigate**. Watch the address bar and the browser tab as you click each link. What changes? Look at the terminal: how many requests are made for each click?
    4. Now **modify** the code. Change the menu so the links appear in the order Home, Calendar, Add, Account. How many files did you need to change?

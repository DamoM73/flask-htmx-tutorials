# 7. Show the Active Link

!!! learn "In this lesson we will learn"
    - how to mark the current page's link with `aria-current`
    - how to use a Jinja `{% if %}` tag
    - how to move the menu into its own template
    - how an HTMX out-of-band swap updates a second part of the page

## Introduction

When we look at the menu, there's no way to tell which page we're on. Most websites highlight the current page's link, so users always know where they are.

HTML has an attribute for this: `aria-current="page"`. It tells screen readers which link is the current page, and we can use CSS to make it look different too.

So let's think about this:

1. The menu needs to know which page is showing → we already send the page's `title` to the templates, so the menu can check it with a Jinja `{% if %}`.
2. When HTMX swaps the content, the menu isn't redrawn, so the highlighted link would never change → HTMX needs to update the menu as well as `<main>`.
3. HTMX has a feature for this, called an **out-of-band swap**. If an element in the response has `hx-swap-oob="true"`, HTMX finds the element on the page with the same `id` and replaces it, wherever it is.
4. Both ***base.html*** and ***fragment.html*** will need the menu → we'll move the menu into its own template, ***nav.html***, and include it in both.

## The menu template

Create a new file, add the code below and save it as ***nav.html*** in the ***templates*** folder.

```html+jinja linenums="1" title="templates/nav.html"
--8<-- "examples/shell/07_active_link/step01/templates/nav.html"
```

??? note "Code explanation"
    - **line 1** → opens the `<nav>` with the id `nav`. If the `oob` variable is true, Jinja adds `hx-swap-oob="true"`, so HTMX swaps this menu into the page in place of the old one.
    - **lines 2–4** → the StudyM8 link, the same as before.
    - **line 5** → the second list, which passes `hx-target` and `hx-push-url` to its links.
    - **line 6** → the Home link. If the title is `"Home"`, Jinja adds `aria-current="page"` to the link.
    - **line 7** → the Add link, which is marked as current when the title is `"Add"`.
    - **line 8** → the Calendar link, which is marked as current when the title is `"Calendar"`.
    - **line 9** → the Account link, which is marked as current when the title is `"Account"`.
    - **lines 10–11** → close the list and the `<nav>`.

!!! tip "Jinja if"
    Jinja's `{% if %}` works like Python's `if`, but it needs an `{% endif %}` to show where it ends, because HTML doesn't use indentation to group things. Anything between `{% if ... %}` and `{% endif %}` only appears in the HTML when the condition is true.

## Use the menu template

Open ***templates/base.html***, change the highlighted code below and save it.

```html+jinja linenums="1" hl_lines="9 14" title="templates/base.html"
--8<-- "examples/shell/07_active_link/step02/templates/base.html"
```

??? note "Code explanation"
    - **line 9** → loads our own stylesheet, ***style.css***, after Pico, so our styles can change Pico's. `url_for('static', filename='style.css')` works out the address of the file in Flask's ***static*** folder.
    - **line 14** → includes ***nav.html*** in place of the menu. `oob` isn't set here, so the menu doesn't get `hx-swap-oob`.

Now open ***templates/fragment.html***, change the highlighted code below and save it.

```html+jinja linenums="1" hl_lines="2" title="templates/fragment.html"
--8<-- "examples/shell/07_active_link/step03/templates/fragment.html"
```

??? note "Code explanation"
    - **line 2** → sets `oob` to `True` and includes ***nav.html***, so every HTMX response carries a new menu that HTMX swaps out of band.

## Style the active link

Pico doesn't style `aria-current` links in the menu, so we'll write a small piece of CSS of our own. Flask serves files like stylesheets and images from a folder called ***static***.

Create a new folder called ***static*** inside the ***studym8*** folder. Then create a new file, add the code below and save it as ***style.css*** in the ***static*** folder.

```css linenums="1" title="static/style.css"
--8<-- "examples/shell/07_active_link/step04/static/style.css"
```

??? note "Code explanation"
    - **line 1** → a CSS **selector** that picks every link inside a `<nav>` that has `aria-current="page"`. The `{` starts the list of styles for those links.
    - **line 2** → makes the text bold.
    - **line 3** → underlines the text.
    - **line 4** → ends the list of styles.

Our ***studym8*** folder should now look like this:

```text
studym8/
    .venv/
    static/
        style.css
    templates/
        partials/
            account.html
            add.html
            calendar.html
            home.html
        base.html
        fragment.html
        nav.html
    app.py
```

!!! primm "PRIMM"
    1. **Predict** what the menu will look like on each page.
    2. **Run** the code by refreshing the browser and clicking each link.
    3. Time to **investigate**. Use the **Network** tab to look at the response when you click a link. How many parts are in it now? Which part goes where?
    4. Now **modify** ***style.css*** so the active link is also a different colour. Search the web for "CSS color property" to find out how.

!!! tip "If the style doesn't change"
    Browsers save copies of stylesheets so they don't have to download them every time. If your changes to ***style.css*** don't show, press ++ctrl+f5++ to reload the page and its stylesheets.

The page shell is finished. In the next section we'll add a database and user accounts.

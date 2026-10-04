# 17. Account Navigation

!!! learn "In this lesson we will learn"
    - how a button can load a page with HTMX
    - how to send new users straight to the Set Details page

## Introduction

The Set Details page works, but the only way to reach it is to type its address. If we look back at the [site map](../start/design.md#site-map), Set Details is reached from the Account page. And new users should set their names as soon as they register.

So we need to:

1. add an **Edit details** button to the Account page → ***templates/partials/account.html***
2. show the Set Details page after registering, instead of the Home page → ***app.py***

## The Edit details button

Open ***templates/partials/account.html***, add the highlighted code below and save it.

```html+jinja linenums="1" hl_lines="6" title="templates/partials/account.html"
--8<-- "examples/account/17_account_navigation/step01/templates/partials/account.html"
```

??? note "Code explanation"
    - **line 6** → a button that loads the Set Details page. HTMX attributes work on any element, not just links: `hx-get` asks for `/account/details`, `hx-target` puts it in `<main>` and `hx-push-url` updates the address bar.

## Set details after registering

Go back to ***app.py*** and change the highlighted code at the end of the `register` function.

```python linenums="84" hl_lines="3-4" title="app.py"
--8<-- "examples/account/17_account_navigation/step02/app.py:84:87"
```

??? note "Code explanation"
    - **lines 86–87** → after logging the new user in, shows the Set Details form and changes the address bar to `/account/details`.

!!! primm "PRIMM"
    1. **Predict** what you'll see straight after registering a new account.
    2. **Run** the code. Register a new account and set your names. Then click Account and Edit details.
    3. Time to **investigate**. On the Set Details page, click the browser's back button. Where do you go? Why?
    4. Now **modify** the Set Details page to add a **Cancel** button that goes back to the Account page without saving. (Hint: copy the Edit details button and change it. Add `type="button"` so it doesn't submit the form.)

The Account section is finished. In the next section we'll start on the reason StudyM8 exists: assessments.

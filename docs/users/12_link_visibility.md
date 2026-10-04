# 12. Account Link Visibility

!!! learn "In this lesson we will learn"
    - how to use `current_user` in a template
    - how to show different links to logged-in and logged-out users
    - why hiding a link doesn't protect a page

## Introduction

At the end of the last lesson we noticed our menu shows every link to everyone. A logged-out visitor sees Logout, and a logged-in user sees Register and Login. Let's fix that:

- logged in → Home, Add, Calendar, Account and Logout
- logged out → Register and Login

Flask-Login gives every template a variable called `current_user`. When someone is logged in, it's their `User` object. When no one is logged in, it's an anonymous user. Either way, `current_user.is_authenticated` tells us whether someone is logged in.

## Show the right links

Open ***templates/nav.html***, add the highlighted code below and save it.

```html+jinja linenums="1" hl_lines="6 12 15" title="templates/nav.html"
--8<-- "examples/users/12_link_visibility/step01/templates/nav.html"
```

??? note "Code explanation"
    - **line 6** → checks whether a user is logged in. Everything up to the `{% else %}` only appears for logged-in users.
    - **line 12** → `{% else %}` starts the links that appear when no one is logged in.
    - **line 15** → ends the `if`.

Think about what happens when a user logs in. The login form swaps the Home page into `<main>`, but the menu is outside `<main>`. So how does the menu change? Remember from [Show the Active Link](../shell/07_active_link.md) that every HTMX response includes ***nav.html*** as an out-of-band swap. When a user logs in or out, the response carries a new menu built for the new `current_user`.

!!! primm "PRIMM"
    1. **Predict** which links you'll see before and after logging in.
    2. **Run** the code. Log out, check the menu, then log in again.
    3. Time to **investigate**. While logged out, type `http://127.0.0.1:5000/account` into the address bar. What happens? What does that tell you about hiding links?
    4. Now **modify** the menu so the logged-out links also include Home.

!!! warning "Hiding a link isn't security"
    Hiding the Add, Calendar and Account links stops logged-out visitors from clicking them, but anyone can still type the address. In [Prevent Unauthorised Access](../assessments/22_unauthorised_access.md) we'll make the server refuse these pages to anyone who isn't logged in.

That's users finished. In the next section we'll build the Account and Set Details pages.

# 5. Connecting Links with HTMX

!!! learn "In this lesson we will learn"
    - why reloading the whole page for every click is wasteful
    - how HTMX attributes send requests and swap content
    - how a server can tell whether a request came from HTMX
    - how to keep the address bar, refresh and back button working

## Introduction

Right now, every time we click a link the browser:

1. sends a request for the whole page
2. throws away everything on the screen
3. draws the whole page again, including the menu that didn't change

For a small website that's fine, but it's wasteful. The only part that changes is what's inside `<main>`, so that's the only part we should need to send.

**HTMX** is a small JavaScript library that lets any HTML element send a request and swap the response into the page. We don't write any JavaScript ourselves; we just add HTMX **attributes** to our HTML.

## Planning

Let's think about what needs to happen when we click a menu link:

| Input | Process | Output |
| :-- | :-- | :-- |
| user clicks the Add link | HTMX sends a request to `/add` | Flask sends back only the Add partial |
| Flask's response arrives | HTMX swaps the response into `<main>` | the Add page shows; the menu isn't redrawn |
| | HTMX updates the address bar | the address bar shows `/add` |

So we need to change two things:

1. the menu links need HTMX attributes → ***base.html***
2. Flask needs to send just the partial when HTMX asks → ***app.py***

## Add HTMX to the page shell

Open ***templates/base.html***, change the highlighted code below and save it.

```html+jinja linenums="1" hl_lines="6 9 15 17-21 25" title="templates/base.html"
--8<-- "examples/shell/05_htmx_links/step01/templates/base.html"
```

??? note "Code explanation"
    - **line 6** → sets an HTMX option. If we press the browser's back button and HTMX doesn't have a saved copy of that page, it reloads the whole page from the server.
    - **line 9** → loads the HTMX library from the internet.
    - **line 15** → adds three HTMX attributes to the StudyM8 link. `hx-get="/"` sends a GET request to `/` when the link is clicked. `hx-target="#content"` says where to put the response: the element with the id `content`. `hx-push-url="true"` changes the address bar to match.
    - **line 17** → puts `hx-target` and `hx-push-url` on the list instead of on every link. HTMX attributes are **inherited**, so every link inside the list uses them.
    - **lines 18–21** → gives each menu link an `hx-get` attribute with its route.
    - **line 25** → gives `<main>` the id `content`, so the `#content` target can find it. An `id` must be unique on the page.

!!! tip "Why keep href?"
    Each link still has its `href` attribute. HTMX uses `hx-get` and stops the browser following the `href`. If HTMX ever fails to load, the browser follows the `href` instead, so the links still work. We can also right-click a link and open it in a new tab.

!!! primm "PRIMM"
    1. **Predict** what will happen when you click the Add link now.
    2. **Run** the code by refreshing the browser, then click Add.
    3. Time to **investigate**. Something's wrong. What do you see? Why do you think it happened?

So what went wrong? HTMX did exactly what we asked: it sent a request to `/add` and swapped the response into `<main>`. But Flask still sends the **whole page** for `/add`, so we end up with a whole page, including a second menu, inside `<main>`.

## Send partials to HTMX

Flask needs to send different responses to different requests:

- a request from HTMX → just the partial, because the page shell is already on screen
- any other request (typing the address, refreshing, opening in a new tab) → the whole page

How does Flask know who's asking? Every request HTMX sends includes an extra **header**, `HX-Request`. A header is a piece of information sent along with a request or response. If the request has an `HX-Request` header, it came from HTMX.

All four routes need this check, so rather than repeating it four times, let's put it in a function.

Go back to ***app.py*** and change the highlighted code below.

```python linenums="1" hl_lines="1 6-13 18 23 28 33" title="app.py"
--8<-- "examples/shell/05_htmx_links/step02/app.py"
```

??? note "Code explanation"
    - **line 1** → also imports `make_response` and `request`. `request` holds everything about the request Flask is handling, including its headers.
    - **line 6** → defines `render_page`, which takes the partial's file name and the page title.
    - **line 7** → checks whether the request has an `HX-Request` header…
    - **line 8** → …if it does, builds just the partial.
    - **line 9** → otherwise…
    - **line 10** → …builds the whole page, with the partial included in the page shell.
    - **line 11** → turns the HTML into a response object, so we can add headers to it.
    - **line 12** → adds a `Vary` header. This tells the browser the response changes depending on the `HX-Request` header, so it doesn't mix up a saved partial with a saved whole page.
    - **line 13** → returns the response.
    - **line 18** → the Home route now uses `render_page`.
    - **line 23** → the Add route uses `render_page`.
    - **line 28** → the Calendar route uses `render_page`.
    - **line 33** → the Account route uses `render_page`.

!!! primm "PRIMM"
    1. **Predict** what will happen when you click each menu link now.
    2. **Run** the code by refreshing the browser and clicking each link. Then try the browser's back button, and refresh the page while you're on Calendar.
    3. Time to **investigate**. Press ++f12++ to open the browser's developer tools and click the **Network** tab. Click a menu link. Click the request that appears, then **Response**. What did Flask send back? Now refresh the page. What's different about this response?
    4. Now **modify** the code. Remove `hx-push-url="true"` from line 17 of ***base.html*** and click the links. What changes? Why is it important? Put it back when you're done.

!!! tip "Why use HTMX?"
    Our pages are small, so the speed difference is hard to notice. On a big website with large menus, images and scripts, sending only the part that changes saves a lot of data and makes the site feel much faster. We'll measure this in the [Optimisation](../optimisation/29_optimisation.md) section.

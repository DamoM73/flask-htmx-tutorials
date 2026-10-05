# HTMX

!!! learn "On this page we will learn"
    - how HTMX attributes send requests and swap the response into the page
    - which HTMX attributes and headers StudyM8 uses
    - how out-of-band swaps update a second part of the page

**HTMX** is a small JavaScript library that lets any HTML element send a request and swap the response into the page, without us writing JavaScript. We added it in [Connecting Links with HTMX](../shell/05_htmx_links.md).

## Load it

```html
<script src="https://unpkg.com/htmx.org@2.0.11"></script>
```

## How it works

```html
<a href="/add" hx-get="/add" hx-target="#content" hx-push-url="true">Add</a>
```

1. The user clicks the link.
2. HTMX sends a GET request to `/add`, with an `HX-Request` header.
3. The server sends back some HTML.
4. HTMX swaps the HTML into the element with the id `content`.
5. HTMX changes the address bar to `/add`.

## Attributes

| Attribute | Does | First used |
| :-- | :-- | :-- |
| `hx-get="/url"` | sends a GET request when the element is clicked | [5. Connecting Links](../shell/05_htmx_links.md) |
| `hx-post="/url"` | sends a POST request; on a form, sends when submitted, with the form's data | [10. Register](../users/10_register.md) |
| `hx-target="#id"` | where to put the response | [5. Connecting Links](../shell/05_htmx_links.md) |
| `hx-target="closest article"` | targets the nearest `<article>` around the element | [25. Complete Assessments](../assessments/25_complete.md) |
| `hx-swap="outerHTML"` | replaces the whole target element; the default, `innerHTML`, replaces only what's inside it | [25. Complete Assessments](../assessments/25_complete.md) |
| `hx-push-url="true"` | changes the address bar to the request's address | [5. Connecting Links](../shell/05_htmx_links.md) |
| `hx-swap-oob="true"` | in a response: swap this element into the page in place of the element with the same `id`, wherever it is | [7. Show the Active Link](../shell/07_active_link.md) |

HTMX attributes are **inherited**: an attribute on a parent element applies to every element inside it. Our menu's `<ul>` sets `hx-target` and `hx-push-url` once for all its links.

## Headers

| Header | Sent by | Means |
| :-- | :-- | :-- |
| `HX-Request: true` | HTMX, with every request | the request came from HTMX, so send a partial instead of a whole page |
| `HX-Push-Url: /home` | our server, in a response | change the address bar to this address |
| `Vary: HX-Request` | our server, in a response | the browser mustn't mix up saved partials and saved whole pages |

## The page title

If a response contains a `<title>` element, HTMX uses it to update the browser tab. That's why ***fragment.html*** starts with a `<title>`. See [Page Titles](../shell/06_page_titles.md).

## Settings

```html
<meta name="htmx-config" content='{"refreshOnHistoryMiss": true}'>
```

`refreshOnHistoryMiss` → if the back button goes to a page HTMX hasn't saved, reload it from the server.

## More for your own website

### Deleting with a confirmation

StudyM8 never deletes anything, but an admin will need to remove old news and events. HTMX can send a **DELETE** request, and `hx-confirm` asks the user first:

```html+jinja
<button class="secondary"
        hx-delete="/events/{{ event.id }}"
        hx-confirm="Delete {{ event.title }}? This can't be undone."
        hx-target="closest article" hx-swap="outerHTML">Delete</button>
```

The Flask route accepts `DELETE`, removes the row and returns an empty response, so the card disappears (see [Flask](flask.md#deleting) and [SQL](sql.md#deleting-rows)).

| Attribute | Does |
| :-- | :-- |
| `hx-delete="/url"` | sends a DELETE request |
| `hx-put="/url"`, `hx-patch="/url"` | send PUT or PATCH requests, sometimes used for updates |
| `hx-confirm="Message"` | shows a browser confirmation box; the request is only sent if the user clicks OK |

### Filters that update as the user chooses

A `<select>` can ask the server for a new list as soon as its value changes:

```html
<select name="team" hx-get="/events/list" hx-target="#event-list" hx-trigger="change">
    <option value="">All teams</option>
    <option value="u12">Under 12s</option>
</select>

<div id="event-list">
    ...event cards...
</div>
```

HTMX sends the select's value with the request, as `/events/list?team=u12`. Flask reads it with `request.args` (see [Flask](flask.md#query-strings)).

### Live search

```html
<input type="search" name="q" placeholder="Search news"
       hx-get="/news/search" hx-target="#results"
       hx-trigger="input changed delay:500ms">
<div id="results"></div>
```

`hx-trigger` says **when** to send the request:

| Trigger | Sends a request |
| :-- | :-- |
| `click` | when clicked (the default for links and buttons) |
| `submit` | when a form is submitted (the default for forms) |
| `change` | when the value changes (the default for selects) |
| `input changed delay:500ms` | half a second after the user stops typing, and only if the text changed |
| `load` | as soon as the element appears on the page |
| `every 60s` | every 60 seconds, for example to refresh a live scoreboard |

### Sending extra values

| Attribute | Does | Example |
| :-- | :-- | :-- |
| `hx-include` | also sends the values of other inputs | `hx-include="[name='team']"` sends the team select with a search |
| `hx-vals` | sends fixed values | `hx-vals='{"page": 2}'` |

### Load more

Instead of showing every news post at once, show the latest ten and a button that loads the next ten. The button replaces **itself** with the next posts and a new button:

```html+jinja
{% for post in posts %}
{{ news_card(post) }}
{% endfor %}
{% if more %}
<button class="secondary" hx-get="/news/more?page={{ page + 1 }}"
        hx-target="this" hx-swap="outerHTML">Load more</button>
{% endif %}
```

The `/news/more` route sends back the same template with the next page of posts. Use `LIMIT` and `OFFSET` to choose which posts (see [SQL](sql.md#the-newest-first-and-limit)).

| `hx-swap` value | Puts the response |
| :-- | :-- |
| `innerHTML` (default) | inside the target, replacing what's there |
| `outerHTML` | in place of the whole target |
| `beforeend` | inside the target, after what's already there |
| `afterbegin` | inside the target, before what's already there |
| `delete` | nowhere; removes the target |

### Loading indicators

```html
<button hx-get="/calendar" hx-target="#content" hx-indicator="#loading">Calendar</button>
<span id="loading" class="htmx-indicator" aria-busy="true">Loading...</span>
```

An element with the class `htmx-indicator` stays hidden until its request is running. Pico's `aria-busy="true"` adds a spinner.

### Boosting ordinary links

If a site doesn't use a page shell and partials, `hx-boost` is a one-line way to get some of HTMX's speed:

```html
<body hx-boost="true">
```

Every link and form inside the body is sent with HTMX. The server sends whole pages as normal, and HTMX swaps in the new `<body>` without reloading the stylesheets and scripts.

## Documentation

Documentation is the official guide written by the people who made the code library, and we can use it to look up every attribute and setting, including ones that aren't covered on this page.

- [HTMX documentation](https://htmx.org/docs/)
- [HTMX attribute reference](https://htmx.org/reference/)

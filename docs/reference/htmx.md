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

## Documentation

Documentation is the official guide written by the people who made the code library, and we can use it to look up every attribute and setting, including ones that aren't covered on this page.

- [HTMX documentation](https://htmx.org/docs/)
- [HTMX attribute reference](https://htmx.org/reference/)

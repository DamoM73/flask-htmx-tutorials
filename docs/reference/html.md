# HTML

!!! learn "On this page we will learn"
    - how HTML elements, tags and attributes fit together
    - which HTML elements StudyM8 uses, and what each is for
    - how forms and inputs send data to the server

**HTML** (HyperText Markup Language) describes the content and structure of a web page. We first met it in [HTML and Templates](../shell/02_html_templates.md).

## Elements, tags and attributes

```html
<a href="/add" class="secondary">Add</a>
```

- `<a href="/add" class="secondary">` → the **opening tag**, with two **attributes**
- `Add` → the content
- `</a>` → the **closing tag**
- the whole thing → an **element**

Some elements, like `<input>` and `<meta>`, have no content and no closing tag.

## Document structure

```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Home | StudyM8</title>
    <link rel="stylesheet" href="style.css">
    <script src="script.js"></script>
</head>
<body>
    <!-- everything we see goes here -->
</body>
</html>
```

| Element | Purpose |
| :-- | :-- |
| `<!doctype html>` | says this is a modern HTML document |
| `<html>` | holds the whole page |
| `<head>` | information about the page that isn't shown on it |
| `<meta>` | settings such as the character set and phone scaling |
| `<title>` | the text on the browser tab |
| `<link>` | connects another file, such as a stylesheet |
| `<script>` | loads JavaScript, such as HTMX or Plotly |
| `<body>` | everything shown on the page |

## Elements StudyM8 uses

| Element | Purpose | First used |
| :-- | :-- | :-- |
| `<h1>`, `<h3>` | headings (`h1` is the most important) | [2. HTML and Templates](../shell/02_html_templates.md) |
| `<p>` | a paragraph | [2. HTML and Templates](../shell/02_html_templates.md) |
| `<a>` | a link; `href` is where it goes | [3. The Page Shell](../shell/03_page_shell.md) |
| `<nav>` | the main navigation links | [3. The Page Shell](../shell/03_page_shell.md) |
| `<main>` | the main content of the page | [3. The Page Shell](../shell/03_page_shell.md) |
| `<header>`, `<footer>` | the top and bottom of the page, or of a card | [4. Styling with Pico](../shell/04_pico.md) |
| `<ul>`, `<li>` | a list and its items | [4. Styling with Pico](../shell/04_pico.md) |
| `<article>` | a self-contained piece of content; Pico draws it as a card | [4. Styling with Pico](../shell/04_pico.md) |
| `<strong>`, `<small>` | bold and small text | [4. Styling with Pico](../shell/04_pico.md) |
| `<div>` | a group of elements with no meaning of its own | [19. Add Page Design](../assessments/19_add_design.md) |
| `<button>` | a button | [10. Register](../users/10_register.md) |

## Forms

```html
<form hx-post="/add" hx-target="#content">
    <label>
        Subject
        <input type="text" name="subject" placeholder="e.g. Maths" required>
    </label>
    <label>
        Details
        <textarea name="details"></textarea>
    </label>
    <button type="submit">Save</button>
</form>
```

| Element or attribute | Purpose |
| :-- | :-- |
| `<form>` | groups inputs and sends them to the server when submitted |
| `<label>` | the text that says what an input is for; an input inside its label is connected to it |
| `<input>` | a single-line input; its `type` decides what kind |
| `<textarea>` | a multi-line text input; its value goes between the tags |
| `name` | the name Flask uses to find the value: `request.form["subject"]` |
| `value` | the value the input starts with |
| `placeholder` | grey hint text shown while the input is empty |
| `required` | the browser won't submit the form while this input is empty |
| `<button type="submit">` | submits the form |
| `<button type="button">` | a button that doesn't submit the form |

### Input types

| Type | Shows | Value sent |
| :-- | :-- | :-- |
| `text` | a text box | what was typed |
| `email` | a text box that checks for an email address | what was typed |
| `password` | a text box that hides what's typed | what was typed |
| `date` | a date picker | the date as `YYYY-MM-DD` |
| `checkbox` | a tick box | sent only when ticked |

!!! warning "Never trust the browser"
    Attributes like `required` and `type="email"` help users, but anyone can remove them. The server must always check the data itself. See [Register](../users/10_register.md#the-register-route).

## Common attributes

| Attribute | Purpose |
| :-- | :-- |
| `id` | a unique name for one element on the page; `#content` in CSS or HTMX finds `id="content"` |
| `class` | one or more style names, shared by many elements; `.error` in CSS finds `class="error"` |
| `aria-current="page"` | marks the link to the current page, for screen readers and our CSS |
| `lang` | the language of the page |

## Documentation

Documentation is the official guide written by the people who made the code library, and we can use it to look up every element and attribute, including ones that aren't covered on this page.

- [MDN HTML reference](https://developer.mozilla.org/en-US/docs/Web/HTML)

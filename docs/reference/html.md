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

## More for your own website

StudyM8 doesn't need the elements below, but most community group websites do.

### Images

```html
<img src="{{ url_for('static', filename='images/team-photo.jpg') }}"
     alt="The under 14s team holding the 2026 premiership trophy"
     width="800" height="450">
```

| Attribute | Purpose |
| :-- | :-- |
| `src` | the image file; keep images in the ***static*** folder and use `url_for` |
| `alt` | a description for people who can't see the image; use `alt=""` for decorative images |
| `width`, `height` | the image's size, so the page doesn't jump around while it loads |

See [Accessibility](accessibility.md#images) for writing good `alt` text, and [Flask](flask.md#file-uploads) for letting admins upload images.

### Tables

Use a table for information with rows and columns, like a training schedule. Don't use tables for page layout.

```html
<table>
    <thead>
        <tr>
            <th scope="col">Day</th>
            <th scope="col">Time</th>
            <th scope="col">Team</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Tuesday</td>
            <td>5:30 pm</td>
            <td>Under 12s</td>
        </tr>
    </tbody>
</table>
```

| Element | Purpose |
| :-- | :-- |
| `<table>` | the whole table |
| `<thead>`, `<tbody>` | the heading rows and the data rows |
| `<tr>` | a table row |
| `<th scope="col">` | a column heading; `scope` tells screen readers which cells it describes |
| `<td>` | a data cell |

In a template, a `{% for %}` loop makes one `<tr>` per row from the database.

### Contact links

```html
<a href="mailto:secretary@example.org">secretary@example.org</a>
<a href="tel:+61730001234">(07) 3000 1234</a>
<a href="https://www.example.org" target="_blank" rel="noopener">Our sponsor</a>
```

| Link | Does |
| :-- | :-- |
| `mailto:` | opens the user's email app with the address filled in |
| `tel:` | phones the number on a mobile; write the number in international form with no spaces |
| `target="_blank"` | opens the link in a new tab; use it for links to other websites, and add `rel="noopener"` for security |

### Embedded maps and videos

An `<iframe>` shows another web page inside ours. Google Maps and YouTube both have a **Share → Embed** option that gives the code to copy.

```html
<iframe src="https://www.google.com/maps/embed?pb=..." width="600" height="450"
        title="Map showing the club's home ground" loading="lazy"></iframe>
```

- `title` → describes the frame for screen readers (required for accessibility)
- `loading="lazy"` → the browser only loads it when it scrolls into view

### More input types

| Input | Shows | Value sent |
| :-- | :-- | :-- |
| `<input type="time">` | a time picker | `HH:MM` in 24-hour time, for example `17:30` |
| `<input type="datetime-local">` | a date and time picker | `YYYY-MM-DDTHH:MM`, for example `2026-03-14T09:00` |
| `<input type="number" min="0" max="50">` | a number box | the number, as text |
| `<input type="url">` | a text box that checks for a web address | what was typed |
| `<input type="tel">` | a text box with a phone keypad on mobiles | what was typed |
| `<input type="search">` | a search box | what was typed |
| `<input type="file" accept="image/*">` | a file chooser | the file (see [Flask file uploads](flask.md#file-uploads)) |

A `<select>` is a drop-down list:

```html
<label>
    Team
    <select name="team">
        <option value="">All teams</option>
        <option value="u12">Under 12s</option>
        <option value="u14" selected>Under 14s</option>
    </select>
</label>
```

The `value` of the chosen `<option>` is sent. `selected` chooses an option when the page loads.

### Page structure

```html
<body>
    <header class="container">...menu...</header>
    <main class="container">
        <section>
            <h2>Upcoming events</h2>
            ...
        </section>
        <section>
            <h2>Latest news</h2>
            ...
        </section>
    </main>
    <footer class="container">
        <p>Bayside Junior Football Club | <a href="/contact">Contact us</a></p>
    </footer>
</body>
```

| Element | Purpose |
| :-- | :-- |
| `<section>` | a themed part of a page, usually with its own heading |
| `<footer>` (outside `<main>`) | the site-wide footer, often with contact details; put it in ***base.html*** so every page has it |
| `<ol>` | a numbered list, for steps in order |
| `<time datetime="2026-03-14T09:00">` | marks a date or time so computers can read it, while showing it any way we like |
| `<blockquote>` | a quote, such as a testimonial from a member |

### Information for search engines

```html
<meta name="description" content="Bayside Junior Football Club: training times, fixtures, news and how to join.">
```

Search engines show this description under the page's title in their results, which helps people who want to join find the group.

## Documentation

Documentation is the official guide written by the people who made the code library, and we can use it to look up every element and attribute, including ones that aren't covered on this page.

- [MDN HTML reference](https://developer.mozilla.org/en-US/docs/Web/HTML)

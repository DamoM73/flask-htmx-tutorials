# Jinja

!!! learn "On this page we will learn"
    - the two kinds of Jinja brackets
    - how to show values, make decisions and repeat HTML in a template
    - how filters, includes and escaping work

**Jinja** is the template language Flask uses to build HTML pages from our data. Flask's `render_template` runs Jinja, then sends the finished HTML to the browser. We first used it in [HTML and Templates](../shell/02_html_templates.md#jinja).

## Brackets

| Brackets | Does | Example |
| :-- | :-- | :-- |
| `{{ }}` | shows a value | `{{ title }}` |
| `{% %}` | does something | `{% if error %}` |

## Sending values

Every keyword argument given to `render_template` becomes a variable in the template:

```python
render_template("partials/account.html", user=current_user)
```

```html+jinja
<p>{{ user.email }}</p>
```

`user.email` works for an object's attribute, a dictionary's key or a database row's column.

## Showing values

| Template | Shows |
| :-- | :-- |
| `{{ title }}` | the value of `title` |
| `{{ user.first_name or "" }}` | the first name, or nothing if it's `None` |
| `{{ assessment.subject }}` | the `subject` column of an assessment row |

A variable that wasn't sent shows nothing. Asking for an attribute of a variable that wasn't sent is an error (see [Common Errors](common_errors.md#values-is-undefined)).

## Decisions

```html+jinja
{% if current_user.is_authenticated %}
<a href="/home">Home</a>
{% else %}
<a href="/login">Login</a>
{% endif %}
```

Jinja needs `{% endif %}` because HTML doesn't use indentation to group things. See [Show the Active Link](../shell/07_active_link.md) and [Account Link Visibility](../users/12_link_visibility.md).

## Loops

```html+jinja
{% for assessment in assessments %}
{% include "partials/assessment_card.html" %}
{% else %}
<p>You have no outstanding assessments.</p>
{% endfor %}
```

The `{% else %}` part runs when the list is empty. See [Home Page Design](../assessments/23_home_design.md).

## Including templates

| Template | Does |
| :-- | :-- |
| `{% include "nav.html" %}` | puts another template here |
| `{% include page %}` | puts the template named in the `page` variable here |
| `{% with oob = True %}...{% endwith %}` | sets a variable for the templates inside |

See [The Page Shell](../shell/03_page_shell.md) and [Show the Active Link](../shell/07_active_link.md).

## Filters

A filter changes a value as it's shown: `{{ value | filter }}`.

| Filter | Does |
| :-- | :-- |
| `au_date` | our own filter: turns `2026-10-12` into `12/10/2026` ([Home Page Code](../assessments/24_home_code.md#use-the-real-data)) |
| `safe` | puts the value in as real HTML instead of escaping it ([Calendar Page](../assessments/27_calendar.md#the-calendar-page)) |

## Escaping

Jinja **escapes** every value: characters like `<` and `>` become `&lt;` and `&gt;`, so they show as text instead of becoming HTML. This stops users typing HTML or JavaScript into a form and having it run on someone else's page (**cross-site scripting**). Only use `| safe` for HTML we trust, like Plotly's chart.

## More for your own website

### Macros: reusable pieces

StudyM8 reuses its card by including ***assessment_card.html***. A **macro** does the same job like a Python function: it takes parameters and returns HTML. It's handy when the same piece appears in several places with different data, like an event card on the Home page and the Events page.

Put macros in their own template, for example ***templates/macros.html***:

```html+jinja
{% macro event_card(event) %}
<article>
    <header><strong>{{ event.title }}</strong></header>
    <p>{{ event.starts_at | au_datetime }}</p>
    <p>{{ event.location }}</p>
</article>
{% endmacro %}
```

Then import and call it in any template:

```html+jinja
{% from "macros.html" import event_card %}

{% for event in events %}
{{ event_card(event) }}
{% endfor %}
```

### The loop variable

Inside a `{% for %}` loop, `loop` tells us where we are:

| Variable | Gives |
| :-- | :-- |
| `loop.index` | the count, starting at 1 |
| `loop.first` | `True` on the first time around |
| `loop.last` | `True` on the last time around |
| `loop.length` | how many items there are |

```html+jinja
{% for event in events %}
{% if loop.first %}<mark>Next up</mark>{% endif %}
{{ event_card(event) }}
{% endfor %}
```

### Setting variables

```html+jinja
{% set attending = event.attending or 0 %}
<p>{{ attending }} going</p>
```

### Built-in filters

| Filter | Shows |
| :-- | :-- |
| `truncate(100)` | the first part of the text, about 100 characters, ending in `...`; good for news previews with a "Read more" link |
| `length` | how many items are in a list |
| `default("TBA")` | the value, or `TBA` if it wasn't sent |
| `title` | Capital Letters For Each Word |
| `upper`, `lower` | upper or lower case |
| `join(", ")` | a list as text, separated by commas |

Use a filter after a `|` symbol:

```html+jinja
<p>{{ news.body | truncate(100) }} <a href="/news/{{ news.id }}">Read more about {{ news.title }}</a></p>
<p>{{ events | length }} upcoming events</p>
<p>Location: {{ event.location | default("TBA") }}</p>
```

### Dates and times

`au_date` from StudyM8 formats dates. Events also need times, stored as `YYYY-MM-DDTHH:MM` (the format of `<input type="datetime-local">`). Add a second filter to ***app.py***, with `from datetime import datetime` at the top:

```python
@app.template_filter("au_datetime")
def au_datetime(iso_text):
    when = datetime.fromisoformat(iso_text)
    hour = when.hour % 12 or 12
    ampm = "am" if when.hour < 12 else "pm"
    return f"{when:%a %d %b}, {hour}:{when:%M} {ampm}"
```

`{{ "2026-03-14T09:00" | au_datetime }}` shows **Sat 14 Mar, 9:00 am**.

| Code inside `{when:...}` | Shows |
| :-- | :-- |
| `%a` / `%A` | `Sat` / `Saturday` |
| `%d` | day of the month, `14` |
| `%b` / `%B` | `Mar` / `March` |
| `%Y` | `2026` |
| `%M` | minutes, `00` |

### Images and links

Always build addresses with `url_for`, so they keep working if the site moves:

```html+jinja
<img src="{{ url_for('static', filename='uploads/' + news.image) }}" alt="{{ news.image_alt }}">
<a href="{{ url_for('event_detail', event_id=event.id) }}">More details</a>
```

`url_for('event_detail', event_id=event.id)` builds the address of the `event_detail` view function, such as `/events/7`.

### Keeping line breaks

Text typed into a `<textarea>` keeps its line breaks in the database, but HTML ignores them, so a news post shows as one long paragraph. Rather than using `| safe` (which is unsafe for text users type), add a CSS rule:

```css
.keep-lines {
    white-space: pre-line;
}
```

```html+jinja
<p class="keep-lines">{{ news.body }}</p>
```

### Extending templates

StudyM8 uses `{% include page %}` because HTMX needs partials. Many Flask websites use **template inheritance** instead, which is simpler if a site doesn't use HTMX:

```html+jinja
{# base.html #}
<main>{% block content %}{% endblock %}</main>
```

```html+jinja
{# news.html #}
{% extends "base.html" %}
{% block content %}
<h1>News</h1>
{% endblock %}
```

`{# ... #}` is a Jinja comment, which never appears in the HTML.

## Documentation

Documentation is the official guide written by the people who made the code library, and we can use it to look up every tag and filter, including ones that aren't covered on this page.

- [Jinja template designer documentation](https://jinja.palletsprojects.com/en/stable/templates/)

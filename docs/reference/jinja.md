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

## Documentation

Documentation is the official guide written by the people who made the code library, and we can use it to look up every tag and filter, including ones that aren't covered on this page.

- [Jinja template designer documentation](https://jinja.palletsprojects.com/en/stable/templates/)

# Pico CSS

!!! learn "On this page we will learn"
    - how Pico styles plain HTML elements
    - which Pico classes and layouts StudyM8 uses
    - how our own stylesheet changes Pico

**Pico CSS** is a ready-made stylesheet that styles semantic HTML elements, so a page looks good with very little CSS of our own. We added it in [Styling with Pico](../shell/04_pico.md).

## Load it

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">
```

Pico follows the computer's light or dark mode automatically.

## What Pico does with our HTML

| HTML | Pico shows |
| :-- | :-- |
| `<nav>` with two `<ul>` lists | a menu bar: the first list on the left, the second on the right |
| `<article>` | a card, with a shaded `<header>` and `<footer>` if it has them |
| `<label>` with an `<input>` inside | a full-width labelled input |
| `<button>` | a coloured button |
| `<input type="checkbox">` | a styled tick box |

## Classes StudyM8 uses

| Class | Used on | Does |
| :-- | :-- | :-- |
| `container` | `<header>`, `<main>` | keeps content centred with space on each side |
| `grid` | `<div>` | puts each element inside it side by side in equal columns, and stacks them on narrow screens |
| `secondary` | `<button>` | a grey button, for less important actions like Edit and Cancel |

## Our own styles

Our ***static/style.css*** loads after Pico, so its rules win:

| Rule | Does | Added in |
| :-- | :-- | :-- |
| `nav a[aria-current="page"]` | bold, underlined active link | [7. Show the Active Link](../shell/07_active_link.md) |
| `.error`, `.success` | red and green messages, using Pico's colour variables | [10. Register](../users/10_register.md#show-the-messages) |
| `.card-footer` | lays out the card footer in a row with flexbox | [25. Complete Assessments](../assessments/25_complete.md#tidy-the-card-footer) |

!!! tip "Pico's colour variables"
    `var(--pico-del-color)` and `var(--pico-ins-color)` are colours Pico defines, for deleted and inserted text. Using Pico's variables means our colours change with light and dark mode too.

## Documentation

Documentation is the official guide written by the people who made the code library, and we can use it to look up every element and class, including ones that aren't covered on this page.

- [Pico CSS documentation](https://picocss.com/docs)

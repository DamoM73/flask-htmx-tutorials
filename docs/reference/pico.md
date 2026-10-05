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

## More for your own website

### Changing the colours

The easiest way to give a site the group's colours is to load one of Pico's colour themes instead of the default (azure) stylesheet. Change the end of the address to the colour's name:

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.green.min.css">
```

The colours are amber, azure, blue, cyan, fuchsia, green, grey, indigo, jade, lime, orange, pink, pumpkin, purple, red, sand, slate, violet, yellow and zinc.

To use an exact colour, set Pico's variables in ***static/style.css***. Pico sets them separately for light and dark mode, so we set both:

```css
[data-theme=light],
:root:not([data-theme=dark]) {
    --pico-primary: #1b5e20;
    --pico-primary-background: #1b5e20;
    --pico-primary-hover: #2e7d32;
    --pico-primary-hover-background: #2e7d32;
}

@media (prefers-color-scheme: dark) {
    :root:not([data-theme]) {
        --pico-primary: #81c784;
        --pico-primary-background: #2e7d32;
    }
}
```

!!! warning "Check the contrast"
    Text must stand out from its background. Check every colour pair with a contrast checker before using it. See [Accessibility](accessibility.md#colour-and-contrast).

### Menus with lots of links

StudyM8's menu has five links. A community site might have more, which won't fit on a phone. Group related pages in a **dropdown**:

```html
<nav>
    <ul>
        <li><a href="/"><strong>Bayside JFC</strong></a></li>
    </ul>
    <ul>
        <li><a href="/news">News</a></li>
        <li><a href="/events">Events</a></li>
        <li>
            <details class="dropdown">
                <summary>Teams</summary>
                <ul dir="rtl">
                    <li><a href="/teams/u12">Under 12s</a></li>
                    <li><a href="/teams/u14">Under 14s</a></li>
                </ul>
            </details>
        </li>
    </ul>
</nav>
```

- `<details class="dropdown">` → a menu item that opens a list when clicked
- `<summary>` → the text shown on the menu
- `dir="rtl"` → lines the list up with the right-hand edge, so it doesn't run off the screen

Pico doesn't make a "hamburger" menu for phones. Keep the menu short (about five items), use dropdowns, and test it on a narrow screen.

### Tables on small screens

Pico styles tables automatically. Wrap a wide table in `overflow-auto` so it scrolls sideways on phones instead of squashing:

```html
<div class="overflow-auto">
    <table>...</table>
</div>
```

Add `class="striped"` to a `<table>` to shade every second row, which makes long schedules easier to read.

### Accordions

A `<details>` element (without the `dropdown` class) is an **accordion**: a heading that opens to show more. It's good for FAQs and long information.

```html
<details>
    <summary>What do new players need to bring?</summary>
    <p>Boots, shin pads, a water bottle and a hat.</p>
</details>
```

Add `open` to `<details>` to start it open. Add the same `name` to several `<details>` to make only one open at a time.

### Modals

A `<dialog>` shows content on top of the page.

```html
<button onclick="document.getElementById('join-info').showModal()">How to join</button>

<dialog id="join-info">
    <article>
        <header>
            <button aria-label="Close" rel="prev"
                    onclick="this.closest('dialog').close()"></button>
            <p><strong>How to join</strong></p>
        </header>
        <p>Fill in the registration form and pay the season fee.</p>
    </article>
</dialog>
```

The two `onclick` attributes are tiny pieces of JavaScript that open and close the dialog. Pico turns the `rel="prev"` button into a close (×) button.

### Buttons and groups

| Code | Shows |
| :-- | :-- |
| `<button>` | the main (primary) colour |
| `<button class="secondary">` | grey, for less important actions |
| `<button class="contrast">` | black or white, for strong emphasis |
| `<button class="outline">` | an outline only; combine with others, for example `class="secondary outline"` |
| `<a href="/join" role="button">` | a link that looks like a button, for calls to action |
| `<div role="group">` | joins buttons or an input and a button into one bar |
| `<button aria-busy="true">` | shows a loading spinner |

### Other layout tools

| Code | Does |
| :-- | :-- |
| `class="container-fluid"` | full-width content instead of centred |
| `<hgroup>` | a heading with a subtitle underneath, in a lighter colour |
| `<mark>` | highlighted text, for example "Cancelled" |
| `<input aria-invalid="true">` | a red border, for an input with an error |
| `<progress>` | a progress bar |

## Documentation

Documentation is the official guide written by the people who made the code library, and we can use it to look up every element and class, including ones that aren't covered on this page.

- [Pico CSS documentation](https://picocss.com/docs)

# Accessibility

!!! learn "On this page we will learn"
    - what web accessibility is and why it matters
    - the four principles of accessible websites
    - a checklist for making our pages accessible
    - how to test a website's accessibility

**Accessibility** means designing websites that everyone can use, including people with disabilities. About one in five Australians has a disability. Some people:

- are blind or have low vision, and use a **screen reader** that reads the page aloud, or zoom in a long way
- are colour-blind
- are Deaf or hard of hearing, and need captions on videos
- can't use a mouse, and use only a keyboard or a switch
- have a learning disability or find long, complicated text hard to read

Accessible design helps everyone else too: captions help in noisy places, good contrast helps in bright sunlight, and clear wording helps people in a hurry.

!!! tip "It's the law"
    In Australia, the **Disability Discrimination Act 1992** makes it unlawful to discriminate against people with disabilities, including through websites. The standard websites are measured against is the **Web Content Accessibility Guidelines (WCAG) 2.2**, level AA.

## The four principles

WCAG is organised around four principles, often remembered as **POUR**:

| Principle | Means | Example |
| :-- | :-- | :-- |
| **Perceivable** | everyone can see or hear the content in some way | images have text descriptions; videos have captions |
| **Operable** | everyone can use the controls | everything works with a keyboard |
| **Understandable** | the content and controls make sense | clear labels and error messages |
| **Robust** | it works with different browsers and assistive technology | correct, semantic HTML |

## Checklist

### Structure

- set the page language: `<html lang="en">`
- use one `<h1>` per page, then `<h2>`, `<h3>` in order, without skipping levels; screen reader users jump between headings
- use semantic elements (`<header>`, `<nav>`, `<main>`, `<footer>`, `<section>`, `<article>`) so assistive technology can find each part
- give every page a unique, descriptive `<title>`
- use real `<button>` elements for actions and `<a>` elements for links to other pages, not clickable `<div>` elements

### Images

Every `<img>` needs an `alt` attribute:

| Image | Good alt text |
| :-- | :-- |
| a photo with information | describe what matters: `alt="Under 12s team celebrating with the 2026 premiership cup"` |
| a logo that links home | the destination: `alt="Bayside JFC home"` |
| decoration only | empty, so screen readers skip it: `alt=""` |
| a poster or flyer with text | the important text from the image, or put the text on the page instead |

Don't start alt text with "image of"; screen readers already say it's an image.

### Colour and contrast

- normal text needs a contrast ratio of at least **4.5:1** with its background
- large text (about 24 pixels, or 19 pixels bold) and parts of controls, like input borders, need at least **3:1**
- check colours with a contrast checker such as [WebAIM's](https://webaim.org/resources/contrastchecker/)
- never use colour alone to show meaning; add text or an icon ("**Cancelled**", not just a red card)

Pico's default colours meet these ratios. Check again after changing them.

### Links and buttons

- link text should make sense on its own: "See the training schedule", not "click here" or "read more"
- if several links say "Read more", add which post they're for, or use the post's title as the link
- buttons say what they do: "Save event", "Delete event"
- make tap targets big enough for fingers (Pico's buttons are)

### Forms

- every input needs a `<label>` (put the input inside it, as StudyM8 does)
- don't use a placeholder instead of a label; it disappears when the user types
- show error messages in words, next to the problem, and keep what the user typed
- mark inputs with errors with `aria-invalid="true"` (Pico shows a red border)
- use the right input `type` (`email`, `tel`, `date`) so phones show the right keyboard

### Keyboard

Many people use only a keyboard. Try using the site with only:

- ++tab++ and ++shift+tab++ → move between links, buttons and inputs
- ++enter++ → follow a link or press a button
- ++space++ → tick a checkbox or press a button
- arrow keys → choose from a `<select>` or a group of options

Check that:

- every link, button and input can be reached, in a sensible order
- you can always see which element has **focus** (Pico shows an outline)
- dropdowns and dialogs can be opened and closed with the keyboard

### Tables

- use `<th scope="col">` for column headings and `<th scope="row">` for row headings
- only use tables for data, never for layout

### Media and embedded content

- give videos captions, and audio a transcript
- give every `<iframe>` a `title`: `title="Map showing the club's home ground"`
- don't autoplay sound or video

### Zoom and screen size

- include `<meta name="viewport" content="width=device-width, initial-scale=1">` so the page fits phones
- the page should still work when zoomed to 200% (++ctrl+plus++), with nothing cut off or overlapping

### Language

- use plain English and short sentences
- explain abbreviations the first time ("Under 12s (U12)")
- keep the layout and menu the same on every page

## Testing accessibility

Use more than one method. Automatic checkers only find some problems; testing by hand finds the rest.

1. **Keyboard test** → put the mouse away and complete each main task with the keyboard only.
    - **Expected result:** every task can be finished, and the focus is always visible.
2. **Lighthouse** → in Chrome, press ++f12++, open the **Lighthouse** tab, tick **Accessibility** and click **Analyze page load**.
    - **Expected result:** a score out of 100 and a list of problems, each with an explanation and the element at fault.
3. **WAVE** → install the [WAVE browser extension](https://wave.webaim.org/extension/) and run it on each page.
    - **Expected result:** icons on the page marking errors (red), contrast errors and warnings.
4. **Contrast checker** → check each text and background colour pair.
    - **Expected result:** at least 4.5:1 for normal text.
5. **Screen reader** → on Windows, turn on **Narrator** with ++win+ctrl+enter++ (the same keys turn it off), then try to use the site.
    - **Expected result:** headings, links, images and form inputs are all announced in a way that makes sense.
6. **Zoom** → zoom to 200% and use each page.
    - **Expected result:** nothing is cut off and no content overlaps.

Record each check in the test plan (see [Test Plans](test_plans.md#kinds-of-testing)).

## What Pico and StudyM8 already do

| Feature | Helps |
| :-- | :-- |
| semantic HTML (`<nav>`, `<main>`, `<article>`) | screen readers find each part |
| inputs inside `<label>` elements | screen readers announce what each input is for |
| `aria-current="page"` on the active link | screen readers announce the current page |
| Pico's default colours and focus outlines | contrast and keyboard users |
| viewport meta tag and Pico's responsive layout | phones and zoom |
| error messages in words, keeping what was typed | everyone, especially users with cognitive disabilities |

## Further reading

- [Australian Human Rights Commission: World Wide Web Access advisory notes](https://humanrights.gov.au/resource-hub/by-resource-type/articles/disability-rights/disability-rights-and-the-disability-discrimination-act/world-wide-web-access-disability-discrimination-act-advisory-notes-ver)
- [WCAG 2 at a glance](https://www.w3.org/WAI/standards-guidelines/wcag/glance/)
- [WebAIM: introduction to web accessibility](https://webaim.org/intro/)

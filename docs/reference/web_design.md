# Web Design Principles

!!! learn "On this page we will learn"
    - how to plan a website around its users and their needs
    - the design principles that make a website clear and easy to use
    - how to plan pages with site maps and wireframes
    - how to explain our design decisions

Good web design isn't about decoration. It's about making it easy for people to find what they need and do what they came to do. These principles apply to any website, whatever it's built with. Each section shows how to apply the principle with HTML and [Pico CSS](pico.md).

## Start with the users

Before designing anything, work out:

1. **Who** will use the site → for a community group: current members, parents, new people who want to join, organisers who post updates.
2. **What** each of them needs to do → find the next training time, check if a game is cancelled, see how to join, post news.
3. **Where** they'll use it → mostly on phones, often in a hurry.

Put the information people need most at the top of the page and in the menu. A parent checking whether training is on shouldn't have to scroll past the club's history.

!!! tip "Requirements first"
    Each design decision should help meet a requirement. If a feature doesn't meet any requirement, ask whether it's needed. See [Test Plans](test_plans.md#requirements-and-success-criteria) for writing requirements.

## The principles

### Visual hierarchy

The most important things should stand out the most. Readers notice size, colour, weight and position first.

- one `<h1>` per page, then `<h2>` and `<h3>` for sections, in order
- put the most important content near the top
- make the main action (for example **Join the club**) a bright button and less important actions grey (`class="secondary"`)

### Consistency

The same things should look and work the same way on every page:

- the menu and footer are in the same place on every page (put them in ***base.html***)
- every event card has the same layout (use one template or [macro](jinja.md#macros-reusable-pieces))
- buttons that do the same kind of thing have the same style and wording

Users learn how the site works once, then it's quick everywhere.

### Contrast

Things that are different should look clearly different, and text must stand out from its background. Low-contrast text (light grey on white) is hard to read, especially on a phone outside. See [Accessibility](accessibility.md#colour-and-contrast) for the ratios to aim for.

### Alignment

Line elements up with each other. Things that are almost lined up look messy. Pico's `container` and `grid` line content up for us; avoid pushing individual elements around with extra spacing.

### Proximity

Put related things close together and unrelated things further apart. An event's date, time and place belong together in one card, with space between cards. Pico's `<article>` cards do this.

### Repetition

Repeat colours, fonts and layouts across the site so it feels like one website. Use the group's two or three colours everywhere (see [changing Pico's colours](pico.md#changing-the-colours)) rather than a different colour on each page.

### White space

Empty space isn't wasted space. Space around text and between sections makes a page easier to scan and helps the important parts stand out. Resist filling every gap.

### Simplicity

Every extra thing on a page competes for attention. Remove anything that doesn't help the user. Fewer menu items, shorter paragraphs and one clear action per section work better than lots of choices.

## Typography

- use one or two fonts at most; Pico's default font is designed to be easy to read on screens
- keep body text at least 16 pixels (Pico's default)
- keep lines of text to about 50–75 characters wide; Pico's `container` does this on large screens
- use headings to break up long text, so readers can scan for what they need
- left-align body text; centred text is hard to read in long paragraphs

## Colour

- choose a small palette: one main colour (often the group's colour), one accent and neutrals (white, greys, black)
- a common guide is **60-30-10**: about 60% neutral background, 30% secondary colour, 10% accent for buttons and highlights
- colours carry meaning: red for errors and cancellations, green for success
- never use colour as the **only** way to show something; add words or icons too (for example "**Cancelled**" as well as red)

## Navigation

- keep the main menu to about five to seven items, with short, clear labels ("Events", not "What's Happening")
- show which page the user is on (StudyM8 uses `aria-current="page"`)
- make the logo or group name link back to the home page
- group extra pages in a [dropdown](pico.md#menus-with-lots-of-links), or link to them from the footer
- every page should be reachable within two or three clicks of the home page

## Layout and scanning

People don't read web pages word by word. They **scan**, usually across the top, then down the left side (an **F-pattern**). So:

- put key information (next event, latest news, how to join) near the top
- start headings and links with the important words
- use cards, lists and short paragraphs rather than long blocks of text
- use a table for schedules (see [HTML tables](html.md#tables))

## Mobile first

Most members will visit on a phone. Design for a narrow screen first, then check it works on a wide one:

- one column of content; Pico's `grid` stacks columns on phones automatically
- buttons and links big enough to tap with a thumb
- wide tables in `overflow-auto` so they scroll (see [Pico tables](pico.md#tables-on-small-screens))
- test with the browser's device toolbar (++f12++, then the phone and tablet icon)

## Calls to action

A **call to action** is a button or link that asks the user to do the thing we most want, like **Join the club** or **RSVP**. Make it:

- a button, not a plain link (`role="button"` on a link)
- short, active wording that says what happens
- easy to find, in the same place on each page where it's needed

## Content and feedback

- write in plain English, with short sentences; avoid jargon only members would understand
- give dates and times in full, with the day: "Sat 14 Mar, 9:00 am"
- tell users what happened after every action: "Event saved", "Message sent"
- explain errors in words, next to the input that's wrong

## Planning layouts

### Site maps

A **site map** shows every page and how they link together. See the [StudyM8 site map](../start/design.md#site-map) for an example. Draw it before the wireframes, so we know which pages to design.

### Wireframes

A **wireframe** is a simple sketch of a page's layout: boxes and labels showing where each thing goes, without colours, images or real text. Wireframes let us try and compare layouts quickly, before writing any code.

A wireframe should show:

- the menu, footer and any other parts that are on every page
- the position and order of each section (headings, cards, forms, tables, images)
- labels for buttons and inputs
- notes (**annotations**) explaining what each part does and why it's there

Draw at least one wireframe for each type of page, and draw both a phone layout and a wide-screen layout for the home page. Draw two or three different designs for the key pages, then choose the best one and explain why.

Wireframes can be drawn on paper or with tools such as draw.io, PowerPoint or Figma.

## Explaining design decisions

When annotating wireframes or the finished site, link each decision to a principle and a user need:

| Element | Principle | Reason |
| :-- | :-- | :-- |
| "Next event" card at the top of the home page | visual hierarchy, layout and scanning | members mostly visit to check the next training or game |
| same menu and footer on every page | consistency | members learn where things are once |
| **Join the club** button in the group's colour | call to action, contrast | new families need to find how to join quickly |
| schedule shown as a table | layout and scanning | days, times and teams are easiest to compare in columns |
| "Cancelled" in words and red | colour, accessibility | colour alone isn't enough for colour-blind users |

## Further reading

- [Laws of UX](https://lawsofux.com/)
- [Nielsen Norman Group: F-shaped reading pattern](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/)

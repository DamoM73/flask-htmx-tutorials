# Tasks for Claude in VS Code

This site was started in Cowork, which can only create and overwrite files in this folder. It can't delete files, run git or access GitHub. Work on `main`. Check with Damien before each task marked **Confirm first**, and report the output of the checks after each task.

## Context

- **Site generator:** Zensical 0.0.67 (pinned in `requirements.txt`). Config is `zensical.toml`. Pages are in `docs/`.
- **Preview:** `zensical serve`. **Build:** `zensical build --clean` (must report "No issues found").
- **Audience:** Year 10 Digital Technologies students (Year 9/10 writing level) using VS Code on Windows school laptops. Students know Python functions and OOP, but no HTML, CSS or SQL; those are taught just in time, with summaries in the Reference section.
- **The app:** StudyM8, a study planner, rebuilt from the Anvil tutorials (<https://damom73.github.io/anvil-python-tutorials/>). Stack: Flask 3.1, sqlite3 with raw SQL (no ORM), Flask-Login with werkzeug password hashing, Pico CSS 2 (CDN), HTMX 2.0.11 (CDN), Plotly `px.timeline` (needs pandas) rendered server-side with Plotly.js 4.1.1 loaded in `base.html`. The finished app is in `studym8_reference/`; the lessons build towards it.
- **HTMX pattern:** `base.html` is the page shell (nav + `<main id="content">` with `{% include page %}`). `render_page(template, title, ...)` in `app.py` returns `fragment.html` (a `<title>`, the nav as an out-of-band swap, then the partial) when the request has an `HX-Request` header, and the full `base.html` otherwise. It sets `Vary: HX-Request`; `base.html` sets `htmx-config` `refreshOnHistoryMiss`. The active link uses `aria-current="page"`, chosen by comparing `title`.
- **Structure:** Home; Start (`docs/start/`: introduction, how_websites_work, design, setup); Page Shell (`docs/shell/01`–`07`); Users (`docs/users/08`–`12`); Account (`docs/account/13`–`17`); Assessments (`docs/assessments/18`–`28`); Optimisation (`docs/optimisation/29`–`32`); Reference (`docs/reference/`). Lessons 8–32 and most Reference pages are placeholders still to be written.
- **Examples:** every version of a file shown on a page is a snippet file at `docs/examples/<section>/<lesson>/stepNN/<path>`, where a step folder holds only the files that changed in that step, at their path in the app (for example `docs/examples/shell/05_htmx_links/step01/templates/base.html`). Pages include them with `--8<-- "examples/..."` inside ```` ```python linenums="1" hl_lines="..." title="app.py" ```` (HTML templates use `html+jinja`); `hl_lines` marks new or changed lines and `title` shows the file's path in the app.
- **Checkpoint zip:** `python scripts/make_zip.py` builds `docs/downloads/studym8_checkpoints.zip`. Each `studym8/<section>/<lesson>/` folder holds every file at the end of that lesson, carried forward in `CHECKPOINTS` order; `REMOVED` lists files a lesson tells students to delete. Add each new lesson to `CHECKPOINTS`.
- **Checks:**
    - `python scripts/check_explanations.py` → `0 issue(s) found`. When a code block has `hl_lines`, only highlighted lines need explaining.
    - `python scripts/test_checkpoints.py` → `0 checkpoint(s) failed`. Extend its `ROUTES` and test as lessons add login and the database.
- **Colour scheme:** crimson `#A4262C` (header, tabs, light-mode links and headings; 7.3:1 with white), crimson light `#C75B5F` (decorative only), rose `#F6D5D7` (active and hovered tab, dark-mode headings and accent), light blue `#8AB4F8` (dark-mode links). Set in `docs/stylesheets/extra.css`. Clearly different from the micro:bit (navy), Lego Spike (magenta), Turtle (teal), Deepest Dungeon (burnt orange) and Space Rescue (charcoal slate) banners.
- **Callouts:** five types, the same on all of Damien's tutorial sites: `!!! learn` (amber, directly under the title; "In this lesson we will learn" on lessons, "On this page we will learn" elsewhere), `!!! primm "PRIMM"` (green, after each change students run), `??? note "Code explanation"` (purple, collapsed, after each snippet), `!!! tip "Title"` (light blue) and `!!! warning "Title"` (hot pink). There are no videos.
- **Writing style:** Australian English, Year 9/10, Damien's inclusive "we" voice. Instructions follow "Open ***templates/base.html***, change the highlighted code below and save it." / "Create a new file, add the code below and save it as ***x*** in the ***y*** folder." Code explanations are `- **line n** → full sentence ending in a full stop.`; ranges use an en dash. Lessons use `## Introduction`, an optional `## Planning` (IPO table or numbered reasoning), then coding sections. No Exercises or Commit and push sections; PRIMM **Modify** prompts take their place. Error messages are real (made by breaking the code), with Windows-style paths, in ```` ``` { .text .error linenums="1" } ```` blocks followed by a line-by-line breakdown.
- **Plan:** the unit plan is in Damien's Claude project as `claude/Flask HTMX StudyM8 unit plan.md`, with progress in `claude/flask-htmx-tutorials_progress.md`.

## 1. Check the deploy workflow

`.github/workflows/deploy.yml` builds the zip and the site with Zensical and deploys with GitHub Pages Actions on pushes to `main`. If it isn't in the repo (Cowork may not be able to write inside `.github/`), create it from Space Rescue's `deploy.yml`. Confirm each action version exists on GitHub before committing.

## 2. Turn on GitHub Pages — Confirm first

Set Pages to deploy from GitHub Actions: **Settings** → **Pages** → **Source** → **GitHub Actions**, or `gh api -X POST repos/DamoM73/flask-htmx-tutorials/pages -f build_type=workflow`. Watch the **Deploy site** run, then check <https://damom73.github.io/flask-htmx-tutorials/>.

## 3. Final checks

1. `python scripts/make_zip.py`
2. `python scripts/check_explanations.py` → `0 issue(s) found`
3. `python scripts/test_checkpoints.py` → `0 checkpoint(s) failed`
4. `zensical build --clean` → `No issues found`
5. Check external links (python.org, code.visualstudio.com, picocss.com, htmx.org, Flask docs, Creative Commons). Report broken ones rather than guessing replacements.

## Tasks for Damien (not for Claude)

These are also in `todo.md`, which Damien keeps up to date. Don't delete or edit it unless he asks.

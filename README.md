# StudyM8 with Flask and HTMX

Tutorials for building StudyM8, a study planner web app, in Python with [Flask](https://flask.palletsprojects.com/), [HTMX](https://htmx.org/), SQLite, [Pico CSS](https://picocss.com/) and [Plotly](https://plotly.com/python/). Written for Year 9/10 Digital Technologies students using VS Code. A Flask/HTMX rebuild of the [Anvil StudyM8 tutorials](https://damom73.github.io/anvil-python-tutorials/).

Live site: <https://damom73.github.io/flask-htmx-tutorials/>

## Preview the site

```
pip install -r requirements.txt
zensical serve
```

Then open <http://localhost:8000>. To build the site: `zensical build --clean` (expect `No issues found`).

## Scripts

- `python scripts/make_zip.py` builds `docs/downloads/studym8_checkpoints.zip`: StudyM8's code at the end of every lesson.
- `python scripts/check_explanations.py` checks every Code explanation box against the code it explains (expect `0 issue(s) found`).
- `python scripts/test_checkpoints.py` loads every checkpoint with Flask's test client and requests each page as a normal request and as an HTMX request (needs Flask; later lessons also need Flask-Login, Plotly and pandas).

## Layout

```
zensical.toml                 site config and navigation
docs/
  index.md                    home page
  start/                      introduction, how websites work, design, setup
  shell/                      lessons 1–7: Flask, templates, Pico, HTMX page shell
  users/                      lessons 8–12: SQLite, register, login
  account/                    lessons 13–17: account and set details pages
  assessments/                lessons 18–28: add, home, complete, edit, calendar, welcome
  optimisation/               lessons 29–32
  reference/                  HTML, Pico, Jinja, HTMX, SQL, Flask, errors, finished app, licence
  examples/<section>/<lesson>/stepNN/<path>
                              every version of every file shown on a page
  assets/                     images
  stylesheets/extra.css       colours, callouts and code block styles
  downloads/                  the checkpoint zip
scripts/                      make_zip.py, check_explanations.py, test_checkpoints.py
studym8_reference/            the finished app the lessons build towards (not part of the site)
```

A `stepNN` folder holds only the files that changed in that step, at their path in the app (for example `step02/templates/base.html`). Pages include them with `--8<-- "examples/..."`, show the path as the code block's `title` and mark new or changed lines with `hl_lines`.

## Run the finished app

```
cd studym8_reference
pip install -r requirements.txt
flask init-db
flask run --debug
```

## Licence

Content is licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Code is licensed under [GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html).

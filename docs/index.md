# StudyM8 with Flask and HTMX

![StudyM8](assets/logo.png){ width="160" }

Build StudyM8, a study planner web app, in Python with Flask, HTMX, SQLite and Pico CSS.

## How to use this site

- Work through the **Start** pages first. They explain how websites work, show the StudyM8 design and set up Python and VS Code.
- The lessons in **Page Shell**, **Users**, **Account**, **Assessments** and **Optimisation** build StudyM8 one feature at a time. Each lesson continues from the one before, so do them in order.
- **Reference** has a summary of each tool (HTML, Pico CSS, Jinja, HTMX, SQL and Flask), common errors and the finished app.

## Callouts

Coloured boxes called **callouts** highlight different kinds of information. Each type of callout has its own colour and icon, so we can tell at a glance what it's for.

!!! learn "Learning intentions"
    This callout is at the top of every lesson page. It lists what we will learn on that page.

!!! primm "PRIMM"
    This callout comes after we change our app. It asks us to **predict** what the code will do, **run** it, and **investigate** how it works. Sometimes it asks us to **modify** the code.

!!! note "Code explanation"
    This callout comes after each piece of code and explains the new or changed lines, line by line. On the lesson pages it starts closed, so we can make our own prediction first. Click its title to open it.

!!! tip "Tip"
    This callout gives extra information, such as definitions, background facts, comparisons and hints.

!!! warning "Warning"
    This callout warns us about mistakes that are easy to make, or things that will stop our website working.

## Code blocks

We build one app across all the lessons, so the code is spread over lots of files. Each code block shows which file it belongs to:

```python linenums="1" hl_lines="1 8" title="app.py"
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")
```

- the **file name** above the code tells us which file to open, from the ***studym8*** folder (for example ***templates/base.html*** is ***base.html*** in the ***templates*** folder)
- **line numbers** match the line numbers in VS Code and in the Code explanation
- **highlighted lines** are new or changed since the last time we saw the file, so they're the lines we need to add or change
- the **copy** button in the top-right corner copies the code to paste into VS Code

Code blocks without colours show commands to type in the terminal, or what appears in the terminal.

## Error messages

Error messages are shown in red code blocks like this one:

``` { .text .error linenums="1" }
Traceback (most recent call last):
  File "C:\Users\student\Documents\studym8\app.py", line 8, in index
    return render_template("index.html")
jinja2.exceptions.TemplateNotFound: index.html
```

Under each error message, the lesson breaks it down line by line, so we learn how to read the error and fix our code. The [Common Errors](reference/common_errors.md) page collects the errors we're most likely to see.

## Tutorial files

If your app stops working and you can't find the problem, you can start again from the end of any lesson. [Download the checkpoints](downloads/studym8_checkpoints.zip) and unzip them. There's a folder for each lesson, holding all of StudyM8's files as they are at the end of that lesson.

To use a checkpoint, copy the files from the lesson's folder into your ***studym8*** folder, replacing the files that are already there. Don't copy over your ***.venv*** folder.

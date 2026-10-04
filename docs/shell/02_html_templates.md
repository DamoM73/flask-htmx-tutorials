# 2. HTML and Templates

!!! learn "In this lesson we will learn"
    - how an HTML document is structured
    - how to keep our HTML in template files
    - how to send a template with `render_template`
    - how to put Python values into a template with Jinja

## Introduction

Writing HTML inside a Python string works for one line, but real pages have hundreds of lines of HTML. Mixing that much HTML into our Python would be very hard to read.

So instead we keep our HTML in separate files called **templates**. Flask looks for templates in a folder called ***templates***, and sends them to the browser when we ask.

## HTML documents

A full HTML page is called an **HTML document**. Every HTML document has the same basic structure.

In VS Code, create a new folder called ***templates*** inside the ***studym8*** folder. Then create a new file, add the code below and save it as ***index.html*** in the ***templates*** folder.

```html+jinja linenums="1" title="templates/index.html"
--8<-- "examples/shell/02_html_templates/step01/templates/index.html"
```

??? note "Code explanation"
    - **line 1** → tells the browser this is a modern HTML document.
    - **line 2** → opens the `<html>` element, which holds the whole page. `lang="en"` is an **attribute** that says the page is in English.
    - **line 3** → opens the `<head>`, which holds information about the page that isn't shown on the page itself.
    - **line 4** → says which character set the page uses, so symbols and emoji display correctly.
    - **line 5** → sets the page title, which shows on the browser tab.
    - **line 6** → closes the `<head>`.
    - **line 7** → opens the `<body>`, which holds everything we see on the page.
    - **lines 8–9** → a main heading and a paragraph.
    - **line 10** → closes the `<body>`.
    - **line 11** → closes the `<html>` element, ending the document.

!!! tip "Elements, tags and attributes"
    An **element** is a part of the page, made from an opening tag, some content and a closing tag:

    - `<p>Your study planner</p>` → a paragraph element
    - `<p>` → the opening tag
    - `</p>` → the closing tag
    - `lang="en"` → an **attribute**, which gives extra information about an element. Attributes go inside the opening tag.

    Elements can go inside other elements. We indent the inner elements so we can see the structure, just like indenting code inside a Python function.

## Render the template

Now we need Flask to send ***index.html*** instead of our HTML string.

Go back to ***app.py*** and change the highlighted code below.

```python linenums="1" hl_lines="1 8" title="app.py"
--8<-- "examples/shell/02_html_templates/step02/app.py"
```

??? note "Code explanation"
    - **line 1** → also imports `render_template`, the Flask function that loads a template.
    - **line 8** → finds ***index.html*** in the ***templates*** folder and returns it as the response.

!!! primm "PRIMM"
    1. **Predict** what the page will look like now. What will the browser tab say?
    2. **Run** the code by refreshing the browser.
    3. Time to **investigate**. Compare the page source with ***index.html***. Are they the same?

!!! warning "TemplateNotFound"
    If the ***templates*** folder is spelt differently (for example ***template***), Flask can't find our template. The browser shows an error page, and the terminal shows a long error message. Here are the important lines:

    ``` { .text .error linenums="1" }
    Traceback (most recent call last):
      File "C:\Users\student\Documents\studym8\app.py", line 8, in index
        return render_template("index.html")
    jinja2.exceptions.TemplateNotFound: index.html
    ```

    - **line 1** → the start of the error report. The lines that follow show which code was running when the error happened.
    - **line 2** → the error happened on line 8 of our ***app.py***, inside the `index` function.
    - **line 3** → the line of code that caused the error.
    - **line 4** → the type of error, `TemplateNotFound`, and the template Flask couldn't find.

    To fix it, check the folder is called ***templates*** (all lower case, with an s) and that it's inside the ***studym8*** folder, next to ***app.py***.

## Jinja

Templates aren't just plain HTML. Flask uses a template language called **Jinja**, which lets us put Python values into our HTML. Anything between double curly brackets `{{ }}` is replaced with a value when the page is built.

Go back to ***app.py*** and change the highlighted code below.

```python linenums="1" hl_lines="8" title="app.py"
--8<-- "examples/shell/02_html_templates/step03/app.py"
```

??? note "Code explanation"
    - **line 8** → sends a variable called `title`, with the value `"Home"`, to the template.

Then go to ***templates/index.html*** and change the highlighted code below.

```html+jinja linenums="1" hl_lines="5 10" title="templates/index.html"
--8<-- "examples/shell/02_html_templates/step03/templates/index.html"
```

??? note "Code explanation"
    - **line 5** → puts the value of `title` in front of `| StudyM8` in the browser tab.
    - **line 10** → puts the value of `title` into a new paragraph.

!!! primm "PRIMM"
    1. **Predict** what the browser tab and the page will show.
    2. **Run** the code by refreshing the browser.
    3. Time to **investigate**. View the page source. Can you find `{{ title }}`? Why not?
    4. Now **modify** the code to send a second variable called `user` with your name, and show it in a new paragraph.

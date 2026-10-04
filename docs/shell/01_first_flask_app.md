# 1. First Flask App

!!! learn "In this lesson we will learn"
    - what Flask is and what a route does
    - how to create a Flask app
    - how to run the Flask development server
    - how debug mode reloads our server when we save

## Introduction

Every website needs a **web server**: a program that waits for requests from browsers and sends back responses. **Flask** is a Python library that makes writing a web server simple. We write normal Python functions, and Flask connects each one to a web address.

In this lesson we'll write the smallest Flask app possible and see it in our browser.

## PRIMM

Throughout this course we'll use **PRIMM** to explore code. PRIMM has five steps:

1. **Predict** what you think the code will do. Be specific.
2. **Run** the code and check whether your prediction was right.
3. **Investigate** the code. What does each line do? The Code explanation boxes help with this.
4. **Modify** the code to make it do something different.
5. **Make** something new using what you've learnt.

## Create the app

In VS Code, create a new file, add the code below and save it as ***app.py*** in the ***studym8*** folder.

```python linenums="1" title="app.py"
--8<-- "examples/shell/01_first_flask_app/step01/app.py"
```

??? note "Code explanation"
    - **line 1** → imports the `Flask` class from the `flask` library.
    - **line 3** → creates our Flask app object and stores it in `app`. `__name__` tells Flask where our project's files are.
    - **line 6** → a **decorator** that tells Flask to run the function below whenever a browser asks for the `/` route. `/` is the **root** of the website: the page we get when we type just the address.
    - **line 7** → defines the `index` function, which handles requests for `/`. A function that handles a route is called a **view function**.
    - **line 8** → returns the text that Flask sends back to the browser as the response.

!!! tip "Why app.py?"
    When we run `flask run`, Flask looks for a file called ***app.py*** in the current folder. Naming our file ***app.py*** means we don't have to tell Flask where our app is.

## Run the server

In the VS Code terminal (check it starts with `(.venv)`), type the command below and press ++enter++:

```text
flask run --debug
```

The terminal shows something like this:

```text
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 932-635-976
```

- `Running on http://127.0.0.1:5000` → our server is running on our own computer. `127.0.0.1` is the address every computer uses for itself, and `5000` is the **port** our server listens on.
- `Debug mode: on` → Flask will restart the server whenever we save a change, and show detailed error messages when something goes wrong.
- `WARNING: This is a development server` → this server is built for testing on our own computer, not for running a real public website.

Hold down ++ctrl++ and click the `http://127.0.0.1:5000` link to open it in the browser.

!!! primm "PRIMM"
    1. **Predict** what you'll see in the browser. Be specific.
    2. **Run** the code by opening the link.
    3. Time to **investigate**. Look at the terminal again. What new line appeared when the browser loaded the page? What do you think `GET`, `/` and `200` mean? (Check back to [How Websites Work](../start/how_websites_work.md#requests-and-responses) if you need a hint.)

!!! warning "Keep the server running"
    The server keeps running in the terminal while we work. To stop it, click in the terminal and press ++ctrl+c++. If we close VS Code or stop the server, the website stops working until we run `flask run --debug` again.

## Send some HTML

Right now our server sends plain text. Browsers understand **HTML**, the language of web pages. HTML uses **tags** in angle brackets to mark what each part of the page is. For example, `<h1>` marks a main heading and `<p>` marks a paragraph.

Go back to ***app.py*** and change the highlighted code below. Save the file, but don't stop the server.

```python linenums="1" hl_lines="8" title="app.py"
--8<-- "examples/shell/01_first_flask_app/step02/app.py"
```

??? note "Code explanation"
    - **line 8** → returns HTML instead of plain text. `<h1>StudyM8</h1>` is a main heading and `<p>Your study planner</p>` is a paragraph. Each tag has an opening tag (`<h1>`) and a closing tag with a slash (`</h1>`).

!!! primm "PRIMM"
    1. **Predict** what will change in the browser when you refresh the page.
    2. **Run** the code by refreshing the browser (press ++f5++). Look at the terminal: what happened when you saved ***app.py***?
    3. Time to **investigate**. Right-click on the page and choose **View page source**. What does the browser actually receive from our server?
    4. Now **modify** the code to add a second paragraph that says who the app is for.

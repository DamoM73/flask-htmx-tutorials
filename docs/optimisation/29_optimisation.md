# 29. Optimisation

!!! learn "In this lesson we will learn"
    - what latency is and where a website's time goes
    - how to measure response sizes and times in the browser
    - how to time every request on the server with `before_request` and `after_request`
    - how to count database connections

## Introduction

StudyM8 has every feature from the design. Now let's make it faster. Making a program use less time or fewer resources is called **optimisation**.

The delay between a user doing something and seeing the result is called **latency**. Every click in StudyM8 goes through these stages:

1. the browser sends a request across the network
2. Flask runs our Python code
3. our code reads from and writes to the database
4. the response travels back across the network
5. the browser draws the result

Some of these we can't control, like the speed of the user's internet connection. But we can control how much we send, how much work our code does, and how often it uses the database.

!!! tip "Measure first"
    Programmers have a saying: measure before you optimise. It's easy to spend hours speeding up code that was never slow. So before we change anything, we'll add some measuring tools to StudyM8.

## Measure in the browser

We already made one big optimisation in [Connecting Links with HTMX](../shell/05_htmx_links.md): clicking a link only sends the part of the page that changes. Let's measure how much difference that makes.

1. Open the developer tools (++f12++) and click the **Network** tab.
    - **Why:** the Network tab lists every request the browser makes, with its size and time.
    - **Expected result:** an empty list of requests.
2. Log in, then refresh the page (++f5++).
    - **Why:** refreshing asks for the whole page, plus every file it needs.
    - **Expected result:** a list of requests, including the page itself, Pico's stylesheet, HTMX and Plotly.
3. Click the **Clear** button (a circle with a line through it), then click **Add** in the menu.
    - **Why:** this shows only the request HTMX makes.
    - **Expected result:** one request for `add`.

Compare the sizes of the requests in step 2 and step 3.

!!! primm "PRIMM"
    1. **Predict** which request in step 2 is the largest.
    2. **Run** the steps above and check.
    3. Time to **investigate**. Refresh the page a second time. What does the **Size** column say for Pico, HTMX and Plotly now? Why do you think the browser doesn't need to download them again?

## Time each request

Now let's measure how long our server takes to handle each request. Flask lets us run a function **before every request** and **after every request**. We'll record the time before, then print how long it took afterwards.

To pass the start time from one function to the other, we'll use Flask's `g` object. `g` is a place to store values while one request is being handled. Each request gets its own fresh `g`, which is thrown away when the request finishes.

Go back to ***app.py*** and add the highlighted imports at the top.

```python linenums="1" hl_lines="1 4" title="app.py"
--8<-- "examples/optimisation/29_optimisation/step01/app.py:1:5"
```

??? note "Code explanation"
    - **line 1** → imports the `time` library, which can measure time very precisely.
    - **line 4** → also imports `g` from Flask.

Then add the highlighted functions below the `load_user` function.

```python linenums="20" hl_lines="5-7 10-14" title="app.py"
--8<-- "examples/optimisation/29_optimisation/step01/app.py:20:33"
```

??? note "Code explanation"
    - **line 24** → a decorator that makes Flask run the function below before every request.
    - **line 25** → defines `start_timer`.
    - **line 26** → stores the current time in `g`. `time.perf_counter()` gives a time in seconds, measured very precisely.
    - **line 29** → a decorator that makes Flask run the function below after every request, just before the response is sent.
    - **line 30** → defines `log_time`. Flask passes it the response.
    - **line 31** → works out how long the request took: the time now, take away the start time, multiplied by 1000 to turn seconds into milliseconds.
    - **line 32** → prints the request's method, address and time in the terminal. `:.1f` shows the number with one decimal place.
    - **line 33** → returns the response, so Flask can send it.

## Count database connections

Opening a database connection takes time, so let's count how many times we do it. Open ***db.py***, add the highlighted code below and save it.

```python linenums="10" hl_lines="2" title="db.py"
--8<-- "examples/optimisation/29_optimisation/step02/db.py:10:15"
```

??? note "Code explanation"
    - **line 11** → prints a message every time a connection is opened.

Now use StudyM8: go to Home, complete an assessment, edit one, change your name and open the Calendar twice. The terminal shows something like this (your times will be different):

```text
Opening a database connection
Opening a database connection
GET /home took 2.7 ms
Opening a database connection
Opening a database connection
Opening a database connection
POST /assessments/3/complete took 2.0 ms
Opening a database connection
Opening a database connection
Opening a database connection
Opening a database connection
POST /assessments/1/edit took 2.1 ms
Opening a database connection
Opening a database connection
Opening a database connection
POST /account/details took 1.9 ms
Opening a database connection
Opening a database connection
GET /calendar took 134.3 ms
Opening a database connection
Opening a database connection
GET /calendar took 29.5 ms
```

!!! primm "PRIMM"
    1. **Predict** which request will be the slowest.
    2. **Run** StudyM8 and check the terminal.
    3. Time to **investigate**. Why does every request open at least one connection, even before our route's code runs? (Hint: what does Flask-Login do at the start of every request?) Which request opens the most connections? Look at its route and count the database calls.

So we've found three things to improve:

1. some routes ask the database for things they already know → [Fewer Database Queries](30_fewer_queries.md)
2. every database call opens its own connection → [One Connection per Request](31_fewer_connections.md)
3. the Calendar rebuilds the chart every time, even when nothing has changed → [Caching the Chart](32_caching_chart.md)

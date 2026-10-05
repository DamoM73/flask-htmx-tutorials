# 32. Caching the Chart

!!! learn "In this lesson we will learn"
    - what a cache is and when it's worth using one
    - how to cache each user's chart in a dictionary
    - how to invalidate a cache when the data changes

## Introduction

The terminal showed that the Calendar is by far our slowest page: well over 100 milliseconds the first time and around 30 after that, while every other page takes a few milliseconds. Building the chart with pandas and Plotly is a lot of work, and we redo it every time the Calendar is opened, even when nothing has changed.

A **cache** stores the result of slow work so it can be reused. The plan:

1. when a user opens the Calendar, check whether their chart is already in the cache
2. if it is → send it straight away
3. if it isn't → build it, store it in the cache, then send it
4. whenever the user adds, edits or completes an assessment, their chart is out of date, so remove it from the cache. This is called **invalidating** the cache.

We'll keep the cache in a dictionary, with the user's `id` as the key and their chart's HTML as the value.

## Cache the chart

Open ***assessment_service.py***, change the highlighted code below and save it.

```python linenums="1" hl_lines="6 17 50 63 67-70 92-93" title="assessment_service.py"
--8<-- "examples/optimisation/32_caching_chart/step01/assessment_service.py"
```

??? note "Code explanation"
    - **line 6** → creates an empty dictionary to hold the cached charts. It's outside any function, so it lasts as long as the server is running.
    - **line 17** → after adding an assessment, removes the user's chart from the cache. `.pop(user_id, None)` doesn't crash if there's no chart to remove.
    - **line 50** → after completing an assessment, removes the user's chart from the cache.
    - **line 63** → after editing an assessment, removes the user's chart from the cache.
    - **line 67** → checks whether this user's chart is in the cache…
    - **line 68** → …if so, prints a message…
    - **line 69** → …and returns the cached chart, skipping all the work below.
    - **line 70** → otherwise, prints a message saying a new chart is being built.
    - **line 92** → stores the new chart's HTML in the cache.
    - **line 93** → returns the chart.

Now open the Calendar twice, add an assessment, then open the Calendar again. The terminal shows something like this:

```text
Opening a database connection
Building new chart from database
GET /calendar took 129.2 ms
Opening a database connection
Using cached chart
GET /calendar took 0.5 ms
```

!!! primm "PRIMM"
    1. **Predict** what the terminal will show each time you open the Calendar.
    2. **Run** StudyM8: open the Calendar twice, add an assessment, then open the Calendar twice more.
    3. Time to **investigate**. Delete line 63 and edit an assessment's due date, then open the Calendar. What's wrong? Why? Put the line back when you're done.

!!! warning "Caches can go stale"
    A cache that isn't invalidated when its data changes shows out-of-date information. This is called a **stale** cache, and it's one of the most common bugs in real websites. Whenever we cache something, we must find every place the data can change.

!!! tip "Restarting clears the cache"
    Our cache lives in the server's memory, so it's emptied every time the server restarts, including every time debug mode reloads after we save a file. That's fine for StudyM8: the worst that happens is one slow Calendar load.

That's StudyM8 finished, and faster. Compare your app with the [Finished App](../reference/finished_app.md).

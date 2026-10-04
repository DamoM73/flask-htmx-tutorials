# 27. Calendar Page

!!! learn "In this lesson we will learn"
    - what a Gantt chart shows
    - how to build a timeline chart with Plotly Express and pandas
    - how to put a Plotly chart into a page
    - why Jinja escapes HTML, and when to use `| safe`

## Introduction

The Calendar page is what makes StudyM8 useful: it shows when the pressure is on. If we look back at the [design](../start/design.md#calendar), the page shows each outstanding assessment as a bar, starting on its start date and ending on its due date. Where lots of bars overlap, the workload is heavy.

This kind of chart is called a **Gantt chart** (or **timeline**). We'll draw it with **Plotly**, a Python library that makes interactive charts. Plotly builds the chart in Python, then turns it into HTML and JavaScript that the browser draws.

So let's think about this:

1. Get the user's outstanding assessments → `get_assessments`, which we already have.
2. Organise them into a table with a start, finish and label for each bar → a **pandas DataFrame**.
3. Build the chart → `px.timeline`.
4. Turn the chart into HTML and send it to the Calendar page.
5. The browser needs Plotly's JavaScript library to draw the chart → load it in ***base.html***.

!!! tip "pandas"
    **pandas** is a Python library for working with tables of data, called **DataFrames**. Plotly Express reads its data from a DataFrame. We installed pandas in [Setting Up](../start/setup.md#install-the-libraries).

## Build the chart

Open ***assessment_service.py*** and add the highlighted imports at the top.

```python linenums="1" hl_lines="1-2" title="assessment_service.py"
--8<-- "examples/assessments/27_calendar/step01/assessment_service.py:1:4"
```

??? note "Code explanation"
    - **line 1** → imports pandas, using the short name `pd`, which is how most programmers write it.
    - **line 2** → imports Plotly Express, using the short name `px`.

Then add the highlighted function to the bottom of the file.

```python linenums="62" hl_lines="4-26" title="assessment_service.py"
--8<-- "examples/assessments/27_calendar/step01/assessment_service.py:62:87"
```

??? note "Code explanation"
    - **line 65** → defines `get_chart`, which builds the chart for a user.
    - **line 66** → gets the user's outstanding assessments.
    - **line 67** → checks whether there are none…
    - **line 68** → …if so, returns `None`, because there's nothing to draw.
    - **line 69** → starts an empty list for the chart's data.
    - **line 70** → loops through each assessment.
    - **line 71** → works out where the bar should end. A due date means the end of that day, so we add one day. Without this, an assessment that starts and ends on the same day (like an exam) would have no length and wouldn't show.
    - **lines 72–77** → adds a dictionary for this assessment to the list: the subject (the bar's row), the details (the bar's label), and the start and end of the bar.
    - **line 78** → starts building a timeline chart.
    - **line 79** → turns the list of dictionaries into a DataFrame.
    - **lines 80–81** → say which columns hold the start and end of each bar.
    - **line 82** → puts one row on the chart for each subject.
    - **line 83** → writes the details on each bar.
    - **line 84** → sets the chart's title.
    - **line 85** → closes the `px.timeline` call.
    - **line 86** → removes the word "Subject" from the side of the chart, because the subject names explain themselves.
    - **line 87** → turns the chart into HTML. `full_html=False` gives just the chart, not a whole page, and `include_plotlyjs=False` leaves out Plotly's JavaScript library, because ***base.html*** will load it.

## Load Plotly's JavaScript

Open ***templates/base.html***, add the highlighted code below and save it.

```html+jinja linenums="9" hl_lines="3" title="templates/base.html"
--8<-- "examples/assessments/27_calendar/step02/templates/base.html:9:12"
```

??? note "Code explanation"
    - **line 11** → loads Plotly's JavaScript library from the internet, so the browser can draw charts.

## The Calendar page

Open ***templates/partials/calendar.html***, change the highlighted code below and save it.

```html+jinja linenums="1" hl_lines="2-6" title="templates/partials/calendar.html"
--8<-- "examples/assessments/27_calendar/step03/templates/partials/calendar.html"
```

??? note "Code explanation"
    - **line 2** → checks whether there's a chart…
    - **line 3** → …if so, puts the chart's HTML into the page.
    - **line 4** → otherwise…
    - **line 5** → …shows a message.
    - **line 6** → ends the `if`.

!!! tip "Why | safe?"
    Jinja normally **escapes** values: it turns characters like `<` into `&lt;`, so they show as text instead of becoming HTML. This stops users typing HTML or JavaScript into a form and having it run on someone's page, an attack called **cross-site scripting**. The chart's HTML comes from Plotly, not from a user, so we mark it `| safe` to tell Jinja to put it in as real HTML. Only ever use `| safe` for HTML we trust.

## The calendar route

Go back to ***app.py*** and change the highlighted code in the `calendar` function.

```python linenums="124" hl_lines="4-5" title="app.py"
--8<-- "examples/assessments/27_calendar/step04/app.py:124:128"
```

??? note "Code explanation"
    - **line 127** → builds the chart for the logged-in user.
    - **line 128** → sends the chart to the Calendar page.

!!! primm "PRIMM"
    1. **Predict** what the Calendar page will show for your assessments.
    2. **Run** the code by clicking Calendar. Hover over a bar, and try dragging across the chart to zoom in. Double-click to zoom out.
    3. Time to **investigate**. Add an assessment that starts and ends on the same day. Then remove `+ pd.Timedelta(days=1)` from line 71 and look at the chart again. What happened to that assessment? Put it back when you're done.
    4. Now **modify** the chart's title to `My Workload`.

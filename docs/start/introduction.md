# Introduction

!!! learn "On this page we will learn"
    - what we're going to build in this course
    - which tools we'll use to build it
    - what we need to know before we start

In this course we're going to explore web development by building our own interactive website from scratch. We'll write the server in Python, the pages in HTML, and store our data in a real database. By the end, we'll have the skills to design and build our own web applications.

## Why web development?

Websites and web applications are everywhere: school portals, online shops, social media, streaming services and the apps on our phones. Learning how they work lets us build platforms for sharing information, running a business, connecting with people and much more.

## The project

We're going to build **StudyM8**, a study planner for students. StudyM8 lets users:

- register an account and log in
- record each assessment item with its subject, details, start date and due date
- tick off assessments as they complete them
- see all their outstanding assessments on a calendar chart, so they can spot the weeks when the pressure is on

You can see what the finished app looks like on the [Finished App](../reference/finished_app.md) page.

## The tools

Real websites are built from a few different technologies working together. We'll use:

| Tool | What it does |
| :-- | :-- |
| **Python** | the programming language for our server code |
| **Flask** | a Python library that turns our Python code into a web server |
| **HTML** | the language that describes what's on each page |
| **Jinja** | the template language Flask uses to put our data into HTML |
| **Pico CSS** | a ready-made stylesheet that makes our HTML look good |
| **HTMX** | a small library that swaps parts of a page without reloading the whole page |
| **SQLite** | a database that stores our users and assessments in a single file |
| **SQL** | the language we use to talk to the database |
| **Plotly** | a Python library that draws our calendar chart |

That looks like a lot, but we don't need to learn them all at once. We'll learn each one when StudyM8 needs it, and the [Reference](../reference/html.md) section has a summary of each tool we can come back to.

!!! tip "If you've used Anvil"
    StudyM8 was first built with Anvil, which hides a lot of the web from us. This time we're building it the way most websites are built: we write the HTML, run our own server and design our own database. It's more work, but we'll understand every part of our website.

## Required knowledge

We'll need solid Python skills before we start. We don't need to know any HTML, CSS or SQL; we'll learn those as we go.

| Skills | Course |
| :-- | :-- |
| Basic syntax and structure<br>Control flow<br>Functions<br>Data structures | [A Turtle Introduction to Python](https://damom73.github.io/turtle-introduction-to-python/) |
| Object-oriented programming | [Deepest Dungeon - Python OOP](https://damom73.github.io/python-oop-with-deepest-dungeon/) |
| Modules and libraries | [Space Rescue](https://damom73.github.io/space-rescue-tutorials/) |

Once we know what we're aiming for, the next page looks at how websites actually work.

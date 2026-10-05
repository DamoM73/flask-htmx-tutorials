# Test Plans

!!! learn "On this page we will learn"
    - how to write requirements and success criteria that can be tested
    - the kinds of testing a website needs
    - how to choose test data
    - how to write a test plan, record a testing log and run a usability test
    - how to use test results to refine and evaluate a website

Testing shows whether a website does what it's meant to do. It isn't something to leave until the end: test each feature as soon as it's built, and fix problems while the code is fresh in your mind.

## Requirements and success criteria

Tests check **requirements**, so the requirements need to be clear enough to test. Give each requirement an ID so tests, refinements and the evaluation can refer to it.

| ID | Requirement | Success criteria |
| :-- | :-- | :-- |
| R1 | Visitors can see upcoming events | the Events page lists every future event in date order; past events aren't shown |
| R2 | Only admins can add, edit and delete events | logged-out visitors and ordinary members can't reach the add, edit or delete pages |
| R3 | Visitors can contact the group | the contact form saves a message with a name, email and message; empty fields show an error |
| R4 | The site is easy to use on a phone | a new user can find the next training time in the phone view in under 30 seconds |
| R5 | The site is accessible | Lighthouse accessibility score of 90 or more on every page; every task can be done with a keyboard |

!!! tip "Testable requirements"
    "The site looks good" can't be tested. "A new user can find the next training time in under 30 seconds" can. Use numbers, specific pages and specific actions wherever possible.

## Kinds of testing

| Kind | Checks | How |
| :-- | :-- | :-- |
| **Functional** | each feature does what it should | try each feature with normal data |
| **Validation** | bad or unusual data is handled properly | try boundary and invalid data in every form |
| **Security** | users can only see and do what they're allowed to | try pages while logged out, as a member and as an admin; type addresses directly |
| **Usability** | real users can use the site easily | watch people from the audience try set tasks |
| **Accessibility** | everyone can use the site | keyboard, Lighthouse, WAVE, contrast and screen reader checks (see [Accessibility](accessibility.md#testing-accessibility)) |
| **Compatibility** | the site works on different browsers and screen sizes | try two or more browsers on our laptop (for example Chrome and Edge), and phone and tablet sizes in the browser's device toolbar |
| **Performance** | pages load quickly | the Network tab and server timings from [Optimisation](../optimisation/29_optimisation.md) |

## Test data

For every input, test three kinds of data:

| Kind | Means | Example (event title, 1–60 characters) |
| :-- | :-- | :-- |
| **Normal** | sensible data that should be accepted | `Under 12s training` |
| **Boundary** | data at the edges of what's allowed | a 1-character title, a 60-character title, and a 61-character title |
| **Invalid** (erroneous) | data that should be rejected | an empty title, only spaces |

Dates need the same thinking: today, yesterday, a date far in the future, an end date before the start date, and no date at all.

## Test plan

Write the test plan **before** testing, from the requirements. Each test says what to do and what should happen.

| Requirement | Criteria | Test method | Expected result |
| :-- | :-- | :-- | :-- |
| R1 | past events aren't shown | add an event dated yesterday and one dated next week, then open the Events page | only next week's event is listed |
| R1 | events are in date order | add events for 20 Mar, 10 Mar and 15 Mar, then open the Events page | they're listed 10 Mar, 15 Mar, 20 Mar |
| R2 | logged-out visitors can't add events | log out, then type `/events/add` into the address bar | the login page is shown |
| R2 | members can't add events | log in as a member who isn't an admin, then go to `/events/add` | a 403 Forbidden page is shown |
| R3 | empty fields show an error | submit the contact form with the message empty | "Please enter a message" is shown, and the name and email are kept |
| R3 | messages are saved | submit the contact form with normal data, then open the admin Messages page | the message is listed with the right name and email |
| R4 | works on a phone | open each page in the device toolbar at 375 pixels wide | nothing is cut off; the menu, tables and buttons can all be used |
| R5 | accessibility score | run Lighthouse on each page | each page scores 90 or more |

## Testing log

Record what actually happened each time a test is run, including the date. When a test fails, record what you'll do about it, then **run the test again** after fixing it.

| Date | Requirement | Actual result | Pass/fail | Action if failed |
| :-- | :-- | :-- | :-- | :-- |
| 12/05/2026 | R1 | yesterday's event was still listed | Fail | changed the query to `WHERE date(starts_at) >= date('now', 'localtime')` |
| 13/05/2026 | R1 | only next week's event listed | Pass | |
| 13/05/2026 | R2 | a member could open `/events/add` | Fail | replaced `@login_required` with `@admin_required` |
| 14/05/2026 | R2 | member shown 403 Forbidden | Pass | |
| 14/05/2026 | R5 | Home page scored 84: logo had no alt text, low-contrast footer text | Fail | added `alt="Bayside JFC home"`; darkened footer text |
| 15/05/2026 | R5 | Home page scored 96 | Pass | |

A failed test isn't a bad thing to record. It's evidence of testing and refining, which is exactly what the Generate stage asks for.

## Usability testing

Usability testing means watching real users try the website. It finds problems we can't see because we already know how the site works.

1. **Choose 3–5 testers** from the audience: a member, a parent, someone who's never heard of the group. The site runs on our laptop, so testers use our laptop, in class or at home. Turn on the device toolbar's phone view when testing phone requirements.
2. **Write 3–5 tasks** that match the requirements, without giving hints about where to click. For example: "Find out when the under 12s train on Tuesdays", "Find out how to join the club".
3. **Ask testers to think aloud** as they go: what they're looking for, what they expect to happen.
4. **Don't help.** If they get stuck, note where and why. That's the useful part.
5. **Record** for each task: whether they finished it, how long it took, and what they said.
6. **Ask a few questions** afterwards, for example: "How easy was the site to use, from 1 (very hard) to 5 (very easy)?", "What was the most confusing part?", "What would you change?"

| Tester | Task | Finished? | Time | Notes |
| :-- | :-- | :-- | :-- | :-- |
| Parent | find Tuesday training time | Yes | 42 s | looked under News first; didn't expect training under Events |
| Member | find how to join | Yes | 12 s | saw the Join button straight away |

## Refining

Turn test failures and feedback into changes, and link each change back to a requirement:

| Feedback or test result | Change made | Requirement |
| :-- | :-- | :-- |
| parent looked under News for training times | added a **Training** link to the menu and a "Next training" card on the home page | R4 |
| Lighthouse: low-contrast footer text | darkened the footer text colour | R5 |

Then test again to check the change worked.

## Evaluating

In the Evaluate stage, go back to every requirement and judge whether the finished site meets it, using evidence from testing:

| ID | Requirement | Met? | Evidence |
| :-- | :-- | :-- | :-- |
| R1 | visitors can see upcoming events | Yes | testing log 13/05: only future events listed, in date order |
| R4 | easy to use on a phone | Partly | 4 of 5 testers found training times in under 30 s; one took 42 s before the menu was changed |

Finish with improvements that could be made with more time, and what you'd do differently in the development process.

## Automated tests (extension)

Flask can test routes automatically, which is handy for re-running security tests after every change:

```python
from app import app

client = app.test_client()


def test_add_event_needs_login():
    response = client.get("/events/add")
    assert response.status_code == 302


def test_events_page_loads():
    response = client.get("/events")
    assert response.status_code == 200
```

Save it as ***test_app.py***, `pip install pytest`, then run `pytest` in the terminal. Each `assert` checks one expected result.

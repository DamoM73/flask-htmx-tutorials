import pandas as pd
import plotly.express as px

from db import get_db

chart_cache = {}


def add_assessment(user_id, subject, details, start_date, due_date):
    db = get_db()
    db.execute(
        """INSERT INTO assessments (user_id, subject, details, start_date, due_date)
           VALUES (?, ?, ?, ?, ?)""",
        (user_id, subject, details, start_date, due_date),
    )
    db.commit()
    chart_cache.pop(user_id, None)


def get_assessments(user_id):
    db = get_db()
    return db.execute(
        """SELECT id, subject, details, start_date, due_date, completed
           FROM assessments
           WHERE user_id = ? AND completed = 0
           ORDER BY due_date""",
        (user_id,),
    ).fetchall()


def get_assessment(assessment_id, user_id):
    db = get_db()
    return db.execute(
        """SELECT id, subject, details, start_date, due_date, completed
           FROM assessments
           WHERE id = ? AND user_id = ?""",
        (assessment_id, user_id),
    ).fetchone()


def set_completed(assessment_id, user_id, completed):
    db = get_db()
    db.execute(
        "UPDATE assessments SET completed = ? WHERE id = ? AND user_id = ?",
        (completed, assessment_id, user_id),
    )
    db.commit()
    chart_cache.pop(user_id, None)


def update_assessment(assessment_id, user_id, subject, details, start_date, due_date, completed):
    db = get_db()
    db.execute(
        """UPDATE assessments
           SET subject = ?, details = ?, start_date = ?, due_date = ?, completed = ?
           WHERE id = ? AND user_id = ?""",
        (subject, details, start_date, due_date, completed, assessment_id, user_id),
    )
    db.commit()
    chart_cache.pop(user_id, None)


def get_chart(user_id):
    if user_id in chart_cache:
        print("Using cached chart")
        return chart_cache[user_id]
    print("Building new chart from database")
    assessments = get_assessments(user_id)
    if not assessments:
        return None
    data = []
    for assessment in assessments:
        due_date = pd.Timestamp(assessment["due_date"]) + pd.Timedelta(days=1)
        data.append({
            "Subject": assessment["subject"],
            "Details": assessment["details"],
            "Start": assessment["start_date"],
            "Due": due_date,
        })
    fig = px.timeline(
        pd.DataFrame(data),
        x_start="Start",
        x_end="Due",
        y="Subject",
        text="Details",
        title="Assessment Schedule",
    )
    fig.update_yaxes(title_text="")
    chart_cache[user_id] = fig.to_html(full_html=False, include_plotlyjs=False)
    return chart_cache[user_id]

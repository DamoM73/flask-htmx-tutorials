import pandas as pd
import plotly.express as px

from db import get_db


def add_assessment(user_id, subject, details, start_date, due_date):
    conn = get_db()
    conn.execute(
        """INSERT INTO assessments (user_id, subject, details, start_date, due_date)
           VALUES (?, ?, ?, ?, ?)""",
        (user_id, subject, details, start_date, due_date),
    )
    conn.commit()
    conn.close()


def get_assessments(user_id):
    conn = get_db()
    rows = conn.execute(
        """SELECT id, subject, details, start_date, due_date, completed
           FROM assessments
           WHERE user_id = ? AND completed = 0
           ORDER BY due_date""",
        (user_id,),
    ).fetchall()
    conn.close()
    return rows


def get_assessment(assessment_id, user_id):
    conn = get_db()
    row = conn.execute(
        """SELECT id, subject, details, start_date, due_date, completed
           FROM assessments
           WHERE id = ? AND user_id = ?""",
        (assessment_id, user_id),
    ).fetchone()
    conn.close()
    return row


def set_completed(assessment_id, user_id, completed):
    conn = get_db()
    conn.execute(
        "UPDATE assessments SET completed = ? WHERE id = ? AND user_id = ?",
        (completed, assessment_id, user_id),
    )
    conn.commit()
    conn.close()


def update_assessment(assessment_id, user_id, subject, details, start_date, due_date, completed):
    conn = get_db()
    conn.execute(
        """UPDATE assessments
           SET subject = ?, details = ?, start_date = ?, due_date = ?, completed = ?
           WHERE id = ? AND user_id = ?""",
        (subject, details, start_date, due_date, completed, assessment_id, user_id),
    )
    conn.commit()
    conn.close()


def get_chart(user_id):
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
    return fig.to_html(full_html=False, include_plotlyjs=False)

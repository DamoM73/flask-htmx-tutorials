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
           WHERE user_id = ?
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

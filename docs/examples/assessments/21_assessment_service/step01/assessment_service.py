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

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db


class User(UserMixin):
    def __init__(self, row):
        self.id = row["id"]
        self.email = row["email"]
        self.first_name = row["first_name"]
        self.last_name = row["last_name"]


def get_user(user_id):
    db = get_db()
    row = db.execute(
        "SELECT id, email, first_name, last_name FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()
    if row is None:
        return None
    return User(row)


def email_taken(email):
    db = get_db()
    row = db.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
    return row is not None


def create_user(email, password):
    db = get_db()
    db.execute(
        "INSERT INTO users (email, password_hash) VALUES (?, ?)",
        (email, generate_password_hash(password)),
    )
    db.commit()


def check_login(email, password):
    db = get_db()
    row = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    if row is None:
        return None
    if not check_password_hash(row["password_hash"], password):
        return None
    return User(row)


def update_details(user_id, first_name, last_name):
    db = get_db()
    db.execute(
        "UPDATE users SET first_name = ?, last_name = ? WHERE id = ?",
        (first_name, last_name, user_id),
    )
    db.commit()

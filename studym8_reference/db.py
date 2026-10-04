import sqlite3
from pathlib import Path

import click
from flask import g

DATABASE = Path(__file__).parent / "studym8.db"
SCHEMA = Path(__file__).parent / "schema.sql"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@click.command("init-db")
def init_db_command():
    db = get_db()
    db.executescript(SCHEMA.read_text())
    click.echo("Database created.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

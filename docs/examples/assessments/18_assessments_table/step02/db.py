import sqlite3
from pathlib import Path

import click

DATABASE = Path(__file__).parent / "studym8.db"
SCHEMA = Path(__file__).parent / "schema.sql"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@click.command("init-db")
def init_db_command():
    conn = get_db()
    conn.executescript(SCHEMA.read_text())
    conn.close()
    click.echo("Database created.")

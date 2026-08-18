import sqlite3
from pathlib import Path

from flask import current_app


def get_db():
    """Create a SQLite connection."""
    database_path = Path(current_app.config["DATABASE"])

    database_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(database_path)

    connection.row_factory = sqlite3.Row

    return connection


def close_db(connection):
    """Close the SQLite connection."""
    if connection is not None:
        connection.close()


def init_db():
    """Create the users table if it does not already exist."""
    connection = get_db()

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        connection.commit()

    finally:
        close_db(connection)


def create_user(username, password_hash):
    """Create a new user."""
    connection = get_db()

    try:
        cursor = connection.execute(
            """
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
            """,
            (username, password_hash),
        )

        connection.commit()

        return cursor.lastrowid

    finally:
        close_db(connection)


def get_user_by_username(username):
    """Retrieve a user by username."""
    connection = get_db()

    try:
        return connection.execute(
            """
            SELECT id, username, password_hash, created_at
            FROM users
            WHERE username = ?
            """,
            (username,),
        ).fetchone()

    finally:
        close_db(connection)


def get_user_by_id(user_id):
    """Retrieve a user by ID."""
    connection = get_db()

    try:
        return connection.execute(
            """
            SELECT id, username, created_at
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        ).fetchone()

    finally:
        close_db(connection)

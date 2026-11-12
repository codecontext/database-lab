"""Operations on book records in the SQLite database."""

from __future__ import annotations

import sqlite3
from contextlib import closing
from pathlib import Path


def insert_book(
    database_path: str | Path,
    title: str,
    author: str,
    year: int | None = None,
) -> int:
    """Insert a book row and return its generated ID.

    Args:
        database_path: Path to an existing database with a ``books`` table.
        title: Book title to store.
        author: Book author to store.
        year: Optional positive publication year; ``None`` means unknown.

    Returns:
        The integer ID assigned to the inserted row.
    """
    with closing(sqlite3.connect(database_path)) as connection:
        with connection:
            # Bind values separately; never build SQL by joining user input.
            cursor = connection.execute(
                "INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
                (title, author, year),
            )
            if cursor.lastrowid is None:
                raise RuntimeError("SQLite did not return an ID for the new book")
            return cursor.lastrowid


def list_books(
    database_path: str | Path,
) -> list[tuple[int, str, str, int | None]]:
    """Return all books ordered by their generated ID.

    Args:
        database_path: Path to a database containing a ``books`` table.

    Returns:
        Book rows as ``(id, title, author, year)`` tuples. The year is ``None``
        when it was not recorded.
    """
    with closing(sqlite3.connect(database_path)) as connection:
        return connection.execute(
            "SELECT id, title, author, year FROM books ORDER BY id"
        ).fetchall()
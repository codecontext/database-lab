"""SQLite schema setup for the learning exercises."""

from __future__ import annotations

import sqlite3
from contextlib import closing
from pathlib import Path


def create_books_table(database_path: str | Path) -> None:
    """Create the database file and books table if needed.

    Args:
        database_path: File path for the SQLite database. Missing parent
            directories are created automatically.

    Returns:
        None.
    """
    path = Path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    # The connection context manages transactions; closing() closes the connection.
    with closing(sqlite3.connect(path)) as connection:
        with connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    -- A year may be unknown (NULL), but if present must be positive.
                    year INTEGER CHECK (year IS NULL OR year > 0)
                )
                """
            )
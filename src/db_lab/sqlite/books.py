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
    order_by: str = "id",
) -> list[tuple[int, str, str, int | None]]:
    """Return books in a chosen order.

    Args:
        database_path: Path to a database containing a ``books`` table.
        order_by: Sort key. Supported values are ``"id"`` and ``"year"``.

    Returns:
        Book rows as ``(id, title, author, year)`` tuples. The year is ``None``
        when it was not recorded.
    """
    if order_by == "id":
        query = "SELECT id, title, author, year FROM books ORDER BY id"
    elif order_by == "year":
        query = "SELECT id, title, author, year FROM books ORDER BY year IS NULL, year, id"
    else:
        raise ValueError(f"Unsupported order_by value: {order_by!r}")

    with closing(sqlite3.connect(database_path)) as connection:
        return connection.execute(query).fetchall()


def update_book(
    database_path: str | Path,
    book_id: int,
    title: str | None = None,
    author: str | None = None,
    year: int | None = None,
) -> None:
    """Update one or more fields on a book row.

    Args:
        database_path: Path to a database containing a ``books`` table.
        book_id: Row ID to update.
        title: New title, if provided.
        author: New author, if provided.
        year: New publication year, if provided.

    Returns:
        None.
    """

    changes: list[str] = []
    parameters: list[str | int] = []

    if title is not None:
        changes.append("title = ?")
        parameters.append(title)

    if author is not None:
        changes.append("author = ?")
        parameters.append(author)

    if year is not None:
        changes.append("year = ?")
        parameters.append(year)

    if not changes:
        raise ValueError("Provide at least one field to update")

    # Final SQL query looks like:
    # UPDATE books
    # SET title = ?, author = ?, year = ?
    # WHERE id = ?
    update_query = f"UPDATE books SET {', '.join(changes)} WHERE id = ?"
    parameters.append(book_id)

    with closing(sqlite3.connect(database_path)) as connection:
        with connection:
            connection.execute(update_query, tuple(parameters))


def count_books(database_path: str | Path) -> int:
    """Return the number of rows stored in the books table.

    Args:
        database_path: Path to a database containing a ``books`` table.

    Returns:
        Total number of rows currently in the table.
    """
    with closing(sqlite3.connect(database_path)) as connection:
        (count,) = connection.execute("SELECT COUNT(*) FROM books").fetchone()
        return count


def get_book(
    database_path: str | Path,
    book_id: int,
) -> tuple[int, str, str, int | None] | None:
    """Return one book row by its generated ID.

    Args:
        database_path: Path to a database containing a ``books`` table.
        book_id: Row ID to fetch.

    Returns:
        The matching ``(id, title, author, year)`` tuple, or ``None`` if no row
        exists for that ID.
    """
    with closing(sqlite3.connect(database_path)) as connection:
        return connection.execute(
            "SELECT id, title, author, year FROM books WHERE id = ?",
            (book_id,),
        ).fetchone()


def delete_book(database_path: str | Path, book_id: int) -> None:
    """Delete one book row by its generated ID.

    Args:
        database_path: Path to a database containing a ``books`` table.
        book_id: Row ID to delete.

    Returns:
        None.
    """
    with closing(sqlite3.connect(database_path)) as connection:
        with connection:
            connection.execute("DELETE FROM books WHERE id = ?", (book_id,))


def find_books(
    database_path: str | Path,
    title: str | None = None,
    author: str | None = None,
    year: int | None = None,
    year_from: int | None = None,
    year_to: int | None = None,
) -> list[tuple[int, str, str, int | None]]:
    """Return books matching the supplied filters.

    Text filters support partial, case-insensitive matching for title and author.
    Exact and range filters can also be applied to the publication year.

    Args:
        database_path: Path to a database containing a ``books`` table.
        title: Optional substring to match against the book title.
        author: Optional substring to match against the author name.
        year: Optional exact publication year to filter on.
        year_from: Optional minimum publication year to include.
        year_to: Optional maximum publication year to include.

    Returns:
        Matching book rows in ascending ID order.
    """

    # Final SQL query looks like:
    # SELECT id, title, author, year
    # FROM books
    # WHERE 1 = 1
    # AND LOWER(title) LIKE LOWER(?)
    # AND LOWER(author) LIKE LOWER(?)
    # AND year = ?
    # AND year >= ?
    # AND year <= ?
    # ORDER BY id

    query = "SELECT id, title, author, year FROM books WHERE 1 = 1"
    parameters: list[str | int] = []

    if title is not None:
        query += " AND LOWER(title) LIKE LOWER(?)"
        parameters.append(f"%{title}%")

    if author is not None:
        query += " AND LOWER(author) LIKE LOWER(?)"
        parameters.append(f"%{author}%")

    if year is not None:
        query += " AND year = ?"
        parameters.append(year)

    if year_from is not None:
        query += " AND year >= ?"
        parameters.append(year_from)

    if year_to is not None:
        query += " AND year <= ?"
        parameters.append(year_to)

    query += " ORDER BY id"

    with closing(sqlite3.connect(database_path)) as connection:
        return connection.execute(query, tuple(parameters)).fetchall()
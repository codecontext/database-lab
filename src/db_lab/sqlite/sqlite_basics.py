"""First SQLite operation: create a books table."""

from __future__ import annotations

import argparse
import sqlite3
from contextlib import closing
from pathlib import Path


def create_books_table(database_path: str | Path) -> None:
    """Create the database file and books table if needed."""
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


def main() -> None:
    """Create a local database with an empty books table."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--database",
        type=Path,
        default=Path("data/books.sqlite3"),
        help="database file path (default: data/books.sqlite3)",
    )
    args = parser.parse_args()

    create_books_table(args.database)
    print(f"Created books table in {args.database}")


if __name__ == "__main__":
    main()
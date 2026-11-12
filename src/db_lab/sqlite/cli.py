"""Command-line entry point for the SQLite learning exercises."""

from __future__ import annotations

import argparse
from pathlib import Path

from .books import insert_book
from .schema import create_books_table


DEFAULT_DATABASE = Path("data/books.sqlite3")


def main() -> None:
    """Parse command-line arguments and run one SQLite operation.

    The operation and its inputs are read from ``sys.argv``. The selected
    command's result is printed to the terminal.

    Returns:
        None.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    operations = parser.add_subparsers(dest="operation")

    create_parser = operations.add_parser(
        "create-table",
        help="create the books table",
    )
    create_parser.add_argument(
        "--database",
        type=Path,
        default=DEFAULT_DATABASE,
        help="database file path (default: data/books.sqlite3)",
    )

    insert_parser = operations.add_parser(
        "insert-book",
        help="insert one book into the books table",
    )
    insert_parser.add_argument("title", help="book title")
    insert_parser.add_argument("author", help="book author")
    insert_parser.add_argument("year", type=int, nargs="?", help="publication year")
    insert_parser.add_argument(
        "--database",
        type=Path,
        default=DEFAULT_DATABASE,
        help="database file path (default: data/books.sqlite3)",
    )

    args = parser.parse_args()

    if args.operation in (None, "create-table"):
        database_path = getattr(args, "database", DEFAULT_DATABASE)
        create_books_table(database_path)
        print(f"Created books table in {database_path}")
    else:
        book_id = insert_book(args.database, args.title, args.author, args.year)
        print(f"Inserted book with ID {book_id}")


if __name__ == "__main__":
    main()
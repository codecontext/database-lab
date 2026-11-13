"""Command-line entry point for the SQLite learning exercises."""

from __future__ import annotations

import argparse
from pathlib import Path

from .books import find_books, insert_book, list_books, update_book
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

    list_parser = operations.add_parser(
        "list-books",
        help="list all books in the books table",
    )
    list_parser.add_argument(
        "--database",
        type=Path,
        default=DEFAULT_DATABASE,
        help="database file path (default: data/books.sqlite3)",
    )

    update_parser = operations.add_parser(
        "update-book",
        help="update one or more fields on an existing book",
    )
    update_parser.add_argument("book_id", type=int, help="book ID to update")
    update_parser.add_argument("--title", help="new title")
    update_parser.add_argument("--author", help="new author")
    update_parser.add_argument("--year", type=int, help="new publication year")
    update_parser.add_argument(
        "--database",
        type=Path,
        default=DEFAULT_DATABASE,
        help="database file path (default: data/books.sqlite3)",
    )

    find_parser = operations.add_parser(
        "find-books",
        help="find books whose title or author contains the given text",
    )
    find_parser.add_argument(
        "--title",
        help="partial title match, case-insensitive",
    )
    find_parser.add_argument(
        "--author",
        help="partial author match, case-insensitive",
    )
    find_parser.add_argument(
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
    elif args.operation == "insert-book":
        book_id = insert_book(args.database, args.title, args.author, args.year)
        print(f"Inserted book with ID {book_id}")
    elif args.operation == "update-book":
        if args.title is None and args.author is None and args.year is None:
            raise ValueError("Provide at least one field to update")

        update_book(
            args.database,
            args.book_id,
            title=args.title,
            author=args.author,
            year=args.year,
        )
        print(f"Updated book with ID {args.book_id}")
    elif args.operation == "find-books":
        books = find_books(args.database, title=args.title, author=args.author)
        if not books:
            print("No books found.")
            return

        for book_id, title, author, year in books:
            display_year = year if year is not None else "year unknown"
            print(f"{book_id}: {title} by {author} ({display_year})")
    else:
        books = list_books(args.database)
        if not books:
            print("No books found.")
            return

        for book_id, title, author, year in books:
            display_year = year if year is not None else "year unknown"
            print(f"{book_id}: {title} by {author} ({display_year})")


if __name__ == "__main__":
    main()
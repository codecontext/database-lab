"""Tests for SQLite book operations."""

import sqlite3
import tempfile
import unittest
from pathlib import Path

from db_lab.sqlite.books import insert_book
from db_lab.sqlite.schema import create_books_table


class InsertBookTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_dir.name) / "books.sqlite3"
        create_books_table(self.database_path)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_insert_book_returns_id_and_stores_values(self) -> None:
        book_id = insert_book(
            self.database_path,
            "The Hobbit",
            "J. R. R. Tolkien",
            1937,
        )

        with sqlite3.connect(self.database_path) as connection:
            row = connection.execute(
                "SELECT id, title, author, year FROM books WHERE id = ?",
                (book_id,),
            ).fetchone()

        self.assertEqual(book_id, 1)
        self.assertEqual(row, (1, "The Hobbit", "J. R. R. Tolkien", 1937))

    def test_insert_book_allows_unknown_year(self) -> None:
        book_id = insert_book(self.database_path, "Untitled", "Unknown Author")

        with sqlite3.connect(self.database_path) as connection:
            row = connection.execute(
                "SELECT id, title, author, year FROM books WHERE id = ?",
                (book_id,),
            ).fetchone()

        self.assertEqual(row, (1, "Untitled", "Unknown Author", None))

    def test_insert_book_rejects_non_positive_year(self) -> None:
        with self.assertRaises(sqlite3.IntegrityError):
            insert_book(self.database_path, "Invalid Year", "Test Author", -1)


if __name__ == "__main__":
    unittest.main()

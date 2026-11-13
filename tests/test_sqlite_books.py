"""Tests for SQLite book operations."""

import sqlite3
import tempfile
import unittest
from pathlib import Path

from db_lab.sqlite.books import find_books, insert_book, list_books, update_book
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

    def test_list_books_returns_empty_list_for_empty_table(self) -> None:
        self.assertEqual(list_books(self.database_path), [])

    def test_list_books_returns_rows_in_id_order(self) -> None:
        insert_book(self.database_path, "Second", "Author B", 2000)
        insert_book(self.database_path, "Third", "Author C")

        self.assertEqual(
            list_books(self.database_path),
            [
                (1, "Second", "Author B", 2000),
                (2, "Third", "Author C", None),
            ],
        )

    def test_find_books_returns_partial_matches_in_id_order(self) -> None:
        insert_book(self.database_path, "The Hobbit", "J. R. R. Tolkien", 1937)
        insert_book(self.database_path, "The Silmarillion", "J. R. R. Tolkien", 1977)
        insert_book(self.database_path, "Pride and Prejudice", "Jane Austen", 1813)

        self.assertEqual(
            find_books(self.database_path, "hobbit"),
            [(1, "The Hobbit", "J. R. R. Tolkien", 1937)],
        )

        self.assertEqual(
            find_books(self.database_path, author="tolkien"),
            [
                (1, "The Hobbit", "J. R. R. Tolkien", 1937),
                (2, "The Silmarillion", "J. R. R. Tolkien", 1977),
            ],
        )

    def test_find_books_supports_combined_title_and_author_filters(self) -> None:
        insert_book(self.database_path, "The Hobbit", "J. R. R. Tolkien", 1937)
        insert_book(self.database_path, "The Silmarillion", "J. R. R. Tolkien", 1977)
        insert_book(self.database_path, "Pride and Prejudice", "Jane Austen", 1813)

        self.assertEqual(
            find_books(self.database_path, title="the", author="tolkien"),
            [
                (1, "The Hobbit", "J. R. R. Tolkien", 1937),
                (2, "The Silmarillion", "J. R. R. Tolkien", 1977),
            ],
        )

    def test_find_books_returns_empty_list_when_no_rows_match(self) -> None:
        insert_book(self.database_path, "The Hobbit", "J. R. R. Tolkien", 1937)

        self.assertEqual(find_books(self.database_path, title="unknown"), [])
        self.assertEqual(find_books(self.database_path, author="austen"), [])

    def test_update_book_changes_selected_fields(self) -> None:
        book_id = insert_book(self.database_path, "Old Title", "Old Author", 2000)

        update_book(
            self.database_path,
            book_id,
            title="New Title",
            author="New Author",
            year=2024,
        )

        with sqlite3.connect(self.database_path) as connection:
            row = connection.execute(
                "SELECT id, title, author, year FROM books WHERE id = ?",
                (book_id,),
            ).fetchone()

        self.assertEqual(row, (1, "New Title", "New Author", 2024))

    def test_update_book_requires_at_least_one_field(self) -> None:
        book_id = insert_book(self.database_path, "Old Title", "Old Author", 2000)

        with self.assertRaises(ValueError):
            update_book(self.database_path, book_id)


if __name__ == "__main__":
    unittest.main()

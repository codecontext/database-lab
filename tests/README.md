# Running Tests

The tests use Python's built-in `unittest` framework. No test packages or virtual
environment are required. Run commands from the repository root.

## Run all tests

```bash
PYTHONPATH=src /usr/bin/python3 -m unittest discover -s tests -v
```

Test discovery finds files named `test_*.py` and runs test methods whose names
start with `test_`.

## Run one test module

```bash
PYTHONPATH=src /usr/bin/python3 -m unittest tests.test_sqlite_books -v
```

## What the SQLite test checks

`test_sqlite_books.py` creates a fresh temporary database for each case.

**`test_insert_book_returns_id_and_stores_values`**

Inserts a book with a publication year, then checks that the function returns
the generated ID and that all book values were saved correctly.

**`test_insert_book_allows_unknown_year`**

Inserts a book without a year and checks that SQLite stores the missing value as
`NULL`.

**`test_insert_book_rejects_non_positive_year`**

Attempts to insert a negative year and checks that the table's `CHECK` constraint
rejects it with an integrity error.

**`test_list_books_returns_empty_list_for_empty_table`**

Checks that listing a table with no rows returns an empty list.

**`test_list_books_returns_rows_in_id_order`**

Inserts two books and checks that listing returns both rows in generated-ID order,
including `None` for an unknown year.

**`test_find_books_returns_partial_matches_in_id_order`**

Inserts several books, then checks that a case-insensitive partial match finds
rows by title and by author in ID order.

**`test_update_book_changes_selected_fields`**

Inserts one book, updates its fields by ID, and verifies that the chosen values
change while the rest of the record remains intact.

**`test_delete_book_removes_selected_row`**

Inserts two books, deletes one by ID, and checks that only the selected row is
removed and the remaining row stays intact.

**`test_get_book_returns_row_for_existing_id`**

Looks up a book by its generated ID and checks that the full row is returned.

**`test_get_book_returns_none_for_missing_id`**

Checks that a missing ID results in `None` instead of an error.

SQLite tests create temporary database files and clean them up after each test,
so they do not change the saved database in `data/`.

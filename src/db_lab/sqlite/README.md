# SQLite: Create the Books Table

This lesson performs one operation: create a `books` table in a SQLite
database file.

## Tools needed

- Python 3.10 or newer.
- Python's built-in `sqlite3` module; no package installation or virtual
  environment is needed.
- Optional: the `sqlite3` command-line tool or a SQLite database viewer to
  inspect the database interactively.

## Run

Run this from the repository root:

```bash
PYTHONPATH=src /usr/bin/python3 -m db_lab.sqlite.sqlite_basics
```

By default, the database is saved at `data/books.sqlite3`. The file is local,
ignored by Git, and remains available to inspect. Choose a different path with:

```bash
PYTHONPATH=src /usr/bin/python3 -m db_lab.sqlite.sqlite_basics --database data/review.sqlite3
```

## Verify

Check the table and its columns using Python's built-in SQLite module:

```bash
/usr/bin/python3 - <<'PY'
import sqlite3

with sqlite3.connect("data/books.sqlite3") as connection:
    columns = [row[1] for row in connection.execute("PRAGMA table_info(books)")]

expected = ["id", "title", "author", "year"]
assert columns == expected, f"Expected {expected}, found {columns}"
print(f"PASS: books table columns are {columns}")
PY
```

## Inspect with a GUI or the command line

You can open `data/books.sqlite3` with a SQLite GUI, for example DB Browser for
SQLite or SQLiteStudio. In the GUI, open the database file and inspect the
`books` table and its schema. These are optional tools; the Python verification
above needs no extra installation.

If the `sqlite3` command-line tool is installed, inspect the database with:

```bash
sqlite3 data/books.sqlite3
```

At the SQLite prompt, try:

```sql
.tables
.schema books
PRAGMA table_info(books);
.quit
```

The expected columns are `id`, `title`, `author`, and `year`. This lesson does
not insert any rows yet.

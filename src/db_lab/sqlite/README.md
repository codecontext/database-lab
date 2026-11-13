# SQLite Basics

This folder teaches SQLite through small operations, one at a time. The current
operations create the `books` table, insert a book, list saved books, and find
matching rows by title or author. The database is a regular file, so you can
keep it and inspect it later without running a database server.

## Code layout

- `cli.py` is the only command-line entry point. Its `main()` parses the command
  and calls the matching function.
- `schema.py` creates the database file and `books` table.
- `books.py` inserts, lists, and searches books in the `books` table.
- `data/books.sqlite3` is the default database file. The `data/` folder is
  ignored by Git, so your local database is not added to code commits.

## Tools needed

- Python 3.10 or newer.
- Python's built-in `sqlite3` module. No package installation, virtual
  environment, or database server is needed.
- Optional GUI: DB Browser for SQLite or SQLiteStudio to browse the database.
- Optional CLI: the `sqlite3` command-line program to inspect it in a terminal.

## How Commands Run

Run commands from the repository root. `PYTHONPATH=src` tells Python to find
the project package under `src/`; `-m db_lab.sqlite.cli` runs the CLI module.
The module's final `if __name__ == "__main__":` block calls `main()` when it is
run this way. `main()` reads the command-line arguments and dispatches the
selected operation to `schema.py` or `books.py`. The CLI has one entry point and
performs one selected operation per invocation.

## Add and View Data

Run the following steps from the repository root.

### 1. Create the table

This creates `data/books.sqlite3` and an empty `books` table:

```bash
PYTHONPATH=src /usr/bin/python3 -m db_lab.sqlite.cli
```

It is safe to run again; an existing table and its rows are left intact. To use
a different database file, specify its path:

```bash
PYTHONPATH=src /usr/bin/python3 -m db_lab.sqlite.cli create-table --database data/review.sqlite3
```

### 2. Insert a book

Insert one row into the default database. The table must already exist:

```bash
PYTHONPATH=src /usr/bin/python3 -m db_lab.sqlite.cli insert-book "The Hobbit" "J. R. R. Tolkien" 1937
```

Title and author are required; year is optional. To leave the year unknown, omit
it. Each run inserts a new row, so running the same command again creates a
duplicate. To insert into a different database, pass `--database`:

```bash
PYTHONPATH=src /usr/bin/python3 -m db_lab.sqlite.cli insert-book "Year Not Recorded" "Database Lab" --database data/review.sqlite3
```

## What the Table Enforces

- `id INTEGER PRIMARY KEY`: SQLite assigns each row an integer ID.
- `title TEXT NOT NULL` and `author TEXT NOT NULL`: these values are required.
- `year INTEGER CHECK (year IS NULL OR year > 0)`: an unknown year is allowed;
  a year that is provided must be positive.

The insert code uses `?` placeholders and supplies values separately. This keeps
book text as data instead of treating it as part of the SQL command.

### 3. List books

Use the CLI to read all rows from the default database:

```bash
PYTHONPATH=src /usr/bin/python3 -m db_lab.sqlite.cli list-books
```

Rows are displayed in ID order. If the table is empty, the command prints
`No books found.` To list rows from another database file, put `--database`
after the operation name:

```bash
PYTHONPATH=src /usr/bin/python3 -m db_lab.sqlite.cli list-books --database data/review.sqlite3
```

### 4. Find books by text

Use partial, case-insensitive matches to search the table. Search by title,
author, or both at the same time:

```bash
PYTHONPATH=src /usr/bin/python3 -m db_lab.sqlite.cli find-books --title "hobbit"
PYTHONPATH=src /usr/bin/python3 -m db_lab.sqlite.cli find-books --author "tolkien"
PYTHONPATH=src /usr/bin/python3 -m db_lab.sqlite.cli find-books --title "the" --author "tolkien"
```

The CLI prints each matching row in ID order. If nothing matches, it prints
`No books found.`

### 5. Inspect the saved rows

If the SQLite CLI is installed, check the table and its contents:

```bash
sqlite3 data/books.sqlite3 ".schema books"
sqlite3 data/books.sqlite3 "SELECT id, title, author, year FROM books;"
```

Or open `data/books.sqlite3` in DB Browser for SQLite or SQLiteStudio to browse
the schema and rows. The expected columns are `id`, `title`, `author`, and
`year`.

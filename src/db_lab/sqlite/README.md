# SQLite Basics

This folder teaches SQLite through small operations, one at a time. The current
operations create the `books` table and insert one book row. The database is a
regular file, so you can keep it and inspect it later without running a database
server.

## Code layout

- `cli.py` is the only command-line entry point. Its `main()` parses the command
  and calls the matching function.
- `schema.py` creates the database file and `books` table.
- `books.py` inserts a book into an existing `books` table.
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

The default command creates the `books` table:

```bash
PYTHONPATH=src /usr/bin/python3 -m db_lab.sqlite.cli
```

This creates `data/books.sqlite3` and prints a confirmation. It is safe to run
again: `CREATE TABLE IF NOT EXISTS` leaves an existing table and its rows intact.
To choose a different database file, use the explicit `create-table` operation:

```bash
PYTHONPATH=src /usr/bin/python3 -m db_lab.sqlite.cli create-table --database data/review.sqlite3
```

The insert operation adds one row. Create the table first; insertion does not
create it automatically:

```bash
PYTHONPATH=src /usr/bin/python3 -m db_lab.sqlite.cli insert-book "The Hobbit" "J. R. R. Tolkien" 1937
```

The title and author are required; the year is optional. Every run inserts a
new row, so running this command repeatedly adds duplicates. To use a non-default
database, pass `--database` after the arguments:

```bash
PYTHONPATH=src /usr/bin/python3 -m db_lab.sqlite.cli insert-book "The Hobbit" "J. R. R. Tolkien" 1937 --database data/review.sqlite3
```

## What the Table Enforces

- `id INTEGER PRIMARY KEY`: SQLite assigns each row an integer ID.
- `title TEXT NOT NULL` and `author TEXT NOT NULL`: these values are required.
- `year INTEGER CHECK (year IS NULL OR year > 0)`: an unknown year is allowed;
  a year that is provided must be positive.

The insert code uses `?` placeholders and supplies values separately. This keeps
book text as data instead of treating it as part of the SQL command.

## Verify and Inspect

If the SQLite CLI is installed, check the table and its contents:

```bash
sqlite3 data/books.sqlite3 ".schema books"
sqlite3 data/books.sqlite3 "SELECT id, title, author, year FROM books;"
```

Or open `data/books.sqlite3` in DB Browser for SQLite or SQLiteStudio to browse
the schema and rows. The expected columns are `id`, `title`, `author`, and
`year`.

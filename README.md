# Database Lab

Database Lab is a hands-on project for learning how databases store, organize,
and retrieve information. Exercises are small and reviewed one concept at a
time. Python is the project language; SQLite is first because it is available
through Python's standard library and needs no separate server.

## Database concepts

- **Relational databases** organize information into tables and use SQL to
    query related rows. Constraints, keys, and transactions help protect data.
- **NoSQL databases** use other models, including documents and key-value pairs.
    Their data structures and query patterns suit different workloads and trade-
    offs; NoSQL is not one single database model.
- **Data modeling** is the practice of choosing how information and
    relationships are represented so common operations remain clear and
    reliable.

## Learning path

1. SQLite: tables, schema, SQL operations, constraints, relationships, and
     transactions.
2. NoSQL fundamentals: compare relational, document, and key-value models.
3. MongoDB: document modeling, queries, and indexes.
4. Redis: key-value structures, expiration, and caching patterns.

## Repository organization

- `src/db_lab/<database>/`: code grouped by database technology.
- `src/db_lab/<database>/README.md`: tools, run instructions, and verification
    steps for that technology.
- `data/`: local database files kept for inspection and ignored by Git.
- `tests/`: automated checks, added alongside the exercises they cover.

Start with the guide in [`src/db_lab/sqlite/README.md`](src/db_lab/sqlite/README.md).

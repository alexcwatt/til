# SQLite Diff

SQLite has a powerful diff feature that outputs the changes required to transform one database into another. This can be useful for figuring out the changes that have taken place between two snapshots of the same database, and can allow for building merge-like workflows on top of SQLite. (Imagine two users are given the same database, and make changes independently, and then wish to merge their changes together: SQLite's tooling enables flows like that.)

To illustrate, let's start with a database created as follows:

```sql
CREATE TABLE books (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL
);

INSERT INTO books (title, author) VALUES
    ('Pride and Prejudice', 'Jane Austen'),
    ('1984', 'George Orwell'),
    ('To Kill a Mockingbird', 'Harper Lee'),
    ('Moby-Dick', 'Herman Melville');
```

With `.mode box` that looks like

```
┌────┬───────────────────────┬─────────────────┐
│ id │         title         │     author      │
├────┼───────────────────────┼─────────────────┤
│ 1  │ Pride and Prejudice   │ Jane Austen     │
│ 2  │ 1984                  │ George Orwell   │
│ 3  │ To Kill a Mockingbird │ Harper Lee      │
│ 4  │ Moby-Dick             │ Herman Melville │
└────┴───────────────────────┴─────────────────┘
```

Then let's make a copy of that database, and mutate it as follows:

```sql
DELETE from books WHERE author = "Jane Austen";
UPDATE books SET title = "Animal Farm" where author = "George Orwell";
INSERT INTO books (title, author) VALUES ('The Great Gatsby', 'F. Scott Fitzgerald');
```

Then I can use `sqldiff original.db new.db` to produce a set of queries that would transform `original.db` into the same state as `new.db`:

```sql
INSERT INTO books(id,title,author) VALUES(1,'Pride and Prejudice','Jane Austen');
UPDATE books SET title='1984' WHERE id=2;
DELETE FROM books WHERE id=5;
```

Neat!

There is also a `--changeset` flag that can write a binary output to a file. We can then process that output using the [session API](https://www.sqlite.org/session/intro.html).

When I used the session API to inspect the output, I realized there doesn't appear to be a way to get the column names out of the changeset file. I wondered if the column order matters in the source files, and it seems to: I created two tables that had the same columns in different orders, and `sqldiff` detected this and outputted a plan to delete and recreate the table instead:

```sql
DROP TABLE books; -- due to schema mismatch
CREATE TABLE books (id integer primary key, author text not null, title text not null);
```

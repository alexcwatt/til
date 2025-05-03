# Upserts

MySQL supports upserts with `INSERT ... ON DUPLICATE KEY UPDATE`.

Suppose we have the following schema:

```sql
CREATE TABLE users (
  id INT PRIMARY KEY,
  email VARCHAR(255) UNIQUE,
  phone VARCHAR(20) UNIQUE,
  name VARCHAR(100)
);
```

And that we wish to create or update "alice@example.com" with the name "Alice Lastname"; in other words, we want to upsert by email and set the name.

We can do this as follows:

```sql
INSERT INTO users (email, phone, name)
VALUES ('alice@example.com', '123-456-7890', 'Alice Lastname')
ON DUPLICATE KEY UPDATE
  name = VALUES(name),
  phone = VALUES(phone),
  email = VALUES(email);
```

However, this approach has a significant pitfall: you cannot control which unique constraint triggers the duplicate key logic.

## Problem Illustration

Let's say our table already contains the following rows:

| id | email             | phone        | name  |
|----|-------------------|--------------|-------|
|  1 | alice@example.com | 123-456-7890 | Alice |
|  2 | bob@example.com   | 333-456-7890 | Bob   |

Let's do another upsert that references multiple unique keys:

```sql
INSERT INTO users (email, phone, name)
VALUES ('bob@example.com', '123-456-7890', 'Robert')
ON DUPLICATE KEY UPDATE
  name = VALUES(name),
  email = VALUES(email),
  phone = VALUES(phone);
```

MySQL will check for _any duplicate key violation_, including `id`, `email`, and `phone`. Since we did not specify `id` in the `INSERT`, we will not have a violation there; but there is still a problem in our example. Since the new phone number maches Alice but the email matches Bob, it's ambiguous which rows should be updated.

Depending on which key is detected first, MySQL may update either row!

Both Postgres [^1] and SQLite [^2] have nicer primitives here, allowing you to specify a conflict target.

## Mitigation

There are several mitigation options. For instance, you could always do `INSERT` and handle the duplicate failure with an `UPDATE` that updates based on the unique column of your choice.

## References

[^1]: [Postgres ON CONFLICT documentation](https://www.postgresql.org/docs/17/sql-insert.html#SQL-ON-CONFLICT)
[^2]: [SQLite upsert clause](https://www.sqlite.org/syntax/upsert-clause.html) with `ON CONFLICT` conflict target option.

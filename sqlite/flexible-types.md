# Flexible Types

One of the most surprising things to me about SQLite, when I did a project with it a couple of years ago, is that types are "flexible" by default. You can read more [in the docs](https://www.sqlite.org/flextypegood.html) - I think it's one of the most important surprising things to know when spinning up a project using SQLite.

You can invent your own types - which I guess is useful for making the schema communicate exactly what you want:

```sql
sqlite> CREATE TABLE persons (first_name name, age integer);
```

This will create a table, even though "name" is probably not a valid column type in any other SQL database.

SQLite also offers [STRICT tables](https://www.sqlite.org/stricttables.html), which prevents data from being written to a column if it doesn't match the type - and to use STRICT, the list of supported column types is a short list of types that SQLite knows how to enforce.

If we try using a STRICT table with the same table definition as above, we will get an error:

```sql
sqlite> CREATE TABLE persons (first_name name, age integer) STRICT;
Parse error: unknown datatype for persons.first_name: "name"
```

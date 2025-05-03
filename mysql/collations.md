# MySQL Collations

MySQL collations define what character set is supported, with suffixes to define other characteristics, like sorting and case insensitivity.

Take the following schema, for example:

```sql
CREATE TABLE users (
  name VARCHAR(100) COLLATE utf8mb4_unicode_ci
);
```

`COLLATE utf8mb4_unicode_ci` does two things:
1. Defines the character set as Unicode with `utf8mb4_unicode`
2. Defines the collation as case insensitive with `ci`

The [full docs for collation names](https://dev.mysql.com/doc/refman/8.4/en/charset-collation-names.html) have more detail.

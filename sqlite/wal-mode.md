# WAL Mode

SQLite [WAL Mode](https://www.sqlite.org/wal.html) has a number of advantages, and my team uses it for a SQLite project at work.

I learned, however, that if you open a SQLite file in WAL mode, even if you remember to flush the writes to the SQLite file itself, the WAL mode setting is persistent: If you send a SQLite database to someone else, they too will open it in WAL mode (or so it seems from my experiments).

When sharing SQLite files, it seems nice to disable WAL mode before sharing the database, to prevent confusion. For instance, I had someone modify a SQLite file with WAL mode still enabled; when they did not explicitly flush their changes, and passed the SQLite file to someone else without also sharing the WAL file, it was not apparent to them why the file seemed to be in one state locally and in another state when the other person received it.

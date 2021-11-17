# Database transactions

Invenio uses [SQLAlchemy](https://www.sqlalchemy.org) for all database related operations.

## Transactions are tied to requests

In Invenio, a transaction is tied to an HTTP request. By default, the transaction is
automatically rolled back unless you explicitly call ``db.session.commit()``.

## Exceptions cause rollback

If an exception occurs during request handling, then the entire transaction will be
rolled back unless there has been an explicit call to ``db.session.commit()``
before the exception was raised. This is because the default behavior is to rollback.

## Why are transactions tied to requests?

Transactions are tied to requests, because the outer view, in charge of handling the
request, needs full control of when a transaction is committed. If the view was not
in charge, you could end up with inconsistent data in the database - for instance
persistent identifier may have been committed, but the associated record was not committed.
That is why Invenio makes use of SQLAlchemy’s version counter feature to provide [optimistic
concurrency control](concurrency-control.md) on the records table when the database
transaction isolation level is below repeatable read isolation level.

## When are SQL statements sent to the database server?

SQLAlchemy only sends the SQL statements (INSERT, UPDATE, SELECT, …) to the database
server when needed, or when explicitly requested via e.g. ``db.session.flush()`` or
``db.session.commit()``.

This means that in many cases, SQL INSERT and UPDATE statements are not sent to the
server until a commit is called.

## What about nested transactions?

Nested transactions are using *database save points*, which allow you to do a partial
rollback. Also, nested transactions cause a flush to the database, meaning that
the SQL statements are sent to the server.

## When are partial rollbacks useful?

Partial rollbacks can be useful for instance if you want to try to insert a user,
but the user already exists in the table. Then you can rollback the insert and
instead execute an update statement at the application level.

## When is flushing useful?

Explicitly forcing the flush of SQL statements to the database can be useful
if you need a value from the database (e.g. auto-incrementing primary keys),
and the application needs the primary key to continue. Also, they can be
useful to force integrity constraints to be checked by the database,
which may be needed by the database.

## What happens with exceptions in nested transactions?

If an exception occurs in a nested transaction, first the save point will be
rolled back, and afterwards the entire transaction will be rolled back unless
the exception is caught.

For instance in the following code example, the entire transaction will be rolled back:

```python
@app.route('/')
def index():
    # db operations 1 ....
    with db.session.begin_nested():
        # db operations 2 ....
        raise Exception()
    db.session.commit()
```

On the other hand, in the following example, the propagation of the exception is stopped,
and only the db operations 2 are rolled back, while db operations 1 are committed to
the database.

```python
@app.route('/')
def index():
    # db operations 1 ....
    try:
        with db.session.begin_nested():
            # db operations 2 ....
        raise Exception()
        db.session.commit()
    except Exception:
        db.session.rollback()
    db.session.commit()
```

# Optimistic concurrency control

Invenio makes use of SQLAlchemy's version counter feature to provide optimistic
concurrency control on the records table when the database transaction
isolation level is below repeatable read isolation level (e.g. read committed
isolation level which is the default in PostgreSQL).

Imagine the following sequence of events for two transactions A and B:

1. Transaction A reads existing record 1.
2. Transaction B reads existing record 1.
3. Transaction A modifies record 1.
4. Transaction B modifies record 1.
5. Transaction A commits.
6. Transaction B commits.

### Repeatable read

Under either *serializable* and *repeatable read* isolation level, the
transaction B in step 4 will wait until transaction A commits in step 5, and
then produce an error as well as rollback then entire transaction B - i.e.
transaction B never commits.

### Read committed

Under *read committed* isolation level (which is the default in PostgreSQL),
then again transaction B in step 4 will wait until transaction A commits in
step 5, however transaction B will then try to update the record with the new
value from transaction A.

The JSON document for a record is stored in a single column, thus under
*read committed* isolation level, changes made by transaction A to the JSON
document would be overwritten by transaction B.

To prevent this scenario under *read committed* isolation level, Invenio stores
a version counter in the database table. The fields of the records table looks
like this:

- ``id`` (uuid)
- ``json`` (jsonb)
- ``version_id`` (integer)
- ``created`` (timestamp)
- ``updated`` (timestamp)

When transaction A modifies the record in step 3, it does it with an ``UPDATE``
statement which looks similar to this:

```sql
UPDATE records_metadata
    SET json=..., version_id=2
    WHERE id=1 AND version_id=1
```

When transaction B tries to modify the record in step 4 it uses the same
``UPDATE`` statement. As described above, transaction B then waits until
transaction A commits in step 5. However, now the ``WHERE`` condition (``id=1``
and ``version_id=1``) will no longer match the record's row in the database
(because ``version_id`` is now 2). Thus transaction B will update 0 rows
and make SQLAlchemy throw an error about stale data, and afterwards rollback
the transaction.

Thus, the version counter prevents scenarios that could cause concurrent
transactions to overwrite each other under read committed isolation level.

!!! note

    The version counter does not prevent concurrent transactions to overwrite
    each other's data if you update many records in a single ``UPDATE``
    statement. Normally this is not possible if you use the Invenio Record API.

    If, however, you use the low-level SQLAlchemy model (e.g.
    ``RecordMetadata``) directly, it is possible to execute ``UPDATE``
    statements that update multiple rows at once and you should be very careful
    and be aware of details (or e.g. change your isolation level to repeatable
    read).

### REST API and ETag

The version counter is also used in the REST API to provide concurrency
control. The version counter is provided in an ``ETag`` header when a record is
retrieved via the REST API. When a client then issues an update of a record and
includes the version counter in the ``If-Match`` header, it's checked against the
current record's version and refused if it doesn't match, thus preventing
REST API clients to overwrite each other's changes.

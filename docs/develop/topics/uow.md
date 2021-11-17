# Unit of work

The unit of work is used to group multiple service operations into a single atomic unit. The Unit
of Work maintains a list of operations and coordinates the commit, indexing and
task execution.

The main purpose of the Unit of Work in Invenio is to coordinate when the database
transaction commit is called, and ensure tasks that have to run after the
transaction are executed (such as indexing and running celery tasks).

This ensures that we can group multiple service calls into a single database
transaction and perform the necessary indexing/task execution afterwards.

**When to use?**

You should use the unit of work instead of running an explicit
``db.session.commit()`` or ``db.session.rollback()`` in the code. Basically
any function where you would normally have called a ``db.session.commit()``
should be changed to something like:

```python
from invenio_records_resources.services.uow import \
    RecordCommitOp, unit_of_work,

@unit_of_work()
def create(self, ... , uow=None):
    # ...
    uow.register(RecordCommitOp(record, indexer=self.indexer))
    # ...
    # Do not use `db.session.commit()` in service.
```

Any private method that need to run operations after the database transaction
commit should take the unit of work as input:

```python
def _reindex_something(uow, ...):
    # Index after transaction (no record commit)
    uow.register(RecordIndexOp(record))

def _send_a_task(uow, ...):
    # Run a celery task after the database transaction commit.
    uow.register(TaskOp(my_celery_task, myarg, ... ))
```

**When not to use?**

If you're not changing the database state there's no need to use the unit of
work. Examples include:

- Reading a record
- Search for records
- Reindex all records - because there's no database transaction involved, and
  the method is also not intended to be grouped together with multiple other
  state changing service calls there's no need to use the unit of work.

**How to group multiple service calls?**

In order to group multiple service calls into one atomic operation you can use
the following pattern:

```python
from invenio_records_resources.services.uow import UnitOfWork

with UnitOfWork() as uow:
    # Be careful to always inject "uow" to the service. If not, the
    # service will create its own unit of work and commit.
    service.communities.add(..., uow=uow)
    service.publish(... , uow=uow)
    uow.commit()
```

If you're not grouping multiple service calls, then simply just call the
service method (and it will commit automatically):

```python
service.publish(...)
```

**Writing your own operation?**

You can write your own unit of work operation by subclassing the operation
class and implementing the desired methods:

```python
from invenio_records_resources.services.uow import Operation

class BulkIndexOp(Operation):
    def on_commit(self, uow):
        # ... executed after the database transaction commit ...
```

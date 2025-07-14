# How to create a new job

_Introduced in v13_

This guide walks developers through implementing a new job using the engine provided by the `invenio-jobs` module. Jobs are asynchronous tasks that can be triggered from the admin UI or REST API. They run using Celery and support logging, argument validation, and result tracking.

---

## Prerequisites

- Python development environment set up with InvenioRDM.
- Understanding of Celery tasks and entry points.
- Access to an InvenioRDM instance with administrator rights.
- A **custom Celery scheduler beat** process configured and running, which is required for executing both scheduled and manual jobs. See [Job System Configuration](../ops/jobs/configure.md) for setup instructions.

## 1. Define Your Celery Task

Create your actual business logic as a Celery task:

```python
from celery import shared_task
from your_package import get_records_with_expired_embargoes, lift_embargo, reindex_records

@shared_task
def update_expired_embargoes(since=None, **kwargs):
    """Update and reindex records with expired embargoes."""
    records = get_records_with_expired_embargoes(since)
    for record in records:
        lift_embargo(record)
    reindex_records(records)
```

### Error Handling and Logging

- Use `current_app.logger` for logs visible in the UI.
- Raise `TaskExecutionPartialError` to mark a job as partially successful.

```python
from invenio_jobs.errors import TaskExecutionPartialError
raise TaskExecutionPartialError("Processed 80%, 10 records failed.")
```

## 2. Create a Job Class

Use `JobType` to define a job that wraps your task. This crucial step ensures that your task appears as an selectable option when you choose what job to run within the UI.
You can inherit directly or use the `create()` helper.

```python
from invenio_jobs.jobs import JobType

class UpdateEmbargoesJob(JobType):
    id = "update_expired_embargoes"
    title = "Update expired embargoes"
    description = "Lift and reindex expired embargoes."
    task = update_expired_embargoes

    @classmethod
    def build_task_arguments(cls, job_obj, since=None, **kwargs):
        return {"since": str(since)}
```

To include custom fields in the admin form, define a Marshmallow schema:

```python
from marshmallow import fields, validate
from invenio_jobs.jobs import PredefinedArgsSchema

class ExportEmbargoSchema(PredefinedArgsSchema):
    dry_run = fields.Boolean(
        required=False,
        missing=False,
        metadata={"description": "If true, no changes will be persisted."}
    )

class UpdateEmbargoesJob(JobType):
    id = "update_expired_embargoes"
    title = "Update expired embargoes"
    description = "Lift and reindex expired embargoes."
    task = update_expired_embargoes
    arguments_schema = ExportEmbargoSchema

    @classmethod
    def build_task_arguments(cls, job_obj, since=None, dry_run=False, **kwargs):
        return {
            "since": str(since) if since else None,
            "dry_run": dry_run
        }
```

## 3. Register Your Job and Task

In your `setup.cfg`, register the task and job using entry points:

```ini
[options.entry_points]
invenio_celery.tasks =
    mysite_tasks = mysite.tasks

invenio_jobs.jobs =
    update_expired_embargoes = mysite.jobs:UpdateEmbargoesJob
```
!!! tip

    **Note (local development only):** If you're developing locally and have modified `setup.cfg`, remember to re-run `pipenv run pip install -e ./site` so that entry point changes take effect.

## 4. Run and Monitor Jobs

Once your instance is restarted:

- Navigate to the **Admin Panel → Jobs**.
- Click **Create Job** and fill in the fields:
    - Title and description.
    - Select the task (e.g. `Update Expired Embargoes`).
    - Choose the queue (a default queue should exist if jobs are enabled).
- After saving, you can trigger the job immediately or schedule it.
- You can also inspect previous runs and access detailed logs.

## Tips

- Make your tasks **idempotent** if they might be run concurrently.
- Jobs and their runs are stored in the database, with status, arguments, and logs recorded for traceability.
- Admins only: only superusers can run jobs.
- See [Job system design](../../maintenance/internals/jobs.md) for an explanation of how the system works internally.

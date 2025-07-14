_Introduced in v13_

## Configuring the Job System

### Config flag
To enable the job system, you need to set the following configuration in your `invenio.cfg` file:

```bash
JOBS_ADMINISTRATION_ENABLED=True
```

### Scheduler
The Invenio job system uses a custom celery task scheduler which requires a separate celery beat. You can run the custom beat in a separate container/shell like so:

```bash
celery -A invenio_app.celery beat --scheduler invenio_jobs.services.scheduler:RunScheduler
```

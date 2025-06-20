_added in v13.0.0_

## Configuring the Job System

### Config flag
To enable the job system, you need to set the following configuration in your `invenio.cfg` file:

```bash
JOBS_ADMINISTRATION_ENABLED=True
```

### Scheduler
Invenio Job System uses a custom celery task scheduler which requires you to run a separate - celery beat. You can run the custom beat in a separate container/shell by running:

```bash
celery -A invenio_app.celery beat --scheduler invenio_jobs.services.scheduler:RunScheduler
```

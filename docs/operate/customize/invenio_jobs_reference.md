_added in v13.0.0_

## Job system and vocabulary updates

A powerful new job management system, giving administrators control over background tasks directly from the administration interface. Such tasks include:

- **Vocabulary updates**: automatically updating vocabularies such as affiliations and funders from ROR, names from ORCID, awards from the OpenAIRE Graph, and more.
- **Any recurring celery task**: Any task added to the jobs registry can be run from the administration interface

These tasks can now be scheduled, run on demand, and managed more efficiently through an intuitive interface. You can also monitor the execution status of each job, run history, and logs.

# Job system

The job system allows administrators to manage background tasks directly from the administration interface.

Jobs are predefined tasks that correspond to specific actions in the system. For example, updating vocabularies from external sources such as affiliations from ROR, names from ORCID, etc., or exporting record data dumps of the system in DataCite XML.

These tasks are implemented as Python classes inheriting the `RegisteredTask` class, and define some common attributes and methods that determine how the task appears in the administration interface and how it is parameterized. An example class definition is shown below:

```python
from celery import shared_task
from marshmallow import fields, validate
from invenio_jobs.jobs import JobType


# The Celery task backing the job
@shared_task
def export_records(since=None, serializer="datacite-xml"):
    """Your celery task."""
    serializer = get_serializer(serializer)

    extra_filter = None
    if since:
        extra_filter = dsl.Q("range", created={"gte": since})

    res = records_service.scan(system_identity, extra_filter=extra_filter)
    ts = datetime.now().strftime("%Y%m%dT%H%M%S")
    filename = f"export-{ts}.tgz"
    with open(filename, "w") as fout, tarfile.open(fileobj=fout, mode="w:gz") as tar:
        for record in res:
            data = record.to_dict()
            tar.addfile(tarfile.TarInfo(data["id"]), BytesIO(serializer.dump(data)))


class ExportRecordsArgumentSchema(PredefinedArgsSchema):
    """Your custom schema needed to validate user input from admin form."""
    serializer = fields.String(
        required=False,
        validate=validate.OneOf(["datacite-xml", "datacite-json", "json"]),
        default="datacite-xml",
    ),


# Class definition for integrating with the job system
class ExportRecords(JobType):
    """Export records to DataCite XML."""

    # Display name and description
    title = "Export records"
    description = "Export records to DataCite XML"

    task = export_records

    # Marshmallow schema for the job arguments. This will be used to generate the form
    # in the admininstration interface and as input to build_task_arguments.
    arguments_schema = ExportRecordsArgumentSchema

    @classmethod
    def build_task_arguments(cls, job_obj, since=None, serializer=None):
        """Build the arguments dict based on user input.
        
            Use it to customize how the arguments are serialized or computed before 
            passed to the task. 
        """

        return {
            "since": since,
            "serializer": serializer,
        }
```

This definition then can be registered via the `invenio_jobs.jobs` entrypoint in a module's `setup.cfg` file:

```ini
...

[options.entry_points]
invenio_jobs.jobs =
    export_records = my_site.jobs:ExportRecords

...
```

## Configuring jobs

Jobs are configured under the "Jobs" administration interface. Here, you can see a list of all configured jobs, their status, and last run. You can also run jobs on demand, and/or schedule them to run at a specific time or interval.

For a specific job, on its page you can also see its run history.

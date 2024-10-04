# Upgrading from v4.0 to v6.0

## Prerequisites

The steps listed in this article require an existing local installation of
InvenioRDM 4.0, please make sure that this is given! If unsure, run
`invenio-cli install` from inside the instance directory before executing the
listed steps.

**Note**: Do *not* delete the old Python virtual environment, or the database
migration may complain about missing packages.

!!! warning "Backup"

    Always backup your database and files before you try to perform an upgrade.

## Upgrade steps

!!! warning upgrade your invenio-cli

    Make sure you have the latest invenio-cli, for InvenioRDM v6 release is v1.0.0

### Upgrade your instance dependencies

Bump the RDM version and rebuild the assets:

```bash
invenio-cli packages update 6.0.0
invenio-cli assets build -d
```

### Prepare vocabularies

Before migrating your data, we have to check that it is compatible with the
v6.0 schemas. Note that many changes have been made to enable the use of
vocabularies.

First of all we have to upgrade the DB:

```
pipenv run invenio alembic upgrade
```

Then, we need to fix the previous version vocabularies. For that we are going
to run the migration script and choose option number 1. It is **very important
to follow the steps in order**.

```bash
pipenv run invenio shell $(find $(pipenv --venv)/lib/*/site-packages/invenio_app_rdm -name migrate_4_0_to_6_0.py)

Choose a step:
[1] Migrate old vocabularies
>> 1
```

Another two important new vocabularies are affiliations and subjects. For this
we need to run specific checks:

**Subjects**

```bash
pipenv run invenio shell $(find $(pipenv --venv)/lib/*/site-packages/invenio_app_rdm -name migrate_4_0_to_6_0.py)

Choose a step:
[2] Check record\'s subjects
>> 2
```

This script will check that your subjects are either free text, which requires
no action on your side, or that they should be a custom vocabulary. In the
latter case, a yaml file will be created in your current folder (`custom_subjects.yaml`).

You move this file to the `app_data` folder and create a `vocabularies.yaml`
file. Then you must reference the subjects file, for example:

```yaml
subjects:
  pid-type: sub
  schemes:
    - id: Custom
      name: Custom subjects
      data-file: custom_subjects.yaml
```

The content of this file will be added to your instance's subjects vocabulary
when running the `fixtures` command.

**Affiliations**

```bash
pipenv run invenio shell $(find $(pipenv --venv)/lib/*/site-packages/invenio_app_rdm -name migrate_4_0_to_6_0.py)

Choose a step:
[3] Check creators/contributors affiliations
>> 3
```

This script will check that your creators and contributors affiliations are
either free text, which will require no action on your side, contain a ROR
identifier or that they should be a custom vocabulary.

If the affiliations contain ROR identifiers, you will need to add that
vocabulary. See more details [here](../../customize/vocabularies/affiliations.md). Otherwise, you will need to create a
custom vocabulary in a similar fashion that was done for the subjects above,
or fix your records (remove the identifiers so only the name is preserved).

### Prepare ES

Once the vocabularies have been checked for compatibility and fixed
accordingly, they need to be created:

```bash
pipenv run invenio rdm-records fixtures
invenio-cli run
```

Note that the second command will run your instance. This is needed because
the creation of records and vocabularies is done asynchronously via celery
tasks. To check that they have been created you can use the [RabbitMQ web UI](http://127.0.0.1:15672/) (user: guest, password: guest) or the the `rabbitmqctl`
command line tool:

```bash
# Get the rabbitmq container id
docker ps -a

# Use said id to connect
~ docker exec -it  <CONTAINER_ID> /bin/bash
root@e1cd455eae68$ rabbitmqctl list_queues
celery	0
```

If you see `celery 0` means that all the required tasks have been run. We
recommend you to check the terminal where you run the instance for errors.

The final step to migrate your data is to remove the old ES indices:

```bash
pipenv run invenio index destroy --yes-i-know
```

### Migrate the data

Once the fixtures are present in your system you can migrate your records/drafts:

```bash
pipenv run invenio shell $(find $(pipenv --venv)/lib/*/site-packages/invenio_app_rdm -name migrate_4_0_to_6_0.py)
[4] Migrate records
>> 4
```

The records will be migrated in the database, but now they need to be indexed
in Elasticsearch:

```bash
pipenv run invenio index init
pipenv run invenio rdm-records rebuild-index
```

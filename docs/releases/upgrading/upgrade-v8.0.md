# Upgrading from v7.0 to v8.0


## Prerequisites

The steps listed in this article require an existing local installation of InvenioRDM 7.0, please make sure that this is given!
If unsure, run `invenio-cli install` from inside the instance directory before executing the listed steps.

!!! warning "Backup"

    Always backup your database and files before you try to perform an upgrade.


## Upgrade Steps

!!! warning upgrade your invenio-cli

    Make sure you have the latest `invenio-cli`, for InvenioRDM v8 the release is v1.0.4


### Installing the Latest Versions

Bump the RDM version and rebuild the assets:

```bash
invenio-cli packages update 8.0.0
invenio-cli assets build
```

These commands should take care of locking the dependencies for v8, installing them, and building the required assets.


### Data Migration

After these steps were completed successfully, the data migration can take place:

```bash
# Perform the database migration and update license vocabularies
pipenv run invenio alembic upgrade
pipenv run invenio shell $(find $(pipenv --venv)/lib/*/site-packages/invenio_app_rdm -name migrate_7_0_to_8_0.py)
```

If errors are encountered during the migration, they will be reported and the changes will be rolled back.
In this case, the errors need to be fixed before attempting the upgrade again - if these errors seem too cryptic, don't be afraid to ask for [help](../../develop/getting-started/help.md)!


### Elasticsearch

The last required step is the migration of Elasticsearch indices, because the default license vocabularies have been enriched with icons and need to be re-indexed.

```bash
pipenv run invenio index destroy --yes-i-know
pipenv run invenio index init
pipenv run invenio rdm-records rebuild-index
```

This will ensure that all indices and their contents are based on the latest definitions and not out of date.

As soon as the indices have been rebuilt, the entire migration is complete! 🥳

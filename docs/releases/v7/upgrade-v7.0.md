# Upgrading from v6.0 to v7.0


## Prerequisites

The steps listed in this article require an existing local installation of
InvenioRDM 6.0, please make sure that this is given! If unsure, run
`invenio-cli install` from inside the instance directory before executing the
listed steps.

!!! warning "Backup"

    Always backup your database and files before you try to perform an upgrade.


### Checking the Database Version

Optionally, make sure that you have the latest database table defintions *before* performing the migration.
This can be ensured by trying to upgrade the database:

```bash
pipenv run invenio alembic upgrade
```

The command is expected to do nothing, but it doesn't hurt to check.
The expected output is:

```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
```

If the command gives a different output, the database was likely on an older state and should have been brought up to speed by the command.


### Updating Configuration Variables

**Note**: The DataCite-related configuration values have been renamed in v7!
Please adjust your configurations in `invenio.cfg` as per the following table:

| Old Name                             | New Name             |
| :----------------------------------- | :------------------- |
| `RDM_RECORDS_DOI_DATACITE_ENABLED`   | `DATACITE_ENABLED`   |
| `RDM_RECORDS_DOI_DATACITE_USERNAME`  | `DATACITE_USERNAME`  |
| `RDM_RECORDS_DOI_DATACITE_PASSWORD`  | `DATACITE_PASSWORD`  |
| `RDM_RECORDS_DOI_DATACITE_PREFIX`    | `DATACITE_PREFIX`    |
| `RDM_RECORDS_DOI_DATACITE_TEST_MODE` | `DATACITE_TEST_MODE` |
| `RDM_RECORDS_DOI_DATACITE_FORMAT`    | `DATACITE_FORMAT`    |


Further, the `OAISERVER_ID_PREFIX` needs to be set to the site name (without the protocol, e.g. `inveniordm.web.cern.ch`),
even if you don't intend to use the OAI-PMH feature.
During the migration, the OAI PIDs will be created for each record and this variable ensures that they have meaningful values.


## Upgrade Steps

!!! warning upgrade your invenio-cli

    Make sure you have the latest invenio-cli, for InvenioRDM v7 release is v1.0.0


### Installing the Latest Versions

Bump the RDM version and rebuild the assets:

```bash
invenio-cli packages update 7.0.0
invenio-cli assets build
```

These commands should take care of locking the dependencies for v7, installing them, and building the required assets.


### Data Migration

After these steps were completed successfully, the data migration can take place:

```bash
# Perform the database migration and migrate records
pipenv run invenio alembic upgrade
pipenv run invenio shell $(find $(pipenv --venv)/lib/*/site-packages/invenio_app_rdm -name migrate_6_0_to_7_0.py)
```

#### Errors

If any errors occur during the execution of the migration script, the offending records should be printed by their ID, along with the error messages in question:

```
Migrating records and record parents...
RDMRecord 'q0k7y-7tv15' has a problem, likely with an invalid 'resource_type' value. This should be fixable by changing its metadata in a way that it can be saved successfully.
> Error message: Failed cross checking value_check value ['depositable'] with record value ['linkable'].

Migrating drafts...
Upgrade aborted: There have been problems with the above mentioned records/drafts - please fix them and try the migration again!
```

In this case, the migration is aborted and the database is left as is.
The mentioned records must be fixed manually (usually a matter of manipulating the metadata and saving the records successfully), after which the migration can be retried.


#### Success

If no errors were reported, congratulations on the successful data migration! 🥳


### Elasticsearch

The last required step is the migration of Elasticsearch indices, because there have been smaller changes to the mappings of RDM-Records.

```bash
pipenv run invenio index destroy --yes-i-know
pipenv run invenio index init
pipenv run invenio rdm-records rebuild-index
```

This will create all required indices that were missing and bring the RDM-Records indices up to speed.

As soon as the indices have been rebuilt, the entire migration is complete!


## Edits

*December 7th, 2021*: Added required last step (Elasticsearch) because we *did* find some changes in the mappings, and updated some wording and headings.

*March 3rd, 2022*: Removed the `invenio alembic stamp` command from the upgrade guide, because the command does not actually find out the current revisions for the database.

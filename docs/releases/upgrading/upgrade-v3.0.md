# Upgrading from v2.0 to v3.0


## Prerequisites

The steps listed in this article require an existing local installation of InvenioRDM 2.0, please make sure that this is given!
If unsure, run `invenio-cli install` from inside the instance directory before executing the listed steps.

**Note**: Do *not* delete the old Python virtual environment, or the database migration may complain about missing packages.

!!! warning "Backup"

    Always backup your database and files before you try to perform an upgrade.

!!! warning "Upgrade from v1 to v2"

    If you are upgrading an instance, that you previously upgrade from v1, please
    check the [troubleshooting section](upgrade-v2.0.md#troubleshooting) for
    errors that were discovered in the v1 to v2 upgrade.

## Upgrade Steps

First, the packages are upgraded. Then, the database is migrated and the custom migration script is run. Finally the Elasticsearch indices are rebuilt.

This can be achieved by the following Bash shell commands:

~~~bash
# NOTE: make sure you're in the instance directory

# Upgrade packages
rm Pipfile.lock
sed -i -E 's/2.0.[0-9]+/3.0.0/' Pipfile
invenio-cli install

# Do the migration
pipenv run invenio alembic upgrade
pipenv run invenio shell $(find $(pipenv --venv)/lib/*/site-packages/invenio_app_rdm -name migrate_2_0_to_3_0.py)
pipenv run invenio index destroy --yes-i-know
pipenv run invenio index init
pipenv run invenio rdm-records rebuild-index
~~~

**Configuration**

You should perform the following configuration changes in ``invenio.cfg`` file:

- Remove ``JSONSCHEMAS_HOST``. The variable is no longer used.

- Add ``SITE_UI_URL`` and ``SITE_API_URL`` (you need to change them according
  where you instance is deployed):

```python
SITE_UI_URL = "https://127.0.0.1:5000"

SITE_API_URL = "https://127.0.0.1:5000/api"
```

Note, the configuration variable ``SITE_HOSTNAME`` is still being used, but
is being phased out.

**Enabling new features**

InvenioRDM ships with two new optional features. In order to use them you need
to first enabled them by editing your ``invenio.cfg``

To enable communities you need:

```diff
- COMMUNITIES_ENABLED = False
+ COMMUNITIES_ENABLED = True
```

To enable DOI registration you add the following configuration variables (
you'll will need a contract with DataCite to obtain a username, password and
DOI prefix):

```python
RDM_RECORDS_DOI_DATACITE_ENABLED = True
RDM_RECORDS_DOI_DATACITE_USERNAME = "..."
RDM_RECORDS_DOI_DATACITE_PASSWORD = "..."
RDM_RECORDS_DOI_DATACITE_PREFIX = "10.1234"
RDM_RECORDS_DOI_DATACITE_TEST_MODE = True
```

To disable DOI registration you need to add:

```python
RDM_RECORDS_DOI_DATACITE_ENABLED = False
```

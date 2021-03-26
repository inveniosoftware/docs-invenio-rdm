# Upgrading from v1.0 to v2.0

**Note**: Do *not* delete the old Python virtual environment, or the database migration may complain about missing packages.

First, the current state of the database has to be determined (for the database migration to work).
Then, the new release must be installed and the database has to be migrated.
At last, the records need to be migrated the Elasticsearch indices have to be rebuilt.

This can be achieved by the following commands:

~~~bash
# NOTE: make sure you're in the instance directory
# determine current state of the database
pipenv run invenio alembic stamp
pipenv run invenio alembic upgrade

# upgrade packages
rm Pipfile.lock
sed -e 's/1.0.0/2.0.0/' -i Pipfile
invenio-cli packages lock
invenio-cli install

# do the migration
pipenv run invenio alembic upgrade
pipenv run invenio shell $(find $(pipenv --venv)/lib/*/site-packages/invenio_app_rdm -name migrate_1_0_records_to_2_0.py)
pipenv run invenio index destroy --yes-i-know
pipenv run invenio index init
pipenv run invenio rdm-records rebuild-index
~~~

Alternatively, just download and copy the [upgrade script](./scripts/upgrade-rdm-1.0-to-2.0.sh) into the instance directory, and execute it.

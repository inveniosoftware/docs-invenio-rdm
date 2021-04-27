# Upgrading from v2.0 to v3.0


## Prerequisites

The steps listed in this article require an existing local installation of InvenioRDM 2.0, please make sure that this is given!
If unsure, run `invenio-cli install` from inside the instance directory before executing the listed steps.

**Note**: Do *not* delete the old Python virtual environment, or the database migration may complain about missing packages.


## Upgrade Steps

First, the packages are upgraded. Then, the database is migrated and the custom migration script is run. Finally the Elasticsearch indices are rebuilt.

This can be achieved by the following Bash shell commands:

~~~bash
# NOTE: make sure you're in the instance directory

# Upgrade packages
rm Pipfile.lock
sed -i -E 's/2.0.[0-9]+/3.0.0/' Pipfile
invenio-cli install --pre

# Do the migration
pipenv run invenio alembic upgrade
pipenv run invenio shell $(find $(pipenv --venv)/lib/*/site-packages/invenio_app_rdm -name migrate_2_0_to_3_0.py)
pipenv run invenio index destroy --yes-i-know
pipenv run invenio index init
pipenv run invenio rdm-records rebuild-index
~~~

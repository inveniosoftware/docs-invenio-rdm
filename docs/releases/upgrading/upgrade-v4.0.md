# Upgrading from v3.0 to v4.0


## Prerequisites

The steps listed in this article require an existing local installation of InvenioRDM 3.0, please make sure that this is given!
If unsure, run `invenio-cli install` from inside the instance directory before executing the listed steps.

**Note**: Do *not* delete the old Python virtual environment, or the database migration may complain about missing packages.

!!! warning "Backup"

    Always backup your database and files before you try to perform an upgrade.


## Upgrade Steps

First, the Elasticsearch indices are deleted and the packages are upgraded. Then, the upgrade command will be executed, this will migrate the database, run the custom migration script and rebuild the Elasticsearch indices .

This can be achieved by the following Bash shell commands:

~~~bash
# NOTE: make sure you're in the instance directory

# Delete ES indices
pipenv run invenio index destroy --yes-i-know

# Upgrade packages
invenio-cli packages update 4.0

# We need the server running in another terminal for the next steps
invenio-cli run

# Do the migration
pipenv run invenio rdm-records fixtures
invenio-cli upgrade --script $(find $(pipenv --venv)/lib/*/site-packages/invenio_app_rdm -name migrate_3_0_to_4_0.py)
~~~

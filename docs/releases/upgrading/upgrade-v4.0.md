# Upgrading from v3.0 to v4.0


## Prerequisites

The steps listed in this article require an existing local installation of InvenioRDM 3.0, please make sure that this is given!
If unsure, run `invenio-cli install` from inside the instance directory before executing the listed steps.

**Note**: Do *not* delete the old Python virtual environment, or the database migration may complain about missing packages.

!!! warning "Backup"

    Always backup your database and files before you try to perform an upgrade.


## Upgrade Steps

First, latest `invenio-cli` must be installed. After, the Elasticsearch indices are deleted and the packages are upgraded. Then, the upgrade command will be executed, this will migrate the database, run the custom migration script and rebuild the Elasticsearch indices .

This can be achieved by the following Bash shell commands:

~~~bash
# NOTE: make sure you're in the instance directory

# Upgrade invenio-cli
pip install invenio-cli --upgrade

# Delete ES indices
pipenv run invenio index destroy --yes-i-know

# Upgraded packages
sed -i -E '/invenio = "~=3.4.0"/d' Pipfile
invenio-cli packages update 4.0.0
invenio-cli assets build -d
~~~

We need the server running in another terminal for the next steps, in a new console run:

~~~bash
# NOTE: make sure you're in the instance directory

invenio-cli run
~~~

Now, when the server started, in the previous console run:

~~~bash
# NOTE: make sure you're in the instance directory

# Do the migration
pipenv run invenio rdm-records fixtures
invenio-cli upgrade --script $(find $(pipenv --venv)/lib/*/site-packages/invenio_app_rdm -name migrate_3_0_to_4_0.py)
~~~

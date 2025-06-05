# Create a database migration

All Invenio modules that provide database tables, must in addition to the
SQLALchemy model also provide a database migration recipe which add, remove or
modify the tables.

In the following example, we'll use Invenio-RDM-Records as an example module.

!!! warning "No alembic folder?"
    If the module you are working at does not have the alembic folder it means that there is no branch for it.
    Therefore the first step is to create the branch with the following command:
    `invenio alembic revision --empty --branch <module_name> "<message>"`

## Step 1 - Install development module

First, install your Invenio module in a virtual environment

```
mkvirtualenv rdm-records
pip install -e ".[all,postgresql,elasticsearch7]"
```

## Step 2 - Boot services

Next, boot the containers that you will also use for testing.

Check the exact command to run for booting the services in the ``run-tests.sh``
script.

```
cat ./run-tests.sh
```

Then run the command you found in ``run-tests.sh`` which would look similar to
the one below:

```
eval "$(docker-services-cli up --db ${DB:-postgresql} --search ${SEARCH:-elasticsearch} --mq redis --env)"
```

Last, export an environment variable (``SQLALCHEMY_DATABASE_URI`` gets added by docker-services-cli):

```
export INVENIO_SQLALCHEMY_DATABASE_URI=${SQLALCHEMY_DATABASE_URI}
```

## Step 3 - Upgrade database to latest head

Next, you need to get the database to the head state, so that you can use
Alembic to auto-generate a migration by comparing the code-level models with
the database tables:

```
invenio db drop
invenio alembic upgrade
```

## Step 4 - Find you parent recipe

Next, you need to find the parent recipe which your recipe should depend on.
Run the following command, to show the latest heads for each of the different
branches.

```
invenio alembic heads
```

Note, some migrations may need to depend both on a parent migration recipe
as well as a migration recipe in another module (e.g. a table that creates a
foreign key to a table defined in another module).

## Step 5 - Create the migration recipe

Next, create your recipe:

```
invenio alembic revision -p <id of parent> -d <list of dependent ids> "Create bla bla."
```

Check the output path and move it into your module:

```
mv <path in output> invenio_rdm_records/alembic/
```

Please check the created recipe in detail. You'll as a minimum need to format
the code according to the code style for tests not to break. See also
troubleshooting guide below.

## Step 6 - Update the unit test

Last, you need to update the unit test usually located in
``tests/test_alembic.py`` (test failure should tell you what to update).

Note that, if your module tests are adding mock modules with database tables
you may need to filter those out in the tests.


## Troubleshooting

Often, you'll find your answers by looking in previous migration recipes.

### UUIDType and JSONType

If the tables use ``UUIDType`` or ``JSONType`` you'll need to add an import
to the script:

```python
from sqlalchemy_utils import JSONType, UUIDType
```

### Failing alembic commands

While upgrading your database or trying to auto-generate migrations you may
encounter exceptions from alembic. Often, this can be due to an older broken
migration or failed SQL statement execution. In these cases, you can try to
identify the failing migration and disable the failing parts.

### Can I edit an existing Alembic migration?

You are allowed to edit an existing (i.e. already committed) Alembic migration
if and only if the migration has not been released as part of Invenio Framework
InvenioRDM or InvenioILS.

If you edit a migration that may already be in use in a production system, you
risk to put the that production system in an inconsistent state once the
following migrations are applied.

### command not found: invenio

If the "invenio" command cannot be found, then simply install Invenio-App:

```
pip install invenio-app
```

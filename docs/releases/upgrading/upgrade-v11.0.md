# Upgrading from v10 to v11

## Prerequisites

The steps listed in this article require an existing local installation of InvenioRDM v10, please make sure that this is given!

If unsure, run `invenio-cli install` from inside the instance directory before executing the listed steps.

!!! warning "Backup"

    Always backup your database and files before you try to perform an upgrade.

!!! info "Older versions"

    In case you have an InvenioRDM installation older than v10, you can gradually upgrade using the existing instructions to v9 and afterwards continue from here.

## Upgrade Steps

!!! warning "Upgrade your invenio-cli"

    Make sure you have the latest `invenio-cli`, for InvenioRDM v11 the release is v1.0.14.

    ```bash
    $ invenio-cli --version
    invenio-cli, version 1.0.14
    ```

!!! info "Virtual environments"
    In case you are not inside a virtual environment, make sure that you prefix each `invenio` command with `pipenv run`.

### Upgrade InvenioRDM

Upgrade the RDM version:

```bash
cd <my-site>
# Upgrade to InvenioRDM v11
invenio-cli packages update 11.0.0
# Re-build assets
invenio-cli assets build
```

### Database migration

Execute the database migration:

```bash
# Execute the database migration
invenio alembic upgrade
```

### Data migration

Execute the data migration:

TODO
```bash
```

### Re-index data

Re-index data in the cluster:

```bash
# Recreate indices
invenio index destroy --yes-i-know
invenio index init
```
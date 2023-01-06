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

    Make sure you have the latest `invenio-cli`, for InvenioRDM v11 the release is v1.0.13.

    ```bash
    $ invenio-cli --version
    invenio-cli, version 1.0.13
    ```

For local installations, make sure that you prefix each `invenio` command with `pipenv run`.

### Re-index data

Re-index data in the cluster:

TODO can we use the new command `invenio rdm rebuild-all-indices`?
```bash
# recreate indices
invenio index destroy --yes-i-know
invenio index init
```

Complete the re-indexing of the data in the search cluster. To do so, run the following command in a terminal:

```terminal
invenio rdm rebuild-all-indices
```

### Re-build assets

Create the required folder for custom fields (even if empty) and rebuild the assets:

```bash
# Create custom fields folder
mkdir assets/templates/custom_fields

# Re-build the instance assets
invenio-cli assets build
```

```bash
# Perform the database migration
invenio alembic upgrade
```
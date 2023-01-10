# Upgrading from v10 to v11

## Prerequisites

The steps listed in this article require an existing local installation of InvenioRDM v10, please make sure that this is given!

If unsure, run `invenio-cli install` from inside the instance directory before executing the listed steps.

!!! warning "Backup"

    Always backup your database and files before you try to perform an upgrade.

!!! info "Older versions"

    In case you have an InvenioRDM installation older than v10, you can gradually upgrade using the existing instructions to v10 and afterwards continue from here.

## Upgrade Steps

!!! warning "Upgrade your invenio-cli"

    Make sure you have the latest `invenio-cli`, for InvenioRDM v11 the release is v1.0.14.

    ```bash
    $ invenio-cli --version
    invenio-cli, version 1.0.14
    ```

!!! info "Virtual environments"
    In case you are not inside a virtual environment, make sure that you prefix each `invenio` command with `pipenv run`.

### Python upgrade

As of InvenioRDM v11.0 only Python 3.9 is supported. Therefore you will need to recreate your virtual environment.

the first step is to edit the `<my-site>/Pipfile`:

```diff
[requires]
---python_version = "3.x"
+++python_version = "3.9"
```

**Container images**

Update the base docker image, and rebuild if necessary:

```diff
---FROM inveniosoftware/centos8-python:3.8
+++FROM registry.cern.ch/inveniosoftware/almalinux:1
```

**Local development**

You need to upgrade the Python version to 3.9. However, this step highly
depends on how you have setup your development environment, and there is no
golden rule. One example would be to use PyEnv.

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

Execute the data migration, note that there is no need to re-index the data:

```bash
pipenv run invenio shell $(find $(pipenv --venv)/lib/*/site-packages/invenio_app_rdm -name migrate_10_0_to_11_0.py)
```
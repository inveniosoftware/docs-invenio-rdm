# Upgrading from v11 to v12

## Prerequisites

The steps listed in this article require an existing local installation of InvenioRDM v11, please make sure that this is given!

If unsure, run `invenio-cli install` from inside the instance directory before executing the listed steps.

!!! warning "Backup"

    Always backup your database and files before you try to perform an upgrade.

!!! info "Older versions"

    In case you have an InvenioRDM installation older than v10, you can gradually upgrade using the existing instructions to v10 and afterwards continue from here.

## Upgrade Steps

!!! warning "Upgrade your invenio-cli"

    Make sure you have the latest `invenio-cli`, for InvenioRDM v11 the release is v1.0.20

    ```bash
    $ invenio-cli --version
    invenio-cli, version 1.0.20
    ```

!!! info "Virtual environments"
    In case you are not inside a virtual environment, make sure that you prefix each `invenio` command with `pipenv run`.

**Local development**

Changing the Python version in your development environment highly
depends on your setup, and there is no golden rule.
One example would be to use [PyEnv](https://github.com/pyenv/pyenv).

You should delete your virtualenv before running `invenio-cli` or `pipenv` commands below.

!!! warning "Risk of losing data"

    Your virtual env folder contains uploaded files in InvenioRDM, in `var/instance/data`.
    If you need to keep such files, make sure you copy them over to the new virtual env in the same location.

### Upgrade InvenioRDM

Make sure you that your virtual env is now running with Python 3.9.

Upgrade the RDM version:

```bash
cd <my-site>
# Upgrade to InvenioRDM v12
invenio-cli packages update 12.0.0.beta
pipenv uninstall flask-babelex
# Re-build assets
invenio-cli assets build
```

Optionally, update the file `<my-site>/Pipfile`. This step is not necessary, but suggested for local development.

```diff
[packages]
---invenio-app-rdm = {extras = [...], version = "~=11.0.0"}
+++invenio-app-rdm = {extras = [...], version = "~=12.0.0"}
```

### Database migration

Execute the database migration:

```bash
# Execute the database migration
invenio alembic upgrade
```


### Declare usage statistics processing queues

```shell
invenio queues declare
```

### Update indices mappings

```shell
invenio index update communities-communities-v1.0.0
invenio index update rdmrecords-drafts-draft-v5.0.0
invenio index update rdmrecords-records-record-v5.0.0
```

### Data migration

Execute the data migration, note that there is no need to re-index the data:

```bash
pipenv run invenio shell $(find $(pipenv --venv)/lib/*/site-packages/invenio_app_rdm -name migrate_11_0_to_12_0.py)
```

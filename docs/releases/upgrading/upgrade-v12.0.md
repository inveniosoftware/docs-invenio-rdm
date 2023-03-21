# Upgrading from v11 to v12

## Prerequisites

The steps listed in this article require an existing local installation of InvenioRDM v11, please make sure that this is given!

If unsure, run `invenio-cli install` from inside the instance directory before executing the listed steps.

!!! warning "Backup"

    Always backup your database and files before you try to perform an upgrade.

!!! info "Older versions"

    In case you have an InvenioRDM installation older than v11, you can gradually upgrade using the existing instructions to v11 and afterwards continue from here.

## Upgrade Steps

!!! warning "Upgrade your invenio-cli"

    Make sure you have the latest `invenio-cli`, for InvenioRDM v12 the release is v1.0.20.

    ```bash
    $ invenio-cli --version
    invenio-cli, version 1.0.20
    ```

!!! info "Virtual environments"
    In case you are not inside a virtual environment, make sure that you prefix each `invenio` command with `pipenv run`.

### Installing the Latest Versions

Bump the RDM version and rebuild the assets:

```bash
invenio-cli packages update 12.0.0
```

These commands should take care of locking the dependencies for v12, installing them, and building the required assets.

### Database chema upgrade

Run the database schema upgrade:

```bash
# Perform the database upgrade
pipenv run invenio alembic upgrade
```

### Initialize new queues

Initialize the new queues with:

```bash
# Perform the initialization of the new queues
pipenv run invenio queues declare
```

### Update OS index

Communities schema was expanded with a new attribute and in consequence the mapping needs to be updated accordingly on the fly.

```bash
# Perform the update
curl -X PUT -k -u <your_user>:<your_password> "https://<your_search_host>/es/<your_community_index>/_mapping?pretty" -H 'Content-Type: application/json' -d'{"properties": {"access": {"properties": {"review_policy": {"type": "keyword"}}}}}'
```

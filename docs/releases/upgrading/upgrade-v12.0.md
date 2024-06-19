# Upgrading from v11 to v12

## Prerequisites

The steps listed in this article require an existing local installation of InvenioRDM v11.

!!! warning "Backup"

    Always backup your database and files before you try to perform an upgrade.

!!! info "Older Versions"

    In case you have an InvenioRDM installation older than v11, you can gradually upgrade
    using the existing infrastructure to v11 and afterwards continue from here.

## Upgrade Steps

!!! warning "Upgrade your invenio-cli"

    Make sure you have the latest `invenio-cli` installed. For InvenioRDM v12 it
    is at least v1.2.0

    ```bash
    $ invenio-cli --version
    invenio-cli, version 1.2.0
    ```

!!! info "Virtual environments"

    In case you are not inside a virtual environment, make sure that you prefix each `invenio`
    command with `pipenv run`.


**Local development**

Changing the Python version in your development environment highly
depends on your setup, and there is no golden rule.
One example would be to use [PyEnv](https://github.com/pyenv/pyenv).

You should delete your virtualenv before running `invenio-cli` or `pipenv` commands below.

!!! warning "Risk of losing data"

    Your virtual env folder contains uploaded files in InvenioRDM, in `var/instance/data`.
    If you need to keep such files, make sure you copy them over to the new virtual env in the same location.

### Upgrade InvenioRDM

Make sure that your virtual env is now running with Python 3.9. InvenioRDM v12
is also tested with Python 3.12.

Upgrade the RDM version:

```bash
cd <my-site>

# Upgrade to InvenioRDM v12
invenio-cli packages update 12.0.0
pipenv uninstall flask-babelex

# Re-build assets
invenio-cli assets build
```

Optionally, update the file `<my-site>/Pipfile`.

```diff
[packages]
---invenio-app-rdm = {extras = [...], version = "~=11.0.0"}
+++invenio-app-rdm = {extras = [...], version = "~=12.0.0"}
```

Due to a dependency upgrade update following line.
```diff
---my-site = {editable="True", path="./site"}
+++my-site = {editable=true, path="./site"}
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

CAVEAT: this is not working because of a permission problem in
[invenio-search](https://github.com/inveniosoftware/invenio-search/blob/d8b23ecf48f63d8d313f90fd4618a480e15fbd7b/invenio_search/ext.py#L448).
The only way to solve it is to destroy the index and reinit and rebuild it from
scratch. Yes the statistics will be only stored in the index but the statistic
indices are created by templates and therefore not affected by `invenio index
destroy --yes-i-know`. The statistic indices will remain in the list of indices
and are totally functional also after a reinit.


### Data migration

Execute the data migration

```bash
pipenv run invenio shell $(find $(pipenv --venv)/lib/*/site-packages/invenio_app_rdm -name migrate_11_0_to_12_0.py)
```

### Reindex

```bash
invenio index destroy --yes-i-know
invenio index init
invenio rdm-records rebuild-index
invenio community rebuild-index
# TODO rebuild users
# TODO rebuild groups
# TODO rebuild community members
```

### New roles

```bash
invenio roles create administration-moderation
invenio roles create administration

invenio access allow administration-moderation role administration-moderation
invenio access allow administration-access role administration
invenio access allow superuser-access role administration
```

### New configuration variables

```bash
COMMUNITIES_IDENTITIES_CACHE_REDIS_URL = "URI_TO_REDIS"
USERS_RESOURCES_ADMINISTRATION_ENABLED = True
THEME_SITENAME = "Project name for header and UI"
```

## Big Changes

- remove: dependency of flask-babelex
- add: concept doi (aka parent doi)
- add: statistics. (NOTE: statistic is stored in opensearch/libresearch)
- add: administration panel
- add: set quota
- add: branded communities
- change: the default delimiter for the licenses vocabulary file has been
  changed from ";" to ",". The default licenses are available
  [here](https://github.com/inveniosoftware/invenio-rdm-records/blob/master/invenio_rdm_records/fixtures/data/vocabularies/licenses.csv).
  You can now add and update licenses with `pipenv run invenio rdm-records
  add-to-fixture licenses`



## OPEN PROBLEMS

- users-user-v2.0.0 vs users-user-v1.0.0 indices
  the problem is that user-v1.0.0 does not have the `confirmed_at` attribute
  which is needed in `/api/users`.
  SOLUTION 1:
  ```bash
  invenio index destroy --yes-i-know
  invenio index init
  invenio rdm rebuild-all-indices
  ```
  SOLUTION 2:
  ```bash
  invenio index delete users-user-v1.0.0-NUMBER --force --yes-i-know
  invenio index create users-user-v2.0.0-NUMBER -b path/to/invenio_users_resources/records/mappings/os-v2/users/user-v2.0.0.json
  invenio shell
    from invenio_search.proxies import current_search_client
    current_search_client.indices.put_alias("users-user-v2.0.0-NUMBER", "users-user-v2.0.0")
    current_search_client.indices.put_alias("users-user-v2.0.0-NUMBER", "users")
    exit
  invenio rdm rebuild-all-indices -o users
  ```

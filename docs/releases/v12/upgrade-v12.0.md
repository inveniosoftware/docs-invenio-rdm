# Upgrading from v11 to v12.0

## Prerequisites

The steps listed in this article require an existing local installation of InvenioRDM v11.

!!! warning "Backup"

    Always backup your database and files before you try to perform an upgrade.

!!! info "Older Versions"

    In case you have an InvenioRDM installation older than v11, you can gradually upgrade
    to v11 and afterwards continue from here.

## Upgrade Steps

Make sure you have the latest `invenio-cli` installed. For InvenioRDM v12, it
should be v1.5.0+

```bash
$ invenio-cli --version
invenio-cli, version 1.5.0
```

!!! info "Virtual environments"

    In case you are not inside a virtual environment, make sure that you prefix each `invenio`
    command with `pipenv run`.

**Local development**

Changing the Python version in your development environment highly
depends on your setup, so we won't cover it here.
One way would be to use [PyEnv](https://github.com/pyenv/pyenv).

!!! warning "Risk of losing data"

    Your virtual environment folder a.k.a., `venv` folder, may contain uploaded files. If you kept the default
    location, it is in `<venv folder>/var/instance/data`. If you need to keep those files,
    make sure you copy them over to the new `venv` folder in the same location.
    The command `invenio files location list` shows the file upload location.

If you upgraded your python version, you should recreate your virtual environment before
running `invenio-cli` or `pipenv` commands below.


### Upgrade InvenioRDM

Python 3.9 or 3.11 or 3.12 is required to run InvenioRDM v12.

There are two options to upgrade your system:

#### Upgrade option 1: In-place

This approach upgrades the dependencies in place. Your virtual environment for the
v11 version will be gone afterwards.

```bash
cd <my-site>

# Upgrade to InvenioRDM v12
invenio-cli packages update 12.0.0
pipenv uninstall flask-babelex

# Re-build assets
invenio-cli assets build
```

#### Upgrade option 2: New virtual environment

This approach will create a new virtual environment and leaves the v11 one as-is.
If you are using a docker image on your production instance this will be the
option you choose.

##### Step 1
- create a new virtual environment
- activate your new virtual environment
- install `invenio-cli` by `pip install invenio-cli`

##### Step 2
Update the file `<my-site>/Pipfile`.

```diff
[packages]
---invenio-app-rdm = {extras = [...], version = "~=11.0.0"}
+++invenio-app-rdm = {extras = [...], version = "~=12.0.0"}
```

Due to changes in Pipenv 2024.0.0, update the following line:
```diff
---my-site = {editable="True", path="./site"}
+++my-site = {editable=true, path="./site"}
```

##### Step 3
Update the `Pipfile.lock` file:

```bash
invenio-cli packages lock
```

##### Step 4
Install InvenioRDM v12:

```bash
invenio-cli install
```

### Activate the virtual environment

Before running any `invenio` commands, activate your virtual environment shell:

```bash
$ invenio-cli shell
Launching subshell in virtual environment...
source <path to virtualenvs>/bin/activate
```

This step ensures that all subsequent commands use the correct Python environment and installed dependencies.

!!! note
    If you are upgrading in an environment that does not use a Python virtualenv, you can skip this step.

### Database migration

Execute the database migration:

```bash
invenio alembic upgrade
```

### Declare usage statistics processing queues

```shell
invenio queues declare
```

### Data migration

Execute the data migration:

```bash
invenio shell $(find $(pipenv --venv)/lib/*/site-packages/invenio_app_rdm -name migrate_11_0_to_12_0.py)
```

### Rebuild search indices

```bash
invenio index destroy --yes-i-know
invenio index init
# if you have records custom fields
invenio rdm-records custom-fields init
# if you have communities custom fields
invenio communities custom-fields init
invenio rdm rebuild-all-indices
```

In v12, record statistics will be stored in search indices rather than the
database. These indices are created through some *index templates* machinery
rather than having indices registered directly in `Invenio-Search`. As such, the
search indices for statistics are not affected by `invenio index destroy
--yes-i-know` and are totally functional after the rebuild step.

### New roles

```bash
invenio roles create administration-moderation
invenio roles create administration

invenio access allow administration-moderation role administration-moderation
invenio access allow administration-access role administration
invenio access allow superuser-access role administration
```

### Optional Step

In order to use the domain feature on `/administration`, it is necessary to
carry out the following steps:

```bash
invenio domains create organization
invenio domains create company
invenio domains create mailprovider
invenio domains create spammer
```

### New configuration variables

These are the new configuration variables introduced in this release. Add them to your `invenio.cfg` as needed:

```python
COMMUNITIES_IDENTITIES_CACHE_REDIS_URL = "URI_TO_REDIS"  # Redis URL for caching community identities
USERS_RESOURCES_ADMINISTRATION_ENABLED = True            # Enables the users administration panel
```

## Big Changes

- remove: dependency of flask-babelex
- add: concept doi (aka parent doi)
- add: statistics. (NOTE: statistic is stored in opensearch/libresearch)
- add: administration panel
- add: set quota
- add: branded communities
- add: share options for drafts and records
- add: built-in optional metadata fields
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
  # if you have records custom fields
  invenio rdm-records custom-fields init
  # if you have communities custom fields
  invenio communities custom-fields init
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

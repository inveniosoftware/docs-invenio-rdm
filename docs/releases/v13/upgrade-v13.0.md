# Upgrading from v12 to v13.0

!!! warning "THIS RECIPE IS A WORK IN PROGRESS"

## Prerequisites

The steps listed in this article require an existing local installation of InvenioRDM v12.

!!! warning "Backup"

    Always backup your database and files before you try to perform an upgrade.

!!! info "Older Versions"

    In case you have an InvenioRDM installation older than v12, you can gradually upgrade
    to v12 and afterwards continue from here.

## Upgrade Steps

Make sure you have the latest `invenio-cli` installed. For InvenioRDM v13, it
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
invenio-cli packages update 13.0.0

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
---invenio-app-rdm = {extras = [...], version = "~=12.0.0"}
+++invenio-app-rdm = {extras = [...], version = "~=13.0.0"}
```

##### Step 3
Update the `Pipfile.lock` file:

```bash
invenio-cli packages lock
```

##### Step 4
Install InvenioRDM v13:

```bash
invenio-cli install
```

### Database migration

Execute the database migration:

```bash
invenio alembic upgrade
```

### Data migration


Execute the data migration:

### TODO


### Rebuild search indices

TODO if not destroying and rebuiliding for names we need to update the mappings:
```bash
invenio index update names-name-v2.0.0 --no-check
```

```bash
invenio index destroy --yes-i-know
invenio index init
# if you have records custom fields
invenio rdm-records custom-fields init
# if you have communities custom fields
invenio communities custom-fields init
invenio rdm rebuild-all-indices
```

From v12 onwards, record statistics will be stored in search indices rather than the
database. These indices are created through some *index templates* machinery
rather than having indices registered directly in `Invenio-Search`. As such, the
search indices for statistics are not affected by `invenio index destroy
--yes-i-know` and are totally functional after the rebuild step.

### New roles

### TODO

### New configuration variables

```bash
from invenio_app_rdm import __version__
ADMINISTRATION_DISPLAY_VERSIONS = [
    ("invenio-app-rdm", f"v{__version__}"),
    ("{{ cookiecutter.project_shortname }}", "v1.0.0"),
]
```

## Big Changes

- feature: invenio jobs module, periodic tasks administration panel
- feature: invenio vocabularies entries deprecation
- improvement: search mappings and analyzers to improve performance

### TODO

## OPEN PROBLEMS


### TODO

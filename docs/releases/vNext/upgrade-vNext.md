# Upgrading from v13 to vNext

!!! warning "In Development Upgrade Process"

    These upgrade instructions are a work in progress and are *not likely to work*
    until we get closer to when this version will be released. This document is
    here as a placeholder so InvenioRDM developers can add details as features get added, and
    the upgrade process is not tested until later in the release process.

## Prerequisites

The steps listed in this article require an existing local installation of
InvenioRDM v13.

!!! warning "Backup"

    Always backup your database, statistics indices and files before you try to perform an upgrade.

!!! info "Older Versions"
    If your InvenioRDM installation is older than v13, you must first upgrade
    to v13 before proceeding with the steps in this guide.

## Upgrade Steps

Make sure you have the latest `invenio-cli` installed. For InvenioRDM vNext,
it should be v1.9.0+.

```bash
$ invenio-cli --version
invenio-cli, version 1.9.0
```

!!! info "Virtual environments"

    In case you are not inside a virtual environment, make sure that you prefix each `invenio`
    command with `pipenv run`.

### Upgrade InvenioRDM

#### Requirements
Python 3.9 or 3.11 or 3.12 is required to run InvenioRDM v13.

!!! info "Python 3.9 end-of-life"
    Official support for Python 3.9 will end on October 31, 2025.
    See the [official Python version status page](https://devguide.python.org/versions/) for more information.
    Future releases of InvenioRDM will require a more recent Python version.

The minimum required OpenSearch version is now **v2.12**. See [below](#opensearch-version) on how to upgrade older versions.

#### Upgrade option 1: In-place
This approach upgrades the dependencies in place. At the end of the process,
your virtual environment for the v13 version will be completely replaced
with the vNext environment and dependencies.

```bash
cd <my-site>

# Upgrade to InvenioRDM vNext
invenio-cli packages update Next
# Re-build assets
invenio-cli assets build
```

#### Upgrade option 2: New virtual environment

This approach will create a new virtual environment and leaves the v13 one as-is.
If you are using a docker image on your production instance this will be the
option you choose.

!!! warning "Risk of losing data"

    Your virtual environment folder a.k.a., `venv` folder, may contain uploaded files. If you kept the default
    location, it is in `<venv folder>/var/instance/data`. If you need to keep those files,
    make sure you copy them over to the new `venv` folder in the same location.
    The command `invenio files location list` shows the file upload location.

##### Step 1

- create a new virtual environment
- activate your new virtual environment
- install `invenio-cli` by running `pip install invenio-cli`

##### Step 2

Update the `<my-site>/Pipfile` by changing the `version` of `invenio-app-rdm`
to `~=Next` and removing the unnecessary `postgresql` extra
(it is already installed by default and will trigger a warning if left in the file):

```diff
[packages]
---invenio-app-rdm = {extras = [..., "postgresql"], version = "~=12.0.0"}
+++invenio-app-rdm = {extras = [...], version = "~=Next"}
```

##### Step 3

Update the `Pipfile.lock` file:

```bash
invenio-cli packages lock
```

##### Step 4

Install InvenioRDM vNext:

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

### Data migration

Execute the data migration:

```bash
invenio shell $(find $(pipenv --venv)/lib/*/site-packages/invenio_app_rdm -name migrate_13_0_to_Next.py)
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

From v12 onwards, search indices for statistics (record's views and downloads) are not
affected by `invenio index destroy --yes-i-know` and are totally functional after the rebuild step.

!!! info "Permission issue"
    If you encounter an error similar to this when indexing:
    ```
    opensearchpy.exceptions.AuthorizationException: AuthorizationException(403, 'security_exception', 'no permissions for [cluster:admin/component_template/put] and User [name=<my-name>, backend_roles=[], requestedTenant=null]')
    opensearchpy.exceptions.AuthorizationException: AuthorizationException(403, 'security_exception', 'no permissions for [indices:admin/index_template/put] and User [name=<my-name>, backend_roles=[], requestedTenant=null]')
    ```
    This means your OpenSearch user does not have sufficient permissions to create or update index templates.
    To resolve this, grant the necessary permissions to your user in the OpenSearch cluster:

      1. Go to **OpenSearch Dashboards** -> **Security** -> **Roles** -> *<your role name>*.
      2. Edit the role and add the following cluster and index permissions:
         - `cluster:admin/component_template/put`
         - `indices:admin/index_template/put`

## Infrastructure/configuration changes

### Required changes

### Optional changes

#### Deprecations

#### New configuration variables

These are the new configuration variables introduced in this release. Make sure that you read the related documentation before enabling them. Add them to your `invenio.cfg` as needed:


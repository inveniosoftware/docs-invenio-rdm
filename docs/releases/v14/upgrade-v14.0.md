# Upgrading from v13 to v14

## Background and prerequisites

This article details the low-level steps to follow to upgrade your InvenioRDM v13 instance to v14.0.

Version 14 introduces a number of default tooling changes (`pipenv` -> `uv`, `npm` -> `pnpm`, ...) and recommends using Python 3.14. Previous tools and Python versions will still work with this release, but this is the last release where we document the upgrade process with the old and new tools. Future releases will only detail the upgrade steps using the new default tools. Don't worry, we point to documentation to upgrade those aspects too.

As usual, these steps do assume an existing installation of InvenioRDM v13, the previous version.
If your InvenioRDM installation is older than v13, you must first upgrade
to v13 before proceeding with the steps in this guide. However, it doesn't assume you are necessarily on [v13.1](../v13/version-v13.1.0.md), and the instructions will work wether you are on v13.0.x or v13.1.y.

The throughline of this article is a sequential series of steps to execute. **Do read** the optional sections as they indicate changes to apply even if NOT adopting change. We highly recommend running the steps in a local development environment first where experience from the particularities of your instance can be gained without data loss worry. Then we recommend you run the steps into a staging environment mirroring your production deployment and accrue further insight into specificities to your environment (or missing details in these update steps!). Equipped with that knowledge, running the steps on your production environment should be smooth.

!!! warning "Backup"

    Always backup your database, statistics indices and files before you try to perform an upgrade.

## Switch from pipenv to uv — optional but recommended

Although not strictly necessary for this upgrade, we highly encourage you to switch to [uv](https://docs.astral.sh/uv/) from [pipenv](https://pipenv.pypa.io/) for your Python package and project manager, for improvements in speed, ergonomics, and [security](https://docs.astral.sh/uv/concepts/resolution/#dependency-cooldowns). Future releases will only document steps using `uv` commands and may remove support for `pipenv`.

See the dedicated [Pipenv-to-uv migration guide](../uv-upgrade.md), which includes a helper script that converts your `Pipfile` to `pyproject.toml`, updates the `site/` package, and adjusts `.invenio` (`python_package_manager = uv`).

If you want to keep using pipenv for now AND you want to use the recommended base Docker image for InvenioRDM v14 in your Dockerfile, you will need to edit your Dockerfile to install `pipenv` (it is not installed in the base image anymore):

```dockerfile
FROM <v14 base image of your choice>

RUN pip install pipenv

# keep the rest of your Dockerfile as it was with calls to pipenv
```

## Switch to supported Python version — required if not already done

With the end-of-life of Python 3.9 in October 2025, InvenioRDM v14 recommends using Python 3.14 for its performance improvements and future-facing features. Python versions still supported by the Python community but below 3.14 (3.10, 3.11, 3.12, 3.13) *may* work but with varying levels of certainty. With high confidence Python 3.11 will work for instance. On the other hand, Python 3.10 has never been recommended and always faced issues, so it will likely not work. Details below take Python 3.14 as the example version to upgrade to.

1.  Install Python 3.14 so it can be used by your application (including in new [virtualenv](../../reference/virtualenvs.md) created by invenio-cli). We only list two methods here — the internet is rife with other examples.

    ```bash
    # with uv
    uv python install 3.14
    # OR with the pyenv tool (https://github.com/pyenv/pyenv)
    pyenv install 3.14
    ```

2.  Change the required Python version in `pyproject.toml` if using `uv` or `Pipfile` if still using `pipenv`.

    **pyproject.toml**

    ```toml
    # Set this line
    requires-python = "~=3.14.0"
    ```

    **Pipfile**

    ```ini
    [requires]
    # Set this line
    python_version = "3.14"
    ```

3.  Regenerate the lock file

    ```bash
    # with uv
    uv lock --refresh
    # with pipenv
    pipenv lock
    ```

    You will then want to use a new virtualenv like [detailed below](#upgrade-option-2-new-virtual-environment). At this point you may want to re-install the v13 packages in this new environment just to make sure your instance is compatible with Python 3.14 and resolve any issues specific to that if any. Keep in mind that InvenioRDM v14 may resolve some too.

4.  Change the `FROM` line in your Dockerfile to a base image using Python 3.14

    ```Dockerfile
    # TODO: Fill with appropriate source
    FROM ghcr.io/...
    ```

## Switch from npm to pnpm — optional but recommended

[Pnpm](https://pnpm.io/) is now the recommended tool to manage Javascript dependencies in InvenioRDM (don't worry npm still works) because it is much faster, [has better protection against supply chain attacks](https://pnpm.io/supply-chain-security), and has good community support. If you have it installed, `invenio-cli` and lower level `invenio` commands will use it under the hood.

1. Locally, simply install [pnpm](https://pnpm.io/installation) version 10 (working version at time of writing).

2. Make sure to set "pnpm" as your invenio javascript package manager in `.invenio`.

```ini
[cli]
# set this line or remove it altogether
javascript_package_manager = pnpm
```

You could remove the line altogether since pnpm is the new default if that line is not present.

Generate the lockfile with `invenio-cli assets lock` and commit the resulting `pnpm-lock.yaml` and `package.json` at the project root. Re-run `assets lock` whenever your JavaScript dependencies change.

That's it, faster JavaScript package resolutions are yours now!

!!! info "Building production Docker images with pnpm"

    - Ensure the image has Node.js ≥18.12 and `pnpm` installed (the `inveniosoftware/almalinux:1` base image ships Node 16, so switch its `nodejs` module stream to `22` and install `pnpm` via `npm install -g pnpm@<version>`).
    - For best layer-cache reuse, run `pnpm install --frozen-lockfile --shamefully-hoist` in its own layer, fed only by `package.json` + `pnpm-lock.yaml`, placed above any layer that copies frequently-changing source.

## Switch from webpack to Rspack — optional but recommended

Switch from `webpack` to [Rspack](https://www.rspack.dev/) for asset bundling. Its Rust-based builds are much faster and drop-in compatible with the existing Invenio asset pipeline. In your `invenio.cfg`:

```python
WEBPACKEXT_PROJECT = "invenio_assets.webpack:rspack_project"
WEBPACKEXT_NPM_PKG_CLS = "pynpm:PNPMPackage"  # only when also using pnpm
```

The second flag tells `flask-webpackext` which `pynpm` class to use when invoking the package manager, so set it whenever you also enable pnpm.

## Upgrade to InvenioRDM v14 proper — required

Here are the core sequential steps to upgrade to InvenioRDM v14.

!!! info "Virtual environments"

    All commands below assume you are running them according to their installation environments. Typically it means `invenio` commands should be executed inside the application's virtual environment or via `pipenv run` or `uv run` in case you are not inside a virtual environment or environment with executables installed globally.

### Upgrade invenio-cli

Make sure you have the latest `invenio-cli` installed. For InvenioRDM v14,
it should be v1.12.0.

```bash
$ invenio-cli --version
invenio-cli, version 1.12.0
```

### Upgrade packages
#### Step 1: New virtual environment

This approach will create a new virtual environment and leaves the v13 one as-is.
If you are using a docker image on your production instance this will be the
option you choose.

!!! warning "Risk of losing data"

    Your virtual environment folder a.k.a., `venv` folder, may contain uploaded files. If you kept the default
    location, it is in `<venv folder>/var/instance/data`. If you need to keep those files,
    make sure you copy them over to the new `venv` folder in the same location.
    The command `invenio files location list` shows the file upload location.

- create a new virtual environment
- activate your new virtual environment
- install `invenio-cli` by running

```bash
# if using uv
uv pip install invenio-cli

# if using pipenv
pip install invenio-cli
```

#### Step 2

Change the version of `invenio-app-rdm` to 14.0 in `<my-site>/pyproject.toml` or `<my-site>/Pipfile`:

**Pipfile**
```diff
[packages]
---invenio-app-rdm = {extras = [...], version = "~=13.0.0"}
+++invenio-app-rdm = {extras = [...], version = "~=14.0.0"}
```

**pyproject.toml**
```diff
dependencies = [
---    invenio-app-rdm[opensearch2]~=13.0.0",
+++    invenio-app-rdm[opensearch2]~=14.0.0",
```

#### Step 4

Install InvenioRDM v14:

```bash
invenio-cli install
```


### Apply database migrations

The database migration consists of three steps:

- check about existing `alembic_version` table
- pre-migration step that cleans up the existing database schema
- Alembic upgrade to the v14 schema

#### Check your database for the `alembic_version` table

InvenioRDM v13 contained a race condition that, in some cases, prevented the `alembic_version` table from being created in the database. [Alembic](https://alembic.sqlalchemy.org/) uses this table to track database schema migrations, and you cannot upgrade to v14 without it.

To check whether your database has the `alembic_version` table, log in to the database and run the following SQL query:

```sql
SELECT * FROM alembic_version;
```

If you get `ERROR: relation "alembic_version" does not exist`, the table is missing and you must create it before proceeding.

To create the table, you need to run the command on the InvenioRDM server. The server **must** be using the same source code version as the one used to install the current database schema. In other words, if you upgraded the source code to a newer v13 release after installation, the source code and database schema may be out of sync and you **cannot** safely use the command below. If that is your situation, please ask for help on our Discord server.

On the server, run the following command to create the `alembic_version` table:

```bash
# if using uv
uv run invenio alembic stamp

# if using pipenv
pipenv run invenio alembic stamp
```

Afterwards, check the `alembic_version` table again to confirm that the operation completed successfully.


#### Run the pre-migration step

Run one of the following commands, depending on whether your installation uses `uv` or `pipenv`:

```bash
# if using uv
invenio shell $(find $(dirname $(dirname $(uv python find)))/lib/*/site-packages/invenio_app_rdm -name prepare_migration_13_0_to_14_0.py)
# if using pipenv
invenio shell $(find $(pipenv --venv)/lib/*/site-packages/invenio_app_rdm -name prepare_migration_13_0_to_14_0.py)
```

If the script completes successfully, it should end with output similar to the following:

```
...

    v13 -> v14 database cleanup completed successfully.

    Please run:

        invenio alembic upgrade

    to finish the database structure migration process. Then continue with the data migration script.
```

#### Run the schema migration step

Once the pre-migration step has completed successfully, run the Alembic migration to update the database schema:

```bash
invenio alembic upgrade
```

### Apply data changes

Execute the data migration script to update the content of the DB:

```bash
# if using uv
invenio shell $(find $(dirname $(dirname $(uv python find)))/lib/*/site-packages/invenio_app_rdm -name migrate_13_to_14.py)
# if using pipenv
invenio shell $(find $(pipenv --venv)/lib/*/site-packages/invenio_app_rdm -name migrate_13_to_14.py)
```


### Update document engine mappings and content

Many mappings have been updated in this release. You can perform granular changes if you want to avoid downtimes or simply discard and rebuild the indices in one go.


**Discard and rebuild indices**
```bash
invenio index destroy --yes-i-know
invenio index init
# if you have records custom fields
invenio rdm-records custom-fields init
# if you have communities custom fields
invenio communities custom-fields init
invenio rdm rebuild-all-indices
```

#### OAI-PMH percolator mapping update

!!! note "TODO: Should become a CLI command"

    Running this part as a script is a temporary solution until it can be integrated
    into an `invenio` CLI command.

```python
from flask import current_app
from invenio_access.permissions import system_identity
from invenio_oaiserver.percolator import _build_percolator_index_name
from invenio_rdm_records.proxies import current_rdm_records
from invenio_search.proxies import current_search_client
from invenio_search.utils import build_alias_name

index = current_app.config["OAISERVER_RECORD_INDEX"]
percolator_index = _build_percolator_index_name(index)
record_index = build_alias_name(index)

# Fetch the mapping from the "live" index (this will include custom fields)
record_mapping = current_search_client.indices.get_mapping(index=record_index)
assert len(record_mapping) == 1
percolator_mappings = list(record_mapping.values())[0]["mappings"]

# Update the mapping
current_search_client.indices.put_mapping(
    index=percolator_index,
    body=percolator_mappings,
)

# Reindex all percolator queries from OAISets
oaipmh_service = current_rdm_records.oaipmh_server_service
oaipmh_service.rebuild_index(identity=system_identity)

#### Job Logs Index Template Update

The job logs datastream index template has been updated to explicitly map two new context fields used for task tracking:

- `task_id` — unique identifier for the Celery task that produced the log
- `parent_task_id` — identifier of the parent task (null for root tasks, set for subtasks)

Because the datastream index has `"dynamic": true` on the `context` object, existing indexed logs are unaffected.

1. **Update the index template** — add the two new fields under `mappings.properties.context.properties` of the `<PREFIX>-job-logs-v1.0.0` template.
   Done with the `invenio index init`

2. **Trigger a rollover of the datastream** — this creates a new backing index using the updated template, cleanly separating old and new log documents.

    Via the OpenSearch Dashboards UI: navigate to **Index Management → Data Streams**, find the `<PREFIX>-job-logs` datastream, click **Actions** (top right) and select **Roll over**.

    Or via curl:

    ```bash
    curl -X POST "http://<OPENSEARCH_HOST>/<PREFIX>-job-logs/_rollover"
    ```


### Update vocabularies

A number of out-of-the-box vocabularies have been enhanced with terms from the DataCite 4.4-4.7 releases, as well as other mapping improvements and translations. In order to update these in your repository, you'll need to reload their fixtures with `invenio rdm-records add-to-fixture <vocabulary fixture>`. The `<vocabulary fixture>` for vocabularies that have updates are:

- datetypes
- descriptiontypes
- licenses
- relationtypes
- resourcetypes
- contributorsroles
- creatorsroles
- titletypes
- removalreasons

For instance, you will want to run: `invenio rdm-records add-to-fixture detetypes`, then `invenio rdm-records add-to-fixture descriptiontypes`, and so on.

If you've customized any of these vocabularies for your instance, you will need to merge changes from the [source files in invenio-rdm-records](https://github.com/inveniosoftware/invenio-rdm-records/tree/master/invenio_rdm_records/fixtures/data/vocabularies) into the custom vocabulary files in your instance before running the `add-to-fixture` command.


## Update your configuration or infrastructure — necessity depends on your instance

This last section highlights the changes to your configuration or infrastrcuture that you should assess. It's the last series of tweaks you want to assess and apply or not to your environment.

### invenio-cli run --host ... --port ...

When running `invenio-cli run` with `--host`/`--port` passed on the command line or host/port defined in `.invenio.private`, it used to be that those values would override `SITE_UI_URL` and `SITE_API_URL`. This is no longer the case in order to allow for listening on a host/port (defined by passed host and port) different than the host/port used to generate the URLs. This is a common situation when listening on 0.0.0.0 and using the exact IP or fully qualified domain name for URL generation. As such you need to provide the appropriate `SITE_UI_URL` and `SITE_API_URL` values for your environment which typically means:

```diff
-SITE_UI_URL = "https://127.0.0.1"
+SITE_UI_URL = "https://127.0.0.1:5000"

-SITE_API_URL = "https://127.0.0.1/api"
+SITE_API_URL = "https://127.0.0.1:5000/api"
```

### Overridable IDs in the deposit form

To improve consistency in naming conventions and structure, some IDs of Overridables in the deposit form have been modified. If you are overriding any of these components, you will need to change the ID in your mapping file to reflect these modifications.

The full list of ID changes [can be found here](https://github.com/inveniosoftware/invenio-rdm-records/pull/2101/files#diff-ff3c479edefad986d2fe6fe7ead575a46b086e3bbcf0ccc86d85efc4a4c63c79).

If you are not overriding any of these components, you do not need to change anything.

### Custom field widget prop names

Many [custom field widgets](../../operate/customize/metadata/custom_fields/widgets.md) used the `icon` and `description` props, which have now been deprecated and replaced with `labelIcon` and `helpText` respectively. This is to improve consistency with the naming of the built-in fields used in the deposit form and thereby avoid confusion. The old names will continue to function for now, but we recommend updating to the new names where applicable.

### Related Identifiers

Backend and frontend functionality has been extended to cover related identifiers. The new `RDM_RECORDS_RELATED_IDENTIFIERS_SCHEMES` setting defines which schemes can be used (defaulting to `RDM_RECORDS_IDENTIFIERS_SCHEMES`). Validation rules, vocabularies in the UI, and scheme label resolution have been updated to ensure identifiers and related identifiers are handled consistently.

### HTTP User-Agent handling

Outbound HTTP requests performed by invenio-vocabularies datastream readers (e.g. OpenAIRE, ROR) now use a centralized HTTP User-Agent helper (`invenio_user_agent`).

No action is required for existing installations. Deployments may optionally review or customize the `SITE_HOSTNAME` and `SITE_UI_URL` configuration values to control the User-Agent string sent to external services.

### Comment replies preview

The new feature of allowing replies to comments available in all requests introduces a new config variable `REQUESTS_COMMENT_PREVIEW_LIMIT`, limiting the number of retrieved indexed documents when comments have many replies.

### Locking/Unlocking a request's conversation

The new feature of allowing locking/unlocking a request's conversation is controlled via a feature flag config variable `REQUESTS_LOCKING_ENABLED`.

### Community reviews for each record version

The new feature of requiring community reviews for each version of a record (rather than just the first) must be [manually configured](../../operate/customize/requests.md#require-reviews-for-each-record-version).
The default behaviour remains unchanged.

### Deprecated GitHub integration

The [`invenio-github`](https://github.com/inveniosoftware/invenio-github) module has been deprecated.
You can continue to use it for now, but it will be fully removed in InvenioRDM v15.

It has been replaced with the new [`invenio-vcs`](https://github.com/inveniosoftware/invenio-vcs) module.

Unlike `invenio-github`, `invenio-vcs` is an optional dependency and must be added to your instance-level dependencies.
There are also some steps involved if you wish to migrate existing `invenio-github` data to `invenio-vcs`.

Please see [this detailed guide](https://github.com/inveniosoftware/invenio-vcs/blob/master/docs/upgrading.rst) for more information on how to upgrade.
This is only necessary if your instance was actively using `invenio-github` (with at least one user having connected their GitHub account) **and**
you want to keep the existing data.

See also the [documentation on how to configure the new module](../../operate/customize/code_archival.md).

That's it, you have upgraded to InvenioRDM v14!


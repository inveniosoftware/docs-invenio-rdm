# Upgrading from v13 to v14

## Background and prerequisites

This article details the low-level steps to follow to upgrade your InvenioRDM v13 instance to v14.0.

Version 14 introduces a number of default tooling changes (`pipenv` -> `uv`, `npm` -> `pnpm`, ...) and recommends using Python 3.14. Previous tools and Python versions will still work with this release, but this is the last release where we document the upgrade process with the old and new tools. Future releases will only detail the upgrade steps using the new default tools. Don't worry, we point to documentation to upgrade those aspects too.

As usual, these steps do assume an existing installation of InvenioRDM v13, the previous version.
If your InvenioRDM installation is older than v13, you must first upgrade
to v13 before proceeding with the steps in this guide. However, it doesn't assume you are necessarily on [v13.1](../v13/version-v13.1.0.md), and the instructions will work wether you are on v13.0.x or v13.1.y.

The throughline of this article is a sequential series of steps to execute. We highly recommend running the steps in a local development environment first where experience from the particularities of your instance can be gained without data loss worry. Then we recommend you run the steps into a staging environment mirroring your production deployment and accrue further insight into specificities to your environment (or missing details in these update steps!). Equipped with that knowledge, running the steps on your production environment should be smooth.

!!! warning "Backup"

    Always backup your database, statistics indices and files before you try to perform an upgrade.

## Switch from pipenv to uv — optional but recommended

Although not strictly necessary for this upgrade, we highly encourage you to switch to [uv](https://docs.astral.sh/uv/) from [pipenv](https://pipenv.pypa.io/) for your Python package and project manager. Future releases will only document steps using `uv` commands and may remove support for `pipenv`.

TODO: Insert link to uv upgrade documentation from https://github.com/inveniosoftware/docs-invenio-rdm/pull/843


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

TODO: adapt text to reflect Python 3.14 being recommended or a requirement based on July discussion

## Switch from npm to pnpm — optional but recommended

[Pnpm](https://pnpm.io/) is now the recommended tool to manage Javascript dependencies in InvenioRDM (don't worry npm still works) because it is much faster and has good community support. If you have it installed, `invenio-cli` and lower level `invenio` commands will use it under the hood.

1. Locally, simply install [pnpm](https://pnpm.io/installation) version 10 (working version at time of writing).

2. Make sure to set "pnpm" as your invenio javascript package manager in `.invenio`.

```ini
[cli]
# set this line or remove it altogether
javascript_package_manager = pnpm
```

You could remove the line altogether since pnpm is the new default if that line is not present.

That's it, faster javascript package resolutions are yours now!

## Upgrade to InvenioRDM v14 proper — required

Here are the core sequential steps to upgrade to InvenioRDM v14.

!!! info "Virtual environments"

    All commands below assume you are running them according to their installation environments. Typically it means `invenio` commands should be executed inside the application's virtual environment or via `pipenv run` or `uv run` in case you are not inside a virtual environment or environment with executables installed globally.

### Upgrade invenio-cli

Make sure you have the latest `invenio-cli` installed. For InvenioRDM v14,
it should be v1.12.0+. (TODO: release v1.12)

```bash
$ invenio-cli --version
invenio-cli, version 1.12.0
```

### Upgrade packages
#### Upgrade option 1: In-place

This approach upgrades the dependencies in place. At the end of the process,
your virtual environment for the v13 version will be completely replaced
with the v14 environment and dependencies.

```bash
cd <my-site>

# Upgrade to InvenioRDM vNext
invenio-cli packages update v14
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

##### Step 3

Update the lock file (whether `uv` or `pipenv`):

```bash
invenio-cli packages lock
```

##### Step 4

Install InvenioRDM v14:

```bash
invenio-cli install
```

#### Activate the virtual environment

Before running any `invenio` commands, activate your virtual environment shell:

```bash
$ invenio-cli shell
Launching subshell in virtual environment...
source <path to virtualenvs>/bin/activate
```

This step ensures that all subsequent commands use the correct Python environment and installed dependencies.

!!! note
    If you are upgrading in an environment that does not use a Python virtualenv, you can skip this step.


### Apply database migrations

Execute the database migrations to update table schemas:

```bash
invenio alembic upgrade
```

TODO: Fill with more advanced migration command of this version that fixes migration histories

### Apply data changes

Execute the data migration script to update the content of the DB:

```bash
# if using uv
invenio shell $(find $(dirname $(dirname $(uv python find)))/lib/*/site-packages/invenio_app_rdm -name migrate_13_to_14.py)
# if using pipenv
invenio shell $(find $(pipenv --venv)/lib/*/site-packages/invenio_app_rdm -name migrate_13_to_14.py)
```
TODO: create migrate_13_to_14.py script

#### OAuth client changes

The `extra_data` column of the `oauthclient_remoteaccount` table, storing remote-specific user information as required by various integrations, has been migrated from the `JSON` type to the `JSONB` type (only on PostgreSQL databases).
This gives significant performance improvements when running certain queries.
An automated Alembic migration is included and has been executed when you ran the [database migration](#apply-database-migrations) step above.

However, if your `oauthclient_remoteaccount` table has more than ~50k rows and you are unable to take the system offline offline for an update, this operation could overload your database and create a lock lasting several minutes, due to the need to individually transform every row.
To avoid issues in such cases, we recommend instead running the migration manually.
Please follow [the upgrade guide](https://invenio-oauthclient.readthedocs.io/en/latest/upgrading.html#v6-0-0).

### Update document engine mappings and content

Many mappings have been updated in this release. You can perform granular changes if you want to avoid downtimes or simply discard and rebuild the indices in one go.

TODO: Check if it is indeed the case that the discard and rebuild is enough

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

OR

**Granular changes**

Apply these granular changes:

- `invenio index update --no-check rdmrecords-records-record-v7.0.0` (for record deletion feature)
- `invenio index update --no-check rdmrecords-drafts-draft-v6.0.0` (for record deletion feature)
- Update OAI-PMH percolators index for records by using the [recipe below](#oai-pmh-percolator-mapping-update) (for record deletion feature)
- `invenio index update --no-check requests-request-v1.0.0` (for commenting, curation, and record deletion)
- Update the job logs index template by using the [recipe below](#job-logs-index-template-update) (for job logs changes)
- `invenio index update --no-check requestevents-requestevent-v1.0.0` (for commenting)
- Update all comment request events in the live index by running the [recipe below](#comment-events-update)
- `invenio index update communitymembers-members-member-v1.0.0 --no-check` (for request to join community)
- `invenio index update communitymembers-archivedinvitations-archivedinvitation-v1.0.0 --no-check` (for request to join community)
- `invenio rdm-records rebuild-all-indices --order requests` (for request commenting)

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
```

#### Job Logs Index Template Update

The job logs datastream index template has been updated to explicitly map two new context fields used for task tracking:

- `task_id` — unique identifier for the Celery task that produced the log
- `parent_task_id` — identifier of the parent task (null for root tasks, set for subtasks)

Because the datastream index has `"dynamic": true` on the `context` object, existing indexed logs are unaffected. However, to ensure the new fields are properly mapped in future write indices, you need to:

1. **Update the index template** — add the two new fields under `mappings.properties.context.properties` of the `<PREFIX>-job-logs-v1.0.0` template.

    Via the OpenSearch Dashboards UI: navigate to **Index Management → Templates**, find the template and edit it.

    Or via curl:

    ```bash
    curl -X POST "http://<OPENSEARCH_HOST>/_index_template/<PREFIX>-job-logs-v1.0.0" \
      -H "Content-Type: application/json" \
      -d '{
        "index_patterns": ["<PREFIX>-job-logs*"],
        "data_stream": {},
        "template": {
          "mappings": {
            "properties": {
              "@timestamp": { "type": "date" },
              "level": { "type": "keyword" },
              "message": { "type": "text" },
              "module": { "type": "keyword" },
              "function": { "type": "keyword" },
              "line": { "type": "integer" },
              "context": {
                "type": "object",
                "properties": {
                  "job_id": { "type": "keyword" },
                  "run_id": { "type": "keyword" },
                  "identity_id": { "type": "keyword" },
                  "task_id": { "type": "keyword" },
                  "parent_task_id": { "type": "keyword" }
                },
                "dynamic": true
              }
            }
          }
        }
      }'
    ```

2. **Trigger a rollover of the datastream** — this creates a new backing index using the updated template, cleanly separating old and new log documents.

    Via the OpenSearch Dashboards UI: navigate to **Index Management → Data Streams**, find the `<PREFIX>-job-logs` datastream, click **Actions** (top right) and select **Roll over**.

    Or via curl:

    ```bash
    curl -X POST "http://<OPENSEARCH_HOST>/<PREFIX>-job-logs/_rollover"
    ```

!!! note
    The template update is done in the **Index Templates** section and the rollover in the **Data Streams** section of the OpenSearch Dashboards UI.

#### Comment events update

You will need to run the code below against the live index **before the new code is deployed**. The script is updating all requestevents documents of type comment to mark them as "parent". This is required so that the `join` relationship queries succeed (the request timeline will be broken otherwise!!!). The script exits when all comments are updated. After deployment of the new code you might need to rerun it to fix the delta-comments created between the last run of the script and the deployment of the new code.

TODO: this should be a script

```python
import time
from datetime import datetime

import click
from invenio_search import current_search_client
from invenio_search.api import build_alias_name
from invenio_requests.records.api import RequestEvent


click.secho("Starting parent_child field migration for parent comments...", fg="green")

# Poll interval in seconds to recheck remaining comments without tagged as parents
poll_interval = 10

# Get the OpenSearch client and index name
index_name = build_alias_name(RequestEvent.index._name)

click.echo(f"Target index: {index_name}")

# Capture migration start timestamp
migration_start_time = datetime.utcnow().isoformat()
click.echo(f"Migration timestamp: {migration_start_time}")

# Query for documents that need updating (created before migration, without parent_child field)
def get_pending_count():
    """Get count of documents that still need updating."""
    return current_search_client.count(
        index=index_name,
        body={
            "query": {
                "bool": {
                    "must": [
                        # Created before migration started
                        {"range": {"created": {"lt": migration_start_time}}},
                    ],
                    "must_not": [
                        # Has parent_id (is a child)
                        {"exists": {"field": "parent_id"}},
                        # Already has parent_child field
                        {"exists": {"field": "parent_child"}},
                    ],
                }
            }
        },
    )

# Initial count
initial_count_response = get_pending_count()
initial_count = initial_count_response["count"]

click.echo(f"\nFound {initial_count} parent comments to update")

# Trigger the update (async with wait_for_completion=False)
click.echo("\nTriggering update_by_query...")
update_response = current_search_client.update_by_query(
    index=index_name,
    body={
        "query": {
            "bool": {
                "must": [
                    # Created before migration started
                    {"range": {"created": {"lt": migration_start_time}}},
                ],
                "must_not": [
                    # Has parent_id (is a child)
                    {"exists": {"field": "parent_id"}},
                    # Already has parent_child field
                    {"exists": {"field": "parent_child"}},
                ],
            }
        },
        "script": {
            "source": "ctx._source.parent_child = ['name': 'parent']",
            "lang": "painless",
        },
    },
    wait_for_completion=False,
    refresh=True,
)

task_id = update_response.get("task")
if task_id:
    click.echo(f"Task ID: {task_id}")

click.echo(f"\nPolling cluster every {poll_interval}s until completion...")
click.echo("(Checking for documents created before {})".format(migration_start_time))

# Poll until all documents are updated
total_updated = 0
poll_count = 0

with click.progressbar(
    length=initial_count,
    label="Migrating parent comments",
    show_eta=True,
) as bar:
    bar.update(0)

    while True and initial_count != 0:
        poll_count += 1
        time.sleep(poll_interval)

        # Check how many documents still need updating
        pending_response = get_pending_count()
        pending_count = pending_response["count"]

        # Calculate how many have been updated
        updated_since_last = (initial_count - total_updated) - pending_count
        if updated_since_last > 0:
            bar.update(updated_since_last)
            total_updated += updated_since_last

        # Check if we're done
        if pending_count == 0:
            # Make sure we update to 100%
            remaining = initial_count - total_updated
            if remaining > 0:
                bar.update(remaining)
            break

        # Progress update every 10 polls
        if poll_count % 10 == 0:
            click.echo(f"\nStill processing... {pending_count} documents remaining")

click.secho(f"\n✓ Migration complete!", fg="green")
click.echo(f"Total updated: {initial_count} parent comments")

# Final verification
final_pending = get_pending_count()["count"]
if final_pending == 0:
    click.secho("✓ Verification passed: All documents updated", fg="green")
else:
    click.secho(f"⚠ Warning: {final_pending} documents still pending", fg="yellow")
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

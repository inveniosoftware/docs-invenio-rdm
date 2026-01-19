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

#### Record Deletion

To start using the new Record Deletion feature, one needs to go through the following steps during deployment:

1. Update mappings and removal reasons vocabulary using new code in a terminal
   - Update mappings
     - Records and drafts have a `tombstone.deletion_policy` (optional) field
       - `invenio index update --no-check rdmrecords-records-record-v7.0.0`
       - `invenio index update --no-check rdmrecords-drafts-draft-v6.0.0`
     - Update OAI-PMH percolators index for records (see [recipe below](#oai-pmh-percolator-mapping-update))
     - Update request mappings to add the `last_reply` and `last_activity_at` fields
       - `invenio index update --no-check requests-request-v1.0.0`
   - Apply the [`invenio_request@1759321170` alembic migration](https://github.com/inveniosoftware/invenio-requests/blob/master/invenio_requests/alembic/1759321170_add_index_to_request_events_request_id_.py)
     - `invenio alembic upgrade invenio_requests@1759321170` (or just `invenio alembic upgrade` if you're doing a full upgrade)
   - Update removal reasons vocabulary to add `request-deletion` tags
     - `invenio rdm-records add-to-fixture removalreasons`
2. Deploy code to the rest of web and workers
3. Reindex all requests to populate the `last_reply` and `last_activity_at` fields
   - `invenio rdm-records rebuild-all-indices --order requests`

##### OAI-PMH percolator mapping update

!!! note "Should become a CLI command"

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

#### OAuth client changes

The `extra_data` column of the `oauthclient_remoteaccount` table, storing remote-specific user information as required by various integrations, has been migrated from the `JSON` type to the `JSONB` type (only on PostgreSQL databases).
This gives significant performance improvements when running certain queries.
An automated Alembic migration is included and will be executed when you run the [database migration](#database-migration) step below.

However, if your `oauthclient_remoteaccount` table has more than ~50k rows and you are unable to take the system offline offline for an update, this operation could overload your database and create a lock lasting several minutes, due to the need to individually transform every row.
To avoid issues in such cases, we recommend instead running the migration manually.
Please follow [the upgrade guide](https://invenio-oauthclient.readthedocs.io/en/latest/upgrading.html#v6-0-0).

#### Commenting features

The new commenting features require the below steps to be completed:

1. Update mappings for `requests` and `requestevents` using new code in a terminal:
    - Update request mappings to add the `last_reply.parent_id` and `is_locked` fields
      - `invenio index update --no-check requests-request-v1.0.0`
    - Update requestevents mapping to add the `parent_child` and `parent_id` fields
      - `invenio index update --no-check requestevents-requestevent-v1.0.0`
2. Update all comment request events in the live index by running the [recipe below](#comment-event-update) 
3. Deploy code to the rest of web and workers

##### Comment events update

You will need to run the code below against the live index **before the new code is deployed**. The script is updating all requestevents documents of type comment to mark them as "parent". This is required so that the `join` relationship queries succeed (the request timeline will be broken otherwise!!!). The script exits when all comments are updated. After deployment of the new code you might need to rerun it to fix the delta-comments created between the last run of the script and the deployment of the new code.

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

TODO: `publication-disseration` has to be added to the vocabulary first. either
with a `vocabulary_service.create` or with some another step.

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
`    opensearchpy.exceptions.AuthorizationException: AuthorizationException(403, 'security_exception', 'no permissions for [cluster:admin/component_template/put] and User [name=<my-name>, backend_roles=[], requestedTenant=null]')
    opensearchpy.exceptions.AuthorizationException: AuthorizationException(403, 'security_exception', 'no permissions for [indices:admin/index_template/put] and User [name=<my-name>, backend_roles=[], requestedTenant=null]')
   `
This means your OpenSearch user does not have sufficient permissions to create or update index templates.
To resolve this, grant the necessary permissions to your user in the OpenSearch cluster:

      1. Go to **OpenSearch Dashboards** -> **Security** -> **Roles** -> *<your role name>*.
      2. Edit the role and add the following cluster and index permissions:
         - `cluster:admin/component_template/put`
         - `indices:admin/index_template/put`

## Infrastructure/configuration changes

### Required changes

#### Overridable IDs in the deposit form

To improve consistency in naming conventions and structure, some IDs of Overridables in the deposit form have been modified. If you are overriding any of these components, you will need to change the ID in your mapping file to reflect these modifications.

The full list of ID changes [can be found here](https://github.com/inveniosoftware/invenio-rdm-records/pull/2101/files#diff-ff3c479edefad986d2fe6fe7ead575a46b086e3bbcf0ccc86d85efc4a4c63c79).

If you are not overriding any of these components, you do not need to change anything.

#### Marshmallow Context Deprecation

Marshmallow has deprecated `self.context` in `marshmallow<4.0.0` and will remove
it with `marshmallow>=4.0.0`. Until now we don't go to `marshmallow>=4.0.0`,
there would be further work necessary, because there are backwards incompatible
changes coming in with the n ew version.

The changes are split into 4 groups and they are:

the first group is fixed by creating the `ContextVar` `context_schema` in
`marshmallow_utils.context`

- `max_number`
- `identity`
- `field_permission_check`
- `request`
- `object_version_id`
- `bucket`
- `multipart`

the second group is fixed by moving the parameter into the constructor of the Schema

- `doi_all_version`
- `is_parent`
- `record_dict`

the third group is fixed by changing the parameter to a class property

- `object_key` (`= "ui"`)

the fourth group is kept in `self.context` because it never reaches the
marshmallow level, so it doesn't produce a `DeprecationWarning`

- `is_self`

#### utcnow DeprecationWarning

the usage of `datetime.datetime.utcnow` is deprecated. InvenioRDM replaces it
with `datetime.datetime.now(datetime.timezone.utc)`. This means, we go from a
utc unaware datetime to a utc aware datetime.

This change includes the database, where the `db.DateTime` columns are changed
to `db.UTCDateTime` columns.

invenio-stats changes the format from `strict_date_hour_minute_second` to
`strict_date_optional_time` in `file-download-v1.json` and
`record-view-v1.json`. The aggregation templates are already on
`strict_date_optional_time`. If third party packages are implementing their own
statistics they have to update the format too, otherwise the validation would
fail. To migrate you can do it offline, by deleting the index and recreating the
index (with invenio commands), which adds the new templates to opensearch,
otherwise remove the old template and add the new one by hand.

#### fs

Since `pkg-resources` has been deprecated and removed from pypi and the
dependency `fs` has not been updated anymore we decided to reimplement the
interface in `invenio-files-rest`.



### Optional changes

#### Deprecations

##### Custom field widget prop names

Many [custom field widgets](../../operate/customize/metadata/custom_fields/widgets.md) used the `icon` and `description` props, which have now been deprecated and replaced with `labelIcon` and `helpText` respectively. This is to improve consistency with the naming of the built-in fields used in the deposit form and thereby avoid confusion. The old names will continue to function for now, but we recommend updating to the new names where applicable.

#### New configuration variables

These are the new configuration variables introduced in this release. Make sure that you read the related documentation before enabling them. Add them to your `invenio.cfg` as needed:

##### Related Identifiers

Backend and frontend functionality has been extended to cover related identifiers. The new `RDM_RECORDS_RELATED_IDENTIFIERS_SCHEMES` setting defines which schemes can be used (defaulting to `RDM_RECORDS_IDENTIFIERS_SCHEMES`). Validation rules, vocabularies in the UI, and scheme label resolution have been updated to ensure identifiers and related identifiers are handled consistently.

##### Comment replies preview

The new feature of allowing replies to comments available in all requests introduces a new config variable `REQUESTS_COMMENT_PREVIEW_LIMIT`, limiting the number of retrieved indexed documents when comments have many replies.
##### Locking/Unlocking a request's conversation

The new feature of allowing locking/unlocking a request's conversation is controlled via a feature flag config variable `REQUESTS_LOCKING_ENABLED`.

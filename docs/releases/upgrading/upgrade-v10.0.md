# Upgrading from v9 to v10

## Prerequisites

The steps listed in this article require an existing local installation of InvenioRDM v9, please make sure that this is given!

If unsure, run `invenio-cli install` from inside the instance directory before executing the listed steps.

!!! warning "Backup"

    Always backup your database and files before you try to perform an upgrade.

!!! info "Older versions"

    In case you have an InvenioRDM installation older than v9, you can gradually upgrade using the existing instructions to v9 and afterwards continue from here.

## Upgrade Steps

!!! warning "Upgrade your invenio-cli"

    Make sure you have the latest `invenio-cli`, for InvenioRDM v10 the release is v1.0.6.

### Elasticsearch check

InvenioRDM v10.0 removes support for Elasticsearch v6. If you are using it, you will need **first** to migrate to
Elasticsearch v7 or directly to OpenSearch, before upgrading

!!! warning "Elasticsearch v7 change of license"

    Do not upgrade to Elasticsearch v7.11, due to the [change of license](https://www.elastic.co/pricing/faq/licensing).
    The last version is 7.10.2.

#### Elasticsearch v6 to v7

In your InvenioRDM v9, upgrade from Elasticsearch v6 to v7. Upgrade checklist:
1. Prepare your new Elasticsearch 7 cluster. For local development, make sure that you have also upgraded Elasticsearch in your `docker-services.yml`.
2. In your instance, edit the `Pipfile` and replace `invenio-app-rdm = {extras = [...  "elasticsearch6"]...` with `elasticsearch7`. For example, in the `Pipfile`:
    ```bash
    [packages]
    -invenio-app-rdm = {extras = ["postgresql", "elasticsearch6"], version = "~=9.1.0"}
    +invenio-app-rdm = {extras = ["postgresql", "elasticsearch7"], version = "~=9.1.0"}
    ```
3. In your instance, edit the `.invenio` file:
    ```bash
    -search = elasticsearch6
    +search = elasticsearch7
    ```
4. Do you have any customisation or custom module that contains Elasticsearch v6 mappings?
   If not, go to the next step. If yes, [review the breaking changes](https://www.elastic.co/guide/en/elasticsearch/reference/7.17/breaking-changes-7.0.html#breaking_70_indices_changes)
   and make sure that you copy the `v6` folder and paste it in the same location, with the new name `v7`.
   The final folder structure should look like this (do **not** forget the `__init__.py` files, they are required!):

    ```bash
    my-custom-module
    |-- mappings
        |-- __init__.py
        |-- v6
            |-- __init__.py
            |-- <record>
                |-- <record>-v1.0.0.json
        |-- v7
            |-- __init__.py
            |-- <record>
                |-- <record>-v1.0.0.json
    ```
    You can optionally delete the `v6` folder.
5. Upgrade the Python dependencies:
    ```bash
    cd <my-site>
    pipenv run pip uninstall -y elasticsearch elasticsearch-dsl
    pipenv run pip install invenio-search[elasticsearch7]
    ```
6. Change the `INVENIO_SEARCH_ELASTIC_HOSTS` configuration variable to point to the new cluster. Restart all servers and Celery workers.
7. Create the indices and re-index all data:
    ```bash
    cd <my-site>
    # create indices
    pipenv run invenio index init

    # reindex records
    pipenv run invenio rdm-records rebuild-index
    pipenv run invenio communities rebuild-index
    ```

### Installing the Latest Versions

!!! warning "Elasticsearch v7 required"

    Make sure that you are using Elasticsearch v7. Otherwise, upgrade following the procedure above.

#### OpenSearch: prepare upgrade

At this point, if you are planning to upgrade to OpenSearch v1 or v2, you will need to make a few changes
before upgrading InvenioRDM. If you will keep Elasticsearch v7, please skip this step and go to [Upgrade InvenioRDM](#upgrade-inveniordm).

Elasticsearch v7 and OpenSearch v1 are very similar and the upgrade is rather simple (see the official OpenSearch documentation [here](https://opensearch.org/docs/2.0/upgrade-to/upgrade-to/)). For OpenSearch v2, the only breaking change, affecting InvenioRDM, is the removal of `doc_type` support, more information [here](https://github.com/opensearch-project/OpenSearch/issues/2480).

1. Prepare your new OpenSearch v1/v2 cluster. For local development, make sure that you also have upgraded OpenSearch in your `docker-services.yml`, as in [here](https://github.com/inveniosoftware/cookiecutter-invenio-rdm/blob/e8082e71453ca867e503149538c67c66eb182360/%7B%7Bcookiecutter.project_shortname%7D%7D/docker-services.yml).
2. In your instance, edit the `Pipfile` and replace `invenio-app-rdm = {extras = [...  "elasticsearch7"]...` with `opensearch2` (or `opensearch2`). For example, in the `Pipfile`:
    ```bash
    [packages]
    -invenio-app-rdm = {extras = ["postgresql", "elasticsearch7"], version = "~=10.0.0"}
    +invenio-app-rdm = {extras = ["postgresql", "opensearch2"], version = "~=10.0.0"}
    ```
3. In your instance, edit the `.invenio` file:
    ```bash
    -search = elasticsearch7
    +search = opensearch2
    ```
4. Do you have any customisation or custom module that contains Elasticsearch v7 mappings? If not, go to the next step.
   If yes, make sure that you copy the `v7` folder and paste it in the same location, with the new name `os-v2` (or `os-v1`).
   The final folder structure should look like this (do **not** forget the `__init__.py` files, they are required!):

    ```bash
    my-custom-module
    |-- mappings
        |-- __init__.py
        |-- os-v2
            |-- __init__.py
            |-- <record>
                |-- <record>-v1.0.0.json
        |-- v7
            |-- __init__.py
            |-- <record>
                |-- <record>-v1.0.0.json
    ```

    !!! warning "OpenSearch v2 breaking change"

        Make sure that you have removed the `_type` field everywhere. OpenSearch v2 will fail if still present!

5. Rename the `INVENIO_SEARCH_ELASTIC_HOSTS` configuration variable to `INVENIO_SEARCH_HOSTS` and change its value to point to the new cluster.
6. Uninstall the Elasticsearch Python libraries:
    ```bash
    cd <my-site>
    pipenv run pip uninstall -y elasticsearch elasticsearch-dsl
    ```

#### Upgrade InvenioRDM

Bump the RDM version, create a folder for your custom fields and rebuild the assets:

```bash
cd <my-site>
# Upgrade to InvenioRDM v10
invenio-cli packages update 10.0.0
```

### Re-index data

Re-index data in the cluster:

```bash
cd <my-site>
# recreate indices
pipenv run invenio index destroy --yes-i-know
pipenv run invenio index init

# reindex records
pipenv run invenio rdm-records rebuild-index
pipenv run invenio communities rebuild-index
```

### Re-build assets

```bash
# Create custom fields folder
cd <my-site>
mkdir assets/templates/custom_fields

# Build the instance assets
invenio-cli assets build
```

These commands should take care of locking the dependencies for v10, installing them, and building the required assets.

### Data Migration

Finally, you can run the database schema upgrade, and perform the records data migration:

```bash
# Perform the database migration
pipenv run invenio alembic upgrade

# Run data migration script
pipenv run invenio shell $(find $(pipenv --venv)/lib/*/site-packages/invenio_app_rdm -name migrate_9_0_to_10_0.py)
```

### Complete re-indexing

Now that the new search cluster is ready, complete the re-indexing of the data in the search cluster.
In a python shell (`invenio-cli pyshell`), run:

```python
from invenio_access.permissions import system_identity
from invenio_communities.proxies import current_communities
from invenio_records_resources.proxies import current_service_registry
from invenio_requests.proxies import current_events_service, current_requests_service

# reindex users
users_service = current_service_registry.get("users")
users_service.rebuild_index(system_identity)

# reindex groups
groups_service = current_service_registry.get("groups")
groups_service.rebuild_index(system_identity)

# reindex members and archived invitations
members_service = current_communities.service.members
members_service.rebuild_index(system_identity)

# reindex requests
for req_meta in current_requests_service.record_cls.model_cls.query.all():
    request = current_requests_service.record_cls(req_meta.data, model=req_meta)
    if not request.is_deleted:
        current_requests_service.indexer.index(request)

# reindex requests events
for event_meta in current_events_service.record_cls.model_cls.query.all():
    event = current_events_service.record_cls(event_meta.data, model=event_meta)
    current_events_service.indexer.index(event)
```

!!! info "This will be integrated in the cli in future releases"

    This is needed to make sure all record types are re-indexed. However, in future releases these commands will be encapsulated in one.

#### Strict mappings

Previously record and community mappings were dynamic, which means that any unknown value could be added to it. This would be the case for custom elasticsearch dumper extensions. This dumpers need to be modified to dump those fields in new _custom fields_. Then the records and communities need to be re-indexed.

```shell
# destroy the current indices
pipenv run invenio index destroy --yes-i-know
pipenv run invenio index init

# once you have configured your new custom fields
pipenv run invenio rdm-records custom-fields init -f <field name> -f <field name>
pipenv run invenio communities custom-fields init -f <field name> -f <field name>

# reindex records
pipenv run invenio rdm-records rebuild-index
pipenv run invenio communities rebuild-index
```

As soon as the records have been reindexed, the entire migration is complete! :partying_face:

Additionally, the following section will contain an explanation on how to access the new administration panel.

### Accessing the Administration panel

A new permission (`administration-access`) is needed to access the administration panel. There are 2 ways to grant this permission.

1) Permission can be added using a role:
```
# Create a role
pipenv run invenio roles create administration

# Allow access to administration to the administration role
pipenv run invenio access allow administration-access role administration

# Add administration role to an user email
pipenv run invenio roles add <user_email> administration
```

2) Permission can be added to a specific user:
```
# Add access to administration to an user email
pipenv run invenio access allow administration-access user <user_email>
```

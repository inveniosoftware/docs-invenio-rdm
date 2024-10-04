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

    Make sure you have the latest `invenio-cli`, for InvenioRDM v10 the release is v1.0.8.

    ```bash
    $ invenio-cli --version
    invenio-cli, version 1.0.8
    ```

For local installations, make sure that you prefix each `invenio` command with `pipenv run`.

### Elasticsearch check

InvenioRDM v10.0 removes support for Elasticsearch v6. If you are using it, you will need **first** to migrate to
Elasticsearch v7 or directly to OpenSearch, before upgrading.

!!! warning "Elasticsearch v7 change of license"

    Do not upgrade to Elasticsearch v7.11 or newer, due to the [change of license](https://www.elastic.co/pricing/faq/licensing).
    The last version with `Apache 2.0` license is 7.10.2.

### Installing the Latest Versions

If you are planning to migrate from Elasticsearch v7 to OpenSearch, follow the step below. Otherwise, skip to the next section [Upgrade InvenioRDM](#upgrade-inveniordm).

We strongly recommend migrating or planning to migrate to OpenSearch. Elasticsearch support will be removed in a future version of InvenioRDM.

#### Migrate to OpenSearch

Elasticsearch v7 and OpenSearch v1 are very similar and the migration is rather simple (see the official OpenSearch documentation [here](https://opensearch.org/docs/2.0/upgrade-to/upgrade-to/)). For OpenSearch v2, the only breaking change affecting InvenioRDM, is the removal of `doc_type` (you can read more [here](https://github.com/opensearch-project/OpenSearch/issues/2480)). With this release, you can safely migrate to OpenSearch v2, skipping OpenSearch v1.

!!! warning "OpenSearch v1 Log4Shell security vulnerability"

    If you have decided to use OpenSearch v1, make sure you install a version greater or equal to `v1.2.1`: previous versions are affected by the [Log4Shell](https://opensearch.org/blog/releases/2021/12/update-to-1-2-1/) security vulnerability.

1. Prepare your new OpenSearch v2/v1 cluster.

    You can read more on how to setup an OpenSearch cluster in the [official documentation](https://opensearch.org/docs/latest/opensearch/install/index/). [Invenio Helm Charts](https://github.com/inveniosoftware/helm-invenio/) have been updated adding support for OpenSearch, but the configuration will setup a demo cluster and it should **not be used in production**. OpenSearch provides [official Helm charts](https://opensearch.org/docs/latest/opensearch/install/helm/) suitable for production environments.

    For local development, make sure that you have migrated to OpenSearch in your Docker files in your instance:

    - In `docker-services.yml`, replace the `es` and `kibana` sections with `opensearch` and `opensearch-dashboards` sections, as in [here](https://github.com/inveniosoftware/cookiecutter-invenio-rdm/blob/e8082e71453ca867e503149538c67c66eb182360/%7B%7Bcookiecutter.project_shortname%7D%7D/docker-services.yml#L86).
    - In `docker-compose.yml`, replace the `es` and `kibana` keywords with `opensearch` and `opensearch-dashboards` keywords, as in [here](https://github.com/inveniosoftware/cookiecutter-invenio-rdm/blob/e8082e71453ca867e503149538c67c66eb182360/%7B%7Bcookiecutter.project_shortname%7D%7D/docker-compose.yml#L41).
    - In `docker-compose.full.yml`, replace the `es` and `kibana` keywords with `opensearch` and `opensearch-dashboards` keywords, as in [here](https://github.com/inveniosoftware/cookiecutter-invenio-rdm/blob/e8082e71453ca867e503149538c67c66eb182360/%7B%7Bcookiecutter.project_shortname%7D%7D/docker-compose.full.yml#L45).

2. In your instance, edit the `Pipfile` and replace `invenio-app-rdm = {extras = [...  "elasticsearch7"]...` with `opensearch2` (or `opensearch1`). For example, in the `Pipfile`:
    ```diff
    [packages]
    -invenio-app-rdm = {extras = ["postgresql", "elasticsearch7"], version = "~=9.1.0"}
    +invenio-app-rdm = {extras = ["postgresql", "opensearch2"], version = "~=9.1.0"}
    ```

3. In your instance, edit the `.invenio` file:
    ```diff
    -elasticsearch = 7
    +search = opensearch2
    ```

4. Do you have any customisation or custom module that contains Elasticsearch v7 mappings?

    If not, go to the next step, step 5.

    If yes, make sure that you copy the `v7` folder and paste it in the same location, with the new name `os-v2` (or `os-v1`).
    The final folder structure should look like this (do **not** forget the `__init__.py` files, they are required!):

    ```diff
    my-custom-module
    |-- mappings
        |-- __init__.py
    +   |-- os-v2
    +       |-- __init__.py
    +       |-- <record>
    +           |-- <record>-v1.0.0.json
        |-- v7
            |-- __init__.py
            |-- <record>
                |-- <record>-v1.0.0.json
    ```

    !!! warning "OpenSearch v2 breaking change"

        Make sure that you have removed the `_type` field everywhere. OpenSearch v2 will fail if still present!

5. In your `invenio.cfg`, if you have declared your Elasticsearch configuration:
    - Rename the `INVENIO_SEARCH_ELASTIC_HOSTS` configuration variable to `INVENIO_SEARCH_HOSTS`.
    - Change its value to connect to the new cluster (for local development, the default is `localhost:9200`).

6. Uninstall the Elasticsearch Python libraries:
    ```bash
    cd <my-site>
    pip uninstall -y elasticsearch elasticsearch-dsl
    ```

#### Upgrade InvenioRDM

Upgrade the RDM version:

```bash
cd <my-site>
# Upgrade to InvenioRDM v10
invenio-cli packages update 10.0.0
```

Optionally, update the file `<my-site>/Pipfile`. This step is not necessary, but suggested for local development.

```diff
[packages]
---invenio-app-rdm = {extras = [...], version = "~=9.0.0"}
+++invenio-app-rdm = {extras = [...], version = "~=10.0.0"}
```

From now on, make sure that the services (database, search, etc.) are up and running. For a local development, run `invenio-cli services start`.

### Re-index data

Re-index data in the cluster:

```bash
# recreate indices
invenio index destroy --yes-i-know
invenio index init

# reindex records
invenio rdm-records rebuild-index
invenio communities rebuild-index
```

### Re-build assets

Create the required folder for custom fields (even if empty) and rebuild the assets:

```bash
# Create custom fields folder
mkdir assets/templates/custom_fields

# Re-build the instance assets
invenio-cli assets build
```

### Data Migration

Finally, you can run the database schema upgrade, and perform the records data migration:

```bash
# Perform the database migration
invenio alembic upgrade

# Run data migration script
invenio shell $(find $(pipenv --venv)/lib/*/site-packages/invenio_app_rdm -name migrate_9_0_to_10_0.py)
```

### Complete re-indexing

Complete the re-indexing of the data in the search cluster. In a python shell (`invenio-cli pyshell`), run:

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

!!! info

    These commands are needed to make sure all record types are re-indexed. However, in future releases, a new simple command will include all of them.

### Accessing the Administration panel

The new permission action `administration-access` is needed to access the administration panel. There are two ways to allow users to access the new administration panel.

##### Allow specific users

```bash
# Add access to administration to an user by its email
invenio access allow administration-access user <user_email>
```

##### Allow by role

```bash
# Create a role
invenio roles create administrator

# Allow access to administration to the administrator role
invenio access allow administration-access role administrator

# Add administrator role to an user, by its emails
invenio roles add <user_email> administrator
```

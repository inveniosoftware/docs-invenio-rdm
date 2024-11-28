# InvenioRDM v13.0

_Draft_

_DATE_

## Try it

- [Demo site](https://inveniordm.web.cern.ch)

- [Installation instructions](../../install/index.md)

## What's new?

to complete

*TODO*: the quota feature has not been documented. It should be added, with a screenshot of the admin panel.

### Jobs and ORCID/ROR

Explain about jobs and ORCID/ROR jobs.

Related [new doc page](../../customize/vocabularies/names.md#using-orcid-public-data-sync).

### Search improvements

Related [new doc page](../../reference/search.md).

Easier to find records with accents or other non-standard characters, also searching by DOIs [PR](https://github.com/inveniosoftware/invenio-rdm-records/pull/1774)
Users can be found with partial matches [PR](https://github.com/inveniosoftware/invenio-users-resources/pull/127)
Searches like ` Universitatea "Dunărea de Jos” din Galați` now work [PR](https://github.com/inveniosoftware/invenio-app-rdm/issues/2761)

BREAKING -> mapping changes, create new indices

### Names Vocabulary

TODO
Names listing endpoint is now restricted to authenticated users, names can be "unlisted" not showing anymore in the search result for non-admin users

### Collections

Collections are a "big" feature added to v13.

!!!warning Collections require new database tables, therefore its migration recipes must be executed (`invenio db upgrade` or similar)

A collection serves as a curated set of records that are grouped based on a specific filter or query, displayed on a dedicated page, introducing a new way of organizing records within a community. For instance, a collection can be defined within a community to highlight records sharing common attributes, like funding programs or specific categories.

Collections are stored in the Database and each collection defines a search query string that is used to fetch each collection records. Find more information in the [RFC](https://github.com/inveniosoftware/rfcs/blob/master/rfcs/rdm-0079-collections.md).

**How to create a collection for a community**

Currently collections are created using a python shell (`invenio shell`)

Requirements:

- A community.
- A collection tree that acts as the "root" node of the collection.

If you do not have a collection tree, start by creating one:

```python
from invenio_rdm_records.collections.api import CollectionTree

ctree = CollectionTree.create(
    title="Programs", order=10, community_id="<community_uuid>", slug="programs"
)
```

The `order` parameter controls the order that trees are rendered in the UI.

Create a collection under `programs`:

```python
from invenio_rdm_records.proxies import current_rdm_records
from invenio_access.permissions import system_identity

collections_service = current_rdm_records.collections_service

# Use another identity if needed
identity = system_identity

# Desired community ID
community_id = "9d0d45ce-0ea9-424a-ab17-a72215b2e8c3"

collection = collections_service.create(
        identity,
        community_id,
        tree_slug="programs",
        slug="h2020",
        title="Horizon 2020",
        query="metadata.funding.program:h2020",
        order=10
    )
```

For nested collections, the `add` service method can be used:

```python

h2020 = collections_service.read(
    identity, community_id=community_id, tree_slug='programs', slug='h2020'
)

open_records = collections_service.add(
        identity,
        collection=h2020._collection,
        slug="h-open-records",
        title="Horizon 2020 (Open records)",
        query="access.record:public",
        order=20
    )
```

All the service methods that create collections also implements the Unit of Work pattern, so it can used if transactional consistency is needed.

The created collections can be accessed at:

- https://127.0.0.1:5000/communities/<community_slug>/collections/h2020
- https://127.0.0.1:5000/communities/<community_slug>/collections/h-open-records

Adjust the URL and `community_slug` as needed.

An overview of all the collections can be found in the community browse page (if enabled):

- https://127.0.0.1:5000/communities/<community_slug>/browse

### Miscellaneous additions

Here is a quick summary of the myriad other improvements in this release:

- The creators' roles are now displayed [PR](https://github.com/inveniosoftware/invenio-app-rdm/pull/2795)
- You can now see and show the version of InvenioAppRDM and any other module [Issue](https://github.com/inveniosoftware/invenio-app-rdm/issues/2838)
    Change the config ADMINISTRATION_DISPLAY_VERSIONS = [("invenio-app-rdm", f"v{__version__}")] and append to the list the version you want to display.
- The users API endpoint is now protected, in order to access the list of users it's required to be logged in.
- Custom awards: relaxed required fields (see [PR](https://github.com/inveniosoftware/invenio-vocabularies/pull/429))
- ...and many more bug fixes!

## Breaking changes

- fill me in

## Limitations and known issues

- fill me in

## Requirements

InvenioRDM v13 now supports:

- Python 3.9, 3.11 and 3.12
- Node.js 18+
- PostgreSQL 12+
- OpenSearch v2

Notably, older versions of Elasticsearch/Opensearch, PostgreSQL, and Node.js have been phased out.

## Upgrading to v13.0

We support upgrading from v12 to v13. See the [upgrade guide](./upgrade-v13.0.md) for how.

## Questions?

If you have questions related to these release notes, don't hesitate to jump on [discord](https://discord.gg/8qatqBC) and ask us!

## Credit

The development work of this impressive release wouldn't have been possible without the help of these great people:

- CERN: Alex, Anna, Antonio, Javier, Jenny, Karolina, Lars, Manuel, Nicola, Pablo G., Pablo P., Zacharias
- Northwestern University: Guillaume
- TU Graz: Christoph, David, Mojib
- TU Wien: Max
- Uni Bamberg: Christina
- Uni Münster: Werner
- Front Matter: Martin
- KTH Royal Institute of Technology: Sam
- Caltech: Tom

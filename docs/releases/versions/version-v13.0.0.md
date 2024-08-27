# InvenioRDM v13.0

_Draft_

_DATE_

## Try it

- [Demo site](https://inveniordm.web.cern.ch)

- [Installation instructions](../../install/index.md)

## What's new?

to complete

### Jobs and ORCID/ROR

Explain about jobs and ORCID/ROR jobs.

Related [new doc page](../../customize/vocabularies/names.md#using-orcid-public-data-sync).

### Search improvements

Related [new doc page](../../reference/search.md).

Easier to find records with accents or other non-standard characters, also searching by DOIs [PR](https://github.com/inveniosoftware/invenio-rdm-records/pull/1774)
Users can be found with partial matches [PR](https://github.com/inveniosoftware/invenio-users-resources/pull/127)
Searches like ` Universitatea "Dunărea de Jos” din Galați` now work [PR](https://github.com/inveniosoftware/invenio-app-rdm/issues/2761)

BREAKING -> mapping changes, create new indices

### Miscellaneous additions

Here is a quick summary of the myriad other improvements in this release:

- The creators' roles are now displayed [PR](https://github.com/inveniosoftware/invenio-app-rdm/pull/2795)
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

We support upgrading from v12 to v13. See the [upgrade guide](../upgrading/upgrade-v13.0.md) for how.

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

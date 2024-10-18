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

### EuroSciVoc Subjects

#### Optional Feature

You can now import EuroSciVoc subjects using the new Jobs system. If you previously had imported EuroSciVoc subjects, you will need to update the existing records, drafts, and communities that were using these subjects and then deleting the old subjects in the database. This is necessary due to changes in the structure, such as the introduction of the `props` property and updates to the `id` format.
_Note that mapping updates are needed. Also, you would need to reindex the relevant subjects, records, drafts and communities._

### CORDIS Awards

#### Optional Feature

CORDIS data can now be imported to enhance OpenAIRE awards using the new Jobs system. This update allows for the addition of supplementary information to the awards, including subjects _(Note: The EuroSciVoc subjects are needed for this)_, organizations, and other related metadata. The three funding programs supported are `HE`, `FP7` and `H2020`.
_Note that mapping updates are needed. Also, you would need to reindex the relevant awards, records, drafts and communities._

### Miscellaneous additions

Here is a quick summary of the myriad other improvements in this release:

- The creators' roles are now displayed [PR](https://github.com/inveniosoftware/invenio-app-rdm/pull/2795)
- You can now see and show the version of InvenioAppRDM and any other module [Issue](https://github.com/inveniosoftware/invenio-app-rdm/issues/2838)
  Change the config ADMINISTRATION_DISPLAY_VERSIONS = [("invenio-app-rdm", f"v{__version__}")] and append to the list the version you want to display.
- The users API endpoint is now protected, in order to access the list of users it's required to be logged in.
- ...and many more bug fixes!

## Breaking changes

- Mapping updates in Subjects, Awards, Records _(including percolators)_, Drafts and Communities

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

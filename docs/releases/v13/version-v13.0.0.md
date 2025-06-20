# InvenioRDM v13.0

_Draft_

_DATE_

## Try it

- [Demo site](https://inveniordm.web.cern.ch)

- [Installation instructions](../../install/index.md)

## What's new?

to complete

_TODO_: the quota feature has not been documented. It should be added, with a screenshot of the admin panel.

### Jobs and ORCID/ROR

Explain about the new jobs feature, logging and ORCID/ROR jobs.

Related [new doc page](../../operate/customize/vocabularies/names.md#using-orcid-public-data-sync).

### Search improvements

Addition of a [`suggest` API](../../reference/rest_api_suggest.md).

Easier to find records with accents or other non-standard characters, also searching by DOIs [PR](https://github.com/inveniosoftware/invenio-rdm-records/pull/1774)
Users can be found with partial matches [PR](https://github.com/inveniosoftware/invenio-users-resources/pull/127)
Searches like ` Universitatea "Dunărea de Jos” din Galați` now work [PR](https://github.com/inveniosoftware/invenio-app-rdm/issues/2761)

BREAKING -> mapping changes, create new indices

### Names Vocabulary

TODO
Names listing endpoint is now restricted to authenticated users, names can be "unlisted" not showing anymore in the search result for non-admin users

### Optional DOI

DOIs can now be configured as optional. Describe the feature.

### Compare revisions

Administrators can compare revisions from the administration panel.

### Thesis

Anything to mention?

### Requests sharing

When a record is shared, its inclusion requests will be also accessible. There is a new filter in the My Dashboard to show the records shared with me.

### Audit logs

To be completed

### Collections

### Collections

Collections introduce a powerful new way to organize and curate records within your InvenioRDM instance. This major feature enables administrators and community managers to create dynamic, query-based groupings of records that automatically stay current as new content is added.

![Collection page displaying filtered Horizon 2020 records with clean interface and navigation](placeholder-collection-example.png)

*Collections provide dedicated pages showing all records matching specific criteria, such as funding programs or research topics.*

**Key capabilities:**

- **Dynamic record grouping** - Create collections based on any metadata field using search queries
- **Hierarchical organization** - Build nested collection structures using Collection Trees that inherit parent queries
- **Community integration** - Scope collections to specific communities or make them globally available
- **Automatic updates** - Collections automatically include new records matching their criteria
- **Query inheritance** - Child collections combine their filters with parent collections using AND logic

**Hierarchical organization examples:**

Create sophisticated organizational structures like:
- EU funding programs (Horizon Europe → Open Access → Datasets)
- Research fields (Natural Sciences → Physics → Astronomy)
- Resource types with access levels and publication dates

![Collection tree browser showing expandable hierarchy of research topics and funding programs](placeholder-collection-browser.png)

*The collection browser provides an organized view of all available collections within a community.*

**Common use cases**

- Organize records by funding programs (Horizon 2020, NSF, institutional grants)
- Group content by research disciplines using Fields of Science vocabulary
- Create resource type collections (datasets, publications, software)
- Build department or project-specific views
- Highlight featured content or special collections

![Nested collection showing breadcrumb navigation from Natural Sciences to Physics to Astronomy](placeholder-nested-navigation.png)

*Nested collections show clear hierarchical relationships with breadcrumb navigation between levels.*

Collections integrate seamlessly with existing community features and are accessed through intuitive URLs. The feature is currently managed through Python shell commands, with a user interface planned for future releases.

Read more about the [Collections feature](../../operate/customize/collections.md).

### Helm charts

To be announced?

### Diff tool in the admin panel

Explain and screenshot of the diff tool in the admin panel

### FAIR signposting level 1

[FAIR signposting level 2](https://signposting.org/FAIR/#level2) is already enabled by default since v12. The response header of each record's landing page includes a `Link` HTTP response header pointing to a JSON-based linkset which contains the FAIR signposting information.

In order to increase discoverability, [FAIR signposting level 1](https://signposting.org/FAIR/#level1) can be enabled with the configuration flag `APP_RDM_RECORD_LANDING_PAGE_FAIR_SIGNPOSTING_LEVEL_1_ENABLED = True`. Once enabled, FAIR signposting information will be directly included in the `Link` HTTP response header.

Please note that for records having many authors, files, or licenses, FAIR signposting will fall back to level 2 only, in order to avoid generating excessively big HTTP response headers.

However, since enabling FAIR signposting level 1 does increase the size of HTTP response headers, it is recommended to edit the `nginx` configuration and specify [`uwsgi_buffer_size`](https://nginx.org/en/docs/http/ngx_http_uwsgi_module.html#uwsgi_buffer_size) with a higher limit than the default values. If you have enabled `uwsgi_buffering on;`, then [`uwsgi_buffers`](https://nginx.org/en/docs/http/ngx_http_uwsgi_module.html#uwsgi_buffers) may also be adjusted.

```nginx
server {
   # ...
   # Allow for larger HTTP response headers for FAIR signposting level 1 support
   uwsgi_buffer_size 16k;
   # optional if uwsgi_buffering on;
   uwsgi_buffers 8 16k;

   # ...
}
```

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

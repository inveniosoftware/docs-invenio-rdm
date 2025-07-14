# InvenioRDM v13.0

_DATE_

We're happy to announce the release of InvenioRDM v13.0! Version 13 will be maintained until at least 6 months following the next release. Visit our maintenance policy page to learn more.

## Try it

- [Demo site](https://inveniordm.web.cern.ch)

- [Installation instructions](../../install/index.md)

## What's new?
Our latest release, v13, is here, and it's packed with an incredible array of new features and major improvements. We're diving straight into the highlights, then wrapping up with a comprehensive list of all the other valuable enhancements.

### Administration panel
You'll find several new improvements in the administration panel:

- The default number of results of has been increased from 10 to 20 on all panels
- Records and draft panel:
    - More of the title is shown by default
    - Improved display of files and stats information
    - Fixed narrow viewport display, such as on mobile
    - Owner now links to the ID in the user panel
- User panel:
    - ORCID and GitHub icons now link to the user's profile

#### Compare revisions
The new `Compare Revisions` feature allows administrators to audit record updates and follow changes over time.
From the **Records** list in the Administration panel, click the **Compare revisions...** button in the _Actions_ column to open a side-by-side comparison window:

![Records List: Compare Revisions](./imgs/records.png)

A modal window appears, allowing you to choose two revisions to compare:

![Compare Modal: Version Selection](./imgs/records-compare-select.png)

The changes are then displayed in a JSON **side-by-side diff** view:

![Compare Modal: Diff View](./imgs/records-compare.png)

!!! info "Revisions VS versions"

    This feature allows admins to compare revisions, not versions. A revision is the result of editing a record, where each published edit creates a new revision. A new version is a different record which is semantically linked to the previous record. At this time it is not possible to compare different records, including versions.

### Audit logs
InvenioRDM now comes with a new audit logs feature. See the [related documentation here](../../operate/customize/audit-logs.md).

![Administration Panel](../../operate/customize/imgs/audit-logs.png)

### Communities
InvenioRDM v13 introduces a range of exciting new features related to communities.

!!! info
    Such features currently lack a user-friendly interface for easy configuration and require manual setup. Please refer to the linked documentation for detailed activation instructions.

#### Themed communities
Communities can now have their own theming with a custom font and colors, which apply to all community pages including records and requests. Below is an example of one "default" and two themed communities on Zenodo.

![A default community and two themed communities on Zenodo](imgs/themed-communities.png)

Themed communities benefit from a custom homepage, defined by changing its HTML template.

Read more about the [themes communities feature](../../operate/customize/look-and-feel/themed_communities.md).

#### Subcommunities
It is now possible to create hierarchical relationships between communities, allowing for departments, subject areas and other structures to be represented via related communities. Records from the "child" community are automatically indexed in the "parent" community, allowing all the records of the children to be browsed in the parents. The communities are also bidirectionally linked so that it is easy to navigate between both.

Having subcommunities also enables the **Browse** page, which lists all the subcommunities and [collections](#collections) of that community.

!!! note
    By design, communities can only have one level of hierarchy (i.e., no grand-child communities) and communities can only have one parent community.

#### Collections
Collections introduce a powerful new way to organize and curate records within your InvenioRDM instance. This major feature enables administrators to create dynamic, query-based groupings of records that automatically stay current as new content is added.

![Collection page displaying filtered Mathematics records under a nested subject hierarchy](imgs/collection-page.png)
/// caption
Collections provide dedicated pages showing all records matching specific criteria.
///

**Hierarchical organization**
Collections allow you to define hierarchical groupings of records, enabling users to browse content by subject, resource type, funding program, or any other metadata field.

![Community "Browse" tab showing hierachical collections based on subjects](imgs/collection-browse.png)
/// caption
The collection browser provides an organized view of all available collections within a community.
///

**Common use cases**
- Group content by research disciplines using a hierarchical vocabulary
- Organize historical records by publication date
- Organize records by funding programs (Horizon 2020, NSF, institutional grants)
- Create resource type collections (datasets, publications, software)
- Highlight featured content or special collections

Collections integrate seamlessly with existing community features and are accessed through intuitive URLs. The feature is currently managed through Python shell commands, with an administrator user interface planned for future releases.

Read more about the [Collections feature](../../operate/customize/collections.md).

### Curation checks
It is now possible to configure automated **checks** in your communities to provide instant feedback on draft review and record inclusion requests. Checks provide feedback to both the user and reviewer that submissions to your community are compliant with your curation policy. For example, you can enforce that submissions to your community must be preprints, funded by a specific grant or any other requirement on the metadata or files.

![Curation checks enabled in Zenodo](../../operate/customize/imgs/curation-checks-zenodo.jpg)
/// caption
Curation checks in Zenodo's EU Open Research Repository
///

Read the detailed documentation for [Curation checks](../../operate/customize/curation-checks.md).

### DOIs on demand
You can now let users to choose if they need a DOI or not when uploading. See how to configure it in the [related documentation](../../operate/customize/dois.md#dois-on-demand).

![DOIs on demand](../../operate/customize/imgs/dois-on-demand.jpg)

### FAIR Signposting level 1
With v13, you can now enable support for FAIR Signposting level 1 and 2. See [the related documentation](../../operate/customize/FAIR-signposting.md) for more information.

### Jobs
This release introduces a new Jobs feature, providing a comprehensive way to manage asynchronous tasks via the UI or REST API. Jobs are triggered via the admin UI or REST API, run using Celery, and support logging, argument validation, and result tracking. See the related documentation [here](../../operate/ops/jobs/jobs.md).

#### ORCID and ROR integrations
You can now setup jobs to automatically and recurrently fetch ORCID and ROR latest databases.

For ORCID, read more on the [names vocabulary](../../operate/customize/vocabularies/names.md#using-orcid-public-data-sync) documentation page.

With the ROR job, you can automatically load funders or affiliations vocabulary from the InvenioRDM administration panel, and schedule updates with new ROR releases. Instructions can be found on the [affiliations vocabulary](../../operate/customize/vocabularies/affiliations.md) documentation page.
We have also upgraded the integration with ROR to version 2.0 and enhanced the metadata to include organization aliases, status, types, locations, and acronyms, making it easier to find the correct organization or funders.

### New metadata fields
We have introduced new metadata fields that will allow you to capture more useful information when uploading:

- A dedicated **copyright** field is now available, ensuring clear and comprehensive copyright information.
- We've added new add-on **thesis metadata fields**. We've also reorganized the thesis section, grouping thesis fields together. See [here](../../operate/customize/metadata/optional_fields.md) how to enable them.
- The **edition** field has been introduced under the add-on `imprint` set of fields, providing a way to specify the edition of the book.

### Requests sharing
When a record is shared, the review request is now also accessible. We have introduced a new search filter in `My Dashboard`, to easily find records shared with me.

![Shared with me](./imgs/my-dashboard-shared-with-me.jpg)

### Search improvements
Both users and records search have been enhanced to return more accurate results for common names/titles, partial matches (even with typos) and names/titles with accents or diacritics.

Creators, affiliations and funders autocompletion has been improved so that suggestions appear faster and better match what you type.

























### Custom schemes for persistent identifiers

The Invenio [idutils](https://github.com/inveniosoftware/idutils) module handles validation and normalization of persistent identifiers used in scholarly communication, and existing customizations may be affected by changes in v13.
The library has been restructured to use a configurable scheme system with a new entrypoint mechanism for registering custom identifier schemes.

See the [related documentation](../../operate/customize/metadata/custom_pids_schemes.md) how to add your own custom schemes.

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
- Custom awards: relaxed required fields (see [PR](https://github.com/inveniosoftware/invenio-vocabularies/pull/429))
- The configuration flags that control the visibility of menu items in the administration panel have been removed, and they are now visible by default. You can remove such flags from your configuration file (if existing) or leave them there, they will have no effect. Removed flags:
  - `COMMUNITIES_ADMINISTRATION_DISABLED`
  - `USERS_RESOURCES_ADMINISTRATION_ENABLED`
  - `JOBS_ADMINISTRATION_ENABLED`
- Following the [latest COUNTER spec](https://www.countermetrics.org/code-of-practice/), the [list of robots and machines](https://github.com/inveniosoftware/counter-robots) have been updated to ensure the stats are counted on human usage.
- Logging: The Flask root logger level has been set to `DEBUG`, enabling all log messages to pass through by default. Handlers are now responsible for filtering messages at the desired level, offering more flexibility for development and production environments.
- [Sitemaps](../../operate/customize/sitemaps.md) are now generated for search engines and other crawlers to discover and index important content (records and communities by default, but customizable). Sitemaps are even automatically linked in your `robots.txt` for ease of discoverability by machine agents.
- ...and many more bug fixes!

## Breaking changes

- Direct imports of identifier schemes (e.g., from idutils.isbn import normalize_isbn) are now deprecated and will be removed in future versions. If you have custom code that directly imports scheme modules, you'll need to update it to use the new API.
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

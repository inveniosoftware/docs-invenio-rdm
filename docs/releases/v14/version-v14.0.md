# InvenioRDM v14.0

_2026-07-XX_

Here are the release notes for InvenioRDM v14.0, the open-source
repository platform for research data management, institutional repositories,
and digital assets management! Version 14.0 will be maintained until at least
6 months following the next major release. Visit our [maintenance policy page](../maintenance-policy.md) to learn more.
The previous major version, version 13, will be out of support 6 months from today.

## Try it

- [Demo site](https://inveniordm.web.cern.ch)

- [Install from scratch instructions](../../install/index.md)

## What's new?

### Administration panel: users and roles

Administrators can now manage user roles directly from the administration panel. See [User Roles Management](../../use/administration.md#user-roles-management-ui) for details.

![Manage user roles dropdown menu](../../use/imgs/administration/manage-user-roles-dropdow-menu.png){: .screenshot}

### Community membership requests

Users can now request to become members of communities. This feature is opt-in per community and feature-gated at the instance level.

![Request membership](../../use/imgs/communities/community-request-membership.png){: .screenshot}

It should lessen the administrative burden of inviting new users and further let them self-organize around their interests.

Enabling the feature is just a matter of turning on a [configuration variable](../../reference/settings.md#membership-requests). See these links for [how to enable it on a per community basis](../../use/communities.md#membership-policy) and what the [usage flow](../../use/communities.md#members) is like.

### Community reviews for each record version

Previously, when [submitting a record to a community](../../use/requests.md), only the first version of the record required a review by the community's curators.
It was not possible to require a review for new versions of the record.

**It is now possible to require a review for all record versions**, subject to custom code on the instance level.
The default behaviour (where reviews are only required for the initial version) remains unchanged.

See the [requests documentation](../../operate/customize/requests.md#require-reviews-for-each-record-version) for more information.

### DOI registration with Crossref

[DOI registration](../../operate/customize/dois.md) with Crossref is a new feature in InvenioRDM v14. Crossref has a different metadata schema than DataCite and supports textual content types such as journal articles, books, conference proceedings, preprints, posters or dissertations.
For more advanced use cases, InvenioRDM v14 also supports DOI registration with DataCite **and** Crossref in the same instance and/or using multiple DOI prefixes. Migration of existing DataCite DOIs to Crossref (or vice versa) is another possible advanced use case.

### Files modification

You can now allow users to modify the files of their published records, in accordance with your policies. When enabled, the record's owner can unlock file editing within the first 30 days of publication and modify them within 45 days (by default), thus giving them at least 15 days to upload and publish again. See the [relevant documentation](../../operate/customize/file-modification.md) to see how to enable and customize this feature.

![Showing the flow to edit the files of a record](imgs/file-modification.png){: .screenshot}

### Files quota

You can now specify a default amount of extra storage quota for files which users can spread across their records, allowing them to selectively use a budget of quota for extra large records.

There is a new section added to the deposit form which provides an intuitive interface to manage the extra quota:

![Manage storage area of the deposit form showing increasing quota by 110 GB](imgs/manage-storage.jpg){: .screenshot}

Additionally users can view the extra quota which they have used across their records in the new storage page in their settings.

![Storage settings page showing the 110 GB quota assigned to our record](imgs/storage-settings.jpg){: .screenshot}

See the [related documentation](../../operate/customize/file-uploads/user-quota.md) to discover how to enable and customize this feature.

### GeoJSON and Web Archive previewers

You can now preview GeoJSON files uploaded by users directly on an interactive map rendered with [Leaflet](https://leafletjs.com) and [OpenStreetMap](https://www.openstreetmap.org/) tiles.

![GeoJSON previewer](imgs/geojson.jpg){: .screenshot}

The new previewer automatically detects and displays GeoJSON files as maps within the existing JSON file previewer. When users upload a GeoJSON file, it will be rendered as an interactive map instead of raw JSON.

Due to content security policy restrictions, you must allow embedding assets from OpenStreetMap. See [the dedicated section](https://github.com/inveniosoftware/invenio-previewer/blob/master/invenio_previewer/__init__.py#L258) in the README for more information.

You can also preview web archives (WACZ, WARC, HAR, CDX, CDXJ) using an embedded [ReplayWeb.page](https://replayweb.page/) viewer. See [the dedicated section](https://github.com/inveniosoftware/invenio-previewer/blob/master/invenio_previewer/__init__.py#L290) in the README to discover how to enable it.

![Web Archive previewer](imgs/web-archive-previewer.jpg){: .screenshot}

### Job notifications

Jobs can now send email notifications to configured recipients when runs complete with specific statuses. This enables administrators and librarians to be automatically informed about the outcome of scheduled or manually triggered jobs.

See [Job Notifications](../../use/administration.md#job-notifications) for usage details and [Email Notification Templates](../../operate/customize/jobs.md#email-notification-templates) for customization options.

### Metadata schema update

We have aligned the core metadata schema and vocabularies with the latest additions from DataCite Schemas v4.5, v4.6 and v4.7. The goal is to adopt relevant updates that benefit InvenioRDM instances while strictly limiting breaking changes to ensure a smooth upgrade path. Additional breaking changes will happen in a future release.

List of changes:

- The existing resource types "Publication / Thesis" (id `publication-thesis`) and "Publication / Dissertation" (id `publication-dissertation`) were merged into the former, which has been mapped to the resource type `Dissertation` in DataCite. Migrating your existing records to this change is entirely optional; see [aligning the "Thesis" and "Dissertation" resource types](./upgrade-v14.0.md#align-thesis-and-dissertation-resource-types) in the upgrade guide.
- Added `Poster`, `Presentation`, and `Study Registration` to the depositable default resource types. Added `Project` and `Instrument` to the linkable default resource types.
- Added `IsTranslationOf`, `HasTranslation`, `IsCollectedBy`, `Collects`, and `Other` to the default relation types . Added the new contributor type `Translator` and the new date type `Coverage` to their respective default vocabularies.
- Added `CSTR` (Science and Technology Resource Identifier) and `RRID` (Research Resource Identifier) as identifiable related identifiers.
- When minting DataCite DOIs, renamed the `identifiers` field to `alternateIdentifiers` and moved the `doi` identifier to its own field.

### Modern toolchain

The modern build toolchain introduced as experimental in v13 is now considered stable and ready for adoption:

- **[uv](https://docs.astral.sh/uv/)** in place of `pipenv` for Python dependency management.
- **[pnpm](https://pnpm.io/)** in place of `npm` for JavaScript dependency management, with faster installs and a disk-efficient content-addressable store.
- **[Rspack](https://www.rspack.dev/)** in place of `webpack` for asset bundling, with Rust-based builds that are much faster and drop-in compatible with the existing Invenio asset pipeline.

Each tool is opt-in independently. See the [upgrade guide](./upgrade-v14.0.md) for how to enable each of them.

Python 3.14 also becomes the required Python version. Starting with v14, InvenioRDM follows a new explicit Python support policy.
Each InvenioRDM major version will have an official anointed Python version guaranteed to work that establishes a modern baseline to develop against.
The same version will typically be kept for a few major versions.
See the [RFC](https://github.com/inveniosoftware/rfcs/blob/master/rfcs/rdm-0109-python-versions.md) for all the details.

### OAuth improvements

We've added a few small but crucial improvements to the [invenio-oauthclient](https://github.com/inveniosoftware/invenio-oauthclient) module, improving security and bringing Invenio's third-party authentication in line with modern standards.

- **Refresh tokens** are now supported, meaning we now have full compatibility with all OAuth 2.0 authorization servers. This means we can securely store long-lived tokens and exchange them for short-lived access tokens as and when needed, allowing us to integrate with modern third-party apps ([invenio-oauthclient#328](https://github.com/inveniosoftware/invenio-oauthclient/pull/328)).

- The `extra_data` column of the `oauthclient_remoteaccount` table is now stored in the more efficient `JSONB` type when using PostgreSQL, improving the performance and flexibility of queries ([invenio-oauthclient#360](https://github.com/inveniosoftware/invenio-oauthclient/pull/360)).

### Overridable: easily find components IDs

When customizing InvenioRDM, you often need the UI component ID to override. Developer mode now highlights all overridable components on a page, making it easy to find the ID you need.

![Metadata-only checkbox overridable ID in an overlay](../../operate/customize/look-and-feel/imgs/metadata_id_overlay.png){: .screenshot}

See the [documentation](../../operate/customize/look-and-feel/override_components.md#1-find-the-component-to-override) for details.

### Preview content of ZIP files and others

We've added support for ZIP files and introduced a flexible framework for handling container formats (e.g., NetCDF, TAR). Users can now explore and access files inside archives without downloading them entirely, making large datasets easier to work with.

These new features allow:

- Browsing archive contents directly in the UI with a hierarchical tree view

- Previewing files inside ZIPs (images, PDFs, text, notebooks, audio/video, etc.)

- Downloading individual files or directories without extracting the entire archive

![ZIP file preview](imgs/container-file-formats.png){: .screenshot}

See the [ZIP and other container files configuration guide](../../operate/customize/file-uploads/zip-and-container-files.md) for how to enable the feature and tune its behavior, and the [REST API reference](../../reference/rest_api_drafts_records.md#container-files) for the new API endpoints.

### Publication date range facet

InvenioRDM v14 introduces an interactive publication date facet on the search
page. Users can filter records by year using a histogram and range slider, or
pick from preset ranges (last 6 months, last year, last 5 years) and enter a
custom date range.

![Publication date range facet](../../operate/customize/imgs/publication-date-range-facet.png){ width="300", : .screenshot}

You can enable additional date facets, tune backend aggregation settings, and
override the frontend UI. See [Configure date range
facets](../../operate/customize/search.md#configure-date-range-facets).

### Record deletion

You can now configure InvenioRDM to allow users to delete, or request deletion of, their own published records in accordance with any policy or criteria you may have. When enabled, the default behavior is that records can be deleted within 30 days of publication. After, the deletion can be requested to repository's administrators. Deletion requests are visible within the administration panel and the user's request dashboard.

![Modal to immediately delete a record](imgs/deletion-modal.png){: .screenshot}
/// caption
Modal to immediately delete a record
///

This feature is highly customizable. You can introduce deletion policies based on resource type, community role, file type, or any other criteria you require. Additionally, you can prevent unnecessary record deletion by adding a deletion checklist that suggests how users can resolve the issue correctly instead of deleting the record. See the [relevant documentation](../../operate/customize/record_deletion.md) to enable and customize this feature.

### Request commenting enhancements

We've introduced a number of exciting new features to improve the commenting experience on requests, which are currently used across InvenioRDM for a range of purposes such as community record submission.

#### Sharing a link to a comment

You can now copy a link to a comment directly, allowing for easy and precise sharing.
When opened, the link will take the user to the comment and highlight it, regardless of which page it's on.

To share a link to a comment, simply click the "Copy link" button on a comment:

![Comment with the "copy link" button](imgs/comment-deep-link.png){: .screenshot}

#### LaTeX equations

Comments now support LaTeX, so mathematical equations can be written inline (using `$`) or as full-width blocks (using `$$`). A "Preview math equations" button lets you check the rendered result before publishing the comment.

#### Quoting comments

You can now quote a comment, or part of a comment, when writing a reply. When quoting a whole comment, there is a "Quote reply" option in its action menu. To quote just part of it, highlight the text you want to quote and a "Quote reply" option will appear in line.

![Quoting other comments](imgs/quote-reply-popover.png){: .screenshot}

#### Replying to comments

A dedicated "Write a reply" box lets you reply directly to a specific comment, keeping related discussion grouped together and the conversation easier to follow.

#### Locking conversations

Community curators, managers, and owners can now lock a request's conversation to prevent further comments at any time, with locking and unlocking events recorded in the conversation timeline for transparency. Once a conversation is locked, existing comments can still be deleted but not edited.

![The "lock"/"unlock" events in the timeline](imgs/locking-event.png){: .screenshot}

#### Attaching files to comments

You can now attach files directly to a comment, with attachments displayed beneath the comment text once submitted.

![A submitted comment showing an attached file below the comment text](imgs/attached-file-comment.png){: .screenshot}

### Software archiving (from GitHub, GitLab, etc.)

Software releases can now be archived not only from GitHub, but also from other code forges such as GitLab and GitHub Enterprise.
The new [`invenio-vcs`](https://github.com/inveniosoftware/invenio-vcs/) module replaces the existing `invenio-github` module with a nearly identical end-user experience while adding support for a generic code forge interface.

![GitLab integration](imgs/gitlab.jpg){: .screenshot}

This new module addresses existing limitations, such as allowing users to select which community should receive their code releases.

The module is **optional** and must be installed and configured.
See [the documentation](../../operate/customize/software_archival.md) for more details.

### Miscellaneous additions

Here is a summary of other improvements in this release:

- In the search page, users can now sort search results by **number of downloads**.
- Deposit form: the **"Creators"** label has been changed to **"Authors"** to clarify that these names appear in citations.
- This release features an upgraded PDF previewer to [**PDF.js v5**](https://github.com/mozilla/pdf.js), which includes bugfixes and new features.
- The new configuration variable **`RDM_RECORDS_RELATED_IDENTIFIERS_SCHEMES`** enables configuring identifier schemes specifically for related identifiers. Previously, identifiers and related identifiers used a single shared list, making it impossible to have separate configurations.
- The new configuration variable **`RDM_RECORDS_REQUIRE_SECRET_LINKS_EXPIRATION`** controls whether an expiration date must be set for access links and secret links. It defaults to **`FALSE`** when not defined.
- Added support for **`Wikidata`** identifiers (QIDs) for creators, contributors, and their affiliations.
- Fixed permissions to enable community owners to [**remove a community from a record**](../../use/communities.md#curate-records). This does not affect the behavior when a [community is required](../../operate/customize/require_community.md#require-community-for-record-publication) for record publication.
- Jobs in the administration panel: added a [**Delete action**](../../use/administration.md#deleting-a-job) to the jobs list, allowing administrators to remove jobs directly from the UI.
- Added **cache-control headers** for both local and S3-served files. This is necessary for repositories that use a proxy service such as Cloudflare in front of InvenioRDM.
- Added an HTTP User-Agent helper (**`invenio_user_agent`**) for outbound HTTP requests in `invenio-vocabularies` datastreams to identify requests performed by InvenioRDM.
- Reproducible Javascript builds are finally possible. See [**Build and Lock Assets**](../../operate/ops/deploy.md#inveniordm-application).
- Decoupled `invenio-checks` from `invenio-communities`. [Checks](../../operate/customize/curation-checks.md) can now be used with any request type!
- Plenty of bug fixes as usual!

## Deprecations

- The configuration variable `COMMUNITIES_GROUPS_ENABLED` (used to enable Groups) is deprecated. Use `USERS_RESOURCES_GROUPS_ENABLED` instead.
- Several [custom field widgets](../../operate/customize/metadata/custom_fields/widgets.md) previously accepted the props `icon` and `description`. These have been renamed to `labelIcon` and `helpText` to match the built-in deposit form fields and reduce confusion. The old prop names still work for now but are deprecated.
- Preparing for `Marshmallow 4+`, we changed how schema context is handled. A `ContextVar` was added at `marshmallow_utils.context`, some context values are now passed to Schema constructors, and a few class properties were converted to parameters. Some values remain in self.context if they are not used during serialization/deserialization.
- The older `PyFilesystem2 (fs)` dependency has been removed from `invenio-files-rest`. Its required functionality has been incorporated into the module to avoid breaking changes.
- The `invenio-github` module for archiving software from GitHub is deprecated. Migrate to `invenio-vcs` (supports GitHub, GitLab, and other forges). See the [upgrade notes](./upgrade-v14.0.md#deprecated-github-integration) to learn how to migrate.
- More than 15 other deprecations (mostly from third-party libraries) were cleaned up in this release to keep the codebase current and reduce noisy warnings.

## Breaking changes

- The deposit form's overridable component IDs have been renamed to improve structure and naming consistency. No `<Overridable>` components were removed. If you override components by ID, review [the full list of updates](https://github.com/inveniosoftware/invenio-rdm-records/pull/2101/files#diff-ff3c479edefad986d2fe6fe7ead575a46b086e3bbcf0ccc86d85efc4a4c63c79) and update your IDs accordingly.
- The underlying Flask and Werkzeug Python libraries now handle multiple reverse proxies differently in production deployments. In Invenio-App-RDM, `WSGI_PROXIES` has been removed in [PR 3284](https://github.com/inveniosoftware/invenio-app-rdm/pull/3284); configure `PROXYFIX_CONFIG` instead. See documentation [here](https://github.com/inveniosoftware/invenio-base/blob/77a5b438340a1efb048963257129eeab5d56aeca/invenio_base/wsgi.py#L66), [here](https://werkzeug.palletsprojects.com/en/stable/middleware/proxy_fix/) and our [cookiecutter example here](https://github.com/inveniosoftware/cookiecutter-invenio-rdm/blob/83bb37436980ab8998a80fa0429e7d09f01f45f2/%7B%7Bcookiecutter.project_shortname%7D%7D/docker-services.yml#L24). In your `invenio.cfg`:

    ```diff
    - WSGI_PROXIES = 2
    + PROXYFIX_CONFIG={'x_for': 1, 'x_proto': 1}  # This is just an example; adjust it for your infrastructure
    ```

- The community `Browse` menu configuration variable has been renamed from `COMMUNITIES_SHOW_BROWSE_MENU_ENTRY` to `COMMUNITIES_COLLECTIONS_ENABLED`. Update your `invenio.cfg` if it is declared:

    ```diff
    - COMMUNITIES_SHOW_BROWSE_MENU_ENTRY = True
    + COMMUNITIES_COLLECTIONS_ENABLED = True
    ```

- Per the [v13 deprecation notice](../v13/version-v13.0.0.md#deprecations), `invenio_records_resources.services.Link` has been replaced by `invenio_records_resources.services.EndpointLink` for InvenioRDM links and `invenio_records_resources.services.ExternalLink` for external links. Continuing to import `Link` is incorrect and it will be removed completely.
- If you override the default `DataCite45JSONSerializer`, the `is_parent` argument must now be passed directly. In your `invenio.cfg` or custom code, replace:

    ```diff
    - serializer=DataCite45JSONSerializer(schema_context={"is_parent": True})
    + serializer=DataCite45JSONSerializer(is_parent=True)
    ```

## Requirements

For InvenioRDM v14:

- Python 3.14 is required (3.11, 3.12, 3.13 may happen to work, but there is no guarantee).
- Node.js 24+ is required. This release has been tested with version 26 too.
- PostgreSQL 15+ is required.
- OpenSearch v2.12+ is required.

## Upgrading to v14

Detailed instructions on how to upgrade from v13 to v14 are in the [v14 upgrade guide](./upgrade-v14.0.md).

## Questions?

If you have questions related to these release notes, don't hesitate to jump on [Discord](https://discord.gg/8qatqBC) and ask us!

## Credit

The development of this release wouldn't have been possible without the help of these smart people (name or GitHub handle, alphabetically sorted):

- Alex Ioannidis
- Alžběta Pokorná
- Anika Churilova
- Brian Kelly
- Carlin MacKenzie
- Chokri Ben Romdhane
- Chris Wagner
- Christoph Ladurner
- Dan Granville
- ducica
- Dusan Stojanovic
- enitu
- Eric Newman
- Esteban J. G. Gabancho
- Fatimah Zulfiqar
- gressho
- Guillaume Viger
- Hrafn Malmquist
- Ian Scott
- Jacob Collins
- Jakob
- jakob miesner
- Javier Romero Castro
- Jorge Marco
- Julie Hinge
- Karl Krägelin
- Karolina Przerwa
- Lars Holm Nielsen
- Laura
- Maira Salazar
- Markus Klöpper
- Martin Fenner
- Maximilian Moser
- Miroslav Bauer
- Miroslav Simek
- mkloeppe
- Mohammed Taha Khan
- Nicola
- Oliver Geneser
- Ondřej Ruml
- Orkun BALCI
- Pablo Saiz
- Pablo Tamarit
- Pal Kerecsenyi
- Pascal Repond
- Peter Desmet
- Peter Weber
- Rafael Martínez-Estévez
- Rishabh Oberoi
- ron
- Saksham
- Sam Arbid
- Sarah Wiechers
- senyaaa
- Simone Tripodi
- sushmithainjeti
- Taha Khan
- Till Korten
- Tom Morrell
- Uma Ganapathy
- Werner Greßhoff
- yashlamba
- Zacharias Zacharodimos
- Zübeyde Civelek

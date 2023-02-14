# InvenioRDM v11.0

_2023-01-26_

_Short-term support (STS) release_

We're happy to announce the release of InvenioRDM v11.0. The release is a short-term support release which is maintained until v12.0.

## Try it

- [Demo site](https://inveniordm.web.cern.ch)

- [Installation instructions](https://inveniordm.docs.cern.ch/install/)

## What's new?

### DOI and publisher field

Minting DOIs now requires to have the `publisher` field defined. Submitters will see an error in the upload form if such field is not provided when requesting a DOI.

### ROR for funders

[ROR](https://ror.org) identifiers have been added under the `funders.identifiers` field in the funders vocabulary.
You can read more about it in the [Funding](../../customize/vocabularies/funding.md#funders-ror) documentation page.

### Static pages

You can now add new static pages to your instance, for example an "About" or "Terms of Use" page.
See the [static pages](../../customize/static_pages.md) customization section to learn how.

### Featured communities

You can now manage featured communities from the administration panel, and show them in the homepage.
This is a **preview** feature and it is disabled by default: the user experience and features currently available in the administration panel are limited. It will be improved in the upcoming releases.

You can try this feature out by changing the configuration variable `COMMUNITIES_ADMINISTRATION_DISABLED` to `False`.

### Custom code

With InvenioRDM v11, you can now add your own custom code and views directly to your instance,
without creating extra modules and adding them to the list of dependencies.

Discover how by reading the dedicated [How-to](../../develop/howtos/custom_code.md).

### Override landing page template

The record landing page template can now be overridden by editing the configuration variable `APP_RDM_RECORD_LANDING_PAGE_TEMPLATE`.
You can read more on how to customize template in the [dedicated guide](../../customize/look-and-feel/templates.md).

### Override upload form template

The upload form template can now be overridden by editing the configuration variable `APP_RDM_DEPOSIT_FORM_TEMPLATE`.
You can read more on how to customize template in the [dedicated guide](../../customize/look-and-feel/templates.md).

### URL redirection

InvenioRDM now includes a redirector module. It allows an instance to define a mapping of URLs to redirect via a configuration variable.
This is particularly useful when migrating from an old instance to InvenioRDM.

See instructions on how to configure URL redirection in its [How-to](../../develop/howtos/route_migration.md).

### Search query parser

Search fields and parameters may change overtime. You can now map legacy search terms into newer terms.

See instruction on how to add search terms mappings in its [How-to](../../develop/howtos/search_terms_migration.md).

### User visibility

The users' profile and e-mail visibility for new users can now be set by default to either `restricted` or `public`, by editing the configuration variables `ACCOUNTS_DEFAULT_USER_VISIBILITY` and `ACCOUNTS_DEFAULT_EMAIL_VISIBILITY` respectively.

```python
ACCOUNTS_DEFAULT_USER_VISIBILITY = "public"
ACCOUNTS_DEFAULT_EMAIL_VISIBILITY = "restricted"
```

This change only affects new accounts, already existing accounts will keep their existing profile and e-mail visibility.

### Download all files

You can now enable downloading of a single archive containing all of a record's uploaded files at once. Read more [here](../../customize/record_landing_page.md#download-all-files-button).

### Deployment

This new release introduces various changes to the official InvenioRDM Docker image:

- The base image now uses [AlmaLinux](https://almalinux.org/) instead of `CentOS`, after the choice of [changing focus to CentOS Stream](https://blog.centos.org/2020/12/future-is-centos-stream/). See more information in the [docker-invenio](https://github.com/inveniosoftware/docker-invenio) repository.
- This new Docker image is now published in the CERN registry, to provide an alternative to the InvenioRDM community to the [Docker Hub rate limits](https://www.docker.com/increase-rate-limits/). The images will be versioned and checked with security scans.

[Helm charts](https://github.com/inveniosoftware/helm-invenio/) are now updated with the latest deployment recipes, configuration variables and secrets.

We have also added a new [dedicated deployment guide](../../deploy/index.md) to this documentation to give an overview and some tips related to deploying InvenioRDM. This is a work in progress and will be improved taking into account the input from the InvenioRDM community.

### CLI commands

#### Rebuild all search indices

A new command `rebuild-all-indices` was added to `invenio rdm` command. It will rebuild the index of every service that is registered in the service registry.

#### Confirm user on creation

Command `invenio users create` has a new flag `--confirm`, or `-c` in short, that automatically confirms an user when created through the CLI.

### Files integrity

InvenioRDM v11 comes with new features to check files integrity.

#### Checksum

A new asynchronous task now automatically checks whether files have been corrupted, meaning that a file's checksum differs from its original checksum.
The celery task can be configured by editing the configuration `CELERY_BEAT_SCHEDULE['file-checks']`.

#### Reports

When the above task detects corrupted files, it generates a report that it is sent by e-mail, by default every day at 07:00 UTC.
The celery task can be configured by editing the configuration `CELERY_BEAT_SCHEDULE['file-integrity-report']`.

The e-mail delivery options can be modified by editing the following configurations:

- `MAIL_DEFAULT_SENDER`: modifies the e-mail sender (field `from`).
- `APP_RDM_ADMIN_EMAIL_RECIPIENT`: modifies the e-mail recipient (field `to`).
- `FILES_INTEGRITY_REPORT_SUBJECT`: modifies the  subject of the e-mail (field `subject`).

The e-mail template can be overridden by setting the configuration variable `FILES_INTEGRITY_REPORT_TEMPLATE`.

## Changes

#### Python and Node.js versions

While you can run InvenioRDM with Python version 3.7, 3.8 and 3.9, the recommended version for development and deployment is 3.9. We suggest switching to **Python 3.9**.

We recommend upgrading **Node.js** to **v16**. Next InvenioRDM releases will support more recent versions.

#### OAuth users auto-confirmed

For external authentication methods (e.g. ORCID, GitHub, SSO, etc.), the default behavior **has changed** and
for newly logged in users (users without an Invenio account yet):

- The account is already confirmed
- They will not receive a confirmation e-mail

This is applied to all OAuth plugins, but **ORCID**: when logging in with ORCID, the e-mail is provided by the user
and not retrieved from the authentication provider, and thus it requires the user to confirm the e-mail address.

For more information on how to change this setting, see the [Auto-confirm user](../../customize/authentication.md#auto-confirm-user) section in the authentication documentation.

You can also customize how user information is retrieved from the external provider. See the [Custom user info](../../customize/authentication.md#custom-user-info) section in the authentication documentation.

#### OpenAIRE OAI-PMH sets

New installations of InvenioRDM v11 will come with the default OAI-PMH sets [harvested by OpenAIRE](https://provide.openaire.eu/).
You can also use the administration panel to manually add the OpenAIRE OAI-PMH set in existing installations or use the [provided fixture](https://github.com/inveniosoftware/invenio-app-rdm/blob/master/invenio_app_rdm/fixtures/data/oai_sets.yaml).

### Breaking changes

- The following changes should not affect the majority of the users. We recommend to verify if any usage can be found in customisations or modules:
    - in [Invenio-Records-Resources](https://github.com/inveniosoftware/invenio-records-resources), the function `pick` in the `ExpandableField` class, the function `expand` in `LinksTemplate` class and the function `pick_resolved_fields` in `EntityProxy` class now require a new parameter `identity`.

## Deprecations

Support for Elasticsearch v7 is deprecated and it will be removed in a future release.

## Limitations

- The featured communities administration panel is disabled by default, due to the limited user experience and features available.
- The possibility of overriding UI components is now available with InvenioRDM, but *experimental*: the documentation is limited and components might include breaking changes in future releases.

## Upgrading to v11.0

We support upgrading from v10 to v11. Please see the [upgrade notice](../upgrading/upgrade-v11.0.md).

## Maintenance policy

InvenioRDM v11.0 is a **short-term support** (STS) release which is supported until InvenioRDM v12.0. See our [Maintenance Policy](../maintenance-policy.md).

If you plan to deploy InvenioRDM as a production service, please use InvenioRDM v9.1 Long-Term Support (LTS) Release.

## Requirements

InvenioRDM v11 supports:

- Python 3.9
- Node.js 14 and 16
- PostgreSQL 10+
- OpenSearch v1 and v2 (Elasticsearch 7 deprecated)

## Questions?

If you have questions related to these release notes, don't hesitate to jump on our chat and ask questions: [Getting help](../../develop/getting-started/help.md)

## Credit

The development work in this release was done by:

- CERN: Alex, Anna, Antonio, Javier, Jenny, Karolina, Lars, Manuel, Nicola, Pablo G., Pablo P., Zacharias
- Northwestern University: Guillaume
- TU Graz: Christoph, David, Mojib
- TU Wien: Max
- Uni Bamberg: Christina
- Uni Münster: Werner
- Front Matter: Martin
- KTH Royal Institute of Technology: Sam

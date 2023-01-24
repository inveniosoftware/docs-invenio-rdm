# InvenioRDM v11.0

_2023-01-25_

_Short-term support (STS) release_

We're happy to announce the release of InvenioRDM v11.0. The release is a short-term support release which is maintained until v12.0.

## Try it

- [Demo site](https://inveniordm.web.cern.ch)

- [Installation instructions](https://inveniordm.docs.cern.ch/install/)

## What's new?

### DOI and publisher field

Minting DOIs now requires to have the publisher field defined. Submitters will see an error if such field is not provided when requesting a DOI.

### Static pages

You can now add new static pages to your instance, for example About page or Contact page.
See the [static pages](../../customize/static_pages.md) customization section to learn how.

### Featured communities

You can now manage featured communities from the administration panel, and show them in the homepage.
This is a **preview** feature and it is disabled by default: this is because of the limited user experience and features currently available in the administration panel. It will be improved in the upcoming releases.

You can try this out by changing the configuration variable `COMMUNITIES_ADMINISTRATION_DISABLED` to `True`.

### Custom code

With InvenioRDM v11, you can now add your own custom code and views directly to your instance,
without creating extra modules and adding them to the list of dependencies.

Discover how to by reading the [Creating custom code and views](../../develop/topics/custom_code.md) topic guide.

### Override landing page template

The record landing page template can now be overridden by editing the configuration variable `APP_RDM_RECORD_LANDING_PAGE_TEMPLATE`.

### Override deposit form template

The deposit form template can now be overridden by editing the configuration variable `APP_RDM_DEPOSIT_FORM_TEMPLATE`.

### URL redirection

InvenioRDM now includes a redirector module. It allows an instance to define a map of URLs to redirect, a configuration variable.
This is particularly useful when migrating from an old instance to InvenioRDM.

See instructions on how to configure URL redirection in its [How-to](../develop/howtos/route_migration.md).

### Search query parser

Search parameters may change overtime. You can now map legacy search terms into newer terms.

See instruction on how to add search terms mappings in its [How-to](../develop/howtos/search_terms_migration.md).

### User visibility

The users' profile and e-mail visibility for new users can now be set by default to either `restricted` or `public`, by editing the configuration variables `ACCOUNTS_DEFAULT_USER_VISIBILITY` and `ACCOUNTS_DEFAULT_EMAIL_VISIBILITY` respectively.

This change only affects new accounts, already existing accounts will keep their profile and e-mail visibility.

### Docker images and helm charts

This new release introduces various changes to the official Docker image:

- The base image now uses [AlmaLinux](https://almalinux.org/) instead of `CentOS`, after the choice of [changing focus to CentOS Stream](https://blog.centos.org/2020/12/future-is-centos-stream/). See more information in the [docker-invenio](https://github.com/inveniosoftware/docker-invenio) repository.
- This new Docker image is now published in the CERN registry, to provide an alternative to the InvenioRDM community to the [Docker Hub rate limits](https://www.docker.com/increase-rate-limits/). The images will be versioned and checked with security scans.

[Helm charts](https://github.com/inveniosoftware/helm-invenio/) are now updated with the latest deployment recipes, configuration variables and secrets.

### CLI commands

#### Rebuild all search indices

A new command `rebuild-all-indices` was added to `invenio rdm` command. It will rebuild the index of every service that is registered in the service registry.

#### Confirm user on creation

Command `invenio users create` has a new flag `--confirm`, or `-c` in short, that automatically confirms an user when created through the cli.

### Files integrity

InvenioRDM v11 comes with new features to check the files integrity.

#### Checksum

A new asynchronous task now automatically checks whether files are corrupted, meaning that a file's checksum differs from the its original checksum.
The celery task can be configured by editing the configuration `CELERY_BEAT_SCHEDULE['file-checks']`.

#### Reports

When the task detects corrupted files, it generates a report that it is sent by e-mail, by default every day at 07:00 UTC.
The celery task can be configured by editing the configuration `CELERY_BEAT_SCHEDULE['file-integrity-report']`.

The e-mail fields can be modified by editing the following configurations:

- `MAIL_DEFAULT_SENDER`: modifies the e-mail sender (field `from`).
- `APP_RDM_ADMIN_EMAIL_RECIPIENT`: modifies the e-mail recipient (field `to`).
- `FILES_INTEGRITY_REPORT_SUBJECT`: modifies the  subject of the e-mail (field `subject`).

The e-mail template can be overridden setting the configuration variable `FILES_INTEGRITY_REPORT_TEMPLATE`.


## Changes
### Breaking changes

- The following changes should not affect the majority of the users. We recommend to verify if any usage can be found in customisations or modules:
    - in [Invenio-Records-Resources](https://github.com/inveniosoftware/invenio-records-resources), the func `pick` in the `ExpandableField` class, the func `expand` in `LinksTemplate` class and the func `pick_resolved_fields` in `EntityProxy` class now require a new param `identity`.

### Other changes

#### OAuth users confirmed

For external authentication methods (e.g. ORCID, GitHub, SSO, etc.), the default behavior **has changed** and
for newly logged in users (users without an Invenio account yet):

    - the account is already confirmed
    - they will not receive a confirmation e-mail

This is applied to all OAuth plugins, but **ORCID**: when logging in with ORCID, the e-mail is provided by the user
and not retrieved from the authentication provider. It requires the user to confirm the e-mail address.

For more information on how to change this setting, see the [Auto-confirm user](../../customize/authentication.md#auto-confirm-user) section in the authentication documentation.

You can also customize how user information is retrieved from the external provided. See the [Custom user info](../../customize/authentication.md#custom-user-info) section in the authentication documentation.

## Deprecations

TODO

## Limitations

TODO

## Upgrading to v11.0

We support upgrading from v10 to v11 Please see the [upgrade notice](../upgrading/upgrade-v11.0.md).

## Maintenance policy

InvenioRDM v11.0 is a **short-term support** (STS) release which is supported until InvenioRDM v12.0. See our [Maintenance Policy](../maintenance-policy.md).

If you plan to deploy InvenioRDM as a production service, please use InvenioRDM v9.1 Long-Term Support (LTS) Release.

## Requirements

TODO

## Questions?

If you have questions related to these release notes, don't hesitate to jump on our chat and ask questions: [Getting help](../../develop/getting-started/help.md)

## Credit

The development work in this release was done by:

- CERN: Alex, Anna, Antonio, Javier, Jenny, Karolina, Lars, Manuel, Nicola, Pablo, Pablo, Zacharias
- Northwestern University: Guillaume
- TU Graz: Christoph, David, Mojib
- TU Wien: Max
- Uni Bamberg: Christina
- Uni Münster: Werner
- Front Matter: Martin

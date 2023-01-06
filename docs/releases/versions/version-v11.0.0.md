# InvenioRDM v11.0

_2023-01-05_ (TBD)

_Short-term support (STS) release_

We're happy to announce the release of InvenioRDM v11.0. The release is a short-term support release which is maintained until v12.0.

## Try it

- [Demo site](https://inveniordm.web.cern.ch)

- [Installation instructions](https://inveniordm.docs.cern.ch/install/)

## What's new?

TODO

## Changes

### Breaking changes

- TODO

### Minor changes

#### Docker images and helm charts

TODO

#### Deposit form template

The deposit form template can now be overriden by editing the configuration variable `APP_RDM_DEPOSIT_FORM_TEMPLATE`.

#### CLI commands

##### Rebuild all search indices

A new command `rebuild-all-indices` was added to `invenio rdm` command. It will rebuild the index of every service that is registered in the service registry.

##### Confirm user on creation

Command `invenio users create` has a new flag `--confirm`, or `-c` in short, that automatically confirms an user when created through the cli.

#### Files integrity

##### Checksum

A task was added to automatically check whether files are corrupted, meaning that a file's checksum differs from the its original checksum.
The celery task can be configured by editing the configuration `CELERY_BEAT_SCHEDULE['file-checks']`.

##### Reports

By default, everyday at 07:00 UTC a file integrity report is sent, by e-mail, in case a file is found to be corrupted.
The celery task can be configured by editing the configuration `CELERY_BEAT_SCHEDULE['file-integrity-report']`.
The e-mail sender and recipient can be modified by editing the following configurations:

- sender: `MAIL_DEFAULT_SENDER`
- recipient: `APP_RDM_ADMIN_EMAIL_RECIPIENT`

> Note: `MAIL_DEFAULT_SENDER` is a configuration used by `Flask-Mail`. If set, you don’t need to set the message sender explicity, as it will use this configuration value by default.

#### URL redirections

The redirector module was added to Invenio RDM. It allows an instance to add URL redirections using a configuration variable. See instructions on how to add an url redirection in its [howto](../develop/howtos/route_migration.md)

#### Search query parser

Search parameters may change overtime. It was added the possibility to map legacy search terms into newer terms. See instruction on how to add search terms mappings in its [howto](../develop/howtos/search_terms_migration.md)

#### Default global visibility setting

New users' profile and e-mail visibility can now be set by default to either `restricted` or `public`, by editing the configuration variables `ACCOUNTS_DEFAULT_USER_VISIBILITY` and `ACCOUNTS_DEFAULT_EMAIL_VISIBILITY` respectively. This change only affects new accounts, already existing accounts will keep their profile and e-mail visibility.

#### Oauth

TODO

#### Custom views

To extend your instance with your own custom views, you can use the predefined “site” folder in your instance. 

See instructions on how to add custom views in its [howto](../develop/../../develop/topics/custom_views.md)

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

- CERN: Alex, Anika, Javier, Jenny, Karolina, Lars, Manuel, Nicola, Nicolas, Pablo, Pablo, Zacharias
- Northwestern University: Guillaume
- TU Graz: Christoph, David, Mojib
- TU Wien: Max
- Uni Bamberg: Christina
- Uni Münster: Werner

TODO add others
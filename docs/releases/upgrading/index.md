# Upgrading

Following are guides for how to upgrade an Invenio instance from version to version.
By default we only support upgrading from the previous latest version. Thus, if you'd like
to upgrade from v1.0 to v3.0, you first have to upgrade to v2.0 and then from v2.0 to v3.0

## Upgrade contract

The following "contract" is meant to align expectations on how and what you'll be able to upgrade from v2.0 to v3.0.

You **MUST** expect **breaking changes** to anything on subsequent releases until the LTS release! REST APIs, programmatic APIs, features, Jinja/React templates, data model, vocabularies, etc.

We will **ONLY** guarantee that you will be able to upgrade a database created with v2.0 to v3.0. With that, we mean that **through a manual, labour intensive and offline process** you'll be able to upgrade your database. Basically this boils down to, that we will document the steps you need to apply in order to move your data from v1.0 to v2.0 code. In no way do we promise it will be easy! You **MAY** need to apply manual changes to records. We of course plan to make this an easy and smooth process for the LTS release, but for now it's not.

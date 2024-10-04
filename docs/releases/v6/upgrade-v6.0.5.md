# Upgrading from v6.0.x to v6.0.5

## Prerequisites

You must have an existing installation of InvenioRDM v6.0.x.

## Steps

### Upgrade your instance dependencies

Bump the RDM version and rebuild the assets:

```bash
cd my-site
invenio-cli packages update 6.0.5
```

Your ``Pipfile`` and ``Pipfile.lock`` should have been updated.

### Verify installed packages

You can now verify that the correct packages have been installed:

```
pipenv run pip freeze | egrep "invenio-(drafts-resources|rdm-records|app-rdm|rest|accounts)"
invenio-accounts==1.4.9
invenio-app-rdm==6.0.5
invenio-drafts-resources==0.13.7
invenio-rdm-records==0.32.6
invenio-rest==1.2.7
```

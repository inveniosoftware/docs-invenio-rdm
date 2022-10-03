# Upgrading from v9.0 to v10.0

## Prerequisites

The steps listed in this article require an existing local installation of InvenioRDM v9.0, please make sure that this is given!

If unsure, run `invenio-cli install` from inside the instance directory before executing the listed steps.

!!! warning "Backup"

    Always backup your database and files before you try to perform an upgrade.

!!! info "Older versions"

    In case you have an InvenioRDM installation older than v9.0, you can gradually upgrade using the existing instructions to v9.0 and afterwards continue from here.

## Upgrade Steps

!!! warning "Upgrade your invenio-cli"

    Make sure you have the latest `invenio-cli`, for InvenioRDM v10 the release is v1.0.5

### Installing the Latest Versions

Bump the RDM version, create a folder for your custom fields and rebuild the assets:

```bash
# Upgrade to InvenioRDM v10
invenio-cli packages update 10.0.0

# Create custom fields folder
cd <my-site>
mkdir assets/templates/custom_fields

# Build the instance assets
invenio-cli assets build
```

These commands should take care of locking the dependencies for v10, installing them, and building the required assets.


### Data Migration

Finally, you can run the database schema upgrade, and perform the records data migration:

```bash
# Perform the database migration
pipenv run invenio alembic upgrade

# Run data migration script
pipenv run invenio shell $(find $(pipenv --venv)/lib/*/site-packages/invenio_app_rdm -name migrate_9_0_to_10_0.py)
```

### Elasticsearch

The last required step is the migration of Elasticsearch indices:

```bash

pipenv run invenio index destroy --yes-i-know
pipenv run invenio index init
pipenv run invenio rdm-records rebuild-index
pipenv run invenio communities rebuild-index
```

This will ensure that all indices and their contents are based on the latest definitions and not out of date.

#### Strict mappings

Previously record and community mappins were dynamic, which means that any unknwon value could be added to it. This would be the case for custom elasticsearch dumper extensions. This dumpers need to be modified to dump those fields in new _custom fields_. Then the records and communities need to be re-indexed.

\`\`\`shell
# destroy the current indices
pipenv run invenio index destroy --yes-i-know
pipenv run invenio index init

# once you have configured your new custom fields
invenio rdm-records custom-fields init -f <field name> -f <field name>
invenio communities custom-fields init -f <field name> -f <field name>

# reindex records
pipenv run invenio rdm-records rebuild-index
pipenv run invenio communities rebuild-index
\`\`\`

As soon as the records have been reindexed, the entire migration is complete! :partying_face:

Additionally, the following section will contain an explanation on how to use the new administration panel.

### Accessing the Administration panel

A new permission (`administration-access`) is needed to access the administration panel. There are 2 ways to grant this permission.

1) Permission can be added using a role:
```
# Create a rol 
pipenv run invenio roles create administration

# Allow access to administration to the administration role
pipenv run invenio access allow administration-access role administration

# Add administration role to an user email
pipenv run invenio roles add <user_email> administration
```

2) Permission can be added to a specific user:
```
# Add access to administration to an user email
pipenv run invenio access allow administration-access user <user_email>
```

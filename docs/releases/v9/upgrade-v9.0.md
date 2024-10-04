# Upgrading from v8.0 to v9.0

## Prerequisites

The steps listed in this article require an existing local installation of InvenioRDM v8.0, please make sure that this is given!

If unsure, run `invenio-cli install` from inside the instance directory before executing the listed steps.

!!! warning "Backup"

    Always backup your database and files before you try to perform an upgrade.

!!! info "Older versions"

    In case you have an InvenioRDM installation older than v8.0, you can gradually upgrade using the existing instructions to v8.0 and afterwards continue from here.

## Upgrade Steps

!!! warning "Upgrade your invenio-cli"

    Make sure you have the latest `invenio-cli`, for InvenioRDM v9 the release is v1.0.5

### Installing the Latest Versions

Clean-up previous versions' Python dependencies and bump the InvenioRDM version:

```bash
# Uninstall modules that were forked/removed and might cause namespace issues
pipenv run pip uninstall -y invenio-iiif flask-security-invenio flask-security flask-kvsession flask-kvsession-invenio

# Upgrade to InvenioRDM v9
invenio-cli packages update 9.0.2
```

These commands should take care of locking the dependencies for v9 and installing them.

### Updating Configuration Variables

Communities feature comes built-in InvenioRDM and cannot be disabled anymore. Therefore, the
`COMMUNITIES_ENABLED` variable is not needed anymore. On the other hand, you can now enable/disable
groups support in communities by setting `COMMUNITIES_GROUPS_ENABLED` to `True`/`False`.

### Update styling

Due to theme refactoring done in order to facilitate the theme customisation, you need to update the following files:

`{{project_shortname}}/assets/less/site/globals/site.overrides`

``` diff
- @import "@less/invenio_app_rdm/theme";
```

`{{project_shortname}}/assets/less/site/globals/site.variables`

```diff
- @import "@less/invenio_app_rdm/variables";
```

`{{project_shortname}}/assets/less/theme.config`

```diff
/* Path to theme packages */
- @themesFolder : 'themes';
+ @themesFolder : '~semantic-ui-less/themes';

...

@siteFolder : '../../less/site';
+ @imagesFolder : '../../images';

...

/*******************************
         Import Theme
*******************************/

- @import (multiple) "~semantic-ui-less/theme.less";
+ @import (multiple) "themes/rdm/theme.less";
```

Please take into account the changes made in the theming, including variable names and overall theme re-structurisation. If you had any customisations done based on the old structure, your styling might need to be updated.

You can afterwards build the instance assets:

```bash
invenio-cli assets build
```

### Data Migration

Due to an inconsistency in the database versioning table, you should start the data migration with:

```bash
# Change entry in alembic versions table
pipenv run invenio shell -c "from invenio_db import db; db.session.execute(\"UPDATE alembic_version SET version_num ='f701a32e6fbe' WHERE version_num='f261e5ee8743'\"); db.session.commit()"
```

Now you can run the database schema upgrade, add new fixtures, and perform the records data migration:

```bash
# Perform the database migration
pipenv run invenio alembic upgrade

# Add new fixtures
pipenv run invenio rdm-records fixtures

# Run data migration script
pipenv run invenio shell $(find $(pipenv --venv)/lib/*/site-packages/invenio_app_rdm -name migrate_8_0_to_9_0.py)
```

Some older parent records might not have the communities field set. To be sure these are updated as well, run the following command:

```bash
# Run data migration script for older records parents
pipenv run invenio shell $(find $(pipenv --venv)/lib/*/site-packages/invenio_app_rdm -name fix_migrated_records_from_8_0_to_9_0.py)
```


### Elasticsearch

The last required step is the migration of Elasticsearch indices:

```bash
# If you're using an index prefix for your Elasticsearch cluster, you'll have to set it
INDEX_PREFIX=""

pipenv run invenio index delete "${INDEX_PREFIX}communitymembers-*" --yes-i-know
pipenv run invenio index delete "${INDEX_PREFIX}request_events-*" --yes-i-know
pipenv run invenio index destroy --yes-i-know
pipenv run invenio index init
pipenv run invenio rdm-records rebuild-index
```

This will ensure that all indices and their contents are based on the latest definitions and not out of date.

As soon as the indices have been rebuilt, the entire migration is complete! 🥳

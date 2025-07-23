# Upgrading from v12 to v13.0

## Prerequisites

The steps listed in this article require an existing local installation of InvenioRDM v12.

!!! warning "Backup"

    Always backup your database, statistics indices and files before you try to perform an upgrade.

!!! info "Older Versions"
    If your InvenioRDM installation is older than v12, you must first upgrade to v12 before proceeding with the steps in this guide.

## Upgrade Steps

Make sure you have the latest `invenio-cli` installed. For InvenioRDM v13,
it should be v1.9.0+.

```bash
$ invenio-cli --version
invenio-cli, version 1.9.0
```

!!! info "Virtual environments"

    In case you are not inside a virtual environment, make sure that you prefix each `invenio`
    command with `pipenv run`.

### Upgrade InvenioRDM

#### Requirements
Python 3.9 or 3.11 or 3.12 is required to run InvenioRDM v13.

!!! info "Python 3.9 end-of-life"
    Official support for Python 3.9 will end on October 31, 2025.
    See the [official Python version status page](https://devguide.python.org/versions/) for more information.
    Future releases of InvenioRDM will require a more recent Python version.

The minimum required OpenSearch version is now **v2.12**. See [below](#opensearch-version) on how to upgrade older versions.

#### Upgrade option 1: In-place
This approach upgrades the dependencies in place. At the end of the process,
your virtual environment for the v12 version will be completely replaced
with the v13 environment and dependencies.

```bash
cd <my-site>

# Upgrade to InvenioRDM v13
invenio-cli packages update 13.0.0
# The old `invenio-admin` dependency has been removed and must be uninstalled
pipenv run pip uninstall -y invenio-admin
# Re-build assets
invenio-cli assets build
```

#### Upgrade option 2: New virtual environment

This approach will create a new virtual environment and leaves the v12 one as-is.
If you are using a docker image on your production instance this will be the
option you choose.

!!! warning "Risk of losing data"

    Your virtual environment folder a.k.a., `venv` folder, may contain uploaded files. If you kept the default
    location, it is in `<venv folder>/var/instance/data`. If you need to keep those files,
    make sure you copy them over to the new `venv` folder in the same location.
    The command `invenio files location list` shows the file upload location.

##### Step 1

- create a new virtual environment
- activate your new virtual environment
- install `invenio-cli` by running `pip install invenio-cli`

##### Step 2

Update the `<my-site>/Pipfile` by changing the `version` of `invenio-app-rdm` to `~=13.0.0` and removing the unnecessary `postgresql` extra
(it is already installed by default and will trigger a warning if left in the file):

```diff
[packages]
---invenio-app-rdm = {extras = [..., "postgresql"], version = "~=12.0.0"}
+++invenio-app-rdm = {extras = [...], version = "~=13.0.0"}
```

If you're using [Sentry](https://sentry.io) (tool for monitoring or error tracking), update the dependency in `<my-site>/Pipfile` to:

```diff
---invenio-logging = {extras = ["sentry_sdk"], version = "~=2.0"}
+++sentry-sdk = {extras = ["flask"], version = ">=1.0.0,<2.0.0"}
```

##### Step 3

Update the `Pipfile.lock` file:

```bash
invenio-cli packages lock
```

##### Step 4

Install InvenioRDM v13:

```bash
invenio-cli install
```

### Activate the virtual environment

Before running any `invenio` commands, activate your virtual environment shell:

```bash
$ invenio-cli shell
Launching subshell in virtual environment...
source <path to virtualenvs>/bin/activate
```

This step ensures that all subsequent commands use the correct Python environment and installed dependencies.

!!! note
    If you are upgrading in an environment that does not use a Python virtualenv, you can skip this step.

### Database migration

Execute the database migration:

```bash
invenio alembic upgrade
```

### Data migration

Execute the data migration:

```bash
invenio shell $(find $(pipenv --venv)/lib/*/site-packages/invenio_app_rdm -name migrate_12_0_to_13_0.py)
```

### Rebuild search indices

```bash
invenio index destroy --yes-i-know
search_prefix=$(invenio shell -c "print(app.config['SEARCH_INDEX_PREFIX'])")
invenio index delete --force --yes-i-know "${search_prefix}rdmrecords-records-record-v6.0.0-percolators"
invenio index init
# if you have records custom fields
invenio rdm-records custom-fields init
# if you have communities custom fields
invenio communities custom-fields init
invenio rdm rebuild-all-indices
```

From v12 onwards, search indices for statistics (record's views and downloads) are not
affected by `invenio index destroy --yes-i-know` and are totally functional after the rebuild step.

!!! info "Permission issue"
    If you encounter an error similar to this when indexing:
    ```
    opensearchpy.exceptions.AuthorizationException: AuthorizationException(403, 'security_exception', 'no permissions for [cluster:admin/component_template/put] and User [name=<my-name>, backend_roles=[], requestedTenant=null]')
    opensearchpy.exceptions.AuthorizationException: AuthorizationException(403, 'security_exception', 'no permissions for [indices:admin/index_template/put] and User [name=<my-name>, backend_roles=[], requestedTenant=null]')
    ```
    This means your OpenSearch user does not have sufficient permissions to create or update index templates.
    To resolve this, grant the necessary permissions to your user in the OpenSearch cluster:

      1. Go to **OpenSearch Dashboards** -> **Security** -> **Roles** -> *<your role name>*.
      2. Edit the role and add the following cluster and index permissions:
         - `cluster:admin/component_template/put`
         - `indices:admin/index_template/put`

### Updated affiliations and funders
InvenioRDM now integrates the updated schema version v2 of ROR (see [announcement here](https://ror.org/blog/2024-04-15-announcing-ror-v2/)). This new version introduces additional fields and improvements, so you will need to re-import both the affiliations and funders vocabularies to ensure your data is up to date.

To re-import, you can either set up a job or perform the import manually via the CLI. Please follow the instructions in the [affiliations](../../operate/customize/vocabularies/affiliations.md) and [funders](../../operate/customize/vocabularies/funding.md) documentation pages for detailed steps.

## Infrastructure/configuration changes

### Required changes

#### OpenSearch version
The minimum required OpenSearch version is now **v2.12**. This change is necessary due to a bug in earlier OpenSearch versions that affects the handling of `geo-shape` fields introduced in InvenioRDM v13.
For more details, see the related [InvenioRDM issue](https://github.com/inveniosoftware/invenio-rdm-records/issues/1807) and the [OpenSearch issue and discussion](https://github.com/opensearch-project/OpenSearch/issues/10958#issuecomment-2037882756).

To check the current version, connect to the OpenSearch Dashboard with your browser or run the following CLI command:

```bash
$ curl -X GET "http://localhost:9200"
{
  ...
  "version" : {
    "distribution" : "opensearch",
    "number" : "2.17.1",
    ...
  },
  ...
}
```

Add `-u <username>:<password>` if you require authentication, or `-k` to ignore SSL certificate warnings.

Please refer to the official [OpenSearch upgrade documentation](https://docs.opensearch.org/docs/latest/install-and-configure/upgrade-opensearch/index/).
If you choose to delete and re-create your search cluster as part of the upgrade, remember to **back up and restore your statistics indices** (see [how to do this here](../../maintenance/internals/statistics.md)).
Be sure to repeat the [Rebuild search indices](#rebuild-search-indices) step to ensure your system is fully functional.

#### Jobs
The new Jobs feature uses a custom celery task scheduler which requires a separate celery beat. See the [related documentation](../../operate/customize/jobs.md#scheduler) or [the scheduler service](https://github.com/inveniosoftware/cookiecutter-invenio-rdm/blob/ff6c652091d56e7a8aa0a90487f91352f70c4e33/%7B%7Bcookiecutter.project_shortname%7D%7D/docker-compose.full.yml) in the InvenioRDM boilerplate for how to add it.

!!! warning
    Be sure to run this additional Celery beat scheduler in **your Docker Compose, any deployed and production environments**. Without it, scheduled and on-demand jobs will not be executed.

#### Updated PDF previewer
The updated PDF file previewer (PDF.js v4) now uses ECMAScript modules (`.mjs`) instead of CommonJS files (`.js`). By default, the `nginx` web server does not recognize `.mjs` files in its [default MIME types configuration](https://github.com/nginx/nginx/blob/master/conf/mime.types#L8). As a result, the MIME type may be reported incorrectly, causing browsers to block the file and resulting in broken PDF previews.

To resolve this, simply add a custom [`types`](https://nginx.org/en/docs/http/ngx_http_core_module.html#types) entry in your `nginx.conf` (for example, in the `http` block). See [this change](https://github.com/inveniosoftware/cookiecutter-invenio-rdm/pull/299) in the InvenioRDM boilerplate for reference.

```diff
  ...
  include       /etc/nginx/mime.types;
  default_type  application/octet-stream;
+ types {
+     # Ensure nginx treats ECMAScript modules as JavaScript
+     application/javascript js mjs;
+ }
  ...
```

### Optional changes

#### Deprecations

*`APP_ALLOWED_HOSTS`*

With the upgrade to Flask version 3, the configuration variable `APP_ALLOWED_HOSTS` has been renamed to `TRUSTED_HOSTS`. The value remains unchanged.
You should review your `invenio.cfg`, environment variables, and deployment configuration for any occurrences of the old variable name.
It is recommended to update all references to `TRUSTED_HOSTS` to avoid deprecation warnings in the console and prepare for its eventual complete removal.

*`invenio_records_resources.services.Link`*

Usage of `invenio_records_resources.services.Link` is deprecated in favor of `invenio_records_resources.services.EndpointLink` for InvenioRDM links and `invenio_records_resources.services.ExternalLink` for external third-party links. Replace instances of `Link` in your custom code, if any, appropriately. `Link` will be removed in a future major InvenioRDM release.

#### Display versions in administration panel
As described in the [release notes](./version-v13.0.0.md#miscellaneous-additions), you can now display the versions of your installed modules directly in the Administration panel.
To enable this feature, add the following to your `invenio.cfg`:

```python
from invenio_app_rdm import __version__
ADMINISTRATION_DISPLAY_VERSIONS = [
    ("invenio-app-rdm", f"v{__version__}"),
    ("<my module name>",
]
```

#### FAIR signposting level 1
If you have enabled FAIR Signposting, ensure that you have updated your web server configuration as required. See the [documentation here](../../operate/customize/FAIR-signposting.md#level-1) for detailed instructions.

Failing to apply these changes may result in errors when accessing certain records.

#### Enhanced File Uploader (Uppy)
If you plan to use the new Uppy file uploader, ensure that your Content Security Policy (CSP) settings are updated in your `invenio.cfg` as described in the [enhanced file uploader documentation](../../operate/customize/file-uploads/uploader.md#enhanced-file-uploader-uppy). Failing to update your CSP rules may prevent the uploader from functioning correctly.

#### New configuration variables

These are the new configuration variables introduced in this release. Make sure that you read the related documentation before enabling them. Add them to your `invenio.cfg` as needed:

```python
# Enable FAIR Signposting
APP_RDM_RECORD_LANDING_PAGE_FAIR_SIGNPOSTING_LEVEL_1_ENABLED = True
# Enable Audit Logs
AUDIT_LOGS_ENABLED = True
# Enable Curation Checks (manual setup required)
CHECKS_ENABLED = True
# Enable the new Uppy file uploader (experimental feature)
APP_RDM_DEPOSIT_NG_FILES_UI_ENABLED = True
```

# Upgrading from v12 to v13.0

!!! warning "THIS RECIPE IS A WORK IN PROGRESS"

## Prerequisites

The steps listed in this article require an existing local installation of InvenioRDM v12.

!!! warning "Backup"

    Always backup your database and files before you try to perform an upgrade.

!!! info "Older Versions"

    In case you have an InvenioRDM installation older than v12, you can gradually upgrade
    to v12 and afterwards continue from here.

!!! read through the whole upgrade steps before upgrading

## Upgrade Steps

Make sure you have the latest `invenio-cli` installed. For InvenioRDM v13, it
should be v1.7.0+

```bash
$ invenio-cli --version
invenio-cli, version 1.7.0
```

!!! info "Virtual environments"

    In case you are not inside a virtual environment, make sure that you prefix each `invenio`
    command with `pipenv run`.

**Local development**

Changing the Python version in your development environment highly
depends on your setup, so we won't cover it here.
One way would be to use [PyEnv](https://github.com/pyenv/pyenv).

!!! warning "Risk of losing data"

    Your virtual environment folder a.k.a., `venv` folder, may contain uploaded files. If you kept the default
    location, it is in `<venv folder>/var/instance/data`. If you need to keep those files,
    make sure you copy them over to the new `venv` folder in the same location.
    The command `invenio files location list` shows the file upload location.

If you upgraded your python version, you should recreate your virtual environment before
running `invenio-cli` or `pipenv` commands below.

### Upgrade InvenioRDM

Python 3.9 or 3.11 or 3.12 is required to run InvenioRDM v12.

Note: endoflife of python3.9 will be 31. October 2025. There will be no
python3.9 related updates done after that date.

There are two options to upgrade your system:

#### Upgrade option 1: In-place

This approach upgrades the dependencies in place. Your virtual environment for the
v12 version will be gone afterwards.

```bash
cd <my-site>

# Upgrade to InvenioRDM v13
invenio-cli packages update 13.0.0

# Re-build assets
invenio-cli assets build
```

#### Upgrade option 2: New virtual environment

This approach will create a new virtual environment and leaves the v12 one as-is.
If you are using a docker image on your production instance this will be the
option you choose.

##### Step 1

- create a new virtual environment
- activate your new virtual environment
- install `invenio-cli` by `pip install invenio-cli`

##### Step 2

Update the file `<my-site>/Pipfile`.

```diff
[packages]
---invenio-app-rdm = {extras = [...], version = "~=12.0.0"}
+++invenio-app-rdm = {extras = [...], version = "~=13.0.0"}
```

If you're using Sentry, update invenio-logging in `<my-site>/Pipfile` to

```diff
---invenio-logging = {extras = ["sentry_sdk"], version = "~=2.0"}
+++invenio-logging = {extras = ["sentry"]}
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


### Configuration change for `nginx`

The new PDF file previewer is based on `pdfjs-dist` v4, which uses ECMAScript modules (`.mjs`) over CommonJS files (`.js`).
These files are not registered in the [default configuration](https://github.com/nginx/nginx/blob/master/conf/mime.types#L8) for `nginx`.
This can result in the MIME type being reported incorrectly, and thus being blocked by the browser, leading to a broken PDF preview.

Luckily, this can be simply fixed by adding a custom [`types`](https://nginx.org/en/docs/http/ngx_http_core_module.html#types) entry;
e.g. in the `http` block in [`nginx.conf`](https://github.com/inveniosoftware/cookiecutter-invenio-rdm/blob/master/%7B%7Bcookiecutter.project_shortname%7D%7D/docker/nginx/nginx.conf)
(cf. this [Cookiecutter PR](https://github.com/inveniosoftware/cookiecutter-invenio-rdm/pull/299)).

```nginx
include       /etc/nginx/mime.types;
default_type  application/octet-stream;
types {
    # Tell nginx that ECMAScript modules are also JS
    application/javascript js mjs;
}
```

### if you plan to use `APP_RDM_DEPOSIT_NG_FILES_UI_ENABLED`

you have to add following

```
        "script-src": [
            "'self'", "blob:", "'wasm-unsafe-eval'"  # for WASM-based workers, e.g. hash-wasm
        ],
```

in the `invenio.cfg` file to the

```
APP_DEFAULT_SECURE_HEADERS = {
    "content_security_policy": {}
}
```

configuration.

### Jobs

#### New worker beat scheduler

```
celery -A invenio_app.celery beat --scheduler invenio_jobs.services.scheduler:RunScheduler
```

#### New Index Template for Job Logs

Replace `localhost:9200` and `__SEARCH_INDEX_PREFIX__ `with your instance values.

Then run:

```bash
curl -X PUT "http://localhost:9200/_index_template/job-logs-v1.0.0" -H "Content-Type: application/json" -d '
{
  "index_patterns": ["__SEARCH_INDEX_PREFIX__job-logs*"],
  "data_stream": {},
  "template": {
    "mappings": {
      "properties": {
        "@timestamp": { "type": "date" },
        "level": { "type": "keyword" },
        "message": { "type": "text" },
        "module": { "type": "keyword" },
        "function": { "type": "keyword" },
        "line": { "type": "integer" },
        "context": {
          "type": "object",
          "properties": {
            "job_id": { "type": "keyword" },
            "run_id": { "type": "keyword" }
          },
          "dynamic": true
        }
      }
    }
  }
}'
```

### Rebuild search indices

#### full rebuild

```bash
invenio index destroy --yes-i-know
invenio index init
invenio rdm rebuild-all-indices
```

From v12 onwards, record statistics will be stored in search indices rather than the
database. These indices are created through some _index templates_ machinery
rather than having indices registered directly in `Invenio-Search`. As such, the
search indices for statistics are not affected by `invenio index destroy
--yes-i-know` and are totally functional after the rebuild step.

#### possible live update

CHECK if that works
```bash
invenio index update names-name-v2.0.0 --no-check
```

TODO: this is also required to create the mapping for the new `copyright` field.



### Updated vocabularies

InvenioRDM now supports ROR v2, and you should update your affiliations and
funders vocabularies following the
instructions on the [affiliations](../../operate/customize/vocabularies/affiliations.md)
and [funders](../../operate/customize/vocabularies/funding.md) documentation pages.


### FAIR signposting level 1

However, since enabling FAIR signposting level 1 does increase the size of HTTP response headers, it is recommended to edit the `nginx` configuration and specify [`uwsgi_buffer_size`](https://nginx.org/en/docs/http/ngx_http_uwsgi_module.html#uwsgi_buffer_size) with a higher limit than the default values. If you have enabled `uwsgi_buffering on;`, then [`uwsgi_buffers`](https://nginx.org/en/docs/http/ngx_http_uwsgi_module.html#uwsgi_buffers) may also be adjusted.

```nginx
server {
   # ...
   # Allow for larger HTTP response headers for FAIR signposting level 1 support
   uwsgi_buffer_size 16k;
   # optional if uwsgi_buffering on;
   uwsgi_buffers 8 16k;

   # ...
}
```

### New roles
nothing yet


### New configuration variables

```bash
from invenio_app_rdm import __version__
ADMINISTRATION_DISPLAY_VERSIONS = [
    ("invenio-app-rdm", f"v{__version__}"),
    ("{{ cookiecutter.project_shortname }}", "v1.0.0"),
]
```

### Changed configuration variables

- change from `APP_ALLOWED_HOSTS` to `TRUSTED_HOSTS` due flask >= 3


## Big Changes

- feature: invenio jobs module, periodic tasks administration panel
- feature: invenio vocabularies entries deprecation
- improvement: search mappings and analyzers to improve performance
- OpenSearch min version now required v2.12 due to breaking changes in `geo-shape` fields, see issue [here](https://github.com/inveniosoftware/invenio-rdm-records/issues/1807) and related OpenSearch issue and comment [here](https://github.com/opensearch-project/OpenSearch/issues/10958#issuecomment-2037882756).
- dashboard: `shared_with_me` drafts and requests. See [issue[(https://github.com/inveniosoftware/docs-invenio-rdm/blob/master/docs/releases/v13/upgrade-v13.0.md)
- custom fields: thesis subfields renamed (TODO: migration recipe)
- custom fields: meeting url changed to identifiers subfield (TODO: migration recipe)
- experimental: using uv (instead of pipenv), rspack (instead of webpack) and pnpm (instead of npm)

Document this error, or actually add it to the upgrade recipe


## OPEN PROBLEMS

```
opensearchpy.exceptions.AuthorizationException: AuthorizationException(403, 'security_exception', 'no permissions for [cluster:admin/component_template/put] and User [name=inveniordm-qa, backend_roles=[], requestedTenant=null]')

opensearchpy.exceptions.AuthorizationException: AuthorizationException(403, 'security_exception', 'no permissions for [indices:admin/index_template/put] and User [name=inveniordm-qa, backend_roles=[], requestedTenant=null]')
```

To solve it, grant permission to the user in OpenSearch cluster:
Go to OpenSearch Dashboards -> Security -> Roles -> <instance name>, edit role and add:

- `cluster:admin/component_template/put`
- `indices:admin/index_template/put`


## OPEN PROBLEMS
nothing yet

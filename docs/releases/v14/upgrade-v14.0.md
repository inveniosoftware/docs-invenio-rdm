# Upgrading from v13 to v14

## Background and prerequisites

This article details the low-level steps to follow to upgrade your InvenioRDM v13 instance to v14.0.

Version 14 introduces a number of default tooling changes (`pipenv` -> `uv`, `npm` -> `pnpm`, ...) and recommends using Python 3.14.

As usual, these steps do assume an existing installation of InvenioRDM v13, the previous version.
If your InvenioRDM installation is older than v13, you must first upgrade to v13 before proceeding
with the steps in this guide. However, it doesn't assume you are necessarily on
[v13.1](../v13/version-v13.1.0.md). The instructions will work whether you are on v13.0 or v13.1.

The throughline of this document is a sequential series of steps to execute. **Do read** the optional sections as they sometimes indicate changes to apply even if NOT adopting change. We highly recommend running the steps in a local development environment first where experience with the particularities of your instance can be gained without data loss worry. Then we recommend you run the steps into a staging environment mirroring your production deployment and accrue further insight into specificities of your environment (or missing details in these update steps!). Equipped with that knowledge, running the steps on your production environment should be smooth.

As always, reach out on [Discord](https://discord.gg/8qatqBC) if you need help! There are more details in this one, so don't hesitate.

!!! warning "Backup"

    Always backup your database, statistics indices and files before you try to perform an upgrade.

## Upgrade to InvenioRDM v14 proper

*Required for upgrade*: **Yes!** This *is* the main upgrade section afterall.

Here are the core sequential steps to upgrade to InvenioRDM v14.

!!! info "Virtual environments"

    All commands below assume you are running them according to their installation environments. Typically it means `invenio` commands should be executed:

    - inside the application's virtual environment OR
    - via `pipenv run` or `uv run` in case you are not inside a virtual environment OR
    - environment with executables installed globally

!!! warning "A note on virtual environments and possible data loss"

    If your deposited files are stored in `<venv folder>/var/instance/data`,
    you should back them up outside this location before you continue. This
    command checks the location of your deposited files:


    ```bash
    invenio files location list
    ```

    This is usually only the case in development, as a containerized
    production deployment will store the deposited files elsewhere.


### Check your database for the `alembic_version` table

In order to proceed with the database migration later on, the
`alembic_version` table must exist in your database. Run the following
to check for its existence:

```bash
invenio alembic current
```

If the command's output is very short and contains no lines of the
shape `{id} -> {id} ({package_name}) (head), {description}`, that
means that the `alembic_versions` table either doesn't exist or is
empty.

On the server (production instance), run the following command to
create the `alembic_version` table. This command should
**only be run now with InvenioRDM v13** (not with InvenioRDM v14).

```bash
invenio alembic stamp
```

!!! info "Why was this necessary"
    InvenioRDM v13 contained a race condition that could have
    prevented the `alembic_version` table from being created.
    [Alembic](https://alembic.sqlalchemy.org/) uses this table to track
    database schema migrations, and you cannot upgrade to v14 without it.

If you encounter issues, please ask for help on our [Discord](https://discord.gg/8qatqBC) server.

### Upgrade invenio-cli

Make sure you have the latest `invenio-cli` installed. For InvenioRDM v14,
it should be v1.12.0 or higher. See [Install the command line tool](../../install/cli.md) for how to install it.

```bash
$ invenio-cli --version
invenio-cli, version 1.12.0
```

### Upgrade packages

Change the version of `invenio-app-rdm` to 14.0 in `<my-site>/pyproject.toml` if using `uv` or `<my-site>/Pipfile` if using `pipenv`:

=== "pyproject.toml"

    ```diff
    dependencies = [
    ---    invenio-app-rdm[opensearch2]~=13.0.0",
    +++    invenio-app-rdm[opensearch2]~=14.0.0",
    ```

=== "Pipfile"

    ```diff
    [packages]
    ---invenio-app-rdm = {extras = [...], version = "~=13.0.0"}
    +++invenio-app-rdm = {extras = [...], version = "~=14.0.0"}
    ```

### Install InvenioRDM v14:


```bash
invenio-cli install
```

### Update database schemas and content

#### Run the pre-migration step

Run one of the following commands, depending on whether your installation uses `uv` or `pipenv`:

=== "uv"

    ```bash
    invenio shell $(find $(dirname $(dirname $(uv python find)))/lib/*/site-packages/invenio_app_rdm -name prepare_migration_13_0_to_14_0.py)
    ```

=== "pipenv"

    ```bash
    invenio shell $(find $(pipenv --venv)/lib/*/site-packages/invenio_app_rdm -name prepare_migration_13_0_to_14_0.py)
    ```

If it exits with an error, please contact us on
[Discord](https://discord.gg/8qatqBC), and we will help you find an individual
solution for the issue.

#### Run the schema migration step

Run the Alembic migration to update the database schema:

```bash
invenio alembic upgrade
```

If this exits with errors, please have a look to the
[Troubleshooting](#troubleshooting) section and if you don't find a
solution there contact us on [Discord](https://discord.gg/8qatqBC).

#### Run the content migration

Execute the data migration script to update the content of the DB:

=== "uv"

    ```bash
    invenio shell $(find $(dirname $(dirname $(uv python find)))/lib/*/site-packages/invenio_app_rdm -name migrate_13_0_to_14_0.py)
    ```

=== "pipenv"

    ```bash
    invenio shell $(find $(pipenv --venv)/lib/*/site-packages/invenio_app_rdm -name migrate_13_0_to_14_0.py)
    ```

### Update search engine mappings and content


```bash
# precede by uv run or pipenv run as appropriate
invenio index destroy --yes-i-know
invenio index init
# if you have records custom fields
invenio rdm-records custom-fields init
# if you have communities custom fields
invenio communities custom-fields init
invenio rdm rebuild-all-indices
```

#### Update OAI-PMH percolator mapping and Job Logs Index


Percolators and job datastreams need the `invenio index init` step to
get the new mapping and the new mapping but are not affected by index
rebuild from the step before. They have to be updated by running the
following script.

```bash
curl -LsSf https://raw.githubusercontent.com/inveniosoftware/docs-invenio-rdm/master/docs/releases/v14/migrate_percolator_and_jobs_datastream.py -o /tmp/migrate_percolator_and_jobs_datastream.py
invenio shell /tmp/migrate_percolator_and_jobs_datastream.py
```


### Update vocabularies

The following out-of-the-box vocabularies have been enhanced with terms from the DataCite 4.4-4.7 releases and/or mapping improvements. They all benefited from added translations:

- `datetypes` (new entry, translations)
- `descriptiontypes` (translations)
- `licenses` (new entry, translations)
- `relationtypes` (new entries,  translations)
- `resourcetypes` (new entries, mapping improvements, translations)
- `contributorsroles` (new entry, translations)
- `creatorsroles` (new entry, translations)
- `titletypes` (translations)
- `removalreasons` (translations)

In order to update these in your repository, you'll need for each vocabulary to:

1.  Assess if you've customized the vocabulary for your instance. Check in your instance's `app_data/vocabularies/` directory if you have a corresponding customized vocabulary file.

2.  If you've customized the vocabulary for your instance, you will need to merge changes from the [source files in invenio-rdm-records](https://github.com/inveniosoftware/invenio-rdm-records/tree/master/invenio_rdm_records/fixtures/data/vocabularies) into the custom vocabulary file in your instance according to what you and/or your stakeholders think makes sense in your context. If you have not customized the vocabulary, you are probably fine with adopting the changes, but you can always double-check what those are and decide if you adopt them.

3.  If you've decided to adopt the changes (and have merged the changes per step 2.), run the vocabulary update command: `invenio rdm-records add-to-fixture <vocabulary fixture>`. For example: `invenio rdm-records add-to-fixture datetypes`/

If you plan on adopting all those, you can run all the `add-to-fixture` commands:

```bash
invenio rdm-records add-to-fixture datetypes
invenio rdm-records add-to-fixture descriptiontypes
invenio rdm-records add-to-fixture licenses
invenio rdm-records add-to-fixture relationtypes
invenio rdm-records add-to-fixture resourcetypes
invenio rdm-records add-to-fixture contributorsroles
invenio rdm-records add-to-fixture creatorsroles
invenio rdm-records add-to-fixture titletypes
invenio rdm-records add-to-fixture removalreasons
```

!!! info

    The `resourcetypes` vocabulary was also subject to another cleanup operation upstream that removed an entry from it.
    The commands above only add or update entries. Steps to follow to replicate this removal in your instance can be
    found in the [section about aligning "thesis" and "dissertation" resource types](#align-thesis-and-dissertation-resource-types) below.


## Update your configuration or infrastructure

*Required for upgrade*: Assess on a case by case basis. Typically optional.

This last section highlights the changes to your configuration or infrastructure that you should assess. Determine if each applies to your instance, and perform the appropriate changes.

### Tool Switching

####  Python

InvenioRDM v14 starts applying the new python support policy
[RFC](https://github.com/inveniosoftware/rfcs/blob/master/rfcs/rdm-0109-python-versions.md).
This means for InvenioRDM v14, switching to Python 3.14 is highly recommended.

!!! note "Docker Image"

    The recommended docker-invenio
    [image](https://github.com/inveniosoftware/docker-invenio/pkgs/container/invenio-debian-rdm-v14)
    comes with Python 3.14.

#### pipenv to uv

Please have a look at the dedicated [uv-upgrade](../uv-upgrade.md) section.

!!! note "If keeping pipenv for now"
    If you don't switch, make sure your chosen base Docker image has `pipenv`
    still installed. The default v14 provided ones don't and you will need to
    add `RUN pip install pipenv` inside your Dockerfile to install it in that
    case.

#### npm to pnpm

The new JavaScript dependencies manager `pnpm` makes installations
faster and more secure.

Please have a look at the dedicated [pnpm-upgrade](../pnpm-upgrade.md) section.

#### webpack to rspack

The new assets builder drastically reduces installations time.

Please have a look at the dedicated [rspack-upgrade](../rspack-upgrade.md) section.


### invenio-cli run --host ... --port ...

`invenio-cli run` no longer overrides `SITE_API_URL` and `SITE_UI_URL`. Passing
`--host` and `--port` only defines the port and host the development server is
listening on. As such, you should change the following lines in `invenio.cfg`
for your non-containerized development environment:

```diff
# in invenio.cfg
-SITE_UI_URL = "https://127.0.0.1"
+SITE_UI_URL = "https://127.0.0.1:5000"

-SITE_API_URL = "https://127.0.0.1/api"
+SITE_API_URL = "https://127.0.0.1:5000/api"
```

### Overridable IDs in the deposit form

If you are not overriding any of these components, you do not need to
change anything, else you will need to change the ID(s) in your
mapping file to reflect these modifications.

The full list of ID changes [can be found here](https://github.com/inveniosoftware/invenio-rdm-records/pull/2101/files#diff-ff3c479edefad986d2fe6fe7ead575a46b086e3bbcf0ccc86d85efc4a4c63c79).

### Custom field widget prop names

Many [custom field widgets](../../operate/customize/metadata/custom_fields/widgets.md)
used the `icon` and `description` props, which have now been
deprecated and replaced with `labelIcon` and `helpText` respectively.

If you have developed React components in your instance, or overridden
existing UI components, look for any declaration of icon or
description and change them to:

```Javascript
import { parametrize } from "react-overridable"
import { TitlesField } from "@js/invenio_rdm_records"

export const overriddenComponents = {
  "InvenioRdmRecords.DepositForm.TitlesField": parametrize(
    TitlesField,
    {
        ...
-      description: "Describe your resource in a few words",
+      helpText: "Describe your resource in a few words",
        ...
-      icon: "barcode",
+      labelIcon: "barcode",
        ...
    }
  )
}
```

The old names are deprecated and will be removed in a future release.
Please update to the new names.


### Deprecated GitHub integration

The [`invenio-github`](https://github.com/inveniosoftware/invenio-github) module has been deprecated and its support will be removed with InvenioRDM v15. Please use [`invenio-vcs`](https://github.com/inveniosoftware/invenio-vcs) instead.

Please see [this detailed guide](https://github.com/inveniosoftware/invenio-vcs/blob/master/docs/upgrading.rst) for more information on how to upgrade.
This is only necessary if your instance was actively using `invenio-github` (with at least one user having connected their GitHub account) **and**
you want to keep the existing data. See also the [documentation on how to configure the new module](../../operate/customize/software_archival.md).


### Align "Thesis" and "Dissertation" resource types

*Required for upgrade*: **No**.

Your upgrade is complete. This last section describes an **entirely optional** change that is not part of the upgrade. Nothing here affects your instance unless you choose to run it, and you can do so at any later time. Because resource types are a highly visible and commonly customized vocabulary, we suggest rather than impose this change. Decide together with your instance's stakeholders (librarians, curators) whether it fits your data before applying it.

#### What changed and why

With InvenioRDM v14, the default resource types "Publication / Thesis" (id `publication-thesis`) and "Publication / Dissertation" (id `publication-dissertation`) were merged into one: "Publication / Thesis" (id `publication-dissertation`). This resource type maps to Datacite's `resourceTypeGeneral` "Dissertation" (`datacite_general: Dissertation` in the InvenioRDM's default resource type YAML file). The separate `publication-thesis` entry is dropped.

InvenioRDM interprets [Datacite's Dissertation](https://datacite-metadata-schema.readthedocs.io/en/4.7/appendices/appendix-1/resourceTypeGeneral/#dissertation) as covering both former entries, so a single entry mapping to "Dissertation" was more accurate. Datacite's `resourceTypeGeneral` "Text" is not as precise in this context. Staying close to the DataCite schema as a default is a core goal of InvenioRDM.

If you deliberately want to keep both types (for example `publication-dissertation` for PhD work and `publication-thesis` for the rest), or you have customized their DataCite mappings, you may prefer to keep your current setup or apply only part of this change. Skipping this section does not affect your InvenioRDM installation.

#### Applying the change

If you decide to go ahead, follow whichever of the two options below matches your instance.

Both rely on the [`migrate_thesis_to_dissertation.py`](./migrate_thesis_to_dissertation.py) helper. This is a set of **reference functions**, not a ready-to-run tool: read it, and copy or adapt the parts that fit your case. One convenient way to use it as-is is to download it and load its functions into an `invenio shell`:

```bash
curl -LsSf https://raw.githubusercontent.com/inveniosoftware/docs-invenio-rdm/master/docs/releases/v14/migrate_thesis_to_dissertation.py -o /tmp/migrate_thesis_to_dissertation.py
invenio shell -i -- /tmp/migrate_thesis_to_dissertation.py
```

Always test against a copy of your data first.

##### Option A: adopt the new default `publication-dissertation`

Use this if you want to switch your `publication-thesis` records over to the new default `publication-dissertation` resource type, id and all. It rewrites your records and drafts, re-registers their DataCite DOIs, and re-indexes them.

1. If you are using a customized list of resource types in `<my_instance>/app_data/vocabularies/resource_types.yaml`, then:
    1. Set `title.<lang>` to "Thesis" (in the appropriate language) for the entry with `id` equal or equivalent to `publication-dissertation`.
    2. Remove the entry with `id` equal or equivalent to `publication-thesis`.

2. Apply the resource types change:
    - `invenio rdm-records add-to-fixture resourcetypes`
    - Note that this changes the vocabulary, but does not delete `publication-thesis` from your data stores. Deletion is done in step 4.

3. Rewrite every existing record and draft from `publication-thesis` to `publication-dissertation`. The `run_update_for_resource_type` function rewrites the resource type (including in related identifiers), re-registers DataCite DOI metadata, and re-indexes the affected records:

    ```python
    # in `invenio shell`, with the helper loaded (see above)
    run_update_for_resource_type()
    ```

4. Delete the `publication-thesis` vocabulary entry via `invenio shell`:

    ```python
    from invenio_vocabularies.proxies import current_service as vocabulary_service
    vocabulary_service.delete(system_identity, ('resourcetypes', 'publication-thesis'))
    ```

##### Option B: keep your resource type, map it to DataCite's "Dissertation"

Use this if you want to keep your own resource type (for example your existing `publication-thesis`, or any custom type) but have its DataCite DOIs use `Dissertation` as a value instead of `Text`. Your records are not changed, only the DataCite metadata of their DOIs is updated.

1. In `<my_instance>/app_data/vocabularies/resource_types.yaml`, set `props.datacite_general` to `Dissertation` for your resource type entry (and adjust `props.datacite_type` if you set one).

2. Apply the vocabulary change:
    - `invenio rdm-records add-to-fixture resourcetypes`

3. Re-register the DataCite DOI metadata of every published record of that resource type, so DataCite reflects the new value. The `run_update_doi_metadata_for_resource_type` function does this without changing the records (replace `publication-thesis` with your resource type id):

    ```python
    # in `invenio shell`, with the helper loaded (see above)
    run_update_doi_metadata_for_resource_type("publication-thesis")
    ```


## Troubleshooting

### Invenio alembic upgrade could cause problems


!!! info "Unique constraint violation errors can be solved with database cleanups"

    In some rare cases, instances have been observed to run into *unique constraint violations* (e.g. `sqlalchemy.exc.IntegrityError: (psycopg2.errors.UniqueViolation) ...`) during the Alembic upgrade.
    This can happen due to leftover artifacts that were never properly cleaned up, likely due to old bugs.
    Removing the offending leftover rows from the database will resolve these errors.

    The necessary steps depend on the concrete situation, but generally what's needed in such cases is to clean up the tables mentioned in the error message.
    For example, the following error would tell you that you need to delete old entries from the `rdm_records_files` table, and which `(record_id, key)` combination to look out for.

    ---

    The following is a real-life example with altered identifiers:
    ```
    sqlalchemy.exc.IntegrityError: (psycopg2.errors.UniqueViolation) could not create unique index "uidx_rdm_records_files_record_id_key"
    DETAIL:  Key (record_id, key)=(imagine-this-were-a-valid-uuid, research_NMR.zip) is duplicated.

    [SQL: CREATE UNIQUE INDEX IF NOT EXISTS uidx_rdm_records_files_record_id_key ON rdm_records_files (record_id, key)]
    ```

    In this example, we can see that there are two entries for the reported `record_id`, and the older one has had its `object_version_id` set to `null`:
    ```
    inveniordm=> SELECT * FROM rdm_records_files WHERE record_id = 'imagine-this-were-a-valid-uuid';
              created           |          updated           |                  id                  | json | version_id |       key        |              record_id               |          object_version_id
    ----------------------------+----------------------------+--------------------------------------+------+------------+------------------+--------------------------------------+--------------------------------------
     2024-12-03 18:09:12.125274 | 2024-12-03 18:09:12.125283 | 20a5a54a-5c6a-400d-aa3e-5db99323768c | {}   |          1 | research_NMR.zip | imagine-this-were-a-valid-uuid       |
     2024-12-03 18:09:33.503182 | 2024-12-03 18:09:33.546971 | 17235935-1e95-4529-b189-82a250113e93 | {}   |          3 | research_NMR.zip | imagine-this-were-a-valid-uuid       | 2e218ef5-ba92-4fa4-a58a-0c204fc771a1
    (2 rows)
    ```

    The duplication was resolved with `DELETE FROM rdm_records_files WHERE record_id = 'imagine-this-were-a-valid-uuid' AND object_version_id IS null`.

    After that cleanup, `invenio alembic upgrade` went through successfully.

    ---

    ⚠️ Be careful to only clean up the *leftover data*, though!
    If you are unsure which entries *are* the leftovers, feel free to ask for help in the Discord server.

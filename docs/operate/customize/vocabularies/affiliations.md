# Affiliations (ROR)

Affiliations are a specific type of vocabulary, which enables users to find affiliations
for their records' creators and contributors. By using a vocabulary the affiliations are
deduplicated and can use *search as you type* style suggesters.

You need to configure your repository to import the [ROR](https://ror.org)
affiliations dataset. The recommended approach depends on your version of
InvenioRDM.

!!! info "Loading time"

    The ROR vocabulary consists of over 100,000 records and with an ingestion
    speed around 100-200 records/s it usually takes between around 8-15 minutes
    to load the records.

    You can follow the progress connecting to the RabbitMQ management web interface.

## Import using a job

_Introduced in v13_

You can set up a job to import the ROR affiliations dataset directly by going
to the Administration panel, Jobs.

Create a new job called "Load Affiliations" in the Default queue with task "Load ROR affiliations". Make
sure to check the "active" checkbox and click the save button.

Then click the "Configure and run" button, select the "celery" queue, and put
"1900-01-01" in the "Since" field. Click "Run now" and your affiliations will
be loaded.

You can also use the "Schedule job" button to download the latest version of
the ROR vocabulary on a regular schedule.

If you prefer to work on the command line, you can type

```bash
pipenv run invenio vocabularies import \
  --vocabulary affiliations \
  --origin ror-http
```

## Manual import

In order to import the [ROR](https://ror.org) affiliations dataset you will need to add
the file containing the dataset itself and then enable it in your instance's `app_data/vocabularies.yaml`
file. For example:

```yaml
affiliations:
  pid-type: aff
  schemes:
    - id: ROR
      name: Research Organization Registry
      uri: "https://ror.org/"
      data-file: vocabularies/affiliations_ror.yaml
```

The `affiliations_ror.yaml` file can be downloaded from [here](https://github.com/inveniosoftware/cookiecutter-invenio-rdm/raw/master/%7B%7Bcookiecutter.project_shortname%7D%7D/app_data/vocabularies/affiliations_ror.yaml).

Afterwards you will need to import the affiliations. To do so, run the following command
from your instance's folder:

```bash
invenio rdm-records fixtures
```

!!! info "Fixtures currently do not support updates"

    This means that once they are created, modifying the file and re-running the above
    command will have no effect. So make sure you have the correct configuration before
    running the `fixtures` command.

_Introduced in v12_

In v12, the previous method has been simplified. You can now enable affiliations directly by specifying the data file in `app_data/vocabularies.yaml`:

```yaml
affiliations:
  pid-type: aff
  data-file: vocabularies/affiliations_ror.yaml
```

To update the fixtures with the new dataset, run the following command:

```bash
invenio rdm-records add-to-fixture affiliations
```

!!! warning "Note"
    This command will not delete existing vocabulary entries.

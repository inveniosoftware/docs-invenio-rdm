# Affiliations (ROR)

Affiliations are a specific type of vocabulary, which enables users to find affiliations
for their records' creators and contributors. By using a vocabulary the affiliations are
deduplicated and can use *search as you type* style suggesters.

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

!!! info "Loading time"

    The ROR vocabulary consists of about 100.000 records and with an ingestion
    speed around 100-200 records/s it usually takes between around 8-15 minutes
    to load the records.

    You can follow the progress via the RabbitMQ management interface
    on [http://127.0.0.1:15672/](http://127.0.0.1:15672/) (guest/guest).


!!! info "Fixtures currently do not support updates"

    This means that once they are created, modifying the file and re-running the above
    command will have no effect. So make sure you have the correct configuration before
    running the `fixtures` command.

_Introduced in InvenioRDM v12_

From V12 onwards, the previous method has been simplified. You can now enable affiliations directly by specifying the data file in `app_data/vocabularies.yaml`:

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

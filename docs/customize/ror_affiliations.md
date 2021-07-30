# ROR Affiliations

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

!!! info Fixtures currently do not support updates

    This means that once they are created, modifying the file and re-running the above
    command will have no effect. So make sure you have the correct configuration before
    running the `fxitures` command.
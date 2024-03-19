# Funding

Funders and Awards are vocabulary types that enable users to provide funding information to their records. They are used in the deposit form to power _search as you type_ suggestions, while still allowing to mix in custom entries. Their data model is closely based on DataCite's Funding References metadata field.

## Funders (ROR)

Funders represent funding public or private bodies and organizations, such as the [European Commission](https://ror.org/00k4n6c32), the [National Institutes of Health](https://ror.org/01cwqze88), the [Alfred P. Sloan Foundation](https://ror.org/052csg198), etc. Out-of-the-box we provide support for importing funders from the [ROR](https://ror.org) dataset.

!!! info "Why ROR?"

    Although the ROR dataset is used as a datasource for importing creator and contributor affiliations, it also contains funding-related information and identifiers (e.g. CrossRef's Funder ID).

### Data model

A **Funder** record contains:

- The unique identifier `id` for the record. This can be either a unique external persistent identifier (e.g. a ROR like `00k4n6c32`, or CrossRef Funder ID like `10.13039/501100000780`) or any unique internal identifier. This value will be used when programmatically referencing the funder, e.g. in a record's metadata.
- The `name` of the funder (e.g. "European Commission").
- An optional list of `identifiers`, composed by their identifier value and scheme. The scheme can potentially be autocompleted if it is known by the _idutils_ library (e.g. ROR, DOI).
- The `country` Alpha‑2 code of the funder (e.g. `DE`, `GB`). This field is optional.

Here is an example of two such records in YAML format:

```yaml
- id: 01cwqze88
  name: National Institutes of Health
  identifiers:
    - identifier: 01cwqze88
      scheme: ror
    - identifier: 0000000122975165
      scheme: isni
  country: US
- id: 202100-0000
  country: SE
  name: Swedish Research Council
  title:
    en: Swedish Research Council
```

### How to import and update your funder records

The **Funder** vocabulary uses the new DataStreams API for importing entries. You can find more information about this new API in [RFC 0053](https://github.com/inveniosoftware/rfcs/pull/53).

#### ROR dataset import

You can fetch the [ROR data dump](https://ror.readme.io/docs/data-dump) and import it directly using the following command:

!!! warning "Long and blocking operation"
    Note that the import process is done synchronously and the ROR dataset is
    relatively large. Therefore, this operation can take a long time.

```bash
invenio vocabularies import \
  --vocabulary funders \
  --origin "/path/to/ror-data-dump.json.zip"
```

#### Custom dataset import

In case you want to import custom funder records, you can use a DataStream definition file. For a simple import you can **read** entries from a YAML file with raw metadata objects (using the same format as the data model example above), and use a service API to **write** and persist the entries to the database. Here is an example of this definition file, lets call it `vocabularies-future.yaml`:

```yaml
funders:
  readers:
    - type: yaml
      args:
        origin: "app_data/vocabularies/funders.yaml"
  writers:
    - type: funders-service
      args:
        update: false
```

To run the actual import using this `vocabularies-future.yaml` file you can call the `vocabularies import` command, if you don't pass origin arg in `vocabularies-future.yaml` you can pass your YAML file containing the funder records via the `--origin` parameter:

```shell
invenio vocabularies import \
  --vocabulary funders \
  --filepath "./vocabularies-future.yaml" \
  --origin "./my-funders.yaml"
```

In addition, you can also update vocabulary records in case you updated the source data file using the `vocabularies update` command:

```bash
invenio vocabularies update \
  --vocabulary funders \
  --filepath "./vocabularies-future.yaml" \
  --origin "./my-funders.yaml"
```

## Awards (OpenAIRE)

Awards represent a detailed description of a sponsored funding/grant (e.g. the [OpenAIRE-Nexus project](https://cordis.europa.eu/project/id/101017452) by the European Commission). Out-of-the-box we provide support for importing awards from the [OpenAIRE Research Graph](https://doi.org/10.5281/zenodo.3516917) projects dataset.

### Data model

An **Award** record contains:

- The unique identifier `id` for the record. This can be either a unique external persistent identifier (e.g. a DOI like `10.35802/221400`) or any unique internal identifier. This value will be used when programmatically referencing the award, e.g. in a record's metadata.
- The `number` of the award (e.g. `101017452`, or `1K12HL137862-01`).
- The `acronym` of the award (e.g. `BiCIKL`, or `CS3MESH4EOSC`). This field is optional
- The `title` of the award (e.g. "OpenAIRE-Nexus Scholarly Communication Services for EOSC users").
- The `funder` the award is issued from. You can reference a record from the **Funder** vocabulary by its `id` (e.g. `"funder": {"id": "01cwqze88"}`).
- An optional list of `identifiers`, composed by their identifier value and scheme. The scheme can potentially be autocompleted if it is known by the _idutils_ library (e.g. ROR, DOI).

Here is an example of two such records in YAML format:

```yaml
- id: "01cwqze88::101007492"
  title:
    en: "Biodiversity Community Integrated Knowledge Library"
  number: "101007492"
  acronym: "BiCIKL"
  funder:
    id: 01cwqze88
  identifiers:
    - identifier: "https://cordis.europa.eu/project/id/101007492"
      scheme: url
- id: "10.35802/221400"
  number: "221400"
  funder:
    id: 029chgv08
  title:
    en: "COVID-Minds: Mental Health during Covid-19"
```

### How to import and update your award records

The **Award** vocabulary uses the new DataStreams API for importing entries. You can find more information about this new API in [RFC 0053](https://github.com/inveniosoftware/rfcs/pull/53).

#### OpenAIRE projects dataset import

You can fetch the latest `project.tar` [OpenAIRE Research Graph dump](https://doi.org/10.5281/zenodo.3516917) and then import it directly using the following command:

!!! warning "Long and blocking operation"
    Note that the import process is done synchronously and the ROR dataset is
    relatively large. Therefore, this operation can take a long time.

!!! info "Sample dataset"
    If you need a smaller sample of the dataset to test things out during
    development, you can find a subset of [~10k awards here](https://github.com/inveniosoftware/demo-inveniordm/blob/master/demo-inveniordm/app_data/vocabularies/awards_sample.tar).

```bash
invenio vocabularies import \
  --vocabulary awards \
  --origin "/path/to/project.tar"
```

#### Custom dataset import

In case you want to import custom award records, you can use a DataStream definition file. For a simple import you can **read** entries from a YAML file with raw metadata objects (using the same format as the data model example above), and use a service API to **write** and persist the entries to the database. Here is an example of this definition file, lets call it `vocabularies-future.yaml`:

```yaml
awards:
  readers:
    - type: yaml
      args:
        origin: "app_data/vocabularies/awards.yaml"
  writers:
    - type: awards-service
      args:
        update: false
```

To run the actual import using this `vocabularies-future.yaml` file you can call the `vocabularies import` command , if you don't pass origin arg in `vocabularies-future.yaml` you can pass your YAML file containing the award records via the `--origin` parameter:

```shell
invenio vocabularies import \
  --vocabulary awards \
  --filepath "./vocabularies-future.yaml" \
  --origin "./my-awards.yaml"
```

In addition, you can also update vocabulary records in case you updated the source data file using the `vocabularies update` command:

```bash
invenio vocabularies update \
  --vocabulary awards \
  --filepath "./vocabularies-future.yaml" \
  --origin "./my-awards.yaml"
```

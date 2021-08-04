# Customize a vocabulary

## Application Data

Your instance can rely on custom data to support your needs. For instance, a medical repository might want to use a different set of subjects than a high-energy physics repository.

This custom data is typically called "fixtures". It's data that is ingested when your instance is initially setup and then depended upon for day-to-day operations.

Because fixtures are loaded when `invenio-cli services setup` is run, you will want to setup your fixtures before running this command, so that your custom data is used and not the defaults. Locally, you can run `invenio-cli services setup --force` to wipe your database + indices and reload them with your fixtures (**DON'T DO THIS IN PRODUCTION!**).

!!! warning "Loading fixtures"
    These fixtures are only loaded when `invenio-cli services setup` is run. This is problematic if you would want to create a role and assign it to a user in your fixtures: there is no moment when you can create that role in the database between the database creation and fixture loading! Loading specific fixtures independent from each other and separate from `invenio-cli services setup` will be possible in the future.

## The app_data/ folder

When initialized, your instance came with an `app_data/` folder. This folder is used to place custom data. InvenioRDM will look there first to use these fixtures. If a particular fixture is not provided in `app_data/`, InvenioRDM loads a default. Placing fixtures in `app_data/` allows you to override the default data. Different fixtures can have different expected structures. We outline here the kind of data that can be customized.

## Vocabularies

```
app_data/
├── vocabularies
│   ├── <vocabulary_identifier_0>.yaml
|   ├── <vocabulary_identifier_1>.yaml
|   └── ...
└── vocabularies.yaml
```

To load vocabularies, the typical file structure is the one depicted above:

- A `vocabularies.yaml` file that contains the specific vocabularies that you want to override.
- A `vocabularies/<vocabulary_identifier>.yaml` files that contains entries for each vocabulary or vocabulary scheme.

For the specifics of a vocabulary, refer to [the default vocabularies](https://github.com/inveniosoftware/invenio-rdm-records/blob/master/invenio_rdm_records/fixtures/data).

The `vocabularies.yml` always has the same structure:

```yaml
<vocabulary type identifier>:
  pid-type: <string>
  data-file: <string>
```

- `<vocabulary type identifier>` : The vocabulary identifier referenced in `vocabularies.yaml`.
- `pid-type` : The persistend identifier type id (refer to the defaults for values).
- `data-file` : The file path (relative to this file) where the matching data file resides.

A vocabulary can have multiple schemes, for example *subjects* might come from OECD FOS, MeSH, and many more. Meaning, that
they have to be loaded from different files. However, they are all *subjects*. For example:

```yaml
subjects:
  pid-type: sub
  schemes:
    - id: MeSH
      name: ...
      uri: ...
      data-file: vocabularies/subjects_mesh.yaml
    - id: FOS
      name: ...
      uri: ...
      data-file: vocabularies/subjects_oecd_fos.yaml
```

The `vocabularies/<vocabulary_identifier>.yaml` may have different `props`, but it is otherwise the same across different vocabularies:

```yaml
- id: <string>
  props: <object>
  title: <object>
```

- `id` : The id of the vocabulary record.
- `props` : A vocabulary specific object (refer to the defaults for exact keys).
- `title` : An object of locales as keys and human readable titles in that locale as values (only include the locales you support).


### Example

To override the resource types in your instance, say you are creating an English repository to exclusively host theses, you would provide the following:

```
app_data/
├── vocabularies
│   └── resource_types.yaml
└── vocabularies.yaml
```

**`vocabularies.yml`**

```yaml
resource_types:
  pid-type: rsrct
  data-file: vocabularies/resource_types.yaml
```

**`vocabularies/resource_types.yaml`**

```yaml
- id: thesis-bachelor_thesis
  props:
    coar: text, thesis
    csl: thesis
    datacite_general: Text
    datacite_type: Bachelor Thesis
    notes: ''
    openaire_resourceType: ''
    openaire_type: bachelorThesis
    schema.org: Thesis
    subtype: thesis-bachelor_thesis
    subtype_name: Bachelor Thesis
    type: thesis
    type_icon: graduation cap
    type_name: Theses and Dissertations
  title:
    en: Bachelor Thesis
- id: thesis-doctoral_thesis
  props:
    coar: text, thesis
    csl: thesis
    datacite_general: Text
    datacite_type: Doctoral Thesis
    notes: ''
    openaire_resourceType: ''
    openaire_type: doctoralThesis
    schema.org: Thesis
    subtype: thesis-doctoral_thesis
    subtype_name: Doctoral Thesis
    type: thesis
    type_icon: graduation cap
    type_name: Theses and Dissertations
  title:
    en: Doctoral Thesis
- id: thesis-masters_thesis
  props:
    coar: text, thesis
    csl: thesis
    datacite_general: Text
    datacite_type: Masters Thesis
    notes: ''
    openaire_resourceType: ''
    openaire_type: masterThesis
    schema.org: Thesis
    subtype: thesis-masters_thesis
    subtype_name: Masters Thesis
    type: thesis
    type_icon: graduation cap
    type_name: Theses and Dissertations
  title:
    en: Masters Thesis
```

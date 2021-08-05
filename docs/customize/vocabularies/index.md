# Customize a vocabulary

## Application Data

Your instance can rely on custom data to support your needs. For instance, a medical repository might want to use a different set of subjects than a high-energy physics repository.

This custom data is typically called "fixtures". It's data that is ingested when your instance is initially setup and then depended upon for day-to-day operations.

Because fixtures are loaded when `invenio-cli services setup` is run, you will want to prepare your fixtures before running this command, so that your custom data is used and not the defaults. Locally, you can run `invenio-cli services setup --force` to wipe your database + indices and reload them with your fixtures (**DON'T DO THIS IN PRODUCTION!**).

Behind the scenes, fixtures are currently loaded in a 2-step process: first `invenio-cli services setup` puts them in the task queue to be loaded and second the task workers take up those tasks and actually create the fixture entries in the database and document index. This is why you won't see changes until you run `invenio-cli run` initially.

Another behind the scenes note, `invenio-cli services setup` calls `pipenv invenio rdm-fixtures` to deal with fixtures. That command-line tool (part of the internal API and therefore subject to change) assesses if fixtures are already existing before submitting them to the task queue. This means, it can be used to **add** new fixtures to your instance by being run again later which can be useful to add new subjects. It won't override/update previously existing fixtures.

!!! warning "Unsupported cases"
    There is no moment between database creation and fixture loading when you can create database entries (e.g., a role) and then use them for your fixtures. However, you can still create roles and assign them to users manually with `invenio` commands. We hope to make loading specific fixtures independent from each other and updating existing fixtures possible in the future.

## The app_data/ folder

When initialized, your instance came with an `app_data/` folder. This folder is used to place custom data. InvenioRDM will look there first to use these fixtures. If a particular fixture is not provided in `app_data/`, InvenioRDM loads one provided by an extension or, finally, a [default](https://github.com/inveniosoftware/invenio-rdm-records/blob/master/invenio_rdm_records/fixtures/data/vocabularies.yaml). Placing fixtures in `app_data/` allows you to override the default data. Different fixtures can have different expected structures. We outline here the kind of data that can be customized.

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
- A series of `vocabularies/<vocabulary_identifier>.yaml` files that contain entries for each vocabulary or vocabulary scheme.

The `vocabularies.yaml` always has the same structure:

```yaml
<vocabulary type identifier>:
  pid-type: <string>
  data-file: <string>
```

- `<vocabulary type identifier>` : The vocabulary identifier of the vocabulary you want to override.
- `pid-type` : The persistent identifier type id (refer to the defaults for values).
- `data-file` : The file path (relative to `vocabularies.yaml`) where the matching data file resides.

A vocabulary can have multiple schemes, for example *subjects* might include terms from OECD FOS, MeSH, and many more. Meaning, that
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

The `vocabularies/<vocabulary_identifier>.yaml` have this structure:

```yaml
- id: <string>
  props: <object>
  title: <object>
```

- `id` : The id of the vocabulary record.
- `props` : A vocabulary specific object (refer to the defaults for exact keys).
- `title` : An object of locales as keys and corresponding human readable titles as values (only include the locales you support).

For the specifics of a vocabulary, refer to [the default vocabularies](https://github.com/inveniosoftware/invenio-rdm-records/tree/master/invenio_rdm_records/fixtures/data/vocabularies).


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
resourcetypes:
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

Then, when you run `invenio-cli services setup` for the first time, only those 3 resource types will be loaded.

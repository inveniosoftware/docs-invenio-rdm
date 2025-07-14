# Customize vocabularies

Your instance can rely on custom data to support your needs. For instance, a medical repository might want to use a different set of subjects than a high-energy physics repository. In this section we give you background on that process and how to generally go about customizing vocabularies. The next sections go over specific vocabularies.

## Background

Vocabularies are ingested as fixtures when your instance is initially setup and then depended upon for day-to-day operations.

Because fixtures are loaded when `invenio-cli services setup` is run, you will want to prepare your fixtures before running this command, so that your custom data is used and not the defaults. Locally, you can run `invenio-cli services setup --force` to wipe your database + indices and reload them with your fixtures (**DON'T DO THIS IN PRODUCTION!**).

Behind the scenes, fixtures are currently loaded in a 2-step process: first `invenio-cli services setup` puts them in the task queue to be loaded and second the task workers take up those tasks and actually create the fixture entries in the database and document index. This is why you won't see changes until you run `invenio-cli run` initially.

Another behind the scenes note, `invenio-cli services setup` calls `pipenv run invenio rdm-records fixtures` to deal with fixtures. That command-line tool (part of the internal API and therefore subject to change) assesses if fixtures are already existing before submitting them to the task queue. This means, it can be used to **add** new fixtures to your instance by being run again later which can be useful to add new subjects. It won't override/update previously existing fixtures.

!!! warning "Unsupported cases"
    There is no moment between database creation and fixture loading when you can create database entries (e.g., a role) and then use them for your fixtures. However, you can still create roles and assign them to users manually with `invenio` commands.

## Add/Update Fixtures Command

_Introduced in v12_

To add or update a vocabulary fixture:

```bash
pipenv run invenio rdm-records add-to-fixture <vocabulary_name>
```

This command enables the addition or updating of entries within specified vocabulary fixtures in InvenioRDM and is operational on live instances.
Note that its functionality is restricted to the addition of new vocabularies or the updating of existing ones.

Example
To update the 'contributorsroles' vocabulary fixture, use:

```bash
pipenv run invenio rdm-records add-to-fixture contributorsroles
```

!!! warning "Note"
    This command will not delete existing vocabulary entries.

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

The `vocabularies.yaml` typically follows one of these 2 structures:

*Classic single vocabulary*
```yaml
<vocabulary type identifier>:
  pid-type: <string>
  data-file: <string>
```

OR

*Vocabulary with many sub-vocabularies (e.g. subjects)*
```yaml
<vocabulary type identifier>:
  pid-type: <string>
  schemes:
    - id: <string>
      name: <string>
      uri: <string>
      data-file: <string>
    ...
...
```

- `<vocabulary type identifier>` : The vocabulary identifier of the vocabulary you want to override.
- `pid-type` : The persistent identifier type id (refer to the defaults for values).
- `data-file` : The file path (relative to `vocabularies.yaml`) where the matching data file resides.
- `schemes.id` : The scheme unique identifier; typically the official acronym (is displayed).
- `schemes.name` : The full scheme name.
- `schemes.uri` : The URI where the scheme is defined.
- `schemes.data-file` : The file path (relative to `vocabularies.yaml`) where the matching scheme data file resides.

A vocabulary can have multiple schemes, for example *subjects* might include terms from OECD FOS, MeSH, and many more.
Meaning, that they have to be loaded from different files. However, they are all *subjects*. For example:

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

We show an example of using these files to override resource types in the next section.

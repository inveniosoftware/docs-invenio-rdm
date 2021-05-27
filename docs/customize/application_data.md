# Application Data

Your instance can rely on custom data to support your needs. For instance, a medical repository might want to use a different set of subjects than a high-energy physics repository. InvenioRDM creates a default admin user with an inveniosoftware.org email; you probably want to change that too. In this section, we outline how to customize the data your instance uses.

This custom data is typically called "fixtures". It's data that is ingested when your instance is initially setup and then depended upon for day-to-day operations.

Because fixtures are loaded when `invenio-cli services setup` is run (in May release, see warning below), you will want to setup your fixtures before running this command, so that your custom data is used and not the defaults. Locally, you can run `invenio-cli services setup --force` to wipe your database + indices and reload them with your fixtures (DON'T DO THIS IN PRODUCTION!).

!!! warning "Loading fixtures"
    As of writing (May release), these fixtures are only loaded when `invenio-cli services setup` is run. This is problematic if you would want to create a role and assign it to a user in your fixtures: there is no moment you can create that role in the database between the database creation and fixture loading! Loading specific fixtures independent from each other and separate from `invenio-cli services setup` will be possible in the future.

## The app_data/ folder

When initialized, your instance came with an `app_data/` folder. This folder is used to place custom data. InvenioRDM will look there first to use these fixtures. If a particular fixture is not provided in `app_data/`, InvenioRDM loads a default. Placing fixtures in `app_data/` allows you to override the default data. Different fixtures can have different expected structures. We outline here the kind of data that can be customized. More will be added over time.

## Users

```
app_data/
└── users.yaml
```

This file contains a list of users to create. If the file is provided but it is empty, no default user is created. If the file is not provided, InvenioRDM creates an admin user with email `admin@inveniosoftware.org` (and a random password).

The content of the file is as follows:

```yaml
<email>:
  active: <bool>
  password: <string>
  roles: <array of strings>
  allow: <array of strings>
```

`<email>` : email of the user
`active` : is the user active or not
`password` : their password. If empty, a random one is generated
`roles` : array of roles the user has. The roles must already be present in the DB
`allow` : array of action needs the user has

## Vocabularies

```
app_data/
├── vocabularies
│   └── <vocabulary_identifier>.yaml
└── vocabularies.yaml
```

To load vocabularies, the typical file structure is the one depicted above:

- a `vocabularies.yaml` files that contains the specific vocabularies that you want to override
- a `vocabularies/<vocabulary_identifier>.yaml` file that contains an entry for each vocabulary record

For the specifics of a vocabulary, refer to [the default vocabularies](https://github.com/inveniosoftware/invenio-rdm-records/blob/master/invenio_rdm_records/fixtures/data).

The `vocabularies.yml` always has the same structure:

```yaml
<vocabulary type identifier>:
  pid-type: <string>
  data-file: <string>
```

`<vocabulary type identifier>` : the vocabulary identifier referenced in `vocabularies.yaml`
`pid-type` : the persistend identifier type id (refer to the defaults for values)
`data-file` : the file path (relative to this file) where the matching data file resides

The `vocabularies/<vocabulary_identifier>.yaml` may have different `props`, but it is otherwise the same across different vocabularies:

```yaml
- id: <string>
  props: <object>
  title: <object>
```

`id` : the id of the vocabulary record
`props` : a vocabulary specific object (refer to the defaults for exact keys)
`title` : an object of locales as keys and human readable titles in that locale as values (only include the locales you support)


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

# Customize the resource types

To override the resource types in your instance, you will want to edit the `vocabularies.yaml` file and create a `vocabularies/resource_types.yaml` file.

Say you are creating an English repository to exclusively host academic theses, you would provide the following:

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
- id: thesis
  title:
    en: Theses and Dissertations
- id: thesis-bachelor_thesis
  props:
    coar: text, thesis
    csl: thesis
    datacite_general: Text
    datacite_type: Bachelor Thesis
    eurepo: info:eu-repo/semantics/bachelorThesis
    notes: ''
    openaire_resourceType: ''
    openaire_type: bachelorThesis
    schema.org: https://schema.org/Thesis
    subtype: thesis-bachelor_thesis
    type: thesis
  tags:
    - depositable
    - linkable
  title:
    en: Bachelor Thesis
- icon: graduation cap
  id: thesis-doctoral_thesis
  props:
    coar: text, thesis
    csl: thesis
    datacite_general: Text
    datacite_type: Doctoral Thesis
    eurepo: info:eu-repo/semantics/doctoralThesis
    notes: ''
    openaire_resourceType: ''
    openaire_type: doctoralThesis
    schema.org: https://schema.org/Thesis
    subtype: thesis-doctoral_thesis
    type: thesis
  tags:
  - depositable
  - linkable
  title:
    en: Doctoral Thesis
- icon: graduation cap
  id: thesis-masters_thesis
  props:
    coar: text, thesis
    csl: thesis
    datacite_general: Text
    datacite_type: Masters Thesis
    eurepo: info:eu-repo/semantics/masterThesis
    notes: ''
    openaire_resourceType: ''
    openaire_type: masterThesis
    schema.org: https://schema.org/Thesis
    subtype: thesis-masters_thesis
    type: thesis
  tags:
  - depositable
  - linkable
  title:
    en: Masters Thesis
```

Then, when you run `invenio-cli services setup` for the first time. Only those 3 resource types will be loaded.

The optional `tags` key accepts an array of options affecting the behavior of these resource tags:

- `depositable` - the resource type will show up in the deposit form dropdown for the field **Resource type**.
- `linkable` - the resource type will show up in the deposit form dropdown for **Related works / Resource type**.

If no tags are passed, the resource type doesn't show there, but it shows in the search facets.

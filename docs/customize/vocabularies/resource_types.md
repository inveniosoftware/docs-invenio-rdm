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

- id: publication
  icon: file alternate
  props:
    csl: report
    datacite_general: Text
    datacite_type: ''
    openaire_resourceType: ''
    openaire_type: publication
    eurepo: info:eu-repo/semantics/other
    schema.org: https://schema.org/CreativeWork
    subtype: ''
    type: publication
  tags:
    - depositable
    - linkable
  title:
    en: Publication
```

As seen in the above example, resource types can be grouped by type (e.g. the thesis examples), or they can be independent (e.g. the publication example). 

If the resource type is part of a group, the `subtype` field should have the value of the `id` of the parent resource type. Note that the parent resource type cannot itself be the subtype of another resource type. Only two levels are allowed.

If the resource type is independent, the `subtype` value has to be empty, and the `id` and `type` values must be the same. Otherwise, there will be issues when loading the facets. 

Then, when you run `invenio-cli services setup` for the first time. Only those 3 resource types will be loaded.

The optional `tags` key accepts an array of options affecting the behavior of these resource tags:

- `depositable` - the resource type will show up in the deposit form dropdown for the field **Resource type**.
- `linkable` - the resource type will show up in the deposit form dropdown for **Related works / Resource type**.

If no tags are passed, the resource type doesn't show there, but it shows in the search facets.

# Customize the resource types

To override the resource types in your instance, you will want to edit the `vocabularies.yaml` file and create a `vocabularies/resource_types.yaml` file. The default `resource_types.yaml` is [available for download here](https://github.com/inveniosoftware/invenio-rdm-records/blob/master/invenio_rdm_records/fixtures/data/vocabularies/resource_types.yaml).

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

If the resource type is part of a group, its `type` value should be the same as the group/parent's resource type `id` and its `subtype` value should be the same as its own `id`. Note that the parent resource type cannot itself be part of a group. Only two levels are allowed.

If the resource type is independent, its `type` value should be the same as its own `id` and its `subtype` value should be empty. Otherwise, there will be issues when loading the facets.

Then, when you run `invenio-cli services setup` for the first time. Only those 3 resource types will be loaded.

The optional `tags` key accepts an array of options affecting the behavior of the resource type:

- `depositable` - the resource type will show up in the deposit form dropdown for the field **Resource type**.
- `linkable` - the resource type will show up in the deposit form dropdown for the field **Related works / Resource type**.

If `tags` is not present, the resource type will only show in the search facets.

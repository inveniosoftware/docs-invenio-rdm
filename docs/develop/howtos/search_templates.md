# Customizing OpenSearch Index Templates

InvenioRDM does a lot to manage indexing for us, but in some cases we may need more control over how the indexes are configured. We might, for example, want to specify how many shards should be assigned for each index. We can configure InvenioRDM to use our own custom OpenSearch index templates to achieve this.

## Configuring the index template files

To understand how to configure InvenioRDM to use custom OpenSearch index templates, we first need to understand a bit about OpenSearch's index templating system. OpenSearch actually provides two different templating systems: the old-style templates at the `_template` endpoint, and the new-style templating system that utilizes the `_index_template` and `_component_template` endpoints.

### **Old-style templates**

The old style system is now deprecated by OpenSearch, but is currently still employed by the `invenio-stats` module and supported by `invenio-search`. Using this system, you can create a template that applies to any index whose name matches an index pattern. If multiple templates match the same index pattern, OpenSearch will merge all of their settings. So all we would have to do is make this PUT request to our OpenSearch `_template` endpoint, sending a template in the body with our desired settings, and making sure that the index pattern would match all of our InvenioRDM instance's indices. (These indices all have the prefix `example_instance`, but this prefix will be unique for each InvenioRDM instance.)

**Example of an old-style `_template`:**

```bash
PUT _template/template_1
{
  "index_patterns": ["example_instance*"],
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 1
  }
}
```

This will configure all of our indices with names starting by `example_instance` to use just one primary shard and one replica (2 shards in total) for each index.

### **New-style templates**

In the newer `_index_template` system, only one index template can be applied to each index. This avoids the  unexpected results that could emerge when two or more old-style templates have conflicting settings. The new index templates can be composed using component templates, but those component templates now have to be explicitly included in the index template.

**Example of a new-style `_index_template`:**

```bash
PUT _index_template/template_2
{
  "index_patterns": ["example_instance*"],
  "template": {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 1
    }
  },
  "priority": 100
}
```

This template applies to indices matching the `example_instance` prefix, again configuring them to use *1 primary shard* and *1 replica*. But what if another index template also has a pattern that matches a given index name? The index `example_instance-records-records-v1.0.0`, for example, would match this template, but it would also match a template with the pattern `example_instance-records*`. The `priority` field allows us to determine which one will override the other. Since our `priority` here is `100`, it will take precedence over any template with a lower `priority` than 100, thus establishing a precedence order.

**Example of a new-style `_comment_template**

In the new `_index_template` system, you can also break down settings into reusable components. So we could put our shard settings into their own `_component_template`:

```bash
PUT _component_template/shard_count_template
{
  "template": {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 1
    }
  }
}
```

This component template can be reused across multiple index templates to define the same shard and replica settings, but we have to do it explicitly. So in our index template we add a `composed_of` value with an array of component templates that should be used:

```bash
PUT _index_template/template_with_component
{
  "index_patterns": ["example_instance*"],
  "composed_of": ["shard_count_template"],
  "priority": 100
}
```

In this setup, the settings from `shard_count_template` are applied to any index that matches the `example_instance*` pattern, unless a different index template has a `priority` greater than 100.

## Configuring InvenioRDM to use custom index templates

The `invenio-search` module handles the creation of search indices for an InvenioRDM instance automatically, behind-the-scenes. So if we want to change the templates for these indices, we have to tell `invenio-search` to send our instance's custom index templates to OpenSearch when it creates the indices.

InvenioRDM is equipped to manage both old and new styles of templates via specific entry points:

- `invenio_search.templates`
- `invenio_search.index_templates`
- `invenio_search.component_templates`

Most InvenioRDM search indices are created by declaring index mappings alone, without any index templates. So in most cases we are free to add index templates without worrying about conflicts with InvenioRDM's defaults. Below are examples of how to register them.

### Declaring a default index template

To adjust the default number of shards across all indices created by Invenio, we can declare a *cluster-wide default index template*. For example, we can match any index beginning with a certain prefix (`example_instance`) and provide a default setting of 3 shards:

```json
{
  "index_patterns": ["example_instance*"],
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1
  }
}
```

We can place this in a JSON file somewhere in our instance's `site` folder. Although the general location is flexible, the file must be contained in a folder named `os-v2` and should be named for the index template it provides. In this case, since we are declaring a default index template, we can name it `default-v1.0.0.json`.

This template can then be registered via the `invenio_search.index_templates` entry point group in our instance's `site/setup.cfg` file (or in an external package's).

```ini
[options.entry_points]
# ...
invenio_search.index_templates =
    example_instance = example_instance.index_templates.templates:get_index_templates
```

The value provided for the entry point is an import path to an iterable of import paths or a function that returns an iterable of such paths. Each such import path string should point to a folder containing an index template. In this example, it's the function `get_index_templates` with the sole resulting import path of `"example_instance.index_templates.default"`:

```python
def get_index_templates():
    return ["example_instance.index_templates.default"]
```

The folder containing the index template must contain an `os-v2` subfolder, which in turn contains the json file with our custom template. So our folder structure should look like this:

```
example_instance/
    site/
        example_instance/
            index_templates/
                default/
                    __init__.py
                    os-v2/
                        default-v1.0.0.json
```


### Index Templates for Specific Indices

When needed, additional new-style index templates can be declared with a *higher priority* to override the default settings for specific indices. These, too, are registered on the `invenio_search.index_templates` entry point group. The import paths for the containing folders must be provided as strings in the entry point value, just like our default index template example above. And as with the default index template, the folder containing the index template must contain an `os-v2` subfolder, which in turn contains the json file with our custom template, named for the index template it provides.

If you would like to take advantage of template composition, you can also declare component templates via the `invenio_search.component_templates` entry point group.

If for some reason you need to use old-style templates for specific indices, you can register them via the `invenio_search.templates` entry point group instead.

### Special Handling for Stats Indices

InvenioRDM's indices for usage statistics are managed via old-style templates separately from the rest of the search indices. These templates, which include both index settings and field mappings, are not handled by the `invenio-search` module. So they aren't discovered via the `invenio_search.index_templates` entry point. Instead, the stats templates are defined in the app configuration objects (`STATS_EVENTS` and `STATS_AGGREGATIONS`). The default stats configuration objects include declarations for the default stats index templates found in `invenio_rdm_records.records.stats.templates.events`.

To customize these templates, we modify the template information in these config objects. If we want to use a custom template for the indexing of "file-download" events, for example, we modify the `STATS_EVENTS` object like this:

```python
STATS_EVENTS = {
    "file-download": {
        "templates": "import.path.to.my.template.folder",
        # ...
    },
    # ...
}
```

As with other registered templates, the path declared here should be to a folder that contains an `os-v2` subfolder (for OpenSearch 2), which in turn contains the json file with our custom template.

If we prefer for InvenioRDM to register new-style index templates for statistics, we must set:

```python
STATS_REGISTER_INDEX_TEMPLATES = True
```

!!! info "Stats index templates must include mappings."
    When defining templates for stats indices, the new template must contain *the entire content* of the original template, including mappings and settings that you do not want to override. Unlike other search indices (which separate field mappings from the settings in an index template) the stats indices declare all of the index parameters in these template files. So our custom template must also include *all* of the necessary settings and mappings for the indices.

### Leveraging `__search_index_prefix__`

In both old- and new-style templates, you can make use of the placeholder `__search_index_prefix__` in your template’s `index_patterns` matching strings. This is automatically replaced by InvenioRDM with the correct prefix when applying the template.

### Applying the custom templates

Index templates are applied (sent to OpenSearch via the opensearchpy Python interface) during the setup stage of the search indices, before any data has actually been indexed. This can be done manually using the cli command `invenio index init` and it is done automatically during the service setup process for a new InvenioRDM instance.
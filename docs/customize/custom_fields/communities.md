# Custom fields

Communities' custom fields can be configured in a very similar manner than [records'](./records.md).
The only difference is the prefix of the configuration variables and the place where the information
is displayed.

## Configure

In order to add custom fields to your instance you have to configure in your `invenio.cfg` the following variables:

- `COMMUNITIES_NAMESPACES` - Used to add context to your fields and avoid name clashes. However, if this variable is not filled in `RDM_NAMESPACES` will be used. Therefore, allowing for global namespacing across custom fields.
- `COMMUNITIES_CUSTOM_FIELDS` - Defines the name, type, and validation rules of your fields.
- `COMMUNITIES_CUSTOM_FIELDS_UI` - Defines how the fields are displayed in the UI.

## Quickstart, how does it look?

To add a _community external URL_ field, you would need to configure the type of
field and how it should be displayed. The configuration would look like:

```python
from invenio_records_resources.services.custom_fields import TextCF

RDM_CUSTOM_FIELDS = [
    TextCF(name="external_url")
]

RDM_CUSTOM_FIELDS_UI = [
    {
        "section": _("Additional information"),
        "fields": [
            dict(
                field="external_url",
                ui_widget="Input",
                props=dict(
                    label="External URL",
                    placeholder="https://your.community.url",
                    icon="pencil",
                    description="The external URL of your community or project.",
                )
            ),
        ]
    }
]
```

### Displaying fields

Now that you have defined your custom fields and configured their type and validation rules, you need to configure how you want them to be displayed on the community settings/profile page.

The fields are added at the bottom of the page similar to the image below:

![Custom fields in community settings page](../img/community_settings_custom_fields.png)

!!! warning Custom fields are currently not displayed

    At the moment communities' custom fields are not displayed in the community profile page. This will come in a following release along with bigger community theming capabilities.

### Applying your config

After configuring your custom fields, you have to update the corresponding search mappings. Otherwise those records will fail to be indexed, and facets/search will not work on them. This is easily done via the `invenio custom-fields ...` command in the following manner:

```bash
# for creating any missing custom field mappings for communities
invenio communities custom-fields init
```

!!! info
Note that if the custom fields are configured **before** the InvenioRDM instance has been setup, this is the `invenio-cli services setup` command has never been run, the custom fields will be added by it and no command needs to be run.

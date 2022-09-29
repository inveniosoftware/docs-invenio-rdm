# Custom Fields Types

In this chapter we will explain how to implement your own custom field. In order to have a use case scenario in mind, we will try to extend the scenario we described in the [Adding fields to the records' data model](../../../customize/custom_fields/records) section. Our example use case will be:

_At CERN... For each experiment a record could belong to, I want to know the title and the research program of said experiment._

To satisfy the the above scenario we will implement a new field `experiments` which will be a list of objects the following structure:

```json
{
  "experiments": [
    {
      "title": "ATLAS",
      "program": "LHC"
    },
    {
      "title": "ALICE",
      "program": "LHC"
    }
  ]
}
```

This will give us the opportunity to add the experiments a record can belong to, and more information about them.

## Implement a new custom field

We will start by defining a new custom field type.

```python
from invenio_records_resources.services.custom_fields import BaseListCF
from marshmallow_utils.fields import SanitizedUnicode

class ExperimentsCF(BaseListCF):
    """List of experiments with extra information."""

    def __init__(self, name, **kwargs):
        """Constructor."""
        super().__init__(
          name,
          field_cls=fields.Nested,
          field_args=dict(
            nested= dict(
                title=SanitizedUnicode(),
                program=SanitizedUnicode()
            )
          ),
          multiple=True,
          **kwargs
        )


    @property
    def mapping(self):
        """Return the mapping."""
        return {
            "properties": {
                "title": {
                    "type": "text"
                },
                "program": {
                    "type": "text"
                },
            }
        }
```

## Implement new UI widget

We will create a new UI widget for our field under the `my-site/assets/custom-fields` folder called `Experiments.js`. This would look like the following:

```javascript
import React, { Component } from "react";

import { Input, Array } from "react-invenio-forms";
import { Grid, Form, Button, Icon } from "semantic-ui-react";

const newExperiment = {
  title: "",
  program: "",
};

export class Experiments extends Component {
  render() {
    const {
      fieldPath, // injected by the custom field loader via the `field` config property
      title,
      program,
      icon,
      addButtonLabel,
      description,
      label,
    } = this.props;
    return (
      <Array
        fieldPath={fieldPath}
        label={label}
        icon={icon}
        addButtonLabel={addButtonLabel}
        defaultNewValue={newExperiment}
        description={description}
      >
        {({ arrayHelpers, indexPath }) => {
          const fieldPathPrefix = `${fieldPath}.${indexPath}`;
          return (
            <Grid>
              <Grid.Column width="7">
                <Input
                  fieldPath={`${fieldPathPrefix}.title`}
                  label={title.label}
                  placeholder={title.placeholder}
                  description={title.description}
                ></Input>
              </Grid.Column>
              <Grid.Column width="8">
                <Input
                  fieldPath={`${fieldPathPrefix}.program`}
                  label={program.label}
                  icon={"building"}
                  placeholder={program.placeholder}
                  description={program.description}
                ></Input>
              </Grid.Column>
              <Grid.Column width="1">
                <Form.Field style={{ marginTop: "1.75rem", float: "right" }}>
                  <Button
                    aria-label={"Remove field"}
                    className="close-btn"
                    icon
                    onClick={() => arrayHelpers.remove(indexPath)}
                    type="button"
                  >
                    <Icon name="close" />
                  </Button>
                </Form.Field>
              </Grid.Column>
            </Grid>
          );
        }}
      </Array>
    );
  }
}
```

## Define the template for the record landing page

We will add a new template so we can display the newly added field to the record's landing page. For that reason, we create a new file `experiments.html` under the `my-site/templates` folder.

```html
<dt class="ui tiny header">{{ _("Experiments")}}</dt>

{% for value in field_value %} {{value.get("title", "Unknown")}} ({{
_("Program") }}: {{value.get("program", "Unknown")}}) {{ ", " if not loop.last
}} {% endfor %}
```

## Applying configuration

We have defined our field, so now we need to add it to the `RDM_CUSTOM_FIELDS` and `RDM_CUSTOM_FIELDS_UI` configuration:

```python
RDM_CUSTOM_FIELDS = [
    ExperimentsCF(name="experiments")
]

RDM_CUSTOM_FIELDS_UI = [{
    "section": "CERN Experiments",
    "fields": [{
        "field": "experiments",
        "ui_widget": "Experiments",
        "template": "experiments.html",
        "props": {
            "title": {
                "label": _("Experiment title"),
                "placeholder": _("Add the title..."),
                "description": _("Add the title of the experiment e.g ATLAS")
            },
            "program": {
                "label": _("Experiment program"),
                "placeholder": _("Add the program..."),
                "description": _("Add the research program in which the experiment belongs to e.g LHC")
            },
            "addButtonLabel": _("Add new experiment"),
            "icon": "lab",
            "description": "Add all the experiments in which your record belongs to."
        }
    }]
}]
```

Now, we need to populate the new added field to ES by running the command:

```bash
invenio rdm-records custom-fields init -f experiments
```

## Display

### Upload form

The new field will be displayed at the bottom of the upload form like below:

![Experiments field upload form](../img/new_custom_field_upload_form.png)

### Landing page

In similar fashion, the field will be displayed in the record's landing page according to the template we defined and it will look like below:

![Experiments field record landing page](../img/new_custom_field_landing_page.png)

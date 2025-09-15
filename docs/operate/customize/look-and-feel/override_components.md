# How to override UI React components

*Introduced in InvenioRDM v11*

This documentation is targeted at developers who want to customize specific UI React components in an instance.
For this guide, we assume that you are familiar with React and JavaScript.

## About overriding

!!! warning "Experimental feature"

    You can now override React components following this guide. However, the overriding mechanism in InvenioRDM v11 is not finalized
    and it has a few limitations. Be aware that future releases of InvenioRDM might introduce breaking changes. We will document them
    as extensively as possible.

    **Use it at your own risk!**

The UI of InvenioRDM is composed of classic HTML web pages for mostly static content, and React web apps for very dynamic content to enhance the user experience.
While a [dedicated guide](./templates.md) describes how to override HTML web pages (Jinja templates), this guide focus on how to override React components.

InvenioRDM uses the React library [`react-overridable`](https://github.com/indico/react-overridable). 
The library provides a mechanism to mark React components as "overridable" by ID, which is implemented for many components across the InvenioRDM codebase.
Developers can define a mapping which is then applied when each React component is rendered.

## 1. Find the component to override

At the moment, the easiest way to identify if the component that you want to override is a classic HTML component or a React component is to use the Developer Tools in your browser (e.g. [Chrome](https://developer.chrome.com/docs/devtools/) or [Firefox DevTools](https://firefox-source-docs.mozilla.org/devtools-user/)). You can inspect the code and take advantage of the [React Developer Tools](https://react.dev/learn/react-developer-tools) browser extension to select and inspect elements:

![React browser extension example](./imgs/react_browser_extension_example.png)

If the component shows up in the React tree, it is a React component and can be overriden using the methods described on this page.
Otherwise, it is an HTML component that can be [overriden using Jinja templates](./templates.md).

Next, you can find the ID of an overridable component using `react-overridable`'s built-in developer tool.
Simply open a browser console on your local instance and call the global function `reactOverridableEnableDevMode()`.
All overridable components will display a small red overlay tag showing their ID.
You can click a tag to copy its ID to your clipboard.

![Metadata-only checkbox overridable ID in an overlay](./imgs/metadata_id_overlay.png)

You can search the ID in the [`inveniosoftware` organisation on GitHub](https://github.com/inveniosoftware/) to find the component and its props, which
can be helpful when overriding.

If you're struggling, you can always [ask for help](../../../install/troubleshoot.md#getting-help)!

## 2. Find or create the mapping file

In new InvenioRDM installations at v11 or above, a near-empty file named `mapping.js` is available at the following path in your `assets` folder:

```terminal
├── assets
|   ├── js
|   |   ├── invenio_app_rdm
|   |   |   ├── overridableRegistry
|   |   |   |   ├── mapping.js
```

For existing installations, you will have to create it. It is a very simple file:

```javascript
export const overriddenComponents = {};
```

The `const overriddenComponents` is the map that will contain all your future overrides.

## 3. Override the component

The override can be specified in one of three ways, depending on your use case and the amount of control you require:

- a static override of the props passed to the component
- a 'dynamic' override of the props based on the form's state
- completely replacing a component with a custom one

### a. Statically override a component's props

You can use the `parametrize` function built into `react-overridable`, into which you need to pass the component you wish to override and an object containing your props.
These props will be 'merged' with the existing props, with yours taking precedence over existing ones of the same name.

In this case, the props are defined once in your `mapping.js` file and are not updated during the runtime of the application.
You are also unable to access any React/Formik context while defining the props.

```javascript
import { parametrize } from "react-overridable"
import { TitlesField } from "@js/invenio_rdm_records"

export const overriddenComponents = {
  "InvenioRdmRecords.DepositForm.TitlesField": parametrize(
    TitlesField,
    {
      helpText: "Describe your resource in a few words"
    }
  )
}
```

### b. Dynamically override a component's props

To implement more complex functionality in the deposit form, you can override the props of components by using a custom function.
This allows you to express a range of behaviours:

- hiding fields that are inapplicable to a certain resource type
- changing the label of fields to be more contextually relevant
- marking a field as disabled when its value has been made obvious by the value of another field
- showing certain fields only when a specific community is selected
- etc.

For this, you can use the `dynamicParametrize` function in `react-invenio-forms`, which behaves similarly to `parametrize`.
The callback you pass will be evaluated whenever the form state changes, and the object you return will override the props
passed to the component.

```javascript
import { dynamicParametrize } from "react-invenio-forms"
import { RelatedWorksField } from "@js/invenio_rdm_records"

export const overriddenComponents = {
  "InvenioRdmRecords.DepositForm.TitlesField": dynamicParametrize(
    TitlesField,
    ({ formValues }) => {
      return {
        helpText: `Enter the title of your ${formValue.metadata.resource_type}`
      }
    }
  )
}
```

The callback function is currently passed an object as its single argument, containing the following values:

- `formValues`: the raw values of the entire deposit form as given by Formik. The majority of field values are under the `metadata` key.
- `existingProps`: the props passed to the element before your override.

### c. Fully replace a component

To fully replace a component with your custom one, first create the component definition within your instance's source code.
For example:

```jsx
import React from "react";
import { Checkbox } from "semantic-ui-react";
import { useFormikContext } from "formik";
import PropTypes from "prop-types";

const MetadataToggle = (props) => {
  const { filesEnabled } = props;
  const { setFieldValue } = useFormikContext();

  const handleOnChangeMetadataOnly = () => {
    setFieldValue("files.enabled", !filesEnabled);
    setFieldValue("access.files", "public");
  };

  return (
    <Checkbox
      toggle
      label="Metadata-only record"
      onChange={handleOnChangeMetadataOnly}
    />
  );
};

export default MetadataToggle;

MetadataToggle.propTypes = {
  filesEnabled: PropTypes.bool.isRequired,
};
```

Now, change the map by adding your new component:

```javascript
...

export const overriddenComponents = {
  "InvenioRdmRecords.DepositForm.FileUploaderToolbar.MetadataOnlyToggle": MetadataToggle,
};
```


## Common field props in the deposit form

The built-in fields in the deposit form (e.g. title, description, etc.) have a number of common props to make customizing basic functionality easier.

The following props may be overriden on all built-in fields:

- `label`: the user-facing short label
- `labelIcon`: the ID of the [Semantic UI Icon](https://semantic-ui.com/elements/icon.html) to include in the label
- `helpText`: a small optional text generally shown below the field, providing additional context to the user
- `placeholder`: same as the [HTML attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/placeholder)

Additionally, the following props may be overriden on fields that are not mandatory. 
At the moment, this is all fields except Resource Type, Title, Publication Date, and Creatibutors.

- `hidden`: if `true`, the field is not rendered at all
    - If a field already had a value before being hidden, this will still be included in the model and will be sent to the server when the form is submitted.
    - Fields retain their values when they are hidden and later re-shown.
- `disabled`: same as the [HTML attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/disabled)
- `required`: if `true`, shows a red asterisk in the field label
    - This does not affect the form validation model on the frontend or the backend, and is purely a stylistic setting.

Many fields have their own props in addition to these. 
Please [view the source code](https://github.com/inveniosoftware/invenio-rdm-records/tree/master/invenio_rdm_records/assets/semantic-ui/js/invenio_rdm_records/src/deposit/fields) for more details.

## Examples

### Showing/hiding

You can completely hide a field in the deposit form, based on either a static `true`/`false` value or in response to the current state of the form.

To simply permanently hide the field, you can use something like this:

```javascript
export const overriddenComponents = {
  "InvenioRdmRecords.DepositForm.RelatedWorksField": () => null,
};
```

The expression `() => null` above is defining an "empty" component, thus removing it from the deposit form.

To dynamically only show the field when the `image` resource type is selected, you can use the `dynamicParametrize` function.

```javascript
import { dynamicParametrize } from "react-invenio-forms"
import { RelatedWorksField } from "@js/invenio_rdm_records"

export const overriddenComponents = {
  "InvenioRdmRecords.DepositForm.RelatedWorksField": dynamicParametrize(
    TitlesField,
    ({ formValues }) => {
      return {
        hidden: formValues.metadata.resource_type !== "image"
      }
    }
  )
}
```

In order to see more examples in action, you can check the [zenodo-rdm](https://github.com/zenodo/zenodo-rdm) repository!

### Custom form fields

You can also override your custom deposit form fields if they use the built-in UI widgets.
This can be useful if you want to dynamically set the props of the widgets without fully re-implementing them yourself.
In this case, the ID of the overridable is the same as the field name (e.g. `cern:experiments`).

For more details, see [the UI widgets documentation](../metadata/custom_fields/widgets.md#dynamic-behaviour).

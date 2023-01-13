# How to override a React component

This documentation is targeted to developers that want to customize a specific React component in an instance.

## Overridable

It is possible to override certain React components in InvenioRDM, by using the library [`react-overridable`](https://github.com/indico/react-overridable). This feature is available to instance developers to customize the look and feel of the React application (e.g. deposit form). The library provides a mechanism to mark React components as "overridable" i.e giving them some unique ids and then override them based on that id.

Despite the library allowing multiple ways of overriding a component, for this guide we will implement a new component to replace the default one. More specifically, in our
example **we will override the component in the upload form that marks a record as "Metadata only"** i.e replace the "Metadata-only record" checkbox with a toggle i.e "switch-like" component.

## Steps

- Make sure that the component you want to override is implemented in the same level as an `override.js` file. For example, for the deposit form, `invenio-app-rdm` has the following structure:

```terminal
├── invenio_app_rdm
│   ├── assets
│   │   ├── semantic-ui
│   │   |   ├── js
│   │   |   |   ├── invenio_app_rdm
│   │   |   |   |   ├── deposit
│   │   |   |   |   |   ├── override.js
│   │   |   |   |   |   ├── RDMDepositForm.js
```

We will override the file `override.js`.

- Find the React component's overridable id for the '`Metadata-only record`' checkbox component. In that case the id is `ReactInvenioDeposit.MetadataAccess.layout`.

!['`Metadata-only record`' checkbox](./img/metadata_only_checkbox.png)

!!! info "You must know the component id beforehand"
In order to override a component, the exact overridable id must be retrieved beforehand.
For now, you must retrieve the component id directly from the module's code.

In order to replace the '`Metadata-only record`' checkbox, we will use the Semantic-UI [Toggle](https://react.semantic-ui.com/modules/checkbox/#types-toggle) component.

- Create a file named `override.js` with the same path as the one defined by the module (e.g. `<instance_name>/assets/js/invenio_app_rdm/deposit/override.js`). Note that `semantic-ui` was omitted.

- Create a file (e.g. `MetadataToggle.js`) to implement your component, under `<instance_name>/assets/js/components`. If the folder `components` does not exist, you can create it.

Your instance's assets folder should look like this by now:

```terminal
├── <instance_name>
│   ├── assets
│   │   ├── js
│   │   |   ├── invenio_app_rdm
│   │   |   |   ├── deposit
│   │   |   |   |   ├── override.js
│   │   |   |   |   ├── RDMDepositForm.js
│   │   |   ├── components
│   │   |   |   ├── MetadataToggle.js
```

- Create a React component to override the default one. In the file `MetadataToggle.js`, add the following code:

  ```javascript
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

- In the `override.js`, you should paste the following code:

```javascript
import MetadataToggle from "../../components/MetadataToggle";

export const overriddenComponents = {
  "ReactInvenioDeposit.MetadataOnlyToggle.layout": MetadataToggle,
};
```

The `overriddenComponents` variable is **important** as it is used to collect the user-defined components that override the default behavior. In our example, we used the
'`Metadata-only record`' checkbox component id i.e `ReactInvenioDeposit.MetadataOnlyToggle.layout` to set it to the new component we implemented previously i.e `MetadataToggle`.

- Lastly, rebuild your assets - the new file needs to be added to your instance. In a terminal, run the following command:

```terminal
cd my-site && invenio-cli assets build
```

- The final result shows the override component:

!["`Metadata-only record`" toggle](./img/metadata_only_toggle.png)

## Other examples

- An alternative scenario would be to hide completely from the upload form the '`Metadata-only record`'checkbox.

  It is possible to remove a component using the overridable strategy. In our previous example, instead of declaring a target component `MetadataToggle` we could simply write:

  ```javascript
  export const overriddenComponents = {
    "ReactInvenioDeposit.MetadataOnlyToggle.layout": () => null,
  };
  ```

  The expression `() => null` above is defining an "empty" component thus removing it from the upload form.

In order to see more examples in action, you can check the [zenodo-rdm](https://github.com/zenodo/zenodo-rdm) repository!

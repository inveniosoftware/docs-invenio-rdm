# UI widgets

## Input

An input field that accepts a single string value.

### Usage

```javascript
<Input
  fieldPath="cern:experiment_url"
  label="Experiment URL"
  placeholder="https://your.experiment.url"
  icon="linkify"
  description="URL of the experiment to which the record belongs to."
  required={true}
/>
```

### Props

- **fieldPath** `String` _required_: The path to the field e.g `cern:experiment`.

- **label** `String` _required_: The label for the element's display. This is used whenever the field should be displayed e.g upload form, landing page etc.

- **placeholder** `String` _required_: The placeholder for the element's display. You should fill this in with an example value.

- **description** `String` _required_: The desciption for the element's display. You should provide useful information on how the users should fill this field in.

- **icon** `String` _optional_: The optional icon that your field might have. The value should be one of the [semantic ui icons](https://react.semantic-ui.com/elements/icon/).

- **required** `Boolean` _optional_: Define if the field should be required i.e display the `*` symbol.

- **disabled** `Boolean` _optional_: Define if the field should be displayed as disabled thus no input can be filled.

## MultiInput

An input field that accepts multiple string values.

### Usage

```javascript
<MultiInput
  fieldPath="cern:experiment_keywords"
  label="Experiment keywords"
  placeholder="Add keywords..."
  icon="tags"
  description="Keywords to describe the experiment."
  required={false}
  disabled={false}
/>
```

### Props

- **fieldPath** `String` _required_: The path to the field e.g `cern:experiment`.

- **label** `String` _required_: The label for the element's display. This is used whenever the field should be displayed e.g upload form, landing page etc.

- **placeholder** `String` _required_: The placeholder for the element's display. You should fill this in with an example value.

- **description** `String` _required_: The desciption for the element's display. You should provide useful information on how the users should fill this field in.

- **icon** `String` _optional_: The optional icon that your field might have. The value should be one of the [semantic ui icons](https://react.semantic-ui.com/elements/icon/).

- **required** `Boolean` _optional_: Define if the field should be required i.e display the `*` symbol.

- **additionLabel** `String` _optional_: The label to show when a user is adding a new value.

## RichInput

A rich input field that accepts HTML text.

### Usage

```javascript
<RichInput
  fieldPath="cern:experiment_abstract"
  label="Experiment abstract"
  description="Long description of the experiment."
  icon="book"
  required={false}
  editorConfig={toolbar: [ 'bold', 'italic' ]}
/>
```

### Props

- **fieldPath** `String` _required_: The path to the field e.g `cern:experiment`.

- **label** `String` _required_: The label for the element's display. This is used whenever the field should be displayed e.g upload form, landing page etc.

- **description** `String` _required_: The desciption for the element's display. You should provide useful information on how the users should fill this field in.

- **icon** `String` _optional_: The optional icon that your field might have. The value should be one of the [semantic ui icons](https://react.semantic-ui.com/elements/icon/).

- **required** `Boolean` _optional_: Define if the field should be required i.e display the `*` symbol.

- **editorConfig** `Object` _optional_: The config to pass to the underlying HTML editor as described in the [CKEditor configuration](https://ckeditor.com/docs/ckeditor5/latest/api/module_core_editor_editorconfig-EditorConfig.html) page.

## TextArea

An input field that accepts a multi line text.

### Usage

```javascript
<TextArea
  fieldPath="cern:experiment_abstract"
  label="Experiment abstract"
  description="Long description of the experiment."
  icon="book"
  required={false}
/>
```

### Props

- **fieldPath** `String` _required_: The path to the field e.g `cern:experiment`.

- **label** `String` _required_: The label for the element's display. This is used whenever the field should be displayed e.g upload form, landing page etc.

- **description** `String` _required_: The desciption for the element's display. You should provide useful information on how the users should fill this field in.

- **icon** `String` _optional_: The optional icon that your field might have. The value should be one of the [semantic ui icons](https://react.semantic-ui.com/elements/icon/).

- **required** `Boolean` _optional_: Define if the field should be required i.e display the `*` symbol.

## Dropdown

A dropdown field that accepts a list of options that the user can select one or multiple values from. It is meant to be used for fields that have values coming from vocabularies.

### Usage

```javascript
<Dropdown
  fieldPath="cern:experiment_keywords"
  label="Experiment keywords"
  placeholder="Select keywords..."
  icon="tags"
  description="List of keywords to select that describe the experiment."
  required={false}
  search={true}
  multiple={false}
  clearable={true}
/>
```

### Props

- **fieldPath** `String` _required_: The path to the field e.g `cern:experiment`.

- **label** `String` _required_: The label for the element's display. This is used whenever the field should be displayed e.g upload form, landing page etc.

- **placeholder** `String` _required_: The placeholder for the element's display. You should fill this in with an example value.

- **description** `String` _required_: The desciption for the element's display. You should provide useful information on how the users should fill this field in.

- **icon** `String` _optional_: The optional icon that your field might have. The value should be one of the [semantic ui icons](https://react.semantic-ui.com/elements/icon/).

- **required** `Boolean` _optional_: Define if the field should be required i.e display the `*` symbol.

- **search** `Boolean` _optional_: Define if the user should be able to search in the current available options.

- **clearable** `Boolean` _optional_: Define if the user can deselect all the selected values.

- **multiple** `Boolean` _optional_: Define if the field accepts multiple values.

## AutocompleteDropdown

A dropdown field that accepts a REST API endpoint that the user can select one or multiple values from. It is meant to be used for fields that have values coming from vocabularies.

### Usage

```javascript
<AutocompleteDropdown
  fieldPath="cern:experiment_keywords"
  label="Experiment keywords"
  placeholder="Select keywords..."
  icon="tags"
  description="List of keywords to select that describe the experiment."
  autocompleteFrom="/api/vocabularies/myexperimentkeywords"
  required={false}
  multiple={false}
  clearable={true}
/>
```

### Props

- **fieldPath** `String` _required_: The path to the field e.g `cern:experiment`.

- **label** `String` _required_: The label for the element's display. This is used whenever the field should be displayed e.g upload form, landing page etc.

- **placeholder** `String` _required_: The placeholder for the element's display. You should fill this in with an example value.

- **description** `String` _required_: The desciption for the element's display. You should provide useful information on how the users should fill this field in.

- **autocompleteFrom** `String` _required_: The endpoint from which the component should fetch options. This will point to your vocabulary endpoint e.g `/api/vocabularies/myvocabulary`.

- **icon** `String` _optional_: The optional icon that your field might have. The value should be one of the [semantic ui icons](https://react.semantic-ui.com/elements/icon/).

- **required** `Boolean` _optional_: Define if the field should be required i.e display the `*` symbol.

- **clearable** `Boolean` _optional_: Define if the user can deselect all the selected values.

- **multiple** `Boolean` _optional_ : Define if the field accepts multiple values.

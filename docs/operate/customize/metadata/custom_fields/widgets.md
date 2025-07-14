# UI widgets

_Introduced in v10_

The following document is a reference guide for all the React UI widgets available for custom fields.

## Input

An input field for a single string value.

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

- **fieldPath** `String` _required_: The path to the field e.g. `cern:experiment`.

- **label** `String` _required_: The label for the element's display. This is used whenever the field should be displayed e.g. upload form, landing page etc.

- **placeholder** `String` _required_: The placeholder for the element's display. You should fill this in with an example value.

- **description** `String` _required_: The description for the element's display. You should provide useful information on how the users should fill this field in.

- **icon** `String` _optional_: The optional icon that your field might have. The value should be one of the [Semantic UI icons](https://react.semantic-ui.com/elements/icon/).

- **required** `Boolean` _optional_: Define if the field should be required i.e. display the `*` symbol.

- **disabled** `Boolean` _optional_: Define if the field should be displayed as disabled thus no input can be filled.

## NumberInput

An input field for numbers e.g. integers, float etc.

### Usage

```javascript
<NumberInput
  fieldPath="cern:experiment_id"
  label="Experiment identifier"
  placeholder="Experiment id..."
  icon="calculator"
  description="Unique integer id of the experiment."
  required={true}
/>
```

### Props

- **fieldPath** `String` _required_: The path to the field e.g. `cern:experiment`.

- **label** `String` _required_: The label for the element's display. This is used whenever the field should be displayed e.g. upload form, landing page etc.

- **placeholder** `String` _required_: The placeholder for the element's display. You should fill this in with an example value.

- **description** `String` _required_: The description for the element's display. You should provide useful information on how the users should fill this field in.

- **icon** `String` _optional_: The optional icon that your field might have. The value should be one of the [Semantic UI icons](https://react.semantic-ui.com/elements/icon/).

- **required** `Boolean` _optional_: Define if the field should be required i.e. display the `*` symbol.

- **disabled** `Boolean` _optional_: Define if the field should be displayed as disabled thus no input can be filled.

## MultiInput

An input field for multiple string values.

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

- **fieldPath** `String` _required_: The path to the field e.g. `cern:experiment`.

- **label** `String` _required_: The label for the element's display. This is used whenever the field should be displayed e.g. upload form, landing page etc.

- **placeholder** `String` _required_: The placeholder for the element's display. You should fill this in with an example value.

- **description** `String` _required_: The description for the element's display. You should provide useful information on how the users should fill this field in.

- **icon** `String` _optional_: The optional icon that your field might have. The value should be one of the [Semantic UI icons](https://react.semantic-ui.com/elements/icon/).

- **required** `Boolean` _optional_: Define if the field should be required i.e. display the `*` symbol.

- **additionLabel** `String` _optional_: The label to show when a user is adding a new value.

#### Warning

If you are going to use a MultiInput widget in a template - you must set the default (or new entry) value as [] as the widget is expecting a list.

## RichInput

A rich input field for HTML text, with a WYSIWYG editor.

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

- **fieldPath** `String` _required_: The path to the field e.g. `cern:experiment`.

- **label** `String` _required_: The label for the element's display. This is used whenever the field should be displayed e.g. upload form, landing page etc.

- **description** `String` _required_: The description for the element's display. You should provide useful information on how the users should fill this field in.

- **icon** `String` _optional_: The optional icon that your field might have. The value should be one of the [Semantic UI icons](https://react.semantic-ui.com/elements/icon/).

- **required** `Boolean` _optional_: Define if the field should be required i.e. display the `*` symbol.

- **editorConfig** `Object` _optional_: The config to pass to the underlying HTML WYSIWYG editor as described in the [CKEditor configuration](https://ckeditor.com/docs/ckeditor5/latest/api/module_core_editor_editorconfig-EditorConfig.html) page.

## TextArea

An input field for multi line text.

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

- **fieldPath** `String` _required_: The path to the field e.g. `cern:experiment`.

- **label** `String` _required_: The label for the element's display. This is used whenever the field should be displayed e.g. upload form, landing page etc.

- **description** `String` _required_: The description for the element's display. You should provide useful information on how the users should fill this field in.

- **icon** `String` _optional_: The optional icon that your field might have. The value should be one of the [Semantic UI icons](https://react.semantic-ui.com/elements/icon/).

- **required** `Boolean` _optional_: Define if the field should be required i.e. display the `*` symbol.

## Dropdown

A dropdown field that renders the complete list of possible options, where the user can select one or multiple values. It is meant to be used with small vocabularies.

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

- **fieldPath** `String` _required_: The path to the field e.g. `cern:experiment`.

- **label** `String` _required_: The label for the element's display. This is used whenever the field should be displayed e.g. upload form, landing page etc.

- **placeholder** `String` _required_: The placeholder for the element's display. You should fill this in with an example value.

- **description** `String` _required_: The description for the element's display. You should provide useful information on how the users should fill this field in.

- **icon** `String` _optional_: The optional icon that your field might have. The value should be one of the [Semantic UI icons](https://react.semantic-ui.com/elements/icon/).

- **required** `Boolean` _optional_: Define if the field should be required i.e. display the `*` symbol.

- **search** `Boolean` _optional_: Define if the user should be able to search in the current available options.

- **clearable** `Boolean` _optional_: Define if the user can deselect all the selected values.

- **multiple** `Boolean` _optional_: Define if the field accepts multiple values.

## AutocompleteDropdown

A dropdown field that allows the user to search for values, connected to the REST API endpoint. It is meant to be used with large vocabularies.

### Usage

```javascript
<AutocompleteDropdown
  fieldPath="cern:experiment_keywords"
  label="Experiment keywords"
  placeholder="Select keywords..."
  icon="tags"
  description="List of keywords to select that describe the experiment."
  autocompleteFrom="/api/vocabularies/myexperimentkeywords"
  autocompleteFromAcceptHeader="application/vnd.inveniordm.v1+json"
  required={false}
  multiple={false}
  clearable={true}
/>
```

### Props

- **fieldPath** `String` _required_: The path to the field e.g. `cern:experiment`.

- **label** `String` _required_: The label for the element's display. This is used whenever the field should be displayed e.g. upload form, landing page etc.

- **placeholder** `String` _required_: The placeholder for the element's display. You should fill this in with an example value.

- **description** `String` _required_: The description for the element's display. You should provide useful information on how the users should fill this field in.

- **autocompleteFrom** `String` _required_: The endpoint from which the component should fetch options. This will point to your vocabulary endpoint e.g. `/api/vocabularies/myvocabulary`.

- **autocompleteFromAcceptHeader** `String` _optional_: The `Accept` header to send to the `autocompleteFrom` API. If not provided, the **default** header is
  `application/vnd.inveniordm.v1+json`.

- **icon** `String` _optional_: The optional icon that your field might have. The value should be one of the [Semantic UI icons](https://react.semantic-ui.com/elements/icon/).

- **required** `Boolean` _optional_: Define if the field should be required i.e. display the `*` symbol.

- **clearable** `Boolean` _optional_: Define if the user can deselect all the selected values.

- **multiple** `Boolean` _optional_ : Define if the field accepts multiple values.

## BooleanCheckbox

A field for boolean values. It displays 2 checkboxes for each corresponding value i.e. true/false.

### Usage

```javascript
<BooleanCheckbox
  fieldPath="cern:experiment_active"
  label="Active experiment"
  icon="check"
  description="Mark if the experiment is active."
  required={true}
/>
```

### Props

- **fieldPath** `String` _required_: The path to the field e.g. `cern:experiment`.

- **label** `String` _required_: The label for the element's display. This is used whenever the field should be displayed e.g. upload form, landing page etc.

- **trueLabel** `String` _required_: The label for the element's display when the value is `true`. This is used whenever the `true` value should be displayed e.g. upload form, landing page etc.

- **falseLabel** `String` _required_: The label for the element's display when the value is `false`. This is used whenever the `false` value should be displayed e.g. upload form, landing page etc.

- **description** `String` _required_: The description for the element's display. You should provide useful information on how the users should fill this field in.

- **icon** `String` _optional_: The optional icon that your field might have. The value should be one of the [Semantic UI icons](https://react.semantic-ui.com/elements/icon/).

- **required** `Boolean` _optional_: Define if the field should be required i.e. display the `*` symbol.

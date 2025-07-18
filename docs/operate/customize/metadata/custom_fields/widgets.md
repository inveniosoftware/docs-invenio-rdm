# UI widgets

_Introduced in v10_

The following document is a reference guide for all the React UI widgets available for custom fields.

## Common props

These props are applicable to all widgets. In the reference below, only props additional to these are shown for each widget.

- **fieldPath** `String` _required_: The path to the field e.g. `cern:experiment`.

- **label** `String` _required_: The label for the element's display. This is used whenever the field should be displayed e.g. upload form, landing page etc.

- **labelIcon** `String` _optional_: The optional icon that your field might have. The value should be one of the [Semantic UI icons](https://react.semantic-ui.com/elements/icon/).
    - Previously known as **icon**.

- **placeholder** `String`: The placeholder for the element's display. You should fill this in with an example value.

- **helpText** `String` _required_: The description for the element's display. You should provide useful information on how the users should fill this field in.
    - Previously known as **description**.

- **required** `Boolean` _optional_: Define if the field should be required i.e. display the `*` symbol.

- **disabled** `Boolean` _optional_: Define if the field should be displayed as disabled thus no input can be filled.

- **hidden** `Boolean` _optional_: Define if the field should be hidden completely. Hiding a field will still retain any value that it already contained.

## Input

An input field for a single string value.

### Usage

```javascript
<Input
  fieldPath="cern:experiment_url"
  label="Experiment URL"
  labelIcon="linkify"
  placeholder="https://your.experiment.url"
  helpText="URL of the experiment to which the record belongs to."
  required={true}
/>
```

### Props

No additional props.

## NumberInput

An input field for numbers e.g. integers, float etc.

### Usage

```javascript
<NumberInput
  fieldPath="cern:experiment_id"
  label="Experiment identifier"
  labelIcon="calculator"
  placeholder="Experiment id..."
  helpText="Unique integer id of the experiment."
  required={true}
/>
```

### Props

No additional props.

## MultiInput

An input field for multiple string values.

### Usage

```javascript
<MultiInput
  fieldPath="cern:experiment_keywords"
  label="Experiment keywords"
  labelIcon="tags"
  placeholder="Add keywords..."
  helpText="Keywords to describe the experiment."
  required={false}
  disabled={false}
/>
```

### Props

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
  labelIcon="book"
  helpText="Long description of the experiment."
  required={false}
  editorConfig={toolbar: [ 'bold', 'italic' ]}
/>
```

### Props

- **editorConfig** `Object` _optional_: The config to pass to the underlying HTML WYSIWYG editor as described in the [CKEditor configuration](https://ckeditor.com/docs/ckeditor5/latest/api/module_core_editor_editorconfig-EditorConfig.html) page.

## TextArea

An input field for multi line text.

### Usage

```javascript
<TextArea
  fieldPath="cern:experiment_abstract"
  label="Experiment abstract"
  labelIcon="book"
  helpText="Long description of the experiment."
  required={false}
/>
```

### Props

No additional props.

## Dropdown

A dropdown field that renders the complete list of possible options, where the user can select one or multiple values. It is meant to be used with small vocabularies.

### Usage

```javascript
<Dropdown
  fieldPath="cern:experiment_keywords"
  label="Experiment keywords"
  labelIcon="tags"
  placeholder="Select keywords..."
  helpText="List of keywords to select that describe the experiment."
  required={false}
  search={true}
  multiple={false}
  clearable={true}
/>
```

### Props

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
  labelIcon="tags"
  placeholder="Select keywords..."
  helpText="List of keywords to select that describe the experiment."
  autocompleteFrom="/api/vocabularies/myexperimentkeywords"
  autocompleteFromAcceptHeader="application/vnd.inveniordm.v1+json"
  required={false}
  multiple={false}
  clearable={true}
/>
```

### Props

- **autocompleteFrom** `String` _required_: The endpoint from which the component should fetch options. This will point to your vocabulary endpoint e.g. `/api/vocabularies/myvocabulary`.

- **autocompleteFromAcceptHeader** `String` _optional_: The `Accept` header to send to the `autocompleteFrom` API. If not provided, the **default** header is
  `application/vnd.inveniordm.v1+json`.

- **clearable** `Boolean` _optional_: Define if the user can deselect all the selected values.

- **multiple** `Boolean` _optional_ : Define if the field accepts multiple values.

## BooleanCheckbox

A field for boolean values. It displays 2 checkboxes for each corresponding value i.e. true/false.

### Usage

```javascript
<BooleanCheckbox
  fieldPath="cern:experiment_active"
  label="Active experiment"
  labelIcon="check"
  helpText="Mark if the experiment is active."
  required={true}
/>
```

### Props

- **trueLabel** `String` _required_: The label for the element's display when the value is `true`. This is used whenever the `true` value should be displayed e.g. upload form, landing page etc.

- **falseLabel** `String` _required_: The label for the element's display when the value is `false`. This is used whenever the `false` value should be displayed e.g. upload form, landing page etc.

# React

React is a very nice JavaScript library for building user interfaces, but its usage should not be abused. Carefully consider pros and cons when deciding if you should create a new React application or not.

## Don't use React when...

- you need a small JavaScript snippet, for example to implement a user action (a click, hide/show, slider/animations). Consider that animations can be done with CSS only;
- you are developing a Jinja `macro`: a macro can be included in the DOM, you don't control it. It could affect web page performance (for example, when added to the homepage). If you are planning to mark some components `Overridable` in a React app in a macro, consider that **it will not work**. Prefer [VanillaJS](https://stackoverflow.com/questions/20435653/what-is-vanillajs) or jQuery.

## Use React when...

- When you need a large, complex or a web app where high user interactivity is needed, for example a search page, avoiding page reload on each user action.

## Best practices

### Use Semantic UI React

Use Semantic UI React components in React, instead of CSS classes. The React versions of Semantic UI components have normally implemented some logic, which is crucial for the component to work correctly. The plain CSS Semantic UI might not have all the features available when you use them in React.

❌ DON'T

```javascript
import React, { Component } from "react";

class MyAccordion extends Component {}
  render(){
    <div className="ui accordion" key={agg.title}></div>
  }
```

✅ DO

```javascript
import React, { Component } from "react";
import { Accordion } from "semantic-ui-react";

class MyAccordion extends Component {}

  render(){
    <Accordion key={agg.title}/>
  }
```

### On Overridable

See the [How to override UI React components](../howtos/override_components.md) how-to for detailed explanations on the library itself.

The library allows developers to mark components that can be overridden. While it is very easy to use, it can also lead to subtle errors.

#### Overridable components naming

The `id` of each Overridable component should use the following pattern:

```javascript
<Overridable id="[InvenioModuleName].[ReactApp].[Component].[Element]" name={name}>
```

- `[InvenioModuleName]`: the Invenio module name, e.g. `InvenioCommunities` or `InvenioAppRDM`.
- `[ReactApp]`: the name of the web page where the ReactApp will be rendered, e.g. `MembersList`, `MyDashboard`, `MyUploads`, `MyCommunities`, `DepositForm`. There is no exact naming here, try to be consistent with the existing ones.
- `[Component]`: the name of the component in the React app, e.g. `ResultsList`, `SortBy`, `ListItem`, `BtnAccept`.
- `[Element]`: the name of the UI section inside the component. `Layout` is normally used of the entire Overridable component, `Title` might be used in an inner section, in case of large components:

  ```javascript
  <Overridable id="InvenioCommunities.InvitationsList.ListItem.Layout">
    ...
      <Overridable id="InvenioCommunities.InvitationsList.ListItem.Title">
  ```

Names should be CamelCase.

#### Clear interfaces

Make sure that your component APIs are very clear. Why? Because when re-implementing a component, the developer should clearly understand what `props` are passed to the Overridable component.

❌ DON'T

```javascript
import React, { Component } from "react";

export class ErrorPage extends Component {
  render() {
    const { errorCode, errorMessage, error, children } = this.props;
    return (
      <Overridable id="..." {...this.props}>
        ...
```

Passing `{...this.props}` as params makes things very hard for developers. The interface of the overridden component will look like:

```javascript
const MyErrorPage = (props) => {
  // what `props`???
}
```

✅ DO

```javascript
export class ErrorPage extends Component {
  render() {
    const { errorCode, errorMessage, error, children } = this.props;
    return (
      <Overridable id="..." errorCode={errorCode} errorMessage={errorMessage}>
        ...
```

The interface is now very clear:

```javascript
const MyErrorPage = ({errorCode, errorMessage}) => {
  ...
}
```

#### Extract inner implementation

It is unfortunately very easy to make a mistake and use `props` from the upper component, without passing them down:

❌ DON'T

```javascript
import React, { Component } from "react";

export class OneComponent extends Component {
  render() {
    const { name, disabled } = this.props;
    return (
      <Overridable id="Invenio[ModuleName].OneComponent.layout" name={name}>  // `disabled` prop forgotten here
        <Element
            name={name}
            disabled={disabled}  // here we use a prop that is not passed!!!
```

✅ DO

```javascript
import React, { Component } from "react";

/*
 * Extracting the inner component helps:
 * - The original developer to make sure the component interface is clear and contains all `props`.
 * - The developer overriding the component to copy/paste it.
 */
const InnerComponent = ({ name }) => {
  return <Element name={name} />
}

export class OneComponent extends Component {
  render() {
    const { name, disabled } = this.props;
    return (
      <Overridable id="Invenio[ModuleName].OneComponent.layout" name={name}>
        <InnerComponent name={name} />
```

This will not ensure that the mistake is avoided, but it hopefully helps detecting it.

#### Re-usable components

When implementing re-usable components, `Overridable` should probably not be used. The generic component should have enough `props` to be customizable and `Overridable` should be outside, as a wrapper.

This is also because it is difficult to inject a variable/prop to be used as `id`. `<Overridable id="${appName}.EditBtn"` might lead to infinite loops!

❌ DON'T

Definition:

```javascript
import React, { Component } from "react";

export class EditButton extends Component {
  render() {
    const { name, disabled } = this.props;
    return <Overridable id="EditBtn" ...> // we don't want hardcoded ids for re-usable components
```

Usage:

```javascript
import React, { Component } from "react";
import { EditButton } from "..."

export class OneComponent extends Component {
  render() {
    const { name, disabled } = this.props;
    return (
      <EditButton ... // Overridable is inside the re-usable component
```

✅ DO

Definition:

```javascript
import React, { Component } from "react";

// Do not use Overridable inside here
export class EditButton extends Component {
  render() {
    const { name, disabled } = this.props;
    return <div>...</div>
```

Usage:

```javascript
import React, { Component } from "react";
import { EditButton } from "..."

export class OneComponent extends Component {
  render() {
    const { name, disabled } = this.props;
    return (
      <Overridable id="InvenioCommunities.InvitationsList.ListItem.Layout">
        <EditButton ...
```

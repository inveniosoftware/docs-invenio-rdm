# Accessibility (a11y)

## Intended audience

This guide is intended for maintainers and developers of InvenioRDM itself.

## Accessibility Goal

The goal is to ensure that the web application and its content can be used by those with diverse hearing, movement, sight, and cognitive abilities.

InvenioRDM adheres to the [Web Content Accessibility Guidelines (WCAG) 2.1 AA](https://www.w3.org/WAI/standards-guidelines/wcag/). These guidelines provide testable success criteria, described by 4 principles.

## Principles

Content and functionality should be Perceivable, Operable, Understandable, and Robust for all.  (POUR is the mnemonic.)

- **Perceivable**
The user can perceive the site – either see it, hear it, or feel it (in the case of haptics or braille.)
- **Operable**
The user can operate and control the interface using their chosen technologies – be it desktop browser with mouse and keyboard, mobile touchscreen device, screen reader, keyboard only, switches.
- **Understandable**
The user can understand the site, because it is consistent, both internally and with common design patterns. It is appropriate to the audience in its voice and tone.
- **Robust**
The technology is standards-compliant and performant.

## Testing

Some criteria can be tested with freely available tools. Other criteria will require manual review.
We recommend all contributors test their code before submitting PRs.

### Useful evaluation plugins

- [Lighthouse Chrome extension](https://chrome.google.com/webstore/detail/lighthouse/blipmdconlkpinefehnmjammfjpmpbjk?hl=en)
- [axe DevTools](https://chrome.google.com/webstore/detail/axe-devtools-web-accessib/lhdoppojpmngadmnindnejefpokejbdd)
- [Screen reader plugin](https://chrome.google.com/webstore/detail/screen-reader/kgejglhpjiefppelpmljglcjbhoiplfn)

### Screen reader software
It's very useful to test a screen reader to understand how it works, and to see if your code is detected and announced the way you intended.

- [VoiceOver](https://support.apple.com/en-gb/guide/voiceover/vo28017/10/mac/12.0) for MacOS.
    Comes with MacOS (just check your Launchpad!).
- [NVDA](https://www.nvaccess.org/download/) for Windows (free download).


## Best practices

For InvenioRDM to be accessible for everyone, there are a few things to consider when developing the frontend. For instance, all interactive elements should be accessible by keyboard, and the HTML should be optimized for assistive technologies.


### Use meaningful markup
{==__Semantic HTML should always be used, unless the element is only for styling purposes.__==}

Using Semantic HTML is probably one of the most important things we can do to ensure accessiblity. Semantic HTML provides context and meaning and to assistive technologies, as well as default keyboard accessibility for interactive elements.

When using Semantic UI React, please be aware that the components are not always converted to an element with semantic meaning. In most cases, you must specify the element by adding `as={tagName}`. Pay attention to this by inspecting the elements in the browser.

✅ __DO__
```html
<!--
Use semantic HTML tags unless the only purpose
of the element is styling
-->

<header class="ui fluid container">
    <div class="ui container">
        <nav></nav>
    </div>
</header>

<main class="ui container">
    <h1>My page</h1>
    <section>
        <h2>My section content</h2>
        <ul>
            <li>List item 1</li>
            <li>List item 2</li>
        </ul>
        <button>Button text</button>
    </section>
</main>

<footer class="ui fluid container">
    Footer content
</footer>
```

_With Semantic UI React:_

```js
// Set the "as"-prop to the semantic HTML element you want

<Container fluid as="header">
    <Container>
        <Menu as="nav"></Menu>
    </Container>
</Container>

<Container as="main">
    <Header as="h1">My page</Header>
    <Container as="section">
        <Header as="h2">My section content</Header>
        <List as="ul">
            <List.Item as="li">List item 1</List.Item>
            <List.Item as="li">List item 2</List.Item>
        </List>
        <Button>Button text</Button>
    </Container>
</Container>

<Container fluid as="footer">
    Footer content
</Container>
```

Whenever you cannot avoid using a non-semantic element, but wish to provide meaning to that element, you can use aria-roles.

For a list of available aria-roles, see [WAI-ARIA roles](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles)


❌ __DON'T__
```html
<!--
Don't use divs or spans in place of semantic elements.
If you do, make sure to add aria-roles!
-->

<div class="ui fluid container">
    <div class="ui container">
        <div class="navigation"></div>
    </div>
</div>

<div class="main">
    <div class="page-header">My page</div>
    <div class="section">
        <div class="section-header">My section content</div>
        <div class="list">
            <div class="list-item">List item 1</div>
            <div class="list-item">List item 2</div>
        </div>
        <span class="button">Button text</span>
    </div>
</div>

<div class="ui fluid container">
    Footer content
</div>
```

### Increase heading levels by one
Always use the correct level of heading. {==Each page should have one, and only one, `<h1>` heading, followed by increasing levels: `<h2>`,`<h3>`,`<h4>`...==}

Headings should be followed by either the same heading-level or one level up, depending on the content structure.

Never skip heading levels only for styling purposes. If you want a different size, use styling instead. Semantic UI already has classes you can combine with `.ui .header` as in the following example:

```html
<!-- Use styling instead of skipping heading levels -->

<h2 class="ui huge header">Huge Header</h2>
<h2 class="ui large header">Large Header</h2>
<h2 class="ui medium header">Medium Header</h2>
<h2 class="ui small header">Small Header</h2>
<h2 class="ui tiny header">Tiny Header</h2>
```

_With Semantic UI React:_

```html
<Header as="h2" size='huge'>Huge Header</Header>
<Header as="h2" size='large'>Large Header</Header>
<Header as="h2" size='medium'>Medium Header</Header>
<Header as="h2" size='small'>Small Header</Header>
<Header as="h2" size='tiny'>Tiny Header</Header>
```

✅ __DO__
```html

<!--
Only one h1 per page,
always increase heading level with one or zero
-->

<h1>Page title</h1>

<h2>Section 1</h2>
<h3>Sub heading 1</h3>
<h3>Sub heading 2</h3>

<h2>Section 2</h2>

<h2>Section 3</h2>
```

_With Semantic UI React:_

```js
/*
Only one h1 per page,
always specify your heading level in Semantic UI React,
increase by one or zero
*/

<Header as='h1'>Page title</Header>

<Header as='h2'>Section 1</Header>
<Header as='h3'>Sub heading 1</Header>
<Header as='h3'>Sub heading 2</Header>

<Header as='h2'>Section 2</Header>

<Header as='h2'>Section 3</Header>
```

❌ __DON'T__
```html
<!--
Don't skip heading levels or add more
than one h1 to the same page
-->

<h1>Page title</h1>

<h1>Section 1</h1>
<h4>Sub heading 1</h4>

<h1>Section 2</h1>

<h3>Section 3</h3>
```

_With Semantic UI React:_

```js
// Don't leave out the as-prop

<Header size="huge">Page title</Header>

<Header size="large">Section 1</Header>
<Header size="medium">Sub heading 1</Header>

<Header size="large">Section 2</Header>

<Header size="large">Section 3</Header>
```

### Give images alt tags
All images should have a descriptive alt-tag. If the image is purely decorative, the alt-tag should be empty to hide the image from screen readers.

✅ __DO__
```html
<!-- Always include the alt-tag -->

<img src="/my-images/my-informative-image.png" alt="Image description"/>
<img src="/my-images/my-decorative-image.png" alt=""/>

```

_With Semantic UI React:_

```js
// Always include the alt-tag

<Image src="/my-images/my-informative-image.png" alt="Image description"/>
<Image src="/my-images/my-decorative-image.png" alt=""/>

```

### Announce important messages

Whenever the user is given important feedback on their actions, the informative element should have the alert-role. These elements include those that can be considered info, warnings, errors and success.

#### Dynamic messages
If the info-message is dynamic, i.e. not available on page-load, you can simply give the container-element an alert-role without further thought.

✅ __DO__
```html
<!--
Add the alert-role to messages that can
be considered info, warnings, errors or success
-->

<div role="alert">
    <p>{infoMessage}</p>
</div>
```

#### Static messages

Some screen readers do not announce content that has not changed. This means that if the alert message is static (i.e. already available on page load), you will have to make sure that the content of the alert-element is changing right after page load. This can be done by simply changing the style of the content from `display:none;` to `display:block;`.

✅ __DO__
```html
<div role="alert" id="info">
    <p id="info-message" style="display:none;">
        This information should be announced
        immediately by a screen reader
    </p>
</div>
```

```js
/*
Make sure that static messages are announced by screen readers
by changing the content on page load.
*/

document.addEventListener('DOMContentLoaded', event => {
  jquery("#info #info-message").css('display', 'block');
})
```


### Use aria-attributes to communicate functionality

#### Non-standard interactive elements
Where elements have functionality that is non-standard, e.g. accordions, tab-menus, popups, modals etc., they should have descriptive aria-attributes.

Follow the guidelines described by [w3.org](https://www.w3.org/TR/wai-aria-practices/#aria_ex).

**Note:** Some interactive elements can be tricky to make accessible with the Semantic UI markup. In these cases, make sure to check out the React version. An example is the Dropdown component in Semantic UI React, which comes with good accessiblity out of the box. Note that this is not the case for all the Semantic UI React components, so pay attention, and make sure to test your component.

✅ __DO__
```html
<!--
Provide meaning and context to non-semantic interactive elements
by adding aria-attributes.

Make sure to update dynamic values such as 'aria-selected' with JavaScript.
-->

<div role="tablist" class="ui top attached tabular menu">
    <a class="active item"
       data-tab="tab-1"
       role="tab"
       id="tab-1"
       tabindex="0"
       aria-controls="tab-panel-1"
       aria-selected="true"
    >
        Tab 1 title
    </a>

    <a class="active item"
       data-tab="tab-2"
       role="tab"
       id="tab-2"
       tabindex="0"
       aria-controls="tab-panel-2"
       aria-selected="false"
    >
        Tab 2 title
    </a>
</div>

<div class="ui bottom attached active tab segment"
     data-tab="tab-1"
     role="tabpanel"
     id="tab-panel-1"
     aria-labelledby="tab-1"
     hidden="false"
>
    Tab panel 1 content
</div>

<div class="ui bottom attached tab segment"
     data-tab="tab-2"
     role="tabpanel"
     id="tab-panel-2"
     aria-labelledby="tab-2"
     hidden="true"
>
    Tab panel 2 content
</div>
```

❌ __DON'T__
```html
<!--
Don't use unsemantic elements without descriptive
aria-attributes.
-->

<div class="ui top attached tabular menu">
    <a class="active item">Tab 1 title</a>
    <a class="item">Tab 2 title</a>
</div>
<div class="ui bottom attached active tab segment">
    Tab panel 1 content
</div>
<div class="ui bottom attached tab segment">
    Tab panel 2 content
</div>
```

#### Interactive elements without descriptive text
Every interactive element should have a related text that describes the element. In cases where no text is available (e.g. the text is replaced by an icon), the element should have an aria-label.

✅ __DO__
```html
<!-- Add aria-labels to interactive elements without text content. -->

<button aria-label="Close">
    <i class="close icon"></i>
</button>
```

_With Semantic UI React:_

```js
// Add aria-labels to interactive elements without text content.

<Button icon="close" aria-label="Close" />
```

❌ __DON'T__
```html
<!-- Don't replace text content by icons without adding aria-labels. -->

<button>
    <i class="close icon"></i>
</button>
```

_With Semantic UI React:_

```js
// Don't replace text content by icons without adding aria-labels.

<Button icon="close" />
```

### Provide keyboard accessibility
{==All interactive elements should be accessible by keyboard.==}

Standard interactive elements such as `<input>` and `<button>` come with default keyboard accessibility. This means the element is reachable and possible to trigger by keyboard. Non-standard interactive elements, such as accordions, tab-menus and dropdowns must be provided this functionality. Do this by giving the element a tabindex and make sure the event is triggered by keyboard interaction.

{==See [w3.org Design Patterns and Widgets](https://www.w3.org/TR/wai-aria-practices/#aria_ex) for accessibility guidelines for non-standard interactive elements.==}

✅ __DO__
```js
// Make sure the interactive element is also triggered by keyboard interaction

$('.ui.tabular.menu .item')
  .on('keydown', function(event) {
    /*
    Handle tab change, including updating
    the aria-attributes such as aria-selected.
    */
  });
```

```html
<!-- Make sure to add tabindex and the recommended aria-attributes -->

<div role="tablist" class="ui top attached tabular menu">
    <div class="active item"
         data-tab="tab-1"
         role="tab"
         id="tab-1"
         tabindex="0"
         aria-controls="tab-panel-1"
         aria-selected="true"
    >
        Tab 1 title
    </div>
    <div class="item"
         data-tab="tab-2"
         role="tab"
         id="tab-2"
         tabindex="0"
         aria-controls="tab-panel-2"
         aria-selected="false"
    >
        Tab 2 title
    </div>
</div>

<div class="ui bottom attached active tab segment"
     data-tab="tab-1"
     role="tabpanel"
     id="tab-panel-1"
     aria-labelledby="tab-1"
     hidden="false"
>
    Tab 1 content
</div>

<div class="ui bottom attached tab segment"
     data-tab="tab-2"
     role="tabpanel"
     id="tab-panel-2"
     aria-labelledby="tab-2"
     hidden="true"
>
    Tab 2 content
</div>
```

_With Semantic UI React:_

```js
/*
Pay attention to the keyboard accessibility of Semantic UI React components!
Some need to be provided this functionality, e.g. the Tab-component.
*/

const TabsExample = () => {
    const keyDownHandler = (event) => {
    // Trigger tab change, see the w3.org guidelines
    }

    const handleTabChange = (event, data) => {
    // Update dynamic aria-attributes
    }

    /*
    Make sure to add aria-attributes to the menu-items.
    These are not always provided by default by Semantic UI React.
    */
    const panes = [
        {
            menuItem: {
            key: "tab-1",
            content: "Tab 1",
            id: "tab-1",
            "aria-controls": "tab-panel-1",
            "aria-selected": true,
            tabIndex: 0,
            onKeyDown: keyDownHandler
            }, render: () => (
                <Tab.Pane role="tabpanel" id="tab-panel-1">
                    Tab 1 Content
                </Tab.Pane>
            )
        },
        {
            menuItem: {
            key: "tab-2",
            content: "Tab 2",
            id: "tab-2",
            "aria-controls": "tab-panel-2",
            'aria-selected': false,
            tabIndex: 0,
            onKeyDown: keyDownHandler
            }, render: () => (
                <Tab.Pane role="tabpanel" id="tab-panel-2">
                    Tab 2 Content
                </Tab.Pane>
            )
        },
    ]
    return <Tab panes={panes} onTabChange={handleTabChange} />
}
```
Note that some Semantic UI React components already come with keyboard accessibility, e.g `<Dropdown/>`. Still, the behavior might not be exactly as expected, so pay attention!

### Use sufficient color contrast
The color contrast between the background and the text should satisfy the WCAG AA level. To test this, a useful tool is provided by [WebAIM - Contrast Checker](https://webaim.org/resources/contrastchecker/).


## Read more
[https://www.w3.org/TR/UNDERSTANDING-WCAG20/intro.html#introduction-fourprincs-head](https://www.w3.org/TR/UNDERSTANDING-WCAG20/intro.html#introduction-fourprincs-head)
[https://uiowa.instructure.com/courses/40/pages/accessibility-principles-pour](https://uiowa.instructure.com/courses/40/pages/accessibility-principles-pour)
[https://dequeuniversity.com/class/archive/basic-concepts1/principles/](https://dequeuniversity.com/class/archive/basic-concepts1/principles/)

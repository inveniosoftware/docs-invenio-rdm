# Develop

**Intended audience**

This guide is intended both for developers that needs to develop new features for their own InvenioRDM instance as well as core InvenioRDM developers.

## Getting started

Explains how to get development install up and running:

- [Source code](getting-started/source-code.md)
- [Package development](getting-started/package-development.md)
- [Instance development](getting-started/instance-development.md)
- [Debugging](getting-started/debugging.md)
- [Coding style](getting-started/code-style.md)
- [Virtual environments](getting-started/virtualenvs.md)
- [Getting help](getting-started/help.md)
- [Development process](process.md)

## Best practices

Development guidelines for specific areas of development.

- [Accessibility (a11y)](best-practices/accessibility.md)
- [Commits, pull requests and reviews](best-practices/commits.md)
- [CSS/JavaScript](best-practices/css-js.md)
- [React](best-practices/react.md)
- [Translation (i18n)](howtos/i18n.md)
- [User interface](best-practices/ui.md)

## Topics

Developer introductions to specific parts of the InvenioRDM source code:

- [Building resources](topics/resource.md)
- [Building services](topics/service.md)
- [Building serializers](topics/serializers.md)
- [Grouping atomic operations](topics/uow.md)
- [Sanitize input data](topics/validation.md)
- [Theming](topics/theming.md)
- [Administration panel](topics/administration_panel.md)

## How-to guides

Step-by-step guides on how to perform certain tasks:

- [Create a new custom field](howtos/custom_fields.md)
- [Create custom code and views](howtos/custom_code.md)
- [Add JavaScript](howtos/add_javascript.md)
- [Override UI React components](howtos/override_components.md)
- [Create search terms mappings](howtos/search_terms_migration.md)
- [Create a database migration](howtos/alembic.md)
- [Fix a vulnerability](howtos/security-fix.md)
- [Test emails locally](howtos/dev_email.md)
- [Migrate legacy routes](howtos/route_migration.md)
- [Restrict access to pages](howtos/restrict_access.md)
- [Create and configure notifications](howtos/notifications.md)

## Architecture

High-level conceptual overviews of the design and the thoughts behind those
choices:

- [Introduction](architecture/index.md)
- [Infrastructure architecture](architecture/infrastructure.md)
- [Software architecture](architecture/software.md)
- [Runtime architecture](architecture/runtime.md)
- [Requests](architecture/requests.md)
- [Communities](architecture/communities.md)
- [Records](architecture/records.md)
- [Notifications](architecture/notifications.md)
- [Recommended reading](architecture/reading.md)

## Concepts

Explanation of general methods and techniques used in InvenioRDM to solve
particular problems:

- [Optimistic concurrency control](concepts/concurrency-control.md)
- [Database transactions](concepts/transactions.md)

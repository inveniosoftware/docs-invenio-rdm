# New core developers and maintainers

**Intended audience**

The guide is intended as a crash course for new core developers/maintainers of InvenioRDM with prior experience in running and installing InvenioRDM.

## Scope

Maintainers and core developers are trusted members of the project that regularly contribute to and manage the core codebase of InvenioRDM.
Some come from CERN and others from partner institutions that have dedicated time and effort to the project over time. Management of the core codebase is done by code contributions, pull request reviews and merges, translation effort coordination, branch and work boards administration and various forms of communication, documentation and process management.

This section provides concrete details about those fundamental aspects of the project. As such, although they are targeted at (often new) maintainers and core developers, they can be useful to the occasional contributor in order to better understand the section of the project that they are contributing to. All of the information detailed in ["Join the InvenioRDM Community"](../community/index.md) is prologue to the additional, more specialized information here.

## Important resources

Still relevant to you as a maintainer, are the [important contributor resources](../community/onboard.md) highlighted in the onboarding section.

Additionally, you will want to make sure you are added to the [relevant GitHub teams](https://github.com/orgs/inveniosoftware/teams) depending on what modules you maintain or role you play by contacting current maintainers (`@maintainers` on Discord). Speaking of, your [Discord](https://discord.gg/8qatqBC) account should be appropriately classified to give you access to the relevant maintainer channels and include you in relevant targeted group-`@mentions` (e.g., `@devops-maintainers` if DevOps is one of your areas of expertise).

Don't forget to watch on GitHub the modules you oversee and pay attention to the [community PR board](https://github.com/orgs/inveniosoftware/projects/109/views/1).

## Design

Experienced maintainers (sometimes referred as architects) and fellow core contributors are go-to resources when it comes to understanding the vision of the InvenioRDM project, the high-level architecture and the low-level internals. The architects are there to help you succeed in contributing, but also have a final say on all design choices made in InvenioRDM. This is to ensure a coherent product and coherent decisions. The [high-level architecture of InvenioRDM section](architecture/index.md) tries to lay out that foundational information, while the [internals section](internals/resource.md) details concrete code structures used in the project.

### Request for Comments (RFCs)

[Requests For Comments](https://github.com/inveniosoftware/rfcs) also capture some of the design information of the project -especially for larger design work. They are more like working documents than a finished, enshrined page found in this documentation site. The documentation site disseminates the current results of the historic decisions made there.

RFCs are used to gather feedback and gain consensus from developers. They record the reasoning behind design decisions. However, they are not necessarily very detailed or precise, and they are not retrospectively edited to reflect the now current state of the architecture. There won't necessarily be a subsequent RFC to invalidate a prior one either as the project is fluid and some decisions are made following meetings or online discussions.

## Development

Follow the approach outlined in the ["Contribute code" section](../community/code/process.md). Checkout source code and organize your environment for development as per the other pages in that section. Parts of the development process as a maintainer or core developer entails performing specialized operations like managing branches and releases or performing database migrations. These additional tasks are listed in the [Operation Tasks section](operations/release-management.md).

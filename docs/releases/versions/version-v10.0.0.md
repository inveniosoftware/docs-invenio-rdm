# InvenioRDM v10.0

_2022-09-30_

_Short-term support (STS) release_

We're happy to announce the release of InvenioRDM v10.0. The release is a short-term support release which is maintained until v11.0 (due MM 202Y).

## Try it

- [Demo site](https://inveniordm.web.cern.ch)

- [Installation instructions](https://inveniordm.docs.cern.ch/install/)

## What's new?

In addition to the many bugs fixed, many features were added. Custom fields both for records and communities, back office administration with support for OAI sets management and OpenSearch support!

### Custom Fields

You can add custom fields to both [bibliographic records'](https://inveniordm.docs.cern.ch/customize/custom_fields/records/) and [communities'](https://inveniordm.docs.cern.ch/customize/custom_fields/communities/) data model. InvenioRDM supports a wide variety of types and UI widgets, you can find more about those in the [custom fields reference](https://inveniordm.docs.cern.ch/customize/custom_fields/records/#reference) and the [UI widgets reference](https://inveniordm.docs.cern.ch/reference/widgets/).

Moreover, you can extend the implementation with more complex objects to support your use cases, find more about that in the [custom fields development section](https://inveniordm.docs.cern.ch/develop/topics/custom_fields/).

#### Upload form

For example, software related fields will look as follows, you can test them out in the [demo site upload form](https://inveniordm.web.cern.ch/uploads/new).

![](img/../v10.0/custom_fields.png)

#### Community settings page

The configured custom fields will be displayed at the bottom of the community's settings page.

![](img/../v10.0/custom_fields_communities.png)

If a field is required to create a new community, then it
be displayed in the [Setup your new community](https://inveniordm-qa.web.cern.ch/communities/new) page.

### Backoffice

The admistration panel provides a modernised, clean and easy to use interface, which fulfils the following users’ needs:

- a graphical, user friendly interface (UI) to efficiently perform daily operations,
- a simple way of managing a repository which does not require technical knowledge.
- easy to extend/customise interface (for developers)

#### Resource based admin views

The newly added invenio-administration module allows to add an administration view with a minimal implementation. Based on exising endpoints of records resources, a developer is able to add more options to the management panel. The module allows to flexibly customise the way user interface elements are displayed.

#### Customisable admin views

The administration panel is fully customisable, which provides flexibility of implementation for even most complex managing actions. The full documentation on how to create, and customise the administration views is available under: //TODO add a link

By default, the administration panel includes out of the box support for OAI sets management.

![](img/../v10.0/backoffice_oai_sets.png)

Some OAI-PMH sets are automatically created when a new community is added. These system created sets are blocked from edition in the administration panel to preserve the data sets integrity.

### OpenSearch

InvenioRDM now support both OpenSearch 1 and 2, switching the default for new instances to OpenSearch 2. In addition, Elasticsearch 6 has been deprecated.

### Minor Changes

**Strict search mappings**

Search mappings have been made strict, which means that no unknown fields will be accepted. Before, no errors were being thrown. If you had custom record dumpers you might need to add custom fields and rebuild the indices. See the [upgrade guide](../upgrading/upgrade-v10.0.md) for more information.

**Deposit form publish modal warning text customization**

The warning text shown in the modal during the publish/submit-for-review action can now be extended via the `APP_RDM_DEPOSIT_FORM_PUBLISH_MODAL_EXTRA` config variable. You can pass text or html there and the result will look like the following:

![Customize publish modal wanring text](./v10.0/publish_modal_text_customize.png)

### Known issues

TODO

## Upgrading to v10.0

We support upgrading from v9.1 to v10 Please see the [upgrade notice](../upgrading/upgrade-v10.0.md).

## Maintenance policy

InvenioRDM v10.0 is a **short-term support** (STS) release which is supported until InvenioRDM v11.0 (release currently planned for MM 202Y). See our [Maintenance Policy](../maintenance-policy.md).

If you plan to deploy InvenioRDM as a production service, please use InvenioRDM v9.1 Long-Term Support (LTS) Release.

## Requirements

InvenioRDM v10.0 supports:

- Python 3.7, 3.8 and 3.9
- PostgreSQL 10+
- Elasticsearch 7 / OpenSearch 1 and 2

## Questions?

If you have questions related to these release notes, don't hesitate to jump on our chat and ask questions: [Getting help](../../develop/getting-started/help.md)

## Credit

The development work in this release was done by:

- CERN: Alex, Javier, Jenny, Karolina, Lars, Manuel, Nicola, Pablo, Pablo, Zacharias
- Northwestern University: Guillaume ??
- TU Graz: Christoph, David ??
- TU Wien: Max ??
- Someone else ??

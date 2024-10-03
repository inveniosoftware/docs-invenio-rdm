# InvenioRDM v10.1

_2022-12-08_

_Short-term support (STS) release_

We're happy to announce the release of InvenioRDM v10.1. The release is a short-term support release which is maintained until v11.0.

## Try it

- [Demo site](https://inveniordm.web.cern.ch)

- [Installation instructions](https://inveniordm.docs.cern.ch/install/)

## What's new?

This release includes translations of all strings included in v10.0 of InvenioRDM.

## Upgrading to v10.1

To upgrade from version 10.0 to 10.1 you need to update your instance's dependencies and assets:

- delete Pipfile.lock

run:

```shell
invenio-cli install
```

## Maintenance policy

InvenioRDM v10.1 is a **short-term support** (STS) release which is supported until InvenioRDM v11.0. See our [Maintenance Policy](../maintenance-policy.md).

If you plan to deploy InvenioRDM as a production service, please use InvenioRDM v9.1 Long-Term Support (LTS) Release.

## Requirements

InvenioRDM v10.1 supports:

- Python 3.7, 3.8 and 3.9
- PostgreSQL 10+
- Elasticsearch v7 / OpenSearch v1 and v2

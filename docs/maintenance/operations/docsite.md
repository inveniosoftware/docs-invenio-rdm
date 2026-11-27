# InvenioRDM Docs site

The documentation site is built with [MkDocs](https://www.mkdocs.org/) from the
[docs-invenio-rdm](https://github.com/inveniosoftware/docs-invenio-rdm) GitHub repository.

## Sites and branches

There are two deployments of the documentation, each tracking a branch of the repository:

| Site | URL | Branch | Content |
| ---- | --- | ------ | ------- |
| Production | [https://inveniordm.docs.cern.ch](https://inveniordm.docs.cern.ch) | `production` | Documentation of the current release of InvenioRDM. |
| Dev | [https://inveniordm-dev.docs.cern.ch](https://inveniordm-dev.docs.cern.ch) | `master` | Documentation of the in-development next version of InvenioRDM. |

## Deployment

The GitHub repository is mirrored to CERN, where the sites are built and deployed.
When new commits are pushed to the `master` or `production` branch on GitHub, the mirror
picks them up and the corresponding site is re-built and deployed. No manual action is needed.

## Making changes

All changes must be made via a PR against the `master` branch. Once merged, they will be
visible on the [dev site](https://inveniordm-dev.docs.cern.ch).

If a change should also be published on the production site (e.g. a fix, or documentation that
applies to the current release), it must be **first merged to `master`** and **then cherry-picked
to `production`**.

!!! warning
    Never commit directly to `production` changes that are not in `master`: they would be lost
    when `production` is reset to `master` at the next release.

## New releases

When a new InvenioRDM version is released, the `production` branch is reset to the `master` branch,
so that the production site shows the documentation of the new version. See the
[Release](release-management.md#release) section of the release management guide.

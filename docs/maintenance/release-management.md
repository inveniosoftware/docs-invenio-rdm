# Release Management

**Intended audience**

This guide is intended for maintainers and developers of InvenioRDM itself.

**Scope**

The guide covers how to release a new version of InvenioRDM.

## Overview

We follow [semantic versioning](https://semver.org/). In particular:

- ``0.y.z`` is for initial development - anything may change at any time.

InvenioRDM consists of:

- a CLI tool,
- an instance template,
- an application, and
- many modules.

### Tool versioning

The Invenio-CLI tool is intended to be able to work with many different application versions, and multiple products (RDM, ILS, ...), and is therefore independently versioned.

### Application versioning

The instance template (Cookiecutter-Invenio-RDM) and the application (Invenio-App-RDM) is together considered the application and therefore versioned together.

The application locks each dependent module to their minor-level versions so that patches can be distributed without breaking compatibility.

### Module versioning

Each module (e.g. Invenio-RDM-Records, Invenio, ...) is versioned independently. Each module MUST follow semantic versioning, so that the application can lock the module version to the minor-level release.

## Release checklist

### Initial iteration

In the beginning of each iteration we start by releasing new development versions of the below modules in the order they specified:

- flask-resources
- react-invenio-forms
- invenio-records-resources
    - bump flask-resources
- react-invenio-deposit
    - bump react-invenio-forms
- invenio-drafts-resources
    - bump invenio-records-resources
- invenio-vocabularies
    - bump invenio-records-resources
- invenio-rdm-records
    - bump invenio-drafts-resources
    - bump invenio-vocabularies
- invenio-communities
    - bump invenio-rdm-records
- invenio-app-rdm
    - bump invenio-rdm-records
    - bump invenio-communities
    - bump react-invenio-deposit
    - bump react-invenio-forms


For modules in ``v0.X.Y``, the new version is ``v0.(X+1).0``.

For modules in ``vX.Y.Z``, the new version is ``v(X+1).0.0.dev0``.

### Pre-release

- Ensure all dependent modules have been released.
- Release Invenio-App-RDM (removing the pre-release suffix - e.g. ``dev0``).
- Cookiecutter-Invenio-RDM:
    - Merge everything to master.
    - Create new version branch from master using the pattern ``vX.Y`` (e.g if Invenio-App-RDM is v1.0.0, the branch should be named ``v1.0``).

### Release

The final step to release the new modules and source code is to release Invenio-CLI. Releasing Invenio-CLI, will make all new installation use the latest released packages.

- Invenio-CLI:
    - Update Cookiecutter-Invenio-RDM branch version in the source code.
    - Bump version of Invenio-CLI and release.

### Post-release

- [Deploy InvenioRDM](demosite.md) to QA and PROD (demo website AND docs).
- Blog post (including adding a link under https://inveniosoftware.org/products/rdm/#status)
- Website update
    - Update [public roadmap](https://inveniosoftware.org/products/rdm/roadmap/).
    - Review project information
- Project tracking:
    - GitHub: Update [internal product roadmap](https://github.com/inveniosoftware/product-rdm/milestones?direction=asc&sort=due_date&state=open)


## Release a Python or JavaScript package

- Ensure all changes are merged in ``master`` branch on GitHub.
- Checkout master branch and make sure it's identical to GitHub.
```
git checkout master
git reset --hard upstream/master
```
- Bump version number:
    - Python: ``<package>/version.py``
    - JavaScript: ``package.json`` and ``package-lock.json``.
- Commit on master:
```
git add <package>/version.py
git commit -m "release: vX.Y.Z"
```
- Tag and push (both master and tag)
```
git tag vX.Y.Z
git push upstream master vX.Y.Z
```

# Release management

**Intended audience**

This guide is intended for maintainers and developers of InvenioRDM itself.

**Scope**

The guide covers how to release a new version of InvenioRDM.

## Overview

We follow [semantic versioning](https://semver.org/). In particular:

- `0.y.z` is for initial development - anything may change at any time.

InvenioRDM consists of:

- a CLI tool, [invenio-cli](https://github.com/inveniosoftware/invenio-cli)
- an instance template, [cookiecutter-invenio-rdm](https://github.com/inveniosoftware/cookiecutter-invenio-rdm)
- an application, [invenio-app-rdm](https://github.com/inveniosoftware/invenio-app-rdm)
- [many modules](../modules.md)

### Tool versioning

The `invenio-cli` tool is intended to be able to work with many different application versions, and multiple products (RDM, ILS, ...), and is therefore independently versioned.

### Application versioning

The instance template (cookiecutter-invenio-rdm) and the application (invenio-app-rdm) are together considered the application and therefore versioned together.

To be more precise: for a new major version of invenio-app-rdm a new branch with
the same version is created for cookiecutter-invenio-rdm (e.g. invenio-app-rdm
releases major version v14.0.0, a new branch v14.0 is created for
cookiecutter-invenio-rdm. This branch is used when `invenio-cli init -c v14.0`
is used to init a new InvenioRDM instance)

A new major version of invenio-app-rdm is released once a year. see
[maintenance-policy](../../releases/maintenance-policy.md). The development is
done on betaXX.devXX tags on master. Since invenio-app-rdm represents the
product InvenioRDM it uses a slightly different versioning schema. It still
follows the semver rules of versioning, but not on he major versions but on the
beta versions. This means: releasing a new major version (e.g. v14.0) starts on
the master branch the tagging of beta versions (e.g. v15.0.0b0.dev0). The new
patch and minor releases of the currently supported major version are done on
the `maint-*` branch (e.g. maint-v14.x)

The application locks each dependent module to their major-level versions so that patches can be distributed without breaking compatibility.

### Module versioning

Each module (e.g. invenio-rdm-records, invenio-records, ...) is versioned independently. Each module MUST follow semantic versioning, so that the application can lock the module version to the major-level release.

### Module releases

Doing a new major release of a module starts a major release chain. A module
supports only 1 major version of another module. This means doing a major break
in a low level package as `invenio-db` starts a long major release chain up to
invenio-app-rdm.

TODO: picture of the graph?

## Product Release

The product is InvenioRDM. The package invenio-app-rdm represents the product
and its versioning represents the product major version. Some packages of
inveniosoftware are tightly coupled with InvenioRDM. Those packages will get a
new major version and a new `maint-vX.0` branch in the moment the feature freeze
will take place.

The product release cycle starts with the release of the major version. This
means that from the date of the major version the new development cycly starts.
The release should take place in the first 2 weeks in July. The feature freeze
in the first two weeks of June. The considering for feature freeze PR's deadline
takes place in the first weeks of April.

With the feature freeze maintenance branches are created in the modules listed here:

- invenio-vocabularies [GitHub](https://github.com/inveniosoftware/invenio-vocabularies)
- invenio-requests [GitHub](https://github.com/inveniosoftware/invenio-requests)
- invenio-administration [GitHub](https://github.com/inveniosoftware/invenio-administration)
- invenio-communities [GitHub](https://github.com/inveniosoftware/invenio-communities)
- invenio-rdm-records [GitHub](https://github.com/inveniosoftware/invenio-rdm-records)
- invenio-app-rdm [GitHub](https://github.com/inveniosoftware/invenio-app-rdm)
- cookiecutter-invenio-rdm [GitHub](https://github.com/inveniosoftware/cookiecutter-invenio-rdm)

The master branch will get a new major release. Yes it could be that the
master branch will get a major version without any real changes on the master
branch and therefor not follow semver in some points. But for the product
InvenioRDM and it's further development it is easier to do it that way. It
enables to merge breaking changes directly after the feature freeze and not
affecting the release of the product.


### Steps

- [feature freeze] create maint branch
    - invenio-vocabularies [GitHub](https://github.com/inveniosoftware/invenio-vocabularies)
    - invenio-requests [GitHub](https://github.com/inveniosoftware/invenio-requests)
    - invenio-administration [GitHub](https://github.com/inveniosoftware/invenio-administration)
    - invenio-communities [GitHub](https://github.com/inveniosoftware/invenio-communities)
    - invenio-rdm-records [GitHub](https://github.com/inveniosoftware/invenio-rdm-records)
    - invenio-app-rdm [GitHub](https://github.com/inveniosoftware/invenio-app-rdm)

- [feature freeze] release on master new major version
    - invenio-vocabularies [GitHub](https://github.com/inveniosoftware/invenio-vocabularies)
    - invenio-requests [GitHub](https://github.com/inveniosoftware/invenio-requests)
    - invenio-administration [GitHub](https://github.com/inveniosoftware/invenio-administration)
    - invenio-communities [GitHub](https://github.com/inveniosoftware/invenio-communities)
    - invenio-rdm-records [GitHub](https://github.com/inveniosoftware/invenio-rdm-records)

- [feature freeze] release bX.devY
    - invenio-app-rdm [GitHub](https://github.com/inveniosoftware/invenio-app-rdm)

- [feature freeze] release release candidate
    - invenio-app-rdm [GitHub](https://github.com/inveniosoftware/invenio-app-rdm)

- [release] cookiecutter-invenio-rdm
    - create next major branch

- [release] invenio-cli:
    - Update default cookiecutter branch [here](https://github.com/inveniosoftware/invenio-cli/blob/master/invenio_cli/helpers/cookiecutter_wrapper.py#L69))

- [release] invenio-app-rdm
    - release vX.0.0 on maint-vX.0 branch


### Post-release

- [Deploy InvenioRDM](demosite.md) to QA and PROD (demo website AND docs).
- Write a blog post for <https://inveniosoftware.org/blog/>.
- Website update
    - Update [public roadmap](https://inveniosoftware.org/products/rdm/roadmap/).
    - Review project information.
    - Subtitle under <https://inveniosoftware.org/products/rdm/> title.
- Project tracking:
    - GitHub: Update [internal product roadmap](https://github.com/inveniosoftware/product-rdm/milestones?direction=asc&sort=due_date&state=open).
- Create maintenance branches of supported modules. See [branch management](branch-management.md).

## Release a Python or JavaScript package

- Ensure all appropriate PR's are merged onto the `master` branch on GitHub.
- Create a PR with commit message "release: vX.Y.Z" and the following content:
    - a list of changes added to the `CHANGES.md` file
    - a bump to the version number:
        - python: `<package>/__init__.py`
        - Javascript: `package.json`, update `package-lock.json`
- Create the tag

```bash
git remote update
git checkout upstream/master
```

for the version number [see above](#overview) about semantic versioning

```bash
git tag vX.Y.Z
git push upstream vX.Y.Z
```

## Maintenance workflow

Bugfixes and features are developed against the master branch and merged into
that branch first. Then the bugfix or feature is backported to the `maint-vX.Y`
branch.

Maintenance releases follow the same workflow as a new version release. You
only need to replace `master` with `maint-vX.Y` branches.

!!! warning PyPI releases are immediately picked up

    Be aware that when the independent modules are released, they will be
    picked up immediately by new InvenioRDM installations. This should not be
    an issues since the releases MUST be backward compatible and invenio-app-rdm
    constrains its dependencies below the next untested major versions.

Details about branch workflows are covered in the next section: [Branch management](branch-management.md)

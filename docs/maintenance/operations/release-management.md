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
- an application: the combination of an instance template,
  [cookiecutter-invenio-rdm](https://github.com/inveniosoftware/cookiecutter-invenio-rdm)
  and the main module
  [invenio-app-rdm](https://github.com/inveniosoftware/invenio-app-rdm)
  collecting and configuring the others
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

A new major version of invenio-app-rdm is released once a year. See the
[maintenance-policy](../../releases/maintenance-policy.md). Development is done
on betaXX.devXX tags on master. Since invenio-app-rdm represents the product
InvenioRDM it uses a slightly different versioning schema than other packages.
The development releases are done via beta releases. Since invenio-app-rdm acts
as the product package of InvenioRDM, the major releases are tied to the major
releases of InvenioRDM. The package follows semver rules of versioning on the
beta level. This means, during the development every major break is reflected on
increasing the beta version (not the major version). At the end of the product
release cycle the major version is bumped.

The patch and minor versioning of InvenioRDM is done on maintenance branches in
invenio-app-rdm, e.g. for InvenioRDM v14 we use maint-v14.x in invenio-app-rdm
and starts after the release of the major version of InvenioRDM (invenio-app-rdm)

The application locks each dependent module to their major-level versions so that patches can be distributed without breaking compatibility.

### Module versioning

Each module (e.g. invenio-rdm-records, invenio-records, ...) is versioned independently. Each module MUST follow semantic versioning, so that the application can lock the module version to the major-level release.

### Module releases

Doing a new major release of a module starts a major release chain. A module
supports only 1 major version of another module. This means doing a major release
in a low level package as `invenio-db` starts a long major release chain up to
invenio-app-rdm.

A major release chain is defined as follow: package B depends on package A.
package C depends on package B. Package A gets a major bump -> package B gets a
major bump and package C gets a major bump.

TODO: picture of the graph?

## Product Release

The product is InvenioRDM. The package invenio-app-rdm represents the product
and its versioning represents the product major version. Some packages of
inveniosoftware are tightly coupled with InvenioRDM. Those packages will get a
new major version and a new `maint-vX.0` branch in the moment the feature freeze
will take place.

The product release cycle (the development cycle) starts with the release of the
major version. The cycle includes following phases:

August - March: development, discuss features
April: finalize RFCs, finalize discussions (features started after will be
considered for the next major release of InvenioRDM. The time to finish the
discussions would outrun the release date)
June (first two week): features freeze (translation window starts)
July (first two week): major release

The features freeze has three implications:

1.) every package which contains a translations directory will be released as a
major version. This means every package which depends on this package will also
be released as a major version. This has the effect that we have a clear line
through the packages between one and the other major version of InvenioRDM
2.) every of those packages will get a `maint-*` branch with the version of the
last major version.
3.) the `maint-*` branches are used to push the translatable strings to
transifex and this starts the translation window which closes with the major release.


!!! warning

    The master branch will get a new major release, even without significant changes
    (in this case, semver on the package level is not strictly followed). This
    approach allows merging unrelated breaking changes after the features
    freeze, without affecting an ongoing release.

### Steps

TODO: this has to be updated

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

Bugfixes and features are developed from and merged into the master branch.
Then, they are backported to the `maint-vX.Y` branch.

Maintenance releases follow the same workflow as a new version release. You
only need to replace `master` with `maint-vX.Y` branches.

!!! warning PyPI releases are immediately picked up

    Be aware that when the independent modules are released, they will be
    picked up immediately by new InvenioRDM installations. This should not be
    an issues since the releases MUST be backward compatible and invenio-app-rdm
    constrains its dependencies below the next untested major versions.

Details about branch workflows are covered in the next section: [Branch management](branch-management.md)

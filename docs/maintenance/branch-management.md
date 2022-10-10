# Branch management

**Intended audience**

This guide is intended for maintainers and developers of InvenioRDM itself.

**Scope**

The guide covers how branches are managed in InvenioRDM in order to support
the maintenance policy.

## Overview

An InvenioRDM Long-Term Support (LTS) release is supported for minimum 1 year
and for minimum 6 months after the next new LTS release (see
[maintenance policy](../releases/maintenance-policy.md)). Only the latest minor
version of an LTS release is supported (e.g. we do not support both v6.0 and
v6.1).

### Opening pull requests

#### PR against ``master``/``main``

You should normally always open pull requests against the ``master``/``main``
branch. One exception is when a bug/security fix is only reproducible on a
maintenance branch.

#### Separate logical commits

If you are fixing a bug, please ensure that the bug is fixed in a separate
logical commit, to ensure that it is easy to backport the fix to previous
maintained releases.

#### Security fixes are done in hidden branches

Note that security fixes are normally done in a coordinated way using hidden
branches until PyPI releases have been issued. Please get in touch with a
maintainer.

### Merging pull requests

A PR is merged as usual once the continuous integration tests pass and the
code has been through a code review.

#### Maintainer is responsible for backporting

The maintainer merging the PR is now responsible for backporting the fix to all
maintained releases. The maintainer is free to ask the developer opening the
PR to backport the fix, but it's the maintainer that's ultimately responsible
for ensuring that the fix is backported.

#### Supported maintenance branches

Following is an overview of which versions/branch(es) are currently supported for
InvenioRDM modules (see the currently supported InvenioRDM versions and their
end of life dates on the
[maintenance policy](../releases/maintenance-policy.md)).

| Module                      | Supported versions     | Supported branches             |
| --------------------------- | ---------------------- | ------------------------------ |
| flask-resources             | ``0.7.x``, ``0.8.x``   | ``maint-0.7``, ``maint-0.8``   |
| invenio-app-rdm             | ``6.0.x``, ``8.0.x``   | ``maint-6.0``, ``maint-8.0``   |
| invenio-communities         | ``2.5.x``, ``2.7.x``   | ``maint-2.5``, ``maint-2.7``   |
| invenio-drafts-resources    | ``0.13.x``, ``0.15.x`` | ``maint-0.13``, ``maint-0.15`` |
| invenio-rdm-records         | ``0.32.x``, ``0.34.x`` | ``maint-0.32``, ``maint-0.34`` |
| invenio-records-permissions | ``0.12.x``, ``0.13.x`` | ``maint-0.12``, ``maint-0.13`` |
| invenio-records-resources   | ``0.16.x``, ``0.18.x`` | ``maint-0.16``, ``maint-0.18`` |
| invenio-requests            | ``0.2.x``              | ``maint-0.2``                  |
| invenio-s3                  | ``1.0.x``              | ``maint-1.0``                  |
| invenio-vocabularies        | ``0.8.x``, ``0.10.x``  | ``maint-0.8``, ``maint-0.10``  |
| marshmallow-utils           | ``0.5.x``              | ``maint-0.5``                  |
| react-invenio-deposit       | ``0.16.x``, ``0.17.x`` | ``maint-0.16``, ``maint-0.17`` |
| react-invenio-forms         | ``0.8.x``, ``0.9.x``   | ``maint-0.8``, ``maint-0.9``   |

!!! info "Didn't find the module?"

    If a module is not listed above, it is because the version is either
    unconstrained or part of Invenio Framework and constrained by the Invenio
    Framework setup. For unconstrained modules you should take great care that
    the change/fix is backward compatible. If not, we have to constrain the
    module version in one of the InvenioRDM modules.

### Backporting

Following is a small recipe for how to backport a fix:

1. Identify the **commit** on ``master``/``main`` that you want to backport.
   ```
   git log master
   ```
2. Identify the **branches** you have to backport the fix to (using above table
   of supported maintenance branches).
3. Cherry-pick the identified commit to all supported maintenance branches.
   ```
   git checkout maint-6.0
   git cherry-pick <commit hash>
   git checkout maint-10.0
   git cherry-pick <commit hash>
   ```

Releasing a new maintenance release is covered under
[release management](release-management.md).

### Branching

#### Table must be kept updated

The table over supported maintenance releases/branches must be updated when:

- a new major version is released
- a major version reaches end of life.

First, make sure the end of life and support versions have been updated in
the [maintenance policy](../releases/maintenance-policy.md).

Once you have determined which major versions of InvenioRDM that are supported,
you can start from ``invenio-app-rdm`` to figuoure out which module versions
and branches that are supported and can update the table accordingly.

#### Create maintenance branches on LTS releases

When a new LTS version is released, the release manager should go through all
above repositories and create ``maint-x.y`` branches from the master/main
branch.

The newly created maintenance branches must be added to [repositories.yml](https://github.com/inveniosoftware/opensource/blob/master/repositories.yml) to configure branch protection in GitHub so only maintainers
can merge to the branch.

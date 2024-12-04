# Branch management

**Intended audience**

This guide is intended for maintainers and developers of InvenioRDM itself.

**Scope**

The guide covers how branches are managed in InvenioRDM in order to support
the maintenance policy.

## Overview

The latest InvenioRDM release is supported until the next release
(see [maintenance policy](../releases/maintenance-policy.md)).

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

#### Create maintenance branches on release

When a new release is released, the release manager should go through all
above repositories and create ``maint-x.y`` branches from the master/main
branch.

The newly created maintenance branches must be added to [repositories.yml](https://github.com/inveniosoftware/opensource/blob/master/repositories.yml) to configure branch protection in GitHub so only maintainers
can merge to the branch.

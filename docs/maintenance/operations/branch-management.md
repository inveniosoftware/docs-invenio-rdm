# Branch management

**Intended audience**

This guide is intended for maintainers and developers of InvenioRDM itself.

**Scope**

The guide covers how branches are managed in InvenioRDM in order to support
the [maintenance policy](../../releases/maintenance-policy.md).

## Overview

InvenioRDM follows [Trunk-Based Development](https://trunkbaseddevelopment.com/) on the main branch (`master`) of all its modules. Changes in `master` usually won't have an out-of-the-box backwards-compatibility assurance. If things break, they are usually fixed as soon as possible anyway, since we want to be able to develop reliably.

Stable releases are being maintained under their equivalent `maint` branches. For example, `v12.0.x` is maintained on the `maint-v12.x` branch of `invenio-app-rdm`. Those releases receive bug fixes following SemVer, e.g., `v12.0.1`, by backporting (usually via cherry-picking) the fixes from the `master` branch into the `maint` branch.

Occasionally, if we see features in `master` that the community agrees should be in the stable branches, we can organize efforts to backport them using a minor version bump in the stable release (e.g., `v12.1.x`). To qualify for such minor version bumps, the changes adhere to the following assurances:
    - The new features **MUST** be disabled by default using config feature flags
    - If an instance doesn't enable or use the new features, it **MUST** still work
    - If an instance wants to enable or use the new features, there **MAY** be some migration/upgrade recipes required to be run

The latest InvenioRDM release is supported until the next release.

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

Make sure the end of life and support versions have been updated in
the [maintenance policy](../../releases/maintenance-policy.md).

#### Create maintenance branches on release

When a new version is released, the release manager should go through all
the repositories and create ``maint-x.y`` branches from the master/main
branch.

The newly created maintenance branches must be added to [repositories.yml](https://github.com/inveniosoftware/opensource/blob/master/repositories.yml) to configure branch protection in GitHub so only maintainers
can merge to the branches.

# Copyright and license policy

Copyright tracks who **owns** the source code. A license gives third-parties
**rights** to the source code.

## License

All released source code should by default be licensed under MIT License.
Exceptions may be made to this policy on a case-by-case basis. Reasons for
exceptions could be (but not limited to):

- Source code already released under another permissive license (e.g. Apache
  v2, BSD) or LGPL.

In all cases, source code should not be released under a copyleft license like
GPL or AGPL.

## Tracking copyright



**Copyright statements**

Copyright statements must be included in:

- ``LICENSE`` file in the root of the repository.
- Headers of all source code files.

Each copyright holder must have their own copyright statement::

```
Copyright (C) 2015-2018 CERN
Copyright (C) 2017 TIND
```

**Copyright holders**

Each copyright holder **must** be a legal entity.

Copyright is tracked for non-trivial contributions (i.e. creative work). By
default we consider anything above 15 lines for a non-trivial contribution.
Examples for which we do not track copyright is e.g. fixing a typo or tiny
bug fixes.

**Legal entity**

A legal entity can be human (physical persons) or
non-human (juridical persons, e.g. corporations). A legal entity has
privileges and obligations such as being able to enter into contracts, to
sue or be sued. Thus, e.g. CERN is a legal entity but e.g. ATLAS, CMS and
Invenio Collaboration are not considered legal entities by the law.

**Maintainer responsibility**

Maintainers are responsible for asking each contributor who is the copyright
holder of a given contribution (often, it's the employer who holds the
copyright).

**Attribution**

Attribution is not tracked via copyright, but via the ``AUTHORS`` file.

## Explicit agreement

**Contributions only via GitHub**

All contributions must be opened via pull requests on GitHub. This way
contributors have agreed to the [GitHub Terms of Use](https://help.github.com/articles/github-terms-of-service/#6-contributions-under-repository-license),
which states:

> "Whenever you make a contribution to a repository containing notice of a
> license, you license your contribution under the same terms, and you agree
> that you have the right to license your contribution under those terms."

This method avoid introducing either a Contributor License Agreement (CLAs) or
a Developer Certificate of Origin.

## Principles

Invenio's copyright and license policy is based on the following principles:

- Shared copyright - every contributor maintain ownership over the code they
  contribute.
- Permissive open source licensing - all copyright holders license their
  contribution under a permissive open source license (MIT License).
- Contributing via GitHub - to obtain explicit agreement from the copyright
  holder to that they agree to license their source code under the open source
  license, and that they have the rights to license it.

We explicitly avoid:

- A single copyright holder or Contributor License Agreements (CLAs)
  which usually amounts to almost the same as a copyright transfer to a single
  copyright holder.
- Viral/Copy-left licenses like GPL and AGPL.

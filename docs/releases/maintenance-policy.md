# Maintenance policy

Our goal is to ensure that the latest InvenioRDM release is supported with bug and security fixes for a minimum of one year after its release date, and 6 months after the next latest release. This promotes stability and gives adopters a dependable transition period. We aim at having a new release every year. We strive our best to ensure that upgrades between versions are straight-forward to ensure users follow our latest releases.

Our maintenance policy strives to strike a balance between supporting a rock-solid secure product, shipping new features + refactoring old code, and ensuring that we have enough resources to do all this. It pushes users to adopt the latest version, so that they can benefit from continued support. Most new features are behind configuration flags, so they can be gradually adopted though.

## Policy

Starting with the v12 release, we have shifted from the Long-Term Support (LTS) and Short-Term Support (STS) model to aiming for one stable major release per year.

**Major release:** Major versions, such as v12, introduce new features, can make backward incompatible changes, and sometimes remove deprecated features in a progressive manner. Only the latest minor-level release for each major version is supported. A major version release is supported for 6 months past the next major version release. In practice, a major version *could* be incompatible with prior customizations, but not necessarily. It is more often a way for the development team to establish a new set of features/modules for which they guarantee cohesion and for which they limit their attention to.

**Minor releases:** Minor versions, such as v12.1, introduce backward compatible changes in a manner that allows users to easily upgrade.

**Patch releases:** Patch versions, such as v12.0.1, allow us to fix bugs and security issues in a manner that allows users to upgrade immediately without breaking backward compatibility.

We may make exceptions to this policy for serious security bugs.

## Support periods

Following is an overview of future end of life (EOL) dates for recent releases:

| Release | Date                   | Maintained | Until                                              |
| ------- | ---------------------- | ---------- | -------------------------------------------------- |
| v13     | 2025-08-01 (tentative) | ✅         | next release + 6 months                            |
| v12     | 2024-08-01             | ✅         | 2026-02-01                                         |
| v11 STS | 2023-01-26             | ❌         | 2024-08-01                                         |
| v10 STS | 2022-10-10             | ❌         | 2023-01-26                                         |
| v9 LTS  | 2022-05-24             | ❌         | 2025-02-01                                         |
| v6 LTS  | 2021-08-05             | ❌         | 2022-12-31                                         |

If your version is not listed, then it is not maintained anymore.

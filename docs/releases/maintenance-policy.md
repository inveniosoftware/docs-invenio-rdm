# Maintenance policy

Our goal is to ensure that the latest InvenioRDM release is supported with bug and security fixes for minimum one year after the release date, and possibly longer.
We aim at having a new release every year. We strive our best to ensure that upgrades between versions are fairly straight-forward to ensure users follow our latest releases.

The maintenance policy is striving to strike a balance between maintaining a rock solid secure product while ensuring that users migrate to latest releases and ensuring that we have enough resources to actually support the maintenance policy.

## Policy

Starting with the v12 release, we have shifted from the Long-Term Support (LTS) and Short-Term Support (STS) model to aiming for one stable major release per year.

**Major release:** Major versions such as v12 allow us to introduce new features, make backward incompatible changes and remove deprecated features in a progressive manner. Only the latest minor-level release for each major version is supported. A major version release is supported until the next major version release.

**Minor releases:** Minor versions such as v3.1 allow us to introduce backward compatible changes in a manner that allow users to easily upgrade.

**Patch releases:** Patch versions such as v3.0.1 allow us to fix bugs and security issues in a manner that allows users to upgrade immediately without breaking backward compatibility.

We may make exceptions to this policy for serious security bugs.

### End of life dates

Following is an overview of future end of life (EOL) dates for currently maintained releases:

| Release     | Earliest EOL Date | Maintained until    |
| ----------- | ----------------- | ------------------- |
| v12.0.0     |                   | next release        |
| v11.0.0 STS |                   | next release        |
| v10.0.0 STS |                   | next SLS            |
| v9.0.0 LTS  | 2023-05-24        | next LTS + 6 months |
| v6.0.0 LTS  |                   | 2022-12-31          |

# Maintenance policy

Our goal is to ensure that InvenioRDM **Long-Term Support releases** are supported with bug and security fixes for minimum one year after the release date and possibly longer.  We aim at having new major releases every 3-months, especially in the early life of InvenioRDM. We strive our best to ensure that upgrades between major versions are fairly straight-forward to ensure users follow our latest releases.

The maintenance policy is striving to strike a balance between maintaining a rock solid secure product while ensuring that users migrate to latest releases and ensuring that we have enough resources to actually support the maintenance policy.

## Policy

**Long-Term Support (LTS) releases:** A major version release may be designated as an LTS release. Only LTS releases should be used for production services. LTS releases is supported with bug and security fixes for minimum 1 year and possibly longer. An LTS release is supported for 6 months after the next LTS release has been released. Only the latest minor-level release for the major version is supported. Example, if v6.0 is designated an LTS release, then only the latest v6.X release is maintained, as minor and patch-level releases

**Major release:** Major versions such as v3 allows us to introduce new features and make backward incompatible changes and remove deprecated features in a progressive manner. Only the latest minor-level release is for each major version is supported. A major version release is supported until the next major version release (except for LTS designated releases).

**Minor releases:** Minor versions such as v3.1 allows us to introduce backward compatible changes in a manner that allow users to easily upgrade.

**Patch releases:** Patch versions such as v3.0.1 allows us fix bugs and security issues in a manner that allow users to upgrade immediately without breaking backward compatibility.

We may make exceptions to this policy for serious security bugs.

### End of life dates

Following is an overview of future end of life (EOL) dates for currently maintained releases:

| Release | Earliest EOL Date | Maintained until |
| ------- | ------------------|----------------- |
| v6.0.0 LTS  | 2022-08-05    | next LTS + 6 months

### End of life releases

The following releases have reached end of life:

| Release | EOL Date    |
| ------- | ----------- |
| v5.0.0  | 2021-08-05  |
| v4.0.0  | 2021-07-23  |
| v3.0.0  | 2021-05-28  |
| v2.0.0  | 2021-04-28  |
| v1.0.0  | 2021-03-26  |

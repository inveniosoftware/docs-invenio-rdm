# Upgrade Policy

Following document is meant to align expectations on the upgrade process
between major versions.

## Supported features

We only support features and APIs which have been **documented** in this
present documentation. Any other feature/API change will not be considered a
breaking change.

## Breaking changes

We use semantic versioning, and thus you **MUST** expect breaking changes
between major versions (REST API, programmatic APIs, templates, data models etc.).
We will document these breaking changes in the release notes, and do our best to
provide automatic upgrades if possible.

## Offline upgrade

You MUST expect the upgrade process to be an offline process that requires the
production system to be offline during the entire upgrade process. We strive
allow online rolling upgrades in the future, but we are not there yet.

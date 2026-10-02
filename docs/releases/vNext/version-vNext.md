# InvenioRDM vNext

_2020-XX-XX_

Here are the release notes for InvenioRDM vNext, the open-source
repository platform for research data management, institutional repositories,
and digital assets management! Version Next will be maintained until at least
6 months following the next major release. Visit our [maintenance policy page](../maintenance-policy.md) to learn more.
The previous major version, version 14, will be out of support 6 months from today.

## Try it

- [Demo site](https://inveniordm.web.cern.ch)

- [Install from scratch instructions](../../install/index.md)

## What's new?

### Asynchronous and subcommunity curation checks

Curation checks now support **asynchronous execution** and can be applied to **communities** in addition to records.

#### Asynchronous checks

![Asynchronous check on RUNNING status](imgs/async-check.png)

Previously, all checks ran synchronously during HTTP requests, meaning long-running or externally-integrated checks would block the user until completion. Checks can now be declared asynchronous by setting `sync = False` on the check class, causing them to dispatch a Celery background task instead of blocking the request.

Checks may also expose a `allow_rerun = True` flag to let privileged users manually re-trigger the check from the UI.

#### Community checks

Checks can now be scoped to **communities** rather than records alone, via the new `target_type` field on `CheckConfig`. Enabling the `CHECKS_SUBCOMMUNITY_ENABLED` feature flag activates automated checks on subcommunity join requests, so curators get an overview of previously defined criteria before accepting a subcommunity.

See the [curation checks documentation](../../operate/customize/curation-checks.md) for full setup instructions and a guide to implementing your own async or community checks.

## Upgrading to vNext

Detailed instructions on how to upgrade from v14 to vNext are in the [vNext upgrade guide](./upgrade-vNext.md).

## Questions?

If you have questions related to these release notes, don't hesitate to jump on [discord](https://discord.gg/8qatqBC) and ask us!

## Credit

The development of this release wouldn't have been possible without the help of these smart people (name or GitHub handle, alphabetically sorted):
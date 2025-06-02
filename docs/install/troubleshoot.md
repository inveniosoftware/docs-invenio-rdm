# Troubleshooting & getting help

Something has gone wrong, now what? Your first reflex should be to consult the logs. Then consult this documentation site or [appropriate repositories](../maintenance/modules.md) for known issues. You can also always [reach out to the community](#getting-help) to ask for help.

## Retrieving logs

If the error comes from the local development instance (`invenio-cli run`), look at the terminal, the logs show up there.

On the other hand, if the error comes from the fully containerized application (`invenio-cli containers start`), you won't see logs on the terminal directly. They will be managed by docker. See the [Operate an Instance section on retrieving logs](../operate/ops/logging.md) in this case. The information is over there since this is a common approach in a small production environment.

## Common issues

### Building on an M1
When building on a M1 (arm64) you might encounter the following error:
```bash
pkg_resources.DistributionNotFound: The 'greenlet!=0.4.17; python_version >= "3" and (platform_machine == "aarch64" or (platform_machine == "ppc64le" or (platform_machine == "x86_64" or (platform_machine == "amd64" or (platform_machine == "AMD64" or (platform_machine == "win32" or platform_machine == "WIN32"))))))' distribution was not found and is required by SQLAlchemy
```

In order to solve it, a common workaround consists in installing the `sqlalchemy[asyncio]` package which brings in the correct dependencies.
As such, you should add the following line inside your `Pipfile`:

```python
sqlalchemy = {version = "*", extras = ["asyncio"]}
```
in the `[packages]` section.

## Getting help

The development community is very active on Discord, so in case the documentation
wasn't sufficient or not clear, simply jump on Discord using the link below,
and ask:

- Join Discord [``inveniosoftware``](https://discord.gg/8qatqBC)

Please bring logs and/or detailed descriptions of what you did, what you got and what you expected. Without that information, community members will have a hard time diagnosing a report of something "not working"!

And if you've encountered a problem someone else is asking about, contribute to the discussion! You don't have to be an expert to help others. Activity around a topic helps maintainers better understand scope and effect of particular situations.

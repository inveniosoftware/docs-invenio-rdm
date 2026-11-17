# Geolocation Services

_Introduced in v15_

InvenioRDM finds the country of a visitor from their IP address. It does this in two places:

| What | Where the country is stored | Where it is shown |
| ---- | --------------------------- | ----------------- |
| Usage statistics events | The `country` field of each event in the events indices. See [Usage statistics](../../maintenance/internals/statistics.md). | Not shown by default. |
| Login sessions | The session activity of the user. | "Location" on the user's security settings page, and the `country` field in the sessions list of the REST API. |

The country is stored as a two-letter [ISO 3166-1](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) code (for example `CH` for Switzerland), or no value if the country is not known.

## Using IPtoCC

This is the default option, nothing needs to be set up. The country is found with the [IPtoCC](https://github.com/roniemartinez/IPToCC) library:

- It needs no account, no licence key and no database to download.
- Its data is part of the installed Python package, and it makes no network calls.
- It is licensed under MIT or Apache 2.0, so you do not need to credit anybody to use it.

Keep the following in mind:

- **The data is as fresh as the installed version.** The library publishes new releases often, with updated data. To get newer data, upgrade the `iptocc` package.
- **The country is the one assigned to the IP block, not where the person is.** Visitors that use a VPN, a proxy or a cloud network can show up with another country than the one they are in. The data comes from the regional internet registries (such as RIPE NCC and ARIN), which assign IP blocks to organisations.
- **Some addresses have no country.** This is the case for loopback addresses such as `127.0.0.1`, for text that is not an IP address, and for blocks that the registries do not assign to one country. These get no country.

## Using a MaxMind database

This needs configuring, for login sessions, you can use a database file in the MaxMind DB format (`.mmdb`) instead, for example [GeoLite2](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data) or [DB-IP](https://db-ip.com/db/lite.php). Set the path in your `invenio.cfg`:

```python
# invenio.cfg
ACCOUNTS_GEOIP_DB_PATH = "/path/to/GeoLite2-Country.mmdb"
```

If the setting is empty (the default), IPtoCC is used. No extra package needs to be installed to read the file.

### Behaviours

- **The file is yours to source and maintain.** InvenioRDM does not download it. Each provider has its own licence, which may require an account, a key, or a credit to the provider. Check and follow the terms of the database you choose.
- **An address that is not in the file has no country.** InvenioRDM does not ask IPtoCC in that case, there will be no country.
- **A file that cannot be read does not stop logins.** If the file is missing, damaged or not a MaxMind database, an error is written to the application log and IPtoCC is used instead. This is logged for every login until the file is fixed, so watch your logs after changing the setting.
- **A new file is picked up without a restart.** When you refresh the file, write the new file next to the old one and rename it over the old one. Do not copy over it in place, because a lookup could then read a half-written file.

!!! info "Only for login sessions"
    This setting only affects the country of login sessions. The country of usage statistics events always comes from IPtoCC, and there is no setting for it yet.

## Upgrading

Earlier versions used the `maxminddb-geolite2` package, which came with a database from 2018 that was never updated. It is no longer used. Countries that are already stored are not changed.

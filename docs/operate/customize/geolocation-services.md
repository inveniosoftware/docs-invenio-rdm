# Geolocation Services

_Introduced in v15_

InvenioRDM can identify the country of origin of a visitor from their IP address. You can configure it in the following ways:

- [Using IPtoCC](#using-iptocc): the default, with nothing to set up.
- [Using an MMDB database file](#using-an-mmdb-database-file): a database file that you provide and keep up to date yourself, for more precise results.

The country is used in two places:

| What | Where the country is stored | Where it is shown |
| ---- | --------------------------- | ----------------- |
| Usage statistics events | The `country` field of each event in the events indices. See [Usage statistics](../../maintenance/internals/statistics.md). | Not shown by default. |
| Login sessions | The session activity of the user. | "Location" on the user's security settings page, and the `country` field in the sessions list of the REST API. |

The country is stored as a two-letter [ISO 3166-1](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) code (for example `CH` for Switzerland), or no value if the country is not known.

## Using IPtoCC

This is the default option, nothing needs to be set up. The country is found with the [IPtoCC](https://github.com/roniemartinez/IPToCC) library, which is installed with InvenioRDM and works offline.

### Where the data comes from

IP addresses are handed out in blocks by five [Regional Internet Registries](https://en.wikipedia.org/wiki/Regional_Internet_registry) (AFRINIC, APNIC, ARIN, LACNIC and RIPE NCC). Each registry publishes the country that every block is assigned to. IPtoCC refreshes this data nightly from the registries and bundles it in each release of its Python package.

This means that the lookup needs no account, no licence key and no database to download, and it makes no external network calls. The library is licensed under MIT or Apache 2.0, so you do not need to credit anybody to use it.

### Accuracy and limitations

- **The country is the one assigned to the IP block, not where the person is.** Visitors that use a VPN, a proxy or a cloud network can show up with another country than the one they are in. According to the IPtoCC documentation, registry data agrees with a widely used commercial geolocation database for about 95% of IPv4 addresses, with minimal differences for IPv6 ([Zander, 2012](https://figshare.swinburne.edu.au/articles/report/On_the_accuracy_of_IP_geolocation_based_on_IP_allocation_data/26254751)).
- **The data is as fresh as the installed version.** When you update your InvenioRDM instance, the latest version of `iptocc` is installed, which may bring a new database. Between updates, the data does not change.
- **Some addresses have no country.** This is the case for loopback addresses such as `127.0.0.1`, and for blocks that the registries do not assign to one country. These get no country.

If this is not accurate enough for your instance, or you need data that does not depend on updating InvenioRDM, use a [database file](#using-an-mmdb-database-file) instead. It is more complex to set up, because you have to source and refresh the file yourself.

## Using an MMDB database file

For more precise geolocation, you can configure InvenioRDM to read a database in the [MMDB format](https://maxmind.github.io/MaxMind-DB/) (`.mmdb`), a binary file that maps IP ranges to locations. Several providers publish country databases in this format.

InvenioRDM expects a country-level file: for each IP, it reads the two-letter country code from the `country.iso_code` field of the record, using the `maxminddb` Python library. A file whose records have no such field gives no country.

This method requires you to set up, outside InvenioRDM, a recurring download of new versions of the database, and to store it in a path that InvenioRDM can read. Then set the path in your `invenio.cfg`:

```python
# Default: use IPtoCC
ACCOUNTS_GEOIP_DB_PATH = None

# Use a database file
ACCOUNTS_GEOIP_DB_PATH = "/path/to/your/file.mmdb"
```

This setting is the switch between the two methods: if it is `None` (the default), IPtoCC is used, and if it has a path, the file is used. No extra package needs to be installed to read the file.

### Behaviours

- **The file is yours to source and maintain.** InvenioRDM does not download it. Each provider has its own licence, which may require an account, a key, or a credit to the provider. Check and follow the terms of the database you choose.
- **A file that cannot be read does not stop logins.** If the file is missing, damaged or not a valid MMDB file, an error is written to the application log and IPtoCC is used instead. This is logged for every login until the file is fixed, so watch your logs after changing the setting.
- **A new file is picked up without a restart.** When you refresh the file, write the new file next to the old one and rename it over the old one. Do not copy over it in place, because a lookup could then read a half-written file.

## Upgrading

Before InvenioRDM v15, the country was found with the `maxminddb-geolite2` package, which came with a database from 2018 that was never updated. From v15, it is replaced by IPtoCC, or by a database file if you set `ACCOUNTS_GEOIP_DB_PATH`. Countries that are already stored are not changed.

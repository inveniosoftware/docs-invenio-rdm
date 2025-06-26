# Deutsche National Bibliothek (DNB) URN registration

*Updated for InvenioRDM v13*

!!! info

    The URN registration feature requires that you have a contract with the [German National Library](https://wiki.dnb.de/display/URNSERVDOK/URN-Service+API). You will need to contact urn-support@dnb.de to get an account for the sandbox and the production REST-API.

In order to register [Uniform Resource Names](https://en.wikipedia.org/wiki/Uniform_Resource_Name) (URNs) with InvenioRDM, you need to install the additional module [invenio-pidstore-extra](https://pypi.org/project/invenio-pidstore-extra/).

If you're interested in the source code, you will find it [here](https://github.com/ulbmuenster/invenio-pidstore-extra).

The module implements a thin wrapper around the [Rest-API](https://wiki.dnb.de/display/URNSERVDOK/URN-Service+API) provided by the DNB (German national library) and enhances InvenioRDM with URN minting support. New is the support of versioning: the first versions URN automatically forwards to the most actual version.

=== "Pipfile"

    ```diff
    [packages]
    ...
    + invenio-pidstore-extra = ">=0.2.0,<1.0.0"
    ```

=== "pyproject.toml"

    ```diff
    dependencies = [
    ...
    +   "invenio-pidstore-extra >= 0.2.0,<1.0.0",
    ]
    ```


And next:

=== "pip"

    ```shell
    rm -f Pipfile.lock
    invenio-cli install
    ```

=== "uv"

    ```shell
    rm -f uv.lock
    invenio-cli install
    ```

## Configure the DNB URN PID provider

!!! tip "DNB sandbox replacement"

    The flask app invenio_pidstore_extra.dnb-sandbox.py contains a very simple implementation of the DNB api to allow testing the URN support when the DNB sandbox is not available or just no user has been provided. You can start it with calling `flask --app invenio_pidstore_extra.dnb-sandbox run --port=8000`.

After adding the module to your InvenioRDM instance you need to add the following snippet to your `invenio.cfg`.
Make sure you have registered at the DNB and set the config variables below to the correct values!
When putting this to production, set `PIDSTORE_EXTRA_TEST_MODE = False`!

```diff
+   PIDSTORE_EXTRA_DNB_SANDBOX_URI = "http://127.0.0.1:8000/"

+   PIDSTORE_EXTRA_DNB_ENABLED = True
+   PIDSTORE_EXTRA_DNB_USERNAME = "username"
+   PIDSTORE_EXTRA_DNB_PASSWORD = "password"
+   PIDSTORE_EXTRA_DNB_ID_PREFIX = "urn:nbn:de:hbz:6"
+   PIDSTORE_EXTRA_FORMAT = "{prefix}-{id}"
+   PIDSTORE_EXTRA_TEST_MODE = True

#
# Persistent identifiers configuration
#
+   from invenio_rdm_records.config import RDM_PERSISTENT_IDENTIFIER_PROVIDERS as DEFAULT_PERSISTENT_IDENTIFIER_PROVIDERS
+   from invenio_pidstore_extra import providers

+   RDM_PERSISTENT_IDENTIFIER_PROVIDERS = DEFAULT_PERSISTENT_IDENTIFIER_PROVIDERS + [
+       providers.DnbUrnProvider(
+         "urn",
+         client=providers.DNBUrnClient("dnb", PIDSTORE_EXTRA_DNB_ID_PREFIX, 
+         PIDSTORE_EXTRA_DNB_USERNAME, PIDSTORE_EXTRA_DNB_PASSWORD, 
+         PIDSTORE_EXTRA_FORMAT),
+         label=_("URN"),
+       ),
+   ]

+   from invenio_rdm_records.config import RDM_PERSISTENT_IDENTIFIERS as +   DEFAULT_PERSISTENT_IDENTIFIERS

+   RDM_PERSISTENT_IDENTIFIERS = {
+       **DEFAULT_PERSISTENT_IDENTIFIERS,
+       "urn": {
+         "providers": ["urn"],
+         "required": True,
+         "label": _("URN"),
+         "is_enabled": providers.DnbUrnProvider.is_enabled,
+       },
+   }

+   from invenio_pidstore_extra.services.components import URNRelationsComponent
+   from invenio_rdm_records.services.components import DefaultRecordsComponents

+   RDM_RECORDS_SERVICE_COMPONENTS = DefaultRecordsComponents + 
+   [URNRelationsComponent]

```

The URN PID provider is configured to automatically generate and mint the URN: there is actually no support
for URNs in the upload form UI.

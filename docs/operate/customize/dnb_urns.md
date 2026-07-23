# Deutsche National Bibliothek (DNB) URN registration

*Updated for InvenioRDM v14*

!!! info

    The URN registration feature requires that you have a contract with the [German National Library](https://wiki.dnb.de/display/URNSERVDOK/URN-Service+API). You will need to contact urn-support@dnb.de to get an account for the sandbox and the production REST-API.

In order to register [Uniform Resource Names](https://en.wikipedia.org/wiki/Uniform_Resource_Name) (URNs) with InvenioRDM, you need to install the additional module [invenio-pidstore-extra](https://pypi.org/project/invenio-pidstore-extra/).

If you're interested in the source code, you will find it [here](https://github.com/ulbmuenster/invenio-pidstore-extra).

The module implements a thin wrapper around the [Rest-API](https://wiki.dnb.de/display/URNSERVDOK/URN-Service+API) provided by the DNB (German national library) and enhances InvenioRDM with URN minting support. Versioning is supported, too: the first versions URN automatically forwards to the most actual version. New in this version is the possibility to define several namespaces (or even clients), so every community can mint URN's in an own namespace. 

=== "pyproject.toml"

    ```diff
    dependencies = [
    ...
    +   "invenio-pidstore-extra >= 0.4.0,<1.0.0",
    ]
    ```

=== "Pipfile"

    ```diff
    [packages]
    ...
    + invenio-pidstore-extra = ">=0.4.0,<1.0.0"
    ```


And next:

=== "uv"

    ```shell
    rm -f uv.lock
    invenio-cli install
    ```

=== "pip"

    ```shell
    rm -f Pipfile.lock
    invenio-cli install
    ```

## Configure the DNB URN PID provider(s)

!!! tip "DNB sandbox replacement"

    The flask app invenio_pidstore_extra.dnb-sandbox.py contains a very simple implementation of the DNB api to allow testing the URN support when the DNB sandbox is not available or just no user has been provided. You can start it with calling `flask --app invenio_pidstore_extra.dnb-sandbox run --port=8000`.

After adding the module to your InvenioRDM instance you need to add the following snippet to your `invenio.cfg`.
Make sure you have registered at the DNB and set the config variables below to the correct values!
When putting this to production, set `PIDSTORE_EXTRA_TEST_MODE = False`!

```diff
+   PIDSTORE_EXTRA_DNB_SANDBOX_URI = "http://127.0.0.1:8000/"

+   PIDSTORE_EXTRA_DNB_ENABLED = True
+   PIDSTORE_EXTRA_FORMAT = "{prefix}-{id}"
+   PIDSTORE_EXTRA_TEST_MODE = True

+   PIDSTORE_EXTRA_URN_PASSWORD_1 = "password"
+   PIDSTORE_EXTRA_URN_PASSWORD_2 = "password"

+   PIDSTORE_EXTRA_DNB_CONFIG = {
+       "urn:nbn:de:hbz:6": {
+           "pidstore_extra_dnb_username": "dnb-user1",
+           "pidstore_extra_dnb_password": PIDSTORE_EXTRA_URN_PASSWORD_1,
+           "pidstore_extra_dnb_id_prefix": "urn:nbn:de:hbz:6",
+           "pidstore_extra_dnb_default": True,
+       },
+       "urn:nbn:de:hbz:6:4": {
+           "pidstore_extra_dnb_username": "dnb-user2",
+           "pidstore_extra_dnb_password": PIDSTORE_EXTRA_URN_PASSWORD_2,
+           "pidstore_extra_dnb_id_prefix": "urn:nbn:de:hbz:6:4",
+           "pidstore_extra_dnb_default": False,
+       },
+   }

#
# Persistent identifiers configuration
#
+   from invenio_rdm_records.config import RDM_PERSISTENT_IDENTIFIER_PROVIDERS as DEFAULT_PERSISTENT_IDENTIFIER_PROVIDERS
+   from invenio_pidstore_extra import providers

+   RDM_PERSISTENT_IDENTIFIER_PROVIDERS = DEFAULT_PERSISTENT_IDENTIFIER_PROVIDERS + [
+       providers.DnbUrnProvider(
+         "urn",
+         client=providers.DNBUrnClient("dnb", PIDSTORE_EXTRA_DNB_CONFIG,
+                                       PIDSTORE_EXTRA_FORMAT),
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

If you want to add support for separate prefixes for separate communities, you need to define a custom field 
on the community. 
You will have to configure the URN prefix in the community administration, then the provider that is configured
for the URN's prefix will automatically hook in and mint the URN.

```diff
+   from invenio_records_resources.services.custom_fields import TextCF

+   COMMUNITIES_CUSTOM_FIELDS = [
+       TextCF(name="urn_prefix")
+   ]

+   COMMUNITIES_CUSTOM_FIELDS_UI = [
+       {
+           "section": _("URN customisation"),
+           "fields": [
+               dict(
+                   field="urn_prefix",
+                   ui_widget="Input",
+                   props=dict(
+                       label="URN Präfix",
+                       placeholder="urn:nbn:de:hbz:6",
+                       icon="pencil",
+                       description="Der URN-Präfix, der für diese Community verwendet werden soll.",
+                   )
+               ),
+           ]
+       }
+   ]

```

The URN PID provider is configured to automatically generate and mint the URN: there is actually no support
for URNs in the upload form UI.
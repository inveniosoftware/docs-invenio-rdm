# DNB URNs registration

*Available since InvenioRDM v11*

!!! info

    The URN registration feature requires that you have a contract with the [German National Library](https://wiki.dnb.de/display/URNSERVDOK/URN-Service+API). You will need to contact urn-support@dnb.de to get an account for the sandbox and the production REST-API.

In order to register URN's with InvenioRDM, you need to two extra modules:

- [dnb-urn-service](https://pypi.org/project/dnb-urn-service/)
- [invenio-dnb-urn](https://pypi.org/project/invenio-dnb-urn/)

If you're interested in the source code, you will find it here:

- [dnb-urn-service](https://github.com/ulbmuenster/dnb-urn-service)
- [invenio-dnb-urn](https://github.com/ulbmuenster/invenio-dnb-urn)

The first one implements a thin wrapper around the Rest-API maintained by the DNB (German national library),
the second enhances the InvenioRDM with URN minting support and xMetaDissPlus serialization via OAI-PMH 2.0.

Adding the `invenio-dnb-urn` module in the list of dependencies is enough: `dnb-urn-service` will be automatically installed.
In your Pipfile:

```diff
[packages]
...
+ invenio-dnb-urn = ">=0.1.3,<1.0.0"
```

You will have to lock again your Pipfile:

- delete Pipfile.lock
- run `invenio-cli install`

## URN PID provider

The DNB URN Rest-API offers a production service and a sandbox service. The `dnb-urn-service` wrapper
automatically chooses the correct URL depending on the configuration variable `URN_DNB_TEST_MODE`.

Add the following to your `invenio.cfg`:

```diff
+ URN_DNB_ENABLED = True
+ URN_DNB_USERNAME = "username"
+ URN_DNB_PASSWORD = "password"
+ URN_DNB_ID_PREFIX = "urn:nbn:de:hbz:6"
+ URN_DNB_TEST_MODE = True

#
# Persistent identifiers configuration
#
RDM_PERSISTENT_IDENTIFIER_PROVIDERS = [
  ...
+   # URN identifier
+   providers.DnbUrnProvider(
+     "urn",
+     client=providers.DNBUrnClient("dnb"),
+     label=_("URN"),
+   ),
]

RDM_PERSISTENT_IDENTIFIERS = {
  ...
+   "urn": {
+     "providers": ["urn"],
+     "required": True,
+     "label": _("URN"),
+     "is_enabled": providers.DnbUrnProvider.is_enabled,
+   },
  ...
}
```

The URN PID provider is configured to automatically generate and mint the URN: there is no support
for URNs in the upload form UI.

## xMetaDissPlus export

The DNB offers harvesting metadata and data for long time preservation. You can configure it by adding
the `xMetaDissPlus` export the InvenioRDM OAI-PMH 2.0 server.
To add the export format to your instance add the following sequence to your `invenio.cfg`:

```diff
OAISERVER_METADATA_FORMATS = {
  ...
+  "xMetaDiss": {
+    "serializer": "invenio_dnb_urn.oai:xmetadiss_etree",
+    "schema": "http://www.d-nb.de/standards/xmetadissplus/xmetadissplus.xsd",
+    "namespace": "http://www.d-nb.de/standards/xmetadissplus/"
+  },
  ...
}
```

The xMetaDissPlus format makes use of the OpenAIRE resource types. If you don't use the default resource
types provided by InvenioRDM you will have to change the following settings accordingly:

```python
XMETADISS_TYPE_DINI_PUBLTYPE = "openaire_type"
XMETADISS_TYPE_DCTERMS_DCMITYPE = "openaire_type"
```

In order to fully implement xMetaDissPlus with all mandatory fields, the metadata definition has to be expanded by [custom
fields](../../develop/howtos/custom_fields.md).
At first add the file `thesis_types.yaml` to `/app_data/vocabularies` (you will find the content [here](https://raw.githubusercontent.com/ulbmuenster/invenio-dnb-urn/main/thesis_types.yaml)):

```yaml
- id: "thesis.doctoral"
  title:
    en: "PhD thesis"
    de: "Dissertation"
- id: "thesis.habilitation"
  title:
    en: "Habilitation treatise"
    de: "Habilitationsschrift"
- id: "bachelor"
  title:
    en: "Bachelor's thesis"
    de: "Bachelorarbeit"
- id: "master"
  title:
    en: "Master's thesis"
    de: "Masterarbeit"
- id: "Staatsexamen"
  title:
    en: "State examination"
    de: "Staatsexamen"
- id: "M.A."
  title:
    en: "Graduate degree"
    de: "Magisterarbeit"
- id: "Diplom"
  title:
    en: "Diploma thesis"
    de: "Diplomarbeit"            
```

Then change the `vocabularies.yaml`:

```yaml
thesis:
  pid-type: ths
  data-file: vocabularies/thesis_types.yaml
```

Next, change your `invenio.cfg`:

```python
from invenio_records_resources.services.custom_fields import TextCF
from invenio_vocabularies.services.custom_fields import VocabularyCF

RDM_NAMESPACES = {
  # DNB Thesis
  "thesis": "https://dnb.de/thesis/",
}

RDM_CUSTOM_FIELDS = {
  VocabularyCF(
    name="thesis:level",
    vocabulary_id="thesis",
    dump_options=True,
    multiple=False,
  ),
  TextCF(
    name="thesis:organisation",
  ),
  TextCF(
    name="thesis:place",
  ),
}

RDM_CUSTOM_FIELDS_UI = [
  {
    "section": _("Hochschulschriftenvermerk"),
    "fields": [
      dict(
        field="thesis:level",
        ui_widget="Dropdown",
        props=dict(
          label="Abschluss",
          placeholder="Grad des Abschlusses",
          icon="pencil",
          description="You should fill this field with the thesis degree",
          search=True,  # True for autocomplete dropdowns with search functionality
          multiple=False,   # True for selecting multiple values
          clearable=True,
          required=False,
        )
      ),
      dict(
        field="thesis:organisation",
        ui_widget="Input",
        props=dict(
          label="Hochschule",
          placeholder="Verleihende Hochschule",
          icon="pencil",
          description="You should fill this field with the institution that awards the degree",
          required=False,
        )
      ),
      dict(
        field="thesis:place",
        ui_widget="Input",
        props=dict(
          label="Ort",
          placeholder="Ort",
          icon="pencil",
          description="Place of the university/institution.",
          required=False,
        )
      ),
    ]
  }
]
```

Init the new custom fields:

```shell
pipenv run invenio rdm-records custom-fields init
```

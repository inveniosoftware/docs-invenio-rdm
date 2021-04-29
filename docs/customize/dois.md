# DOI Registration

InvenioRDM support minting of DOIs provided by DataCite. You can enable this feature in the `invenio.cfg` file:

```cfg
RDM_RECORDS_DOI_DATACITE_ENABLED = False
```

Doing this will generate DOIs but only create/register them in the local instance (DB), they will not be registed in DataCite.
For that, you will need to set credentials for DataCite. You can set them in the same way:

```cfg
RDM_RECORDS_DOI_DATACITE_USERNAME = "<YOUR.USERNAME>"
RDM_RECORDS_DOI_DATACITE_PASSWORD = "<YouR_P4ssW0rd"
RDM_RECORDS_DOI_DATACITE_PREFIX = "10.1234"  # Your prefix
```

And finally you can choose if you want to register in DataCite test or production site:

```cfg
RDM_RECORDS_DOI_DATACITE_TEST_MODE = True
```

These variables are already available at the bottom of the `invenio.cfg` file, you simply need to change its values.

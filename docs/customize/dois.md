# DOI registration

!!! info

    The DOI registration feature requires that you have a contract with [DataCite](https://datacite.org/feemodel.html). In addition, you will also need a [DataCite test account](https://support.datacite.org/docs/getting-a-test-account) to test the feature.

## Configure

#### Enable DOI registration

You enable the DOI minting feature in your ``invenio.cfg`` file:

```cfg
DATACITE_ENABLED = True
```

#### Credentials and prefix

Before you continue, make sure you first have a [DataCite test account](https://support.datacite.org/docs/getting-a-test-account).

You need to provide the account credentials and and the DOI prefix for the DataCite repository account in your  in ``invenio.cfg`` file:

```cfg
DATACITE_USERNAME = "..." # Your username
DATACITE_PASSWORD = "..."  # Your password
DATACITE_PREFIX = "10.1234"  # Your prefix
```

!!! tip

    Never commit or store credentials in a source code repository.

#### Mode: Test or production

InvenioRDM by default uses the [DataCite Test Environment](https://support.datacite.org/docs/testing-guide) to avoid accidentally
registering DOIs during test. In test mode InvenioRDM will use the following DatCite test systems:

- DOI Fabrica (https://doi.test.datacite.org).
- REST API (https://api.test.datacite.org).

To enable production mode, set the following configuration variable in ``invenio.cfg``:

```cfg
DATACITE_TEST_MODE = False
```

In production mode, InvenioRDM will use the following DataCite systems:

- DOI Fabrica (https://doi.datacite.org).
- REST API (https://api.datacite.org).


!!! tip "Did you know?"

    You can write your own persistent identifier plugin in InvenioRDM to support other types of persistent identifiers.

#### Generated DOI

By default, InvenioRDM generates a DOI using the prefix and internal persistent
identifier. You can change the generated DOI string by editing your ``invenio.cfg``.

```
DATACITE_FORMAT = "{prefix}/inveniordm.{id}"
```

!!! tip

    Before branding your DOIs, please read about
    [Cool DOIs](https://doi.org/10.5438/55e5-t5c0) and why it might not be a
    good idea.


## Known issues

- **Restricted records:** DOIs are registered for all records including restricted
  records, thus metadata like titles, authors, description and more is sent to
  DataCite Metadata registry where it is public. Provide an external DOI if
  no DOI should be registered by InvenioRDM.

# DOI registration

!!! info

    The DOI registration feature requires that you have a contract with [DataCite](https://datacite.org/feemodel.html). In addition, you will also need a [DataCite test account](https://support.datacite.org/docs/getting-a-test-account) to test the feature.

## Configure

#### Enable DOI registration

You enable the DOI minting feature in your ``invenio.cfg`` file:

```python
DATACITE_ENABLED = True
```

#### Credentials and prefix

Before you continue, make sure you first have a [DataCite test account](https://support.datacite.org/docs/getting-a-test-account).

You need to provide the account credentials and the DOI prefix for the DataCite repository account in your ``invenio.cfg`` file:

```python
DATACITE_USERNAME = "..." # Your username
DATACITE_PASSWORD = "..."  # Your password
DATACITE_PREFIX = "10.1234"  # Your prefix
```

!!! tip

    Never commit or store credentials in a source code repository.

#### Mode: Test or production

InvenioRDM by default uses the [DataCite Test Environment](https://support.datacite.org/docs/testing-guide) to avoid accidentally
registering DOIs during test. In test mode InvenioRDM will use the following DataCite test systems:

- DOI Fabrica (https://doi.test.datacite.org).
- REST API (https://api.test.datacite.org).

To enable production mode, set the following configuration variable in ``invenio.cfg``:

```python
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

```python
DATACITE_FORMAT = "{prefix}/inveniordm.{id}"
```

!!! tip

    Before branding your DOIs, please read about
    [Cool DOIs](https://doi.org/10.5438/55e5-t5c0) and why it might not be a
    good idea.

#### Parent or Concept DOIs

_Introduced in v12_

By default InvenioRDM will create two DOIs when an initial record is
published, and create one DOI each time a new version of the record is
published. The first DOI is the version DOI, which represents the specific
record that is published. The second DOI is the parent DOI, which represents
the concept of the record and will always resolve to the latest version.
This feature has been implemented in Zenodo for many years, and the concept DOI enables
researchers to cite something that won't change when they make changes to their
records.

![Concept DOI help-text](./imgs/concept_doi.png)

The parent DOI is optional and can be disabled by setting the following in
invenio.cfg:

```python
RDM_PARENT_PERSISTENT_IDENTIFIERS={}
```

#### OAI-PMH

The OAI-PMH server's metadata format ``oai_datacite`` that allows you to harvest record from InvenioRDM in DataCite XML needs to be configured with your DataCite data center symbol. This is only required if you want your records to be harvestable in DataCite XML format.

```python
DATACITE_DATACENTER_SYMBOL = "CERN.INVENIORDM"
```

### Versioning and externally managed DOI

By default, InvenioRDM allows versioning for any DOI type - internally or externally managed. Internally managed DOI is a DOI which is given thanks to InvenioRDM feature which allows us to configure the DOI registration on DataCite (check #Enable DOI registration). The external DOIs are not minted by our instance and in some cases repository manager decides to disallow versioning of records identified by external DOI. To disable versioning for external DOIs you need to set:

```python
RDM_ALLOW_EXTERNAL_DOI_VERSIONING = False
```

### Configuring DOI behavior

You can change how DOIs work in InvenioRDM by adding to your `invenio.cfg`:

```python
RDM_PERSISTENT_IDENTIFIERS = {
    # DOI automatically removed if DATACITE_ENABLED is False.
    "doi": {
        "providers": ["datacite", "external"],
        "required": False,
        "label": _("DOI"),
        "validator": idutils.is_doi,
        "normalizer": idutils.normalize_doi,
        "is_enabled": providers.DataCitePIDProvider.is_enabled,
    },
    "oai": {
        "providers": ["oai"],
        "required": True,
        "label": _("OAI"),
        "is_enabled": providers.OAIPIDProvider.is_enabled,
    },
}
```
You [can view the default configuration in invenio-rdm-records](https://github.com/inveniosoftware/invenio-rdm-records/blob/e64dd0b81757a391584e63d162d5e6caf6780637/invenio_rdm_records/config.py#L322)

### DOIs on demand

_Introduced in v13_

You can configure InvenioRDM to allow users to choose whether or not to register a DOI when uploading a record.

![DOIs on demand](imgs/dois-on-demand.jpg)

To enable this feature, configure the following in your `invenio.cfg`:

```python
### Do not require DOIs for record and parent
RDM_PERSISTENT_IDENTIFIERS["doi"]["required"] = False
RDM_PARENT_PERSISTENT_IDENTIFIERS["doi"]["required"] = False
RDM_PERSISTENT_IDENTIFIERS["doi"]["ui"]["default_selected"] = "not_needed"  # "yes", "no" or "not_needed"
```

With this option enabled, users can decide whether or not to request a DOI for their record. However, managing different versions of a record with and without DOIs can introduce complexities. Ideally, once a DOI is registered for a record, all subsequent versions should also have a DOI to avoid resolving to a version with a DOI, and creating confusion.

The default behavior in InvenioRDM enforces this principle. Nevertheless, you can customize the behavior in two ways.

**1. Basic**

Provide your rules between records' versions by setting the config variable `INVENIO_OPTIONAL_DOI_TRANSITIONS`. The rules are evaluated each time a draft is saved, or on publish. This config expect rules defined in the format *from*/*to* states: given the DOI state in the previous record's version (*from*), it defines what are the allowed states for the current draft (*to*).

```
{
    <from>: {
        "allowed_providers": [<to>, <to>, ...],
        "message": invalid state msg
    }

}
```

*from*/*to* possible values:

    - `datacite` (or other provider): in the current draft, the user selected to register a DOI with the provider. The provider name must be configured in the DOI configuration above in this documentation.
    - `external`: in the current draft, the user selected an external DOI.
    - `not_needed`: in the current draft, the user selected that a DOI is not needed.

As an example, in your `invenio.cfg`, you can define that when the previous record version has a DOI registered with DataCite, then the current draft must have the same. The user cannot input an external DOI or select that it is not needed.

```python
OPTIONAL_DOI_TRANSITIONS = {
    "datacite": {
        "allowed_providers": ["datacite"],
        "message": "<error message if the user selected a DOI option that is not in the allowed_providers field above>",
    },
    ...
}
```

**2. Advanced**

Assign your custom function to `RDM_OPTIONAL_DOI_VALIDATOR = my_function`. The custom function will be called on each save or publish of a draft.

```python
def validate_optional_doi(draft, previous_published_record, errors=None, transitions_config=None):
    ...
```

You can find an example [here](https://github.com/CERNDocumentServer/cds-rdm/blob/4d7400111dd29d6d38f29534c5044d0b57f0bd20/site/cds_rdm/pids.py#L15) on how to develop a custom validation.

## Limitations

- **Restricted records:** Once a DOI is created, it cannot be fully removed from DataCite. Starting with v12, InvenioRDM will not register DOIs for restricted records. It will also hide a DOI from the DataCite Search if a record is changed from public to restricted. However that DOI will still resolve and metadata may be available to DataCite members.

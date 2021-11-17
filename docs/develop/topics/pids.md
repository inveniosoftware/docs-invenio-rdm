# Persistent identifiers for records

**Intended audience**

This guide is intended for developers that needs to develop new features for
their own InvenioRDM instance.

## Overview

InvenioRDM comes out-of-the-box with support for for user-provided DOIs,
registering DataCite DOIs and OAI-PMH IDs.

- Scheme
- Providers
- Clients


## Configuration

```
RDM_PERSISTENT_IDENTIFIER_PROVIDERS = [
    # DataCite DOI provider
    providers.DataCitePIDProvider(
        "datacite",
        client=providers.DataCiteClient("datacite", config_prefix="DATACITE"),
        label=_("DOI"),
    ),
    # DOI provider for externally managed DOIs
    providers.ExternalPIDProvider(
        "external",
        "doi",
        validators=[
            providers.BlockedPrefixes(config_names=['DATACITE_PREFIX'])
        ],
        label=_("DOI"),
    ),
    # OAI identifier
    providers.OAIPIDProvider("oai", label=_("OAI ID"),),
]
```

```
RDM_PERSISTENT_IDENTIFIERS = {
    # DOI automatically removed if DATACITE_ENABLED is False.
    "doi": {
        "providers": ["datacite", "external"],
        "required": True,
        "label": _("DOI"),
        "validator": idutils.is_doi,
        "normalizer": idutils.normalize_doi,
    },
    "oai": {
        "providers": ["oai"],
        "required": True,
        "label": _("OAI"),
    },
}
```

### Data flow



### Writing a client for an existing provider




### Writing a new provider

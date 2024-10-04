# Metadata reference

**Summary**

The following document is a reference guide for the internal metadata schema of bibliographic records in InvenioRDM.

**Intended audience**

This guide is intended for advanced users, administrators and developers of InvenioRDM with significant prior experience.

## Overview

InvenioRDM's bibliographic records are stored as JSON documents in a structure
that is aligned with DataCite's Metadata Schema v4.x with minor additions
and modifications.

!!! info "Datacite references"

    This document refers to Datacite schema properties for the reader's convenience (e.g., "*2. Creator* in DataCite"). The corresponding Datacite document can be found under <https://schema.datacite.org/>. The currently supported version is [v4.3](https://schema.datacite.org/meta/kernel-4.3).

**Schema version**

All records contain a schema definition in the top-level key ``$schema``. The value
is a link to the internal JSONSchema which is being used to validate the structure of the record.
This field is fully system-managed.

```json
{
    "$schema": "local://records/record-v2.0.0.json",
    ...
}
```

**Top-level fields**

Following is an overview of the top-level fields in a record:

|     Field      | Description                                                                          |
|:--------------:|:-------------------------------------------------------------------------------------|
| ``id``/``pid`` | The internal persistent identifier for a specific version.                           |
|   ``parent``   | The internal persistent identifier for all versions.                                 |
|    ``pids``    | System-managed external persistent identifiers (DOIs, Handles, OAI-PMH identifiers). |
|   ``access``   | Access control information.                                                          |
|  ``metadata``  | Descriptive metadata for the resource.                                               |
|   ``files``    | Associated files information.                                                        |
| ``tombstone``  | Tombstone information.                                                               |

Each of these keys will be explained below. Following is an example of how the
top-level fields in a record look like:

```json
{
    "$schema": "local://records/record-v1.0.0.json",
    "id": "q5jr8-hny72",
    "pid": { ... },
    "pids" : { ... },
    "parent": { ... },
    "access" : { ... },
    "metadata" : { ... },
    "files" : { ... },
    "tombstone" : { ... },
}
```

**Database-level fields**

In addition to the JSON document, the following fields are also stored for each
record in the database table:

- Creation timestamp (UTC).
- Modification timestamp (UTC).

When querying for a record, they are shown as `created` and `updated` in the top level of the record JSON.

## System-managed persistent identifiers

A key part of InvenioRDM is the management of persistent identifiers for records.
A record always has an internal PID.

### Internal PIDs

A record stores information about two internal PIDs:

Specific version PID:

|  Field  | Description                                                                   |
|:-------:|:------------------------------------------------------------------------------|
| ``id``  | The value of the internal record identifier.                                  |
| ``pid`` | Object level information about the identifier needed for operational reasons. |

Concept version PID:

|     Field     | Description                                 |
|:-------------:|:--------------------------------------------|
| ``parent.id`` | The value of the concept record identifier. |

Example:

```json
{
  "id": "abcde-12345",
  "pid": {
    "pk": 1,
    "status": "R"
  },
  "parent": {
    "id": "hg5de-2dw08"
  },
}
```

See [Parent](#parent) for details on the `parent` field.

### External PIDs

External PIDs are persistent identifiers managed via [Invenio-PIDStore](https://invenio-pidstore.readthedocs.io) that may require integration
with external registration services.

Persistent identifiers are globally unique in the system, thus you cannot have two records
with the same system-managed persistent identifier (see also [Metadata > Identifiers](#alternate-identifiers-0-n)).

You can add a DOI that is not managed by InvenioRDM by using the provider `external`. You are not able to add `external` DOIs that have a prefix that is configured as part of a different PID provider.

Only one identifier can be registered per system-defined scheme. Each identifier has the following subfields:

|     Field      | Cardinality | Description                                                                      |
|:--------------:|:-----------:|:---------------------------------------------------------------------------------|
| ``identifier`` |     (1)     | The identifier value.                                                            |
|  ``provider``  |     (1)     | The provider identifier used internally by the system.                           |
|   ``client``   |    (0-1)    | The client identifier used for connecting with an external registration service. |

```json
{
  "pids": {
    "doi": {
      "identifier": "10.1234/rdm.5678",
      "provider": "datacite",
      "client": "datacite"
    },
    "concept-doi": {
      "identifier": "10.1234/rdm.5678",
      "provider": "datacite",
      "client": "datacite"
    }
  }
}
```

Other system-managed identifiers will also be recorded here such as the OAI id.

## Parent

Information related to the record as a concept is recorded under the top-level ``parent`` key. Every record has a ``parent`` and that parent connects all versions of a record together. The goal here is to connect these records and store shared information - ownership for now.

Subfields:

|   Field    | Cardinality | Description                               |
|:----------:|:-----------:|:------------------------------------------|
|   ``id``   |     (1)     | The identifier of the parent record.      |
| ``access`` |     (1)     | Access details for the record as a whole. |

The ``access`` is described with the following subfields:

|    Field     | Cardinality | Description         |
|:------------:|:-----------:|:--------------------|
| ``owned_by`` |    (1)    | A single owner. (*WARNING: This was changed in v12. It used to be an array.*)|

Owners are defined as:

|  Field   | Cardinality | Description                                      |
|:--------:|:-----------:|:-------------------------------------------------|
| ``user`` |     (1)     | The id of the user owning the record as a whole. |


Example:

```json
{
  "parent": {
    "id": "fghij-12345",
    "access": {
      "owned_by": {
        "user": 2
      }
    }
  },
}
```

## Access

The `access` field denotes record-specific read (visibility) options.

The `access` field has this structure:

|   Field   | Cardinality | Description                                                      |
|:---------:|:-----------:|:-----------------------------------------------------------------|
| `record`  |     (1)     | `"public"` or `"restricted"`. Read access to the record.         |
|  `files`  |     (1)     | `"public"` or `"restricted"`. Read access to the record's files. |
| `embargo` |    (0-1)    | Embargo options for the record.                                  |

`"public"` means anyone can see the record/files. `"restricted"` means only the owner(s) or
specific users can see the record/files. Only in the cases of `"record": "restricted"` or
`"files": "restricted"` can an embargo be provided as input. However, once an embargo is
lifted, the `embargo` section is kept for transparency.

### Embargo

The `embargo` field denotes when an embargo must be lifted, at which point the record
is made publicly accessible. The `embargo` field has this structure:

|  Field   | Cardinality | Description                                                                                |
|:--------:|:-----------:|:-------------------------------------------------------------------------------------------|
| `active` |     (1)     | boolean. Is the record under embargo or not.                                               |
| `until`  |    (0-1)    | Required if `active` true. ISO date string. When to lift the embargo. e.g., `"2100-10-01"` |
| `reason` |    (0-1)    | string. Explanation for the embargo.                                                       |

Example:

```json
{
  "access": {
    "record": "public",
    "files": "public",
    "embargo": {
      "active": false
    }
  },
}
```

The `access` field will default to `"public"` for both `record` and `files` fields if not
provided to the REST API.

## Metadata

The fields are listed below in the combined order of "required" and "appearance on the deposit page". So required fields are listed first and then other fields are listed in the order of their appearance on the deposit page.

The cardinality of each field is expressed in between parenthesis on the title of each field's section.
Cardinality here indicates if the field is required by the REST API.

The abbreviation `CV` stands for *Controlled Vocabulary*.

### Resource type (1)

The type of the resource described by the record. The resource type must be selected from a controlled vocabulary which can be customized by each InvenioRDM instance.

When interfacing with Datacite, this field is converted to a format compatible with *10. Resource Type*  (i.e. ``type`` and ``subtype``). DataCite allows free text for the subtype, however InvenioRDM requires this to come from a customizable controlled vocabulary.

The resource type vocabulary also defines mappings to other vocabularies than Datacite such as Schema.org, Citation Style Language, BibTeX, and OpenAIRE. These mappings are very important for the correct generation of citations due to how different types are being interpreted by reference management systems.

Subfields:

| Field  | Cardinality | Description                                          |
|:------:|:-----------:|:-----------------------------------------------------|
| ``id`` |   (1, CV)   | The resource type id from the controlled vocabulary. |

Example:

```json
{
  "resource_type": {
    "id": "image-photo"
  },
}
```

Note that only the subtype (which is more specific) is displayed if it exists.

### Creators (1-n)

The creators field registers those persons or organisations that should be credited for the resource described by the record. The list of persons or organisations in the creators field is used for generating citations, while the persons or organisations listed in the contributors field are not included in the generated citations.

The field is compatible with *2. Creator* in DataCite. In addition we are adding the possibility of associating a role (like for contributors). This is specifically for cases where e.g. an editor needs to be credited for the work, while authors of individual articles will be listed under contributors.

Subfields:

|       Field       | Cardinality | Description                                                                                |
|:-----------------:|:-----------:|:-------------------------------------------------------------------------------------------|
| ``person_or_org`` |     (1)     | The person or organization.                                                                |
|     ``role``      |  (0-1, CV)  | The role of the person or organisation selected from a customizable controlled vocabulary. |
| ``affiliations``  |    (0-n)    | Affilations if ``person_or_org.type`` is ``personal``.                                     |

A `person_or_org` is described with the following subfields:

|      Field      |                          Cardinality                          | Description                                                                                                  |
|:---------------:|:-------------------------------------------------------------:|:-------------------------------------------------------------------------------------------------------------|
|    ``type``     |                              (1)                              | The type of name. Either ``personal`` or ``organizational``.                                                 |
| ``given_name``  | (1 if `type` is `personal` / 0 if `type` is `organizational`) | Given name(s).                                                                                               |
| ``family_name`` | (1 if `type` is `personal` / 0 if `type` is `organizational`) | Family name.                                                                                                 |
|    ``name``     | (0 if `type` is `personal` / 1 if `type` is `organizational`) | The full name of the organisation. For a person, this field is generated from `given_name` and `family_name` |
| ``identifiers`` |                             (0-n)                             | Person or organisation identifiers.                                                                          |

Identifiers are described with the following subfields (note, we only support one identifier per scheme):

|      Term      | Cardinality | Description                     |
|:--------------:|:-----------:|:--------------------------------|
|   ``scheme``   |   (1, CV)   | The identifier scheme.          |
| ``identifier`` |     (1)     | Actual value of the identifier. |

Supported creator identifier schemes:

- [ORCID][]
- [GND][]
- [ISNI][]
- [ROR][]

Supported affiliation identifier schemes:

- [ISNI][]
- [ROR][]


[ORCID]: https://orcid.org/
[GND]: https://www.dnb.de/EN/gnd
[ISNI]: https://isni.org/
[ROR]: https://ror.org/

Note that the identifiers' schemes are passed lowercased e.g. ORCID is ``orcid``.


The ``affiliations`` field consists of objects with the following subfields:

|  Field   | Cardinality | Description                                                            |
|:--------:|:-----------:|:-----------------------------------------------------------------------|
|  ``id``  |  (0-1, CV)  | The organizational or institutional id from the controlled vocabulary. |
| ``name`` |    (0-1)    | The name of the organisation or institution.                           |

One of ``id`` or ``name`` must be given. It's recommended to use ``name`` if there is no matching ``id`` in the controlled vocabulary.


The `role` field is as follows:

| Field  | Cardinality | Description                                  |
|:------:|:-----------:|:---------------------------------------------|
| ``id`` |   (1, CV)   | The role's controlled vocabulary identifier. |

Example:

```json
{
  "creators": [{
    "person_or_org": {
      "name": "Nielsen, Lars Holm",
      "type": "personal",
      "given_name": "Lars Holm",
      "family_name": "Nielsen",
      "identifiers": [{
        "scheme": "orcid",
        "identifier": "0000-0001-8135-3489"
      }],
    },
    "affiliations": [{
      "id": "01ggx4157",
      "name": "CERN",
    }]
  }],
}
```

### Title (1)

A primary name or primary title by which a resource is known. May be the title of a dataset or the name of a piece of software. The primary title is used for display purposes throughout InvenioRDM.

The field is compatible with *3. Title* in DataCite. Compared to DataCite, the field does not support specifying the language of the title.

Example:

```json
{
  "title": "InvenioRDM",
}
```

### Publication date (1)

The date when the resource was or will be made publicly available.

The field is compatible *5. PublicationYear* in DataCite. In case of time intervals, the earliest date is used for DataCite.

Format:

The string must be formatted according to [Extended Date Time Format (EDTF)](http://loc.gov/standards/datetime/) Level 0. Only *"Date"* and *"Date Interval"* are supported. *"Date and Time"* is not supported. The following are examples of valid values:

- Date:
    - ``2020-11-10`` - a complete ISO8601 date.
    - ``2020-11`` - a date with month precision
    - ``2020`` - a date with year precision
- Date Interval:
    - ``1939/1945`` a date interval with year precision, beginning sometime in 1939 and ending sometime in 1945.
    - ``1939-09-01/1945-09`` a date interval with day and month precision, beginning September 1st, 1939 and ending sometime in September 1945.

The localization (L10N) of EDTF dates is based on the [skeletons](http://cldr.unicode.org/translation/date-time-1/date-time-patterns) defined by the [Unicode Common Locale Data Repository (CLDR)](http://cldr.unicode.org).


Example:

```json
{
  "publication_date": "2018/2020-09",
}
```

### Additional titles (0-n)

Additional names or titles by which a resource is known.

The field is compatible with *3. Title* in DataCite. Compared to DataCite, InvenioRDM splits *3. Title* into two separate fields ``title`` and ``additional_titles``. This is to ensure consistent usage of a record's title throughout the entire software stack for display purposes.

Subfields:

| Field     | Cardinality |   Description              |
|:---------:|:-----------:|:---------------------------|
| ``title`` | (1)         | The additional title.      |
| ``type``  | (1)         | The type of the title.     |
| ``lang``  | (0-1, CV)   | The language of the title. |

The ``type`` field is as follows:

|   Field   | Cardinality | Description                                                                                                                             |
|:---------:|:-----------:|:----------------------------------------------------------------------------------------------------------------------------------------|
|  ``id``   |   (1, CV)   | Title type id from the controlled vocabulary. By default one of: ``alternative-title``, ``subtitle`` ``translated-title`` or ``other``. |
| ``title`` |     (1)     | The corresponding localized human readable label. e.g. ``{"en": "Alternative title"}``                                                  |

Note that multiple localized titles are supported e.g. ``{"en": "Alternative title", "fr": "Titre alternatif"}``. Use ISO 639-1 codes (2 letter locales) as keys.
Only ``id`` needs to be passed on the REST API.

The `lang` field is as follows:

| Field  | Cardinality |   Description                |
|:------:|:-----------:|:-----------------------------|
| ``id`` | (1, CV)     | The ISO-639-3 language code. |

Example:

```json
{
  "additional_titles": [{
    "title": "A research data management platform",
    "type": {
      "id": "alternative-title",
      "title": {
        "en": "Alternative Title"
      }
    },
    "lang": {"id": "eng"}
  }]
}
```

### Description (0-1)

The description of a record.

The field is compatible with *17. Description* in DataCite. Compared to DataCite the field does not support specifying the language of the description.

The description may use a whitelist of HTML tags and attributes to style the text.

Example:

```json
{
  "description": "<strong>Test</strong>"
}
```

### Additional descriptions (0-n)

Additional descriptions in addition to the primary description (e.g. abstracts in other
languages), methods or further notes.

The field is compatible with *17. Description* in DataCite.

Subfields:

| Field            | Cardinality |   Description                    |
|:----------------:|:-----------:|:---------------------------------|
| ``description``  | (1)         | Free text.                       |
| ``type``         | (1)         | The type of the description.     |
| ``lang``         | (0-1)       | The language of the description. |

The ``type`` field is as follows:

|   Field   | Cardinality | Description                                                                                                                                                                     |
|:---------:|:-----------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|  ``id``   |   (1, CV)   | Description type id from the controlled vocabulary. By default one of: ``abstract``, ``methods``, ``series-information``, ``table-of-contents``, ``technical-info``, ``other``. |
| ``title`` |     (1)     | The corresponding localized human readable label. e.g. ``{"en": "Abstract"}``                                                                                                   |

Note that multiple localized titles are supported e.g. ``{"en": "Table of contents", "fr": "Table des matières"}``. Use ISO 639-1 codes (2 letter locales) as keys.
Only ``id`` needs to be passed on the REST API.

The `lang` field is as follows:

| Field  | Cardinality |   Description                |
|:------:|:-----------:|:-----------------------------|
| ``id`` | (1, CV)     | The ISO-639-3 language code. |

Example:

```json
{
  "additional_descriptions": [{
    "description": "The description of a research data management platform.",
    "type": {
      "id": "methods",
      "title": {
        "en": "Methods"
      }
    },
    "lang": {"id": "eng"}
  }]
}
```

### Rights (Licenses) (0-n)

Rights management statement for the resource.

When interfacing with Datacite, this field is converted to be compatible with *16. Rights*.

The rights field is intended to primarily be linked to a customizable vocabulary
of licenses (defaults [SPDX](https://spdx.org/licenses/)). It should however also be possible to provide
custom rights statements.

The rights statements does not have any impact on access control to the resource.

Subfields:

|      Field      | Cardinality | Description                                                                       |
|:---------------:|:-----------:|:----------------------------------------------------------------------------------|
|     ``id``      |    (0-1)    | Identifier value                                                                  |
|    ``title``    |    (0-1)    | Localized human readable title e.g., ``{"en": "The ACME Corporation License."}``. |
| ``description`` |    (0-1)    | Localized license description text e.g., ``{"en": "This license..."}``.           |
|    ``link``     |    (0-1)    | Link to full license.                                                             |

REST API:

Either ``id`` or ``title`` must be passed, but not both.

Example:

```json
{
  "rights": [{
    "id": "cc-by-4.0",
    "title": {"en": "Creative Commons Attribution 4.0 International"},
    "description": {"en": "The Creative Commons Attribution license allows re-distribution and re-use of a licensed work on the condition that the creator is appropriately credited."},
    "link": "https://creativecommons.org/licenses/by/4.0/"
  }],
}
```

### Contributors (0-n)

The organisations or persons responsible for collecting, managing, distributing, or otherwise contributing to the development of the resource.

This field is compatible with *7. Contributor* in DataCite.

The structure is identical to the Creators field. The "creators" field records those persons or organisations that should be credited for the resource described by the record (e.g. for citation purposes). The "contributors" field records all other persons or organisations that have contributed, but which should not be credited for citation purposes.

Subfields:

- *See [Creators field](#creators-1-n), but ``role`` is required.*

Note that Creators and Contributors may use different controlled vocabularies for the ``role`` field.

Example:

```json
{
  "contributors": [{
    "person_or_org": {
      "name": "Nielsen, Lars Holm",
      "type": "personal",
      "given_name": "Lars Holm",
      "family_name": "Nielsen",
      "identifiers": [{
        "scheme": "orcid",
        "identifier": "0000-0001-8135-3489"
      }],
    },
    "role": {"id": "editor"},
    "affiliations": [{
      "id": "01ggx4157",
      "name": "CERN",
    }]
  }],
}
```

### Subjects (0-n)

Subject, keyword, classification code, or key phrase describing the resource.

This field is compatible with *6. Subject* in DataCite.

Subfields:

|    Field    | Cardinality | Description                                                   |
|:-----------:|:-----------:|:--------------------------------------------------------------|
|   ``id``    |  (0-1, CV)  | The identifier of the subject from the controlled vocabulary. |
| ``subject`` |    (0-1)    | A custom keyword.                                             |

Either ``id`` or ``subject`` must be passed.

Example:

```json
{
  "subjects": [{
    "id": "https://id.nlm.nih.gov/mesh/D000001",
  }],
}
```

### Languages (0-n)

The languages of the resource.

This field is compatible with *9. Language* in DataCite. DataCite however only supports one primary language, while this field supports multiple languages.

Subfields:

| Field  | Cardinality | Description                  |
|:------:|:-----------:|:-----------------------------|
| ``id`` |   (1, CV)   | The ISO-639-3 language code. |

Example:

```json
{
  "languages": [{"id": "dan"}, {"id": "eng"}]
}
```

### Dates (0-n)

Different dates relevant to the resource.

The field is compatible with *8. Date* in DataCite.

Subfields:

|      Field      | Cardinality | Description                                                             |
|:---------------:|:-----------:|:------------------------------------------------------------------------|
|    ``date``     |     (1)     | A date or time interval according to Extended Date Time Format Level 0. |
|    ``type``     |     (1)     | The type of date.                                                       |
| ``description`` |    (0-1)    | free text, specific information about the date.                         |

The ``type`` field is as follows:

|   Field   | Cardinality | Description                                                                                                                                                                                                            |
|:---------:|:-----------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|  ``id``   |   (1, CV)   | Date type id from the controlled vocabulary. By default one of: ``accepted``, ``available``, ``collected``, ``copyrighted``, ``created``, ``issued``, ``other``, ``submitted``, ``updated``, ``valid``, ``withdrawn``. |
| ``title`` |     (1)     | The corresponding localized human readable label. e.g. ``{"en": "Accepted"}``                                                                                                                                          |

Note that multiple localized titles are supported e.g. ``{"en": "Available", "fr": "Disponible"}``. Use ISO 639-1 codes (2 letter locales) as keys.
Only ``id`` needs to be passed on the REST API.

Example:

```json
{
  "dates": [{
    "date": "1939/1945",
    "type": {
      "id": "other",
      "title": {
        "en": "Other"
      }
    },
    "description": "A date"
  }],
}
```

### Version (0-1)

The version number of the resource. Suggested practice is to use [semantic versioning](https://semver.org). If the version number is provided, it's used for display purposes on search results and landing pages.

This field is compatible with *15. Version* in DataCite.

Example:

```json
{
  "version": "v1.0.0",
}
```

### Publisher (0-1)

The name of the entity that holds, archives, publishes, prints, distributes, releases, issues, or produces the resource. This property will be used to formulate the citation, so consider the prominence of the role. For software, use Publisher for the code repository. If there is an entity other than a code repository, that "holds, archives, publishes, prints, distributes, releases, issues, or produces" the code, use the property Contributor field for the code repository.

Defaults to the name of the repository.

Example:

```json
{
  "publisher": "InvenioRDM"
}
```

### Alternate identifiers (0-n)

Persistent identifiers for the resource other than the ones registered as system-managed internal or external persistent identifiers.

This field is compatible with *11. Alternate Identifiers* in DataCite.

The main difference between the system-managed identifiers and this field, is that system-managed identifiers are fully controlled and managed by InvenioRDM, while identifiers listed here are used solely for display purposes. For instance, a DOI registered in the system-managed identifiers will prevent another record with the same DOI from being created. A DOI included in this field, will not prevent another record from including the same DOI in this field.

Subfields:

| Field          | Cardinality | Description                   |
|:--------------:|:-----------:|:------------------------------|
| ``identifier`` | (1)         | identifier value              |
| ``scheme``     | (1, CV)     | The scheme of the identifier. See below.  |


#### Identifier schemes

The default valid schemes are listed below. They are defined in [invenio-rdm-records](https://github.com/inveniosoftware/invenio-rdm-records/blob/master/invenio_rdm_records/config.py) and configurable via `RDM_RECORDS_IDENTIFIERS_SCHEMES`.

|        Scheme        |       Label        |
| :------------------: | :----------------: |
|       ``ark``        |        ARK         |
|      ``arxiv``       |       arXiv        |
|       ``ads``        |      Bibcode       |
| ``crossreffunderid`` | Crossref Funder ID |
|       ``doi``        |        DOI         |
|      ``ean13``       |       EAN13        |
|      ``eissn``       |       EISSN        |
|       ``grid``       |        GRID        |
|      ``handle``      |       Handle       |
|       ``igsn``       |        IGSN        |
|       ``isbn``       |        ISBN        |
|       ``isni``       |        ISNI        |
|       ``issn``       |        ISSN        |
|       ``istc``       |        ISTC        |
|      ``lissn``       |       LISSN        |
|       ``lsid``       |        LSID        |
|       ``pmid``       |        PMID        |
|       ``purl``       |        PURL        |
|       ``upc``        |        UPC         |
|       ``url``        |        URL         |
|       ``urn``        |        URN         |
|       ``w3id``       |        W3ID        |
|      ``other``       |       Other        |


Example:

```json
{
  "identifiers": [{
    "identifier": "1924MNRAS..84..308E",
    "scheme": "bibcode"
  }],
}
```

### Related identifiers/works (0-n)

Identifiers of related resources.

This field is compatible with *12. Related Identifiers* in DataCite. The field however
does not support the subfields *12.c relatedMetadataScheme*, *12.d schemeURI* and *12.e schemeType* used for linking to additional metadata.

Subfields:

|       Field       | Cardinality | Description                                                                                                   |
| :---------------: | :---------: | :------------------------------------------------------------------------------------------------------------ |
|  ``identifier``   |   (1, CV)   | A global unique persistent identifier for a related resource.                                                 |
|    ``scheme``     |   (1, CV)   | The scheme of the identifier. See [identifier schemes](#identifier-schemes).                                                                                |
| ``relation_type`` |     (1)     | The relation of the record to this related resource.                                                          |
| ``resource_type`` |    (0-1)    | The resource type of the related resource. Can be different from the [Resource type](#resource-type-1) field. |

Supported identifier schemes:

ARK, arXiv, Bibcode, DOI, EAN13, EISSN, Handle, IGSN, ISBN, ISSN, ISTC, LISSN, LSID, PubMed ID, PURL, UPC, URL, URN, W3ID. See `RDM_RECORDS_IDENTIFIERS_SCHEMES` in [invenio-rdm-records](https://github.com/inveniosoftware/invenio-rdm-records/blob/master/invenio_rdm_records/config.py).

Note that those are passed lowercased e.g., arXiv is ``arxiv``.

The field ``relation_type`` is of this shape:

|   Field   | Cardinality | Description                                                                                                                                                                                                         |
|:---------:|:-----------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|  ``id``   |   (1, CV)   | Relation type id from the controlled vocabulary. The default list is [here](https://github.com/inveniosoftware/invenio-rdm-records/blob/master/invenio_rdm_records/fixtures/data/vocabularies/relation_types.yaml). |
| ``title`` |     (1)     | The corresponding localized human readable label. e.g. ``{"en": "Is cited by"}``                                                                                                                                    |

The field ``resource_type`` is of this shape:

|   Field   | Cardinality | Description                                                                                                                                                                                                     |
|:---------:|:-----------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|  ``id``   |   (1, CV)   | Date type id from the controlled vocabulary. The default list is [here](https://github.com/inveniosoftware/invenio-rdm-records/blob/master/invenio_rdm_records/fixtures/data/vocabularies/resource_types.yaml). |
| ``title`` |     (1)     | The corresponding localized human readable label. e.g. ``{"en": "Annotation collection"}``                                                                                                                      |

For both ``relation_type.title`` and ``resource_type.title`` multiple localized titles are supported e.g. ``{"en": "Cites", "fr": "Cite"}``. Use ISO 639-1 codes (2 letter locales) as keys. In both cases, only ``id`` needs to be passed on the REST API.

Example:

```json
{
  "related_identifiers": [{
    "identifier": "10.1234/foo.bar",
    "scheme": "doi",
    "relation_type": {
      "id": "cites",
      "title": {
        "en": "Cites"
      }
    },
    "resource_type": {
      "id": "dataset",
      "title": {
        "en": "Dataset"
      }
    }
  }],
}
```

### Sizes (0-n)

!!! warning "Not part of the deposit page yet."
    Although available via the API, this field may see changes when added to the deposit page.

Size (e.g. bytes, pages, inches, etc.) or duration (extent), e.g. hours, minutes, days, etc., of a resource.

This field is compatible with *13. Size* in DataCite.

Example:

```json
{
  "sizes": [
    "11 pages"
  ],
}
```

### Formats (0-n)

!!! warning "Not part of the deposit page yet."
    Although available via the API, this field may see changes when added to the deposit page.

Technical format of the resource.

This field is compatible with *14. Format* in Datacite.

Example:

```json
{
  "formats": [
    "application/pdf"
  ],
}
```

### Locations (0-n)

!!! warning "Not part of the deposit page yet."
    Although available via the API, this field may see changes when added to the deposit page.

Spatial region or named place where the data was gathered or about which the data is focused.

The field is compatible with *18. GeoLocation* in DataCite Metadata Schema. The field however has important differences:

- The field allows associating geographical identifiers with a location.
- The field allows associating a free text description to the location.
- The field uses the GeoJSON specification for describing geospatial coordinates instead of the individual fields used by DataCite.

The location fields is modelled over GeoJSON [FeatureCollection](https://tools.ietf.org/html/rfc7946#section-3.3) and [Feature](https://tools.ietf.org/html/rfc7946#section-3.2) objects using foreign members (for ``identifiers``, ``place`` and ``description``). We do not store the GeoJSON type information (e.g. ``"type": "FeatureCollection"`` and ``"type": "Feature"``) because this information is implicit. The JSON served on the REST API (external JSON), *will* include
the type information as well as ``"properties": null`` in order to make it valid GeoJSON.

Subfields:

|    Field     | Cardinality | Description                                                                                                                                                                                       |
|:------------:|:-----------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ``features`` |     (1)     | A list of GeoJSON feature objects. The reason for this keyword is to align with GeoJSON and allow for later expansion with other subfields such as bounding box (``bbox``) from the GeoJSON spec. |

Subfields of items in ``features``:

|      Field      | Cardinality | Description                                                                                                                                                                                                                                                         |
|:---------------:|:-----------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|  ``geometry``   |    (0-1)    | A GeoJSON [Geometry Object](https://tools.ietf.org/html/rfc7946#section-3.1) according to RFC 7946. Note, GeoJSON's coordinate reference system is [WGS84](https://tools.ietf.org/html/rfc7946#section-4).                                                          |
| ``identifiers`` |    (0-1)    | A list of geographic location identifiers. This could for instance be from [GeoNames](https://www.geonames.org) or [Getty Thesaurus of Geographic Names](http://www.getty.edu/research/tools/vocabularies/tgn/) (TGN) which would allow linking to historic places. |
|    ``place``    |    (0-1)    | Free text, used to describe a geographical location.                                                                                                                                                                                                                |
| ``description`` |    (0-1)    | Free text, used for any extra information related to the location.                                                                                                                                                                                                  |

Identifier object in ``identifiers``:

|     Field      | Cardinality | Description                                    |
|:--------------:|:-----------:|:-----------------------------------------------|
| ``identifier`` |   (1, CV)   | A globally unique identifier for the location. |
|   ``scheme``   |   (1, CV)   | The scheme of the identifier.                  |

Notes:

- Indexing: The ``geometry`` field is indexed as a [``geo_shape``](https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-shape.html) field type in Elasticsearch which allows advanced geospatial querying.
  In addition, for each geometry object, we calculate the centroid using the [Shapely](https://pypi.org/project/Shapely/) library and index it as a [``geo_point``](https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-point.html) field type in Elasticsearch which supports more specialised queries for points.
- Initially only [``Point``](https://tools.ietf.org/html/rfc7946#section-3.1.2) objects will be supported in the upload form and landing page.
  This is primarily due to need for a user-friendly field.
- GeoJSON lists [``positions (coordinates)``](https://www.rfc-editor.org/rfc/rfc7946#section-3.1.1) in the order of (longitude, latitude), which is opposite from what is used in many other coordinate systems. It's easy to mess this up!

Example:

```json
{
  "locations": {
    "features": [{
      "geometry": {
        "type": "Point",
        "coordinates": [46.23333, 6.05]
      },
      "identifiers": [{
        "scheme": "geonames",
        "identifier": "2661235"
      }],
      "place": "CERN",
      "description": "Invenio birth place."
    }],
  },
}
```

### Funding references (0-n)

Information about financial support (funding) for the resource being registered.

This field is compatible with *19. Funding Reference* in DataCite.

The funder subfield is intended to be linked to a customizable vocabulary from Open Funder Registry or ROR. The award subfield is intended to be either linked to a customizable vocabulary sourced from the OpenAIRE grant database, or specified explicitly to allow linking to grants not provided by the grant database.

Subfields:

|   Field    | Cardinality | Description                                |
|:----------:|:-----------:|:-------------------------------------------|
| ``funder`` |     (1)     | The organisation of the funding provider.  |
| ``award``  |    (0-1)    | The award (grant) sponsored by the funder. |

The ``funder`` subfields:

|  Field   | Cardinality | Description                                   |
|:--------:|:-----------:|:----------------------------------------------|
|  ``id``  |  (0-1, CV)  | The funder id from the controlled vocabulary. |
| ``name`` |    (0-1)    | The name of the funder.                       |

One of ``id`` OR ``name`` must be given. It's recommended to use ``name`` if there is no matching ``id`` in the controlled vocabulary.

The ``award`` subfields:

|      Field      | Cardinality | Description                                                                 |
|:---------------:|:-----------:|:----------------------------------------------------------------------------|
|     ``id``      |  (0-1, CV)  | The award id from the controlled vocabulary.                                |
|    ``title``    |    (0-1)    | The localized title of the award (e.g., `{"en": "Nobel Prize in Physics"}`) |
|   ``number``    |    (0-1)    | The code assigned by the funder to a sponsored award (grant).               |
| ``identifiers`` |    (0-N)    | Identifiers for the award.                                                  |

One of ``id`` OR (``title`` and ``number``) must be given. It's recommended to use ``title`` and ``number`` if there is no matching ``id`` in the controlled vocabulary.

Example:

```json
{
  "funding": [{
      "funder": {
        "id": "00k4n6c32"
      },
      "award": {
        "id": "00k4n6c32::246686"
      }
    }, {
      "funder": {
        "id": "00k4n6c32"
      },
      "award": {
        "title": {
          "en": "Research on Experimental Physics"
        },
        "number": "EP-123456",
        "identifiers": [{
          "scheme": "url",
          "identifier": "https://experimental-physics.eu"
        }]
      }
    }
  ]
}
```

### References (0-n)

A list of reference strings.

Subfields:

|     Field      | Cardinality | Description                                                                  |
| :------------: | :---------: | :--------------------------------------------------------------------------- |
| ``reference``  |     (1)     | The full reference string.                                                   |
|   ``scheme``   |  (0-1, CV)  | The scheme of the identifier. See [identifier schemes](#identifier-schemes). |
| ``identifier`` |    (0-1)    | The identifier if known.                                                     |

Example:

```json
{
  "references": [{
      "reference": "Nielsen et al,..",
      "identifier": "10.1234/foo.bar",
      "scheme": "other"
  }]
}
```

## Files

Records may have associated digital files. A record is not meant to be associated
with a high number of files, as the files are stored inside the record and thus
increase the overall size of the JSON document.

All the fields below are under the ``"files"`` key.

### Enabled (1)

The ``enabled`` field determines if the record is a metadata-only record or if
files are associated.

Example:

```json
{
  "enabled": false
}
```

In this case, the record has (and can have) no associated files. It is a metadata-only record.

### Entries (0-n)

The entries field lists the associated digital files for the resource described
by the record. The files must all be registered in Invenio-Files-REST store
independently. This is to ensure that files can be tracked and fixity can be
checked.

The key (``paper.pdf`` below) represents a file path.

Subfields:

|       Field       | Cardinality | Description                                                                                          |
|:-----------------:|:-----------:|:-----------------------------------------------------------------------------------------------------|
|   ``bucket_id``   |     (1)     | The bucket identifier.                                                                               |
|   ``checksum``    |     (1)     | The checksum of the file in the form ``<algorithm>:<value>``.                                        |
|    ``created``    |     (1)     | Date of creation (init) of the file record.                                                          |
|    ``file_id``    |     (1)     | The digital file instance identifier (references a file on storage).                                 |
|      ``key``      |     (1)     | The filepath of the file.                                                                            |
|     ``link``      |     (1)     | Links to the file (_self_, _content_, _iiif\_canvas_, _iiif\_base_, _iiif\_info_, _iiif\_api_, etc.) |
|   ``metadata``    |     (1)     | Dictionary of free key-value pairs with meta information about the file (e.g. description).          |
|   ``mimetype``    |     (1)     | The mimetype of the file.                                                                            |
|     ``size``      |     (1)     | The size in bytes of the file.                                                                       |
|    ``status``     |     (1)     | The current status of the file ingestion (_completed_ or _pending_).                                 |
| ``storage_class`` |     (1)     | The backend for the file (e.g. local or external storage).                                           |
|    ``updated``    |     (1)     | Date of latest update of the file record metadata or file.                                           |
|  ``version_id``   |     (1)     | The logical object identifier.                                                                       |

Example:

```json
{
  "entries": {
    "paper.pdf": {
      "bucket_id": "<bucket-id>",
      "checksum": "md5:abcdef...",
      "created": "2022-10-12T11:08:56.953781+00:00",
      "file_id": "<file-id>",
      "key": "paper.pdf",
      "links": {
        "self": "{scheme+hostname}/api/records/12345-abcde/files/your_file.png",
        "content": "{scheme+hostname}/api/records/12345-abcde/files/your_file.png/content",
        "iiif_canvas": "{scheme+hostname}/api/iiif/record:8a4dq-z5237/canvas/your_file.png",
        "iiif_base": "{scheme+hostname}/api/iiif/record:8a4dq-z5237:your_file.png",
        "iiif_info": "{scheme+hostname}/api/iiif/record:8a4dq-z5237:your_file.png/info.json",
        "iiif_api": "{scheme+hostname}/api/iiif/record:8a4dq-z5237:your_file.png/full/full/0/default.png"
      },
      "metadata": {
        "width": 2302,
        "height": 948
      },
      "mimetype": "application/pdf",
      "size": 12345,
      "status": "completed",
      "storage_class": "A",
      "updated": "2022-10-12T11:08:56.970805+00:00",
      "version_id": "<object-version-id>",
    },
  }
}
```

!!! info "IIIF links only on image formats"
    IIIF links are only returned for files who are compatible with IIIF.
    Those formats are defined by the `IIIF_FORMATS` configuration variable.
    By default _gif_, _jp2_, _jpeg_, _jpg_, _png_, _tif_, and _tiff_.

### Default preview (0-1)

The default preview field names the filename of the file which should by default
be shown on the record landing page.

Example:

```json
{
  "default_preview": "paper.pdf"
}
```

## Tombstone

A tombstone is created when a record is removed from the system. The tombstone
records the reason for the removal, a category for statistics purposes, who
removed the record and when.

Subfields:

|     Field      | Cardinality | Description                                                                                                                 |
|:--------------:|:-----------:|:----------------------------------------------------------------------------------------------------------------------------|
|   ``reason``   |     (1)     | Free text, the reason for removal.                                                                                          |
|  ``category``  |     (1)     | An identifier for a category of reasons. Used for statistics purposes and for extracting e.g. spam records from the system. |
| ``removed_by`` |     (1)     | The user who removed the record.                                                                                            |
| ``timestamp``  |     (1)     | The UTC timestamp when the record was removed.                                                                              |

Example:

```json
{
  "tombstone": {
    "reason": "Spam record, removed by InvenioRDM staff.",
    "category": "spam_manual",
    "removed_by": {"user": 1},
    "timestamp": "2020-09-01T12:02:00Z"
  }
}
```

## Future directions

The record metadata model will evolve over time, during which
some of the following information will be added:

- Usage statistics
- Communities
- Extra metadata formats
- Primary contact (contact email)
- Vocabulary extensions

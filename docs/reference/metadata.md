# Metadata reference

**Summary**

The following document is a reference guide for the internal metadata schema of bibliographic records in InvenioRDM.

**Intended audience**

This guide is intended for advanced users, administrators and developers of InvenioRDM with significant prior experience.

## Overview

InvenioRDM's bibliographic records are stored as JSON documents in a structure
that is aligned with DataCite's Metadata Schema v4.x with minor additions
and modifications.

**Schema version**

All records contain a schema definition in the top-level key ``$schema``. The value
is a link to the internal JSONSchema which is being used to validate the structure of the record.
This field is fully system-managed.

```json
{
    "$schema": "https://localhost/schemas/records/record-v1.0.0.json",
    ...
}
```

**Top-level fields**

Following is an overview of the top-level fields in a record:

| Field |   Description   |
|:-----:|:----------------|
|  ``id``/``pid``  | The internal persistent identifier for a specific version.  |
|  ``conceptid``/``conceptpid``  | The internal persistent identifier for all versions.  |
|  ``pids`` | System-managed external persistent identifiers (DOIs, Handles, OAI-PMH identifiers).  |
|  ``metadata`` | Descriptive metadata for the resource.  |
|  ``ext`` | Instance specific descriptive metadata for the resource.  |
|  ``provenance`` | System-managed provenance information.  |
|  ``access`` | Access control information.  |
|  ``files`` | Associated files information.  |
|  ``tombstone`` | Tombstone information.  |

Each of these keys will be explained below. Following is an example of how the
top-level fields in a record look like:

```json
{
    "$schema": "https://localhost/schemas/records/record-v1.0.0.json",
    "id": "q5jr8-hny72",
    "pid": { ... },
    "conceptid": "adf7e-kop86",
    "conceptpid": { ... },
    "pids" : { ... },
    "metadata" : { ... },
    "ext" : { ... },
    "provenance" : { ... },
    "access" : { ... },
    "files" : { ... },
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
A record always have an internal PID.

### Internal PIDs

A record stores information about two internal PIDs:

Specific version PID:

| Field |   Description   |
|:-----:|:----------------|
|``id`` | The value of the internal record identifier. |
| ``pid`` | Object level information about the identifier needed for operational reasons. |

Concept version PID:

| Field |   Description   |
|:-----:|:----------------|
| ``conceptid`` | The value of the internal record identifier. |
| ``conceptpid`` | Object level information about the identifier needed for operational reasons. |

Example:

```json
{
  "id": "abcde-12345",
  "conceptid": "12345-abcde",
  "pid": {
    "pk": 1,
    "status": "R"
  },
  "conceptpid": {
    "pk": 2,
    "status": "R"
  },
}
```

### External PIDs

External PIDs are persistent identifiers managed via Invenio-PIDStore and that may require integration
with external registration services.

Persistent identifiers are globally unique in the system, thus you cannot have two records
with the same system-managed persistent identifer (see also [Metadata > Identifiers](#identifiers-0-n)).

Only one identifier can be registered per system defined scheme. Each identifier has the following subfields:

| Field | Cardinality |   Description   |
|:-----:|:-----------:|:----------------|
|``identifier`` | (1) | The identifier value. |
| ``provider`` | (1) | the provider identifier used internally by the system. |
| ``client`` | (0-1) | The client identifier used for connecting with an external registration service. |

```json
{
    "pids": {
        "doi": {
            "identifier": "10.5281/zenodo.1234",
            "provider": "datacite",
            "client": "zenodo"
        },
        "concept-doi": {
            "identifier": "10.5281/zenodo.1234",
            "provider": "datacite",
            "client": "zenodo"
        }
}
```

Other system managed identifiers will also be be recorded here such as the OAI id.

## Metadata

The cardinality of each field is expressed in between parenthesis on the title of each field's section.

### Resource Type (1)

The type of the resource described by the record. The resource type must be selected from a  controlled vocabulary which can be customized by each InvenioRDM instance.

This field is compatible with *10. Resource Type`* in DataCite. DataCite allows free text for the specific subtype, however InvenioRDM requires this to come from an customizable controlled vocabulary.

The resource type vocabulary also defines mappings to other vocabularies such as Schema.org, Citation Style Language, BibTeX, DataCite and OpenAIRE. These mappings are very important for the correct generation of citations due to how different types are being interpreted by reference management systems.

Subfields:

| Field |   Description   |
|:-----:|:----------------|
| ``type`` | The general resource type from the controlled vocabulary. |
| ``subtype`` |  The specific resource type from the controlled vocabulary. |

Example:

```json
{
    "resource_type": {
      "type": "text",
      "subtype": "article"
    }
}
```

### Creators (1-n)

The creators field registers those persons or organisations that should be credited for the resource described in by the record. The list of person or organisations in the creators field is used for e.g. generating citations, while persons or organisations listed in the contributors field are not included the generated citations.

The field is compatible with *2. Creator* in DataCite. In addition we are adding the possiblity of associating a role (like for contributors). This is specifically for cases where e.g. an editor needs to be credited for the work, while authors of individual articles will be listed under contributors.

Subfields:

| Field | Cardinality |   Description   |
|:-----:|:-----------:|:----------------|
| ``person_or_org`` | (1) | The person or organization. |
| ``affiliations`` | (0-n) | Affilations if type is a personal name. |

A `person_or_org` is described with the following subfields:

| Field | Cardinality |   Description   |
|:-----:|:-----------:|:----------------|
| ``name`` | (0 if `type` is `personal` / 1 if `type` is `organisational`) | The full name of the organisation. For a person this field is generated from `given_name` and `family_name` |
| ``type`` | (0-1, CV) | The type of name. Either ``personal`` or ``organisational``. |
| ``role`` | (0-1, CV) | The role of the person or organisation selected from a customizable controlled vocabulary. |
| ``given_name``  | (1 if `type` is `personal` / 0 if `type` is `organisational`) | Given name(s) if the type is a personal name. |
| ``family_name`` | (1 if `type` is `personal` / 0 if `type` is `organisational`) | Family name if type is a personal name. |
| ``identifiers``  | (0-n) | Person or organisation identifiers. |

Affiliations are described with the following subfields:

| Field | Cardinality |   Description   |
|:-----:|:-----------:|:----------------|
| ``name`` | (1) | The organizational or institutional affiliation of the creator. |
| ``identifiers`` | (0-n) | Organisation identifiers. |

Identifiers are described with the following subfields (note, we only support one identifier per scheme):

| Field | Cardinality |   Description   |
|:-----:|:-----------:|:----------------|
| ``scheme`` | (1, CV) | The identifier scheme. |
| ``identifier`` | (1) | Actual value of the identifier. |

Supported creator identifier schemes:

- ORCID
- GND
- ISNI
- ROR

Supported affiliation identifier schemes:

- ISNI
- ROR

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
          "name": "CERN",
          "identifiers": [{
              "scheme": "ror",
              "identifier": "01ggx4157",
          }, {
              "scheme": "isni",
              "identifier": "000000012156142X",
          }]
      }]
    }],
}
```

Note that the identifier's schemes are lowercased.

### Title (1)

A primary name or primary title by which a resource is known. May be the title of a dataset or the name of a piece of software. The primary title is used for display purposes throughout InvenioRDM.

The fields is compatible with *3. Title* in DataCite. Compared to DataCite the field does not support specifying the language of the title.

Example:

```json
{
    "title": "InvenioRDM"
}
```

### Additional titles (0-n)

Additional names or titles by which a resource is known.

The fields is compatible with *3. Title* in DataCite. Compared to DataCite, InvenioRDM splits *3. Title* into two separate fields ``title`` and ``additional_titles``. This is to ensure consistent usage of a record's title throughout the entire software stack for display purposes.

Subfields:

- ``title`` (1) - The addtional title.
- ``type`` (1, CV) - The type of the title. One of: ``alternative_title``, ``subtitle`` ``translated_title`` or ``other``.
Other
- ``lang`` (0-1, CV) - The language of the title. ISO 639-3 language code.

Example:

```json
{
    "additional_titles": [{
      "title": "a research data management platform",
      "type": "subtitle",
      "lang": "eng"
    }]
}
```

### Description (1)

The description of a record.

The fields is compatible with *17. Description* in DataCite. Compared to DataCite the field does not support specifying the language of the description.

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

The fields is compatible with *17. Description* in DataCite.

Subfields:

- ``description`` (1) - Free text.
- ``type`` (1, CV) - The type of the description. One of ``abstract``, ``method``, ``seriesinformation``, ``tableofcontents``, ``technicalinfo``, ``other``.
- ``lang`` (0-1) -  The language of the description. ISO 639-3 language code.

Example:

```json
{
    "additional_descriptions": [{
      "description": "a research data management platform",
      "type": "methods",
      "lang": "eng"
    }]
}
```

### Publisher (1)

The name of the entity that holds, archives, publishes prints, distributes, releases, issues, or produces the resource. This property will be used to formulate the citation, so consider the prominence of the role. For software, use Publisher for the code repository. If there is an entity other than a code repository, that "holds, archives, publishes, prints, distributes, releases, issues, or produces" the code, use the property Contributor/contributorType/ hostingInstitution for the code repository.

Defaults to the name of the repository.

Example:

```json
{
    "publisher": "InvenioRDM"
}
```

### Publication date (1)

The date when the resource was or will be made publicly available.

The field is compatible *5. PublicationYear* in DataCite. In case of time intervals the earlist date

Format:

The string must be be formatted according to [Extended Date Time Format (EDTF)](http://loc.gov/standards/datetime/) Level. Only a *"Date"* or a *"Time Interval"* is supported. A *"Date and Time"* is not supported. Following are examples of valid values:

- Date:
    - ``2020-11-10`` - a complete ISO8601 date.
    - ``2020-11`` - a date with month precision
    - ``2020`` - a date with year precision
- Time Interval:
    - ``1939/1945`` a time interval with year precision, beginning sometime in 1939 and ending sometime in 1945.
    - ``1939-09-01/1945-09`` a time interval with day and month precision, beginning September 1st, 1939 and ending sometime in September 1945.


The localization (L10N) of EDTF dates is based on the [skeletons](http://cldr.unicode.org/translation/date-time-1/date-time-patterns) defined by the [Unicode Common Locale Data Repository (CLDR)](http://cldr.unicode.org).


Example:

```json
{
    "publication_date": "2018/2020-09",
}
```

### Subjects (0-n)

!!! warning "Work in progress"
    This field may change after work done on controlled vocabulary management is
    completed during December 2020.


Subject, keyword, classification code, or key phrase describing the resource.

This field is compatible with *6. Subject* in DataCite.

Subfields:

- ``subject`` (1) - free text, the subject term.
- ``identifier`` (0-1) - the identifier of the term (``scheme`` also be specified).
- ``scheme`` (0-1, CV) - the subject scheme or classification code or authority.

Supported subject schemes:

- URL
- URN

Example:

```json
{
    "subjects": [{
        "subject": "Brain",
        "identifier": "D001921",
        "scheme": "mesh"
      },
      {
        "subject": "Invenio"
      }
    ],
}
```

### Contributors (0-n)

The organisation or person responsible for collecting, managing, distributing, or otherwise contributing to the development of the resource.

This field is compatible with 7. Contributor in DataCite.

The structure is identical to the Creators field. The creators field record those persons or organisations that should be credited for the resource described in by the record (e.g. for citation purposes). The contributors field record all other persons or organisations that have contributed but which should not be credited for citation purposes.

Subfields:

- *Please see Creators field.*

Note that Creators and Contributors may use different controlled vocabularies for the role field.

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
      "role": "Editor"
    },
    "affiliations": [{
        "name": "CERN",
        "identifiers": [{
            "scheme": "ror",
            "identifier": "01ggx4157",
        }, {
            "scheme": "isni",
            "identifier": "000000012156142X",
        }]
    }]
  }],
}
```

### Dates (0-n)

Different dates relevant to the resource.

The field is compatible with *8. Date* in DataCite.

Subfields:

- ``date`` (1) - A date or time interval according to Extended Date Time Format level 0.
- ``type`` (1, CV) - The type of date. A value from a customizable controlled vocabulary (defaults to DataCite's date type vocabulary).
- ``description`` (0-1) - free text, specific information about the date.

Example:

```json
{
  "dates": [{
      "date": "1939/1945",
      "type": "other",
      "description": "A date"
  }],
}
```

### Languages (0-n)

The languages of the resource.

This field is compatible with *9. Language* in DataCite. DataCite however only supports one primary language, while this field supports multiple languages.

Format:

ISO-639-3 language code

Example:

```json
{
  "languages": ["dan", "eng"]
}
```

### Identifiers (0-n)

Persistent identifiers for the resource other than the ones registered as system-managed internal or external persistent identifers.

This field is compatible with *11. Alternate Identifiers* in DataCite.

The main difference between the system-managed identifiers and this field, is that system-managed identifiers are fully controlled and managed by InvenioRDM, while identifiers listed here are use solely for display purposes. For instance, a DOI registered in the system-managed identifiers will prevent another record with the same DOI from being created. A DOI included in this field, will not prevent another record from including the same DOI in this field.

Subfields:

- ``identifier`` -
- ``scheme`` -

Supported identifier schemes:

- ISBN10, ISBN13, ISSN, ISTC, DOI, Handle, EAN8, EAN13, ISNI ORCID, ARK, PURL, LSID, URN, Bibcode, arXiv, PubMed ID, PubMed Central ID, GND, SRA, BioProject, BioSample, Ensembl, UniProt, RefSeq, Genome Assembly.

Example:

```json
{
  "identifiers": [{
      "identifier": "1924MNRAS..84..308E",
      "scheme": "bibcode"
  }],
}
```

### Related identifiers (0-n)

Identifiers of related resources.

This field is compatible with *12. Related Identifiers* in DataCite. The field however
does not support the subfields *12.c relatedMetadataScheme*, *12.d schemeURI* and *12.e schemeType* used for linking to additional metadata.

Subfields:

- ``identifier`` (1, CV) - A global unique persistent identifier for a related resource.
- ``scheme`` (1, CV) - The scheme of the identifier.
- ``relation`` (1, CV) -
- ``resource_type`` (0-1, CV) - The resource type of the related resource. Uses the same customizable vocabulary as the Resource Type field.

Supported identifier schemes:

- ISBN10, ISBN13, ISSN, ISTC, DOI, Handle, EAN8, EAN13, ISNI ORCID, ARK, PURL, LSID, URN, Bibcode, arXiv, PubMed ID, PubMed Central ID, GND, SRA, BioProject, BioSample, Ensembl, UniProt, RefSeq, Genome Assembly.

Example:

```json
{
  "related_identifiers": [{
      "identifier": "10.1234/foo.bar",
      "scheme": "doi",
      "relation": "cites",
      "resource_type": {"type": "dataset"}
  }],
}
```

### Sizes (0-n)

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

Technical format of the resource.

This field is compatible with *14. Version*

Example:

```json
{
  "formats": [
      "application/pdf"
  ],
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

### Rights (0-n)

!!! warning "Work in progress"
    This field may change after work done on controlled vocabulary management is
    completed during December 2020.

Rights management statement for the resource.

This field is compatible with *16. Rights* in DataCite.

The rights field is intended to primarily be linked to a customizable vocabulary
of licenses (defaults [SPDX](https://spdx.org/licenses/)). It should however also be possible to provide
custom rights statements.

The rights statements does not have any impact on access control to the resource.

Subfields:

- ``rights``
- ``scheme``
- ``identifier``
- ``url``

Example:

```json
{
  "rights": [{
      "rights": "Creative Commons Attribution 4.0 International",
      "scheme": "spdx",
      "identifier": "cc-by-4.0",
      "url": "https://creativecommons.org/licenses/by/4.0/"
  }],
}
```

### Locations (0-n)

Spatial region or named place where the data was gathered or about which the data is focused.

The field is compatible with *18. GeoLocation* in DataCite Metadata Schema. The field however have important differences:

- The field allows associating geographical identifiers with a location.
- The field allows associating a free text description to the location.
- The field uses the GeoJSON specification for describing geospatial coordinates instead of the individual fields used by DataCite.

The location fields is modelled over GeoJSON [FeatureCollection](https://tools.ietf.org/html/rfc7946#section-3.3) and [Feature](https://tools.ietf.org/html/rfc7946#section-3.2) objects using foreign members (for ``identifiers``, ``place`` and ``description``). We do not store the GeoJSON type information (e.g. ``"type": "FeatureCollection"`` and ``"type": "Feature"``) because this information is implicit. The JSON served on the REST API (external JSON), *will* include
the type information as well as ``"properties": null`` in order to make it valid GeoJSON.

Subfields:

- ``features`` (1) - a list of GeoJSON feature objects. The reason for this keyword is to align with GeoJSON and allow for later expanded with other subfields such as bounding box (``bbox``) from the GeoJSON spec.

Subfields of items in ``features``:

- ``geometry`` (0-1) - a GeoJSON [Geometry Object](https://tools.ietf.org/html/rfc7946#section-3.1) according to RFC 7946. Note, GeoJSON's coordinate reference system is [WGS84](https://tools.ietf.org/html/rfc7946#section-4).
- ``identifiers``(0-1) -  Identifiers for the geographic locations. This could for instance be from [GeoNames](https://www.geonames.org) or [Getty Thesaurus of Geographic Names](http://www.getty.edu/research/tools/vocabularies/tgn/) (TGN) which would allow linking to historic places.
- ``place`` (0-1) - free text, used to describe a geographical location.
- ``description`` (0-1) - free text, used for any extra information related to the location.

Notes:

- Indexing: The ``geometry`` field is indexed as a [``geo_shape``](https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-shape.html) field type in Elasticsearch which allows advanced geospatial querying.
  In addition, for each geometry object, we calculate the centroid using the [Shapely](https://pypi.org/project/Shapely/) library and index it as a [``geo_point``](https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-point.html) field type in Elasticsearch which supports more specialised queries for points.
- Initially only [``Point``](https://tools.ietf.org/html/rfc7946#section-3.1.2) objects will be supported in the upload form and landing page.
  This is primarily due to need for a user-friendly field.

Example:

```json
{
  "locations": {
    "features": [{
      "geometry": {
        "type": "Point",
        "coordinates": [6.05, 46.23333]
      },
      "identifiers": {
        "geonames": "2661235",
        "tgn": "http://vocab.getty.edu/tgn/8703679"
      },
      "place": "CERN",
      "description": "Invenio birth place."
    }],
  },
}
```

### Funding references (0-n)

!!! warning "Work in progress"
    This field may change after work done on controlled vocabulary management is
    completed during December 2020.

Information about financial support (funding) for the resource being registered.

This field is compatible with *19. Funding Reference* in DataCite.

The funder subfield is intended to be linked to a customizable vocabulary from Open Funder Registry or ROR. The award subfields is intended to be either linked to a customizable vocabulary sourced from the OpenAIRE grant database, or be specified explicitly to allow linking to grants not provided by the grant database.

Subfields:

- ``funder`` (1) - The organisation of the funding provider.
- ``award`` (0-1) - The award (grant) sponsored by the funder.

Funder subfields:

- ``name`` - The name of the funder.
- ``identifer`` -  An unique identifier for the funder.
- ``scheme`` - The scheme of the identifier.

Supported schemes:

- CrossRef Funder ID
- GRID
- ISNI
- ROR
- Wikidata

Award subfields:

- ``title`` (0-1) - The title of the award
- ``number`` (0-1) - The code assigned by the funder to a sponsored award (grant).
- ``identifer`` (0-1) - An unique identifier for the funder.
- ``scheme`` (0-1) - The scheme of the identifier.

Example:

```json
{
  "funding": [{
      "funder": {
        "name": "European Commission",
        "identifier": "00k4n6c32",
        "scheme": "ror"
      },
      "award": {
        "title": "OpenAIRE",
        "number": "246686",
        "identifier": ".../246686",
        "scheme": "openaire"
      }
  }]
}
```

### References (0-n)

!!! warning "Work in progress"
    This field may be removed prior to the first stable release.

A list of reference strings

Subfields:

- ``reference`` (1) - free text, the full reference string
- ``identifier`` (0-1) - the identifer if known.
- ``scheme`` (0-1) - the scheme of the identifier.

Example:

```json
{
  "references": [{
      "reference": "Nielsen et al,..",
      "identifier": "10.1234/foo.bar",
      "scheme": "doi"
  }]
}
```

## Extensions

!!! warning "Work in progress"
    The access control fields are subject to change during December-January
    2020 when the custom fields feature is being finalized.

InvenioRDM supports extending records with custom metadata per instance. The
instance must configure all the fields. Here, we only describe how the
metadata extensions are integrated into the record.

### Namespace

All custom metadata fields are stored separately from the core metadata fields
in the top-level ``ext`` key. Each subfield is a namespace using an acronym.
For instance in the example below:

- ``dwc`` is an acronym for ``http://rs.tdwg.org/dwc/terms/``
- ``z`` is an acronym for ``https://zenodo.org/terms``

Example:

```json
{
  "ext": {
      "dwc": { ... },
      "z": { ... }
    },
  }
}
```

### Field identifiers

Under each namespace multiple fields can be defined. The namespace and the field
name generates a unique identifier for the field:

For instance ``dwc:collectionCode`` is expanded to ``http://rs.tdwg.org/dwc/terms/collectionCode``.

### Field data types

Each field must define a type. The current JSONSchema allows for the following
primitive types:

- strings
- numbers (integers and floats)
- booleans
- dates (encoded as strings)
- array of any of above primitive types

Extra validation on top of these fields is provided by when configuring the
fields.

Example:

```json
{
  "ext": {
    "dwc": {
      "collectionCode": "abc",
      "collectionCode2": 1.1,
      "collectionCode3": true,
      "test": ["abc", 1, true]
    }
  },
}
```

## Provenance

Basic provenance information is recorded under the top-level ``provenance`` key. The goal here is not to record complete provenance information, but only to record the minimal provenance information needed to effectively run the repository.

Subfields:

- ``created_by`` (1) - The agent who originally created the record (currently only users are supported)
- ``on_behalf_of`` (0-1) - For mediated deposits (currently only users are supported).

Example:

```json
{
  "provenance": {
    "created_by": {
      "user": 1
    },
    "on_behalf_of": {
      "user": 2
    }
  },
}
```

### Owners (1-n)

The owners of the record. All records must be owned by an agent in the system.
Records

```json
{
  "access": {
    "owned_by": [{
      "user": 1
    }],
  }
}
```

## Access information

The `access` field denotes record-specific read (visibility) options.

The `access` field has this structure:

| Field | Cardinality |   Description   |
|:-----:|:-----------:|:----------------|
|`record` | (1) | `"public"` or `"restricted"`. Read access to the record. |
| `files` | (1) |  `"public"` or `"restricted"`. Read access to the record's files. |
| `embargo` | (0-1) | Embargo options for the record. |

`"public"` means anyone can see the record/files. `"restricted"` means only the owner(s) or
specific users can see the record/files. Only in the cases of `"record": "restricted"` or
`"files": "restricted"` can an embargo be provided as input. However, once an embargo is
lifted, the `embargo` section is kept for transparency.

### Embargo

The `embargo` field denotes when an embargo must be lifted, at which point the record
is made publicly accessible. The `embargo` field has this structure:

| Field | Cardinality |   Description   |
|:-----:|:-----------:|:----------------|
|`active` | (1) | boolean. Is the record under embargo or not. |
| `until` | (1) | ISO date string. When to lift the embargo. e.g., `"2100-10-01"` |
| `reason` | (0-1) | string. Explanation behing embargo. |


## Files

!!! warning "Work in progress"

    The files fields are subject to change during November-December
    2020 when the files integration is finalized.

Records may have associated digital files. A record is not meant to be associated
with a high number of files, as the files are stored inside the record and thus
increases the overall size of the JSON document.

### Enabled (1)

The enabled field, determine if the record is a metadata-only records or if
files are associated.

Example:

```json
{
    "files": {
        "enabled": false
    }
}
```

### Entries (0-n)

The entries field lists the associated digital files for the resource described
by the record. The files must all be registered in Invenio-Files-REST store
independently. This is to ensure that files can be tracked and fixity can be
checked.

The key (``paper.pdf`` below) represents a file path.

Subfields:

- ``bucket_id`` (1) - The bucket identifier.
- ``version_id`` (1) - The logical object identifier.
- ``file_id`` (1) -  The digital file instance identifier (references a file on storage).
- ``backend:`` (1) - The backend for the file.
- ``key`` (1) - The filepath of the file.
- ``mimetype`` (1) - The mimetype of the file.
- ``size`` (1) - The size in bytes of the file.
- ``checksum`` (1) - The checksum of the file in the form ``<algorithm>:<value>``.

Example:

```json
{
    "files": {
        "entries": {
            "paper.pdf": {
                "version_id": "<object-version-id>",
                "bucket_id": "<bucket-id>",
                "file_id": "<file-id>",
                "backend": "...",
                "storage_class": "A",
                "key": "paper.pdf",
                "mimetype": "application/pdf",
                "size": 12345,
                "checksum": "md5:abcdef...",
            },
        }
    }
}
```

### Default preview (0-1)

The default preview field names the filename of the file which should by default
be shown on the record landing page.

Example:

```json
{
    "files": {
        "default_preview": "paper.pdf"
    }
}
```

### Order (0-n)

The order field defines a list of filenames which is the default display order
of files. If the order field is not specified, then all alphanumeric ordering
of filenames is used.

Example:

```json
{
    "files": {
        "order": [
            "paper.pdf",
            "...",
        ],
    }
}
```

### File metadata (0-n)

Additional metadata per file can be provided or automatically added by extensions.
Currently, we're planning to add the file extension, image width/height (needed for IIIF)
and a description.

```json
{
    "files": {
        "meta": {
            "paper.pdf": {
                "description": "sdfsdfsdf",
                "ext": "pdf",
                "width": 1024,
                "height": 1280,
            }
        },
    }
}
```

## Tombstone

A tombstone is created when a record is removed from the system. The tombstone
records the reason for the removal, a category for statistics purposes, who
removed the record and when.

Subfields:

- ``reason`` - Free text, the reason for removal.
- ``category`` - An identifier for a category of reasons. Used for statistics purposes and for extracting e.g. spam records from the system.
- ``removed_by`` - The user who removed the record.
- ``timestamp`` - The UTC timestamp when the record was removed.

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

The record metadata model will evolve over the coming half year, during which
some of the following information will be added:

- Usage statistics
- Versioning relationships
- Communities
- Extra metadata formats
- Primary contact (contact email)

## Annex: Full example

Following is a full example of a record:

```json
{
  "$schema": "https://localhost/schemas/records/record-v1.0.0.json",
  "id": "abcde-12345",
  "conceptid": "12345-abcde",
  "pid": {
    "pk": 1,
    "status": "R"
  },
  "conceptpid": {
    "pk": 2,
    "status": "R"
  },
  "pids": {
    "doi": {
      "identifier": "10.5281/zenodo.1234",
      "provider": "datacite",
      "client": "zenodo"
    },
    "concept-doi": {
      "identifier": "10.5281/zenodo.1234",
      "provider": "datacite",
      "client": "zenodo"
    },
    "handle": {
      "identifier": "9.12314",
      "provider": "cern-handle",
      "client": "zenodo"
    },
    "oai": {
      "identifier": "oai:zenodo.org:12345",
      "provider": "zenodo"
    }
  },
  "metadata": {
    "resource_type": {
      "type": "publication",
      "subtype": "article"
    },
    "creators": [{
      "name": "Nielsen, Lars Holm",
      "type": "personal",
      "given_name": "Lars Holm",
      "family_name": "Nielsen",
      "identifiers": {
        "orcid": "0000-0001-8135-3489"
      },
      "affiliations": [{
        "name": "CERN",
        "identifiers": {
          "ror": "01ggx4157",
          "isni": "000000012156142X"
        }
      }]
    }],
    "title": "InvenioRDM",
    "additional_titles": [{
      "title": "a research data management platform",
      "type": "subtitle",
      "lang": "eng"
    }],
    "publisher": "InvenioRDM",
    "publication_date": "2018/2020-09",
    "subjects": [{
      "subject": "test",
      "identifier": "test",
      "scheme": "dewey"
    }],
    "contributors": [{
      "name": "Nielsen, Lars Holm",
      "type": "personal",
      "role": "other",
      "given_name": "Lars Holm",
      "family_name": "Nielsen",
      "identifiers": {
        "orcid": "0000-0001-8135-3489"
      },
      "affiliations": [{
        "name": "CERN",
        "identifiers": {
          "ror": "01ggx4157",
          "isni": "000000012156142X"
        }
      }]
    }],
    "dates": [{
      "date": "1939/1945",
      "type": "other",
      "description": "A date"
    }],
    "languages": ["dan", "eng"],
    "identifiers": [{
      "identifier": "1924MNRAS..84..308E",
      "scheme": "bibcode"
    }],
    "related_identifiers": [{
      "identifier": "10.1234/foo.bar",
      "scheme": "doi",
      "relation": "cites",
      "resource_type": {
        "type": "dataset"
      }
    }],
    "sizes": [
      "11 pages"
    ],
    "formats": [
      "application/pdf"
    ],
    "version": "v1.0",
    "rights": [{
      "rights": "Creative Commons Attribution 4.0 International",
      "scheme": "spdx",
      "identifier": "cc-by-4.0",
      "url": "https://creativecommons.org/licenses/by/4.0/"
    }],
    "description": "Test",
    "additional_descriptions": [{
      "description": "Bla bla bla",
      "type": "methods",
      "lang": "eng"
    }],
    "locations": {
      "features": [{
        "geometry": {
          "type": "Point",
          "coordinates": [6.05, 46.23333]
        },
        "identifiers": {
          "geonames": "2661235",
          "tgn": "http://vocab.getty.edu/tgn/8703679"
        },
        "place": "CERN",
        "description": "Invenio birth place."
      }],
    },
    "funding": [{
      "funder": {
        "name": "European Commission",
        "identifier": "1234",
        "scheme": "ror"
      },
      "award": {
        "title": "OpenAIRE",
        "number": "246686",
        "identifier": ".../246686",
        "scheme": "openaire"
      }
    }],
    "references": [{
      "reference": "Nielsen et al,..",
      "identifier": "101.234",
      "scheme": "doi"
    }]
  },
  "ext": {
    "dwc": {
      "collectionCode": "abc",
      "collectionCode2": 1.1,
      "collectionCode3": true,
      "test": ["abc", 1, true]
    }
  },
  "provenance": {
    "created_by": {
      "user": 1
    },
    "on_behalf_of": {
      "user": 2
    }
  },
  "access": {
    "owned_by": [{
      "user": 1
    }],
    "embargo_date": "2021-01-01T00:00:00+0000",
    "access_condition": {
      "condition": "Medical doctors.",
      "default_link_validity": 30
    }
  },
  "files": {
    "enabled": true,
    "default_preview": "paper.pdf",
    "order": [
      "paper.pdf",
      "..."
    ],
    "meta": {
      "paper.pdf": {
        "description": "An important file.",
        "ext": "pdf",
        "width": 1024,
        "height": 1280
      }
    },
    "entries": {
      "paper.pdf": {
        "version_id": "<object-version-id>",
        "bucket_id": "<bucket-id>",
        "file_id": "<file-id>",
        "backend": "...",
        "storage_class": "A",
        "key": "paper.pdf",
        "mimetype": "application/pdf",
        "size": 1114324524355,
        "checksum": "md5:abcdef..."
      }
    }
  },
  "notes": [
    "Under investigation for copyright infringement."
  ]
}
```

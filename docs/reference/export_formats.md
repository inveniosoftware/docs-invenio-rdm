# InvenioRDM records export formats

InvenioRDN provides various record export formats to allow users to easily download and transfer metadata records between different systems. These formats adhere to widely used metadata standards such as DataCite, Dublin Core, BibTeX, and MARCXML, DCAT-AP making it easier to integrate with other systems that use these standards. Additionally, Invenio-app-rdm provides the ability to export records in the GeoJSON format, which is commonly used for geospatial metadata.

By providing a range of export formats, Invenio-app-rdm enables users to share and exchange metadata records with other systems in a format that is compatible with their respective standards. This makes it easier to ensure that metadata records are accurate, complete, and consistent across different systems.

## DataCite

The DataCite Metadata Schema is a list of core metadata properties chosen for the accurate and consistent identification of a resource for citation and retrieval purposes, along with recommended use instructions. It was designed for use in the citation of research data, and includes both mandatory and optional elements, as well as specific rules for their usage."

The DataCite Metadata Schema is widely used in the research community for the identification, discovery, and citation of research data, and is supported by a number of data repositories, publishers, and other organizations. It is an important tool for ensuring the proper management and sharing of research data, and helps to ensure that research data is findable, accessible, interoperable, and reusable (FAIR).

The official documentation for the DataCite metadata schema can be found on their [website](https://schema.datacite.org/meta/kernel-4.4/).

Example search requests:

```shell
GET /api/records/ HTTP/1.1
Host: inveniordm.web.cern.ch
Accept: application/vnd.datacite.datacite+xml;charset=UTF-8
```

```shell
GET /api/records/ HTTP/1.1
Host: inveniordm.web.cern.ch
Accept: application/application/vnd.datacite.datacite+json;charset=UTF-8
```

## DCAT-AP

DCAT-AP is a specification for describing public sector datasets and data services across Europe. It provides a common metadata vocabulary for describing datasets, catalogs, and services. The goal is to make it easier for users to find, access, and use data. DCAT-AP is based on the Data Catalog Vocabulary (DCAT) specification, which is maintained by the W3C.

The DCAT-AP data model is based on the Dublin Core metadata elements and includes additional properties for describing datasets and data services. It defines a core set of metadata elements that must be provided for each dataset, as well as optional and recommended elements. Some of the core elements include the title, description, publisher, and keyword.

Here is a link to the DCAT-AP data model (format) documentation: https://joinup.ec.europa.eu/collection/semantic-interoperability-community-semic/solution/dcat-application-profile-data-portals-europe.

Example search request:
```shell
GET /api/records/ HTTP/1.1
Host: inveniordm.web.cern.ch
Accept: application/marcxml+xml;charset=UTF-8
```


## Marc21 XML

MARC21 XML is a markup language used to represent bibliographic records in the MARC (MAchine Readable Cataloging) format. It is an XML representation of the MARC21 bibliographic format, which is widely used in libraries for the description of bibliographic items. MARC21 XML includes a standard set of data elements, control fields, and subfields, each with its own tag and indicator values, that allow for the representation of bibliographic metadata.

Here's a link to the official documentation of the MARC21 XML data model:
https://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd

Example search request:
```shell
GET /api/records/ HTTP/1.1
Host: inveniordm.web.cern.ch
Accept: application/dcat+xml;charset=UTF-8
```


## Bibtex

BibTeX is a bibliographic file format commonly used with LaTeX documents. It allows users to easily organize and manage bibliographic references in their documents. The BibTeX format uses a plain text file with a .bib extension and consists of entries, each describing a reference.

Each BibTeX entry starts with a @ symbol, followed by the type of reference (e.g., @article, @book, @inproceedings, etc.) and a unique identifier for the reference. The fields for each entry include the author(s), title, year, publisher, journal, and any other relevant information about the reference.

BibTeX is widely used in the academic community and is supported by many reference management software programs.

Here's a link to the BibTeX documentation: https://www.bibtex.com/format/

Example search request:
```shell
GET /api/records/ HTTP/1.1
Host: inveniordm.web.cern.ch
Accept: application/x-bibtex;charset=UTF-8
```


## Dublin Core

Dublin Core is a metadata standard used to describe digital resources such as web pages, images, and videos. It consists of a set of 15 metadata elements that provide basic descriptive information about a resource, including its title, creator, subject, description, publisher, and date. The elements can be used in a variety of combinations and can be extended to meet specific needs.

Dublin Core is widely used across many domains and is especially popular in the library and cultural heritage communities. It is a simple and flexible standard that allows for easy exchange and sharing of metadata between systems.

Here's a link to the Dublin Core Metadata Element Set specification: https://www.dublincore.org/specifications/dublin-core/dces/

Example search request:

```shell
GET /api/records/ HTTP/1.1
Host: inveniordm.web.cern.ch
Accept: application/x-dc+xml;charset=UTF-8
```


## GeoJSON

GeoJSON is a format for encoding geographic data structures using JSON (JavaScript Object Notation). It supports various types of geometries such as points, lines, and polygons, and allows for additional properties to be associated with those geometries. GeoJSON is often used to exchange data between web services and to display geospatial data on web maps.

Here is a link to the official GeoJSON specification: https://datatracker.ietf.org/doc/html/rfc7946

Example search request:

```shell
GET /api/records/ HTTP/1.1
Host: inveniordm.web.cern.ch
Accept: application/vnd.geojson+json;charset=UTF-8
```
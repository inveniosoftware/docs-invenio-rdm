---
hide:
  - toc
template: features_sub.html
image: ../images/interoperable.png
summary: InvenioRDM is built with REST APIs first, harvestable via OAI-PMH according to the OpenAIRE guidelines and has a metadata model based on the DataCite Metadata Schema.

---

## Data citation

InvenioRDM adheres to the best practices for data citation for scholary research data repositories.

## REST API

InvenioRDM exposes a strong versioned REST API for all operations on the repository, that allows you to build your own integrations on top of InvenioRDM.

## Export formats

InvenioRDM supports exporting a record's metadata in multiple formats such as JSON, Citation Style Language JSON, DataCite JSON/XML, and Dublin Core.

## OAI-PMH server

InvenioRDM ships with a built OAI-PMH server to allow metadata harvesting of records in your repository.

## DataCite-based metadata

InvenioRDMs internal metadata is based on the DataCite Metadata Schema which is a simple yet powerful format for describing nearly any research output (paper, data, software, ...).

## DOI registration via DataCite

InvenioRDM can register DOIs with DataCite for all records, and allows you to write plugins for other identifier schemes.

## Strong support for persistent identifiers

Authors, affiliations, licenses, related papers/datasets, etc. can all be identified via persistent identifiers such as ORCIDs and RORs.

## Metadata-only records

Both records with or without associated files are supported.

## Extended Date Time Format (EDTF) support

Publication dates and other dates support the EDTF format for recording imprecise dates and date ranges such as ``1939/1945``.

## Identifier detection and validation

InvenioRDM comes with support for automatic detection and validation for a large number of persistent identifier schemes (i.e. less typing and clicking for end-users).

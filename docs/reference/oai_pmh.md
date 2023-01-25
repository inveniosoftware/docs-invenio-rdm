# OAI-PMH

InvenioRDM allows to harvest the entire repository via the Open Archives Initiative Protocol for Metadata Harvesting (OAI-PMH). OAI-PMH is a widely used protocol for harvesting metadata and most popular repository software provide support for this protocol.

Metadata and the data files may be either open access and subject to a license described in the metadata or closed access and not available for download.

For a detailed documentation of the protocol, have a look at [http://www.openarchives.org/OAI/openarchivesprotocol.html](http://www.openarchives.org/OAI/openarchivesprotocol.html)

## Base URL

`https://<your-domain>/oai2d`

When running a local setup, this would be [`https://127.0.0.1:5000/oai2d`](https://127.0.0.1:5000/oai2d){:target="_blank"}.

As an example, the `ListRecords` verb would be available under [`https://127.0.0.1:5000/oai2d?verb=ListRecords&metadataPrefix=oai_dc`](https://127.0.0.1:5000/oai2d?verb=ListRecords&metadataPrefix=oai_dc){:target="_blank"}.

## Resumption tokens

Resumption tokens are only valid for 1 minute per default. In case a token expired, you will receive a `422 Unprocessable Entity` HTTP error.

## Rate limit

The OAI-PMH API is rated limited like the REST API - i.e. you will receive a `429 Too Many Requests` HTTP error if you exceed the limit.

## Metadata formats

Metadata for each record is currently available in the following formats:

- `oai_dc` - Dublin Core - Mandatory Dublin Core metadata format without qualification ([ref](http://www.openarchives.org/OAI/2.0/openarchivesprotocol.htm#dublincore){:target="_blank"}).
- `oai_datacite` - OAI DataCite — This metadata format has been specifically established for the dissemination of DataCite records using OAI-PMH.
- `datacite` - DataCite — This metadata format contains only the original DataCite metadata without additions or alterations according to the latest DataCite schema. Please note that this format is not OAI-PMH version 2.0 compliant.

## Sets

The InvenioRDM OAI-PMH server has sets support. Please see the REST API reference for how to create and manage the OAI-PMH sets.

## Deleted records policy

The OAI-PMH server does not maintain information about record deletions and advertises this via the ``Identify`` response. Harvesters are recommended to harvest all identifiers via the ``ListIdentifiers`` and compare against the local set of identifiers to detect deleted records.

## Restricted records

The OAI-PMH standard doesn't say anything about authentication of requests. The OAI-PMH server in InvenioRDM however supports both unauthenticated and authenticated requests using one of InvenioRDM's existing authentication mechanisms (browser sessions or access tokens). This means we're able to serve restricted records via the OAI-PMH server if the request is authenticated.

## OpenAIRE Guidelines

The exposed metadata formats are validated against the [OpenAIRE Guidelines](http://guidelines.openaire.eu).

## Manage sets

You can manage OAI sets by using the administration panel.

### Default sets

*Introduced in InvenioRDM v11*

The OpenAIRE OAI sets is included by default in InvenioRDM.

## Configuration

#### OAI ID Prefix

The prefix that will be applied to the generated OAI-PMH ids. Should be set to the domain of the repository (f.e. `inveniordm.docs.cern.ch`):

```python
OAISERVER_ID_PREFIX = 'inveniordm.docs.cern.ch':
```

#### Admin Emails

The e-mail addresses of administrators of the repository. This should be set accordingly.

```python
OAISERVER_ADMIN_EMAILS = [
    'info@inveniosoftware.org',
]
```

# OAI-PMH
InvenioRDM allows to harvest the entire repository via the Open Archives Initiative Protocol for Metadata Harvesting (OAI-PMH). OAI-PMH is a widely used protocol for harvesting metadata and most popular repository software provide support for this protocol.

Metadata and the data files may be either open access and subject to a license described in the metadata or closed access and not available for download.

For a detailed documentation of the protocol, have a look at [http://www.openarchives.org/OAI/openarchivesprotocol.html](http://www.openarchives.org/OAI/openarchivesprotocol.html)

## ``Base URL``
`https://<your-domain>/oai2d`

When running a local setup, this would be [`https://127.0.0.1:5000/oai2d`](https://127.0.0.1:5000/oai2d){:target="_blank"}.

As an example, the `ListRecords` verb would be available under [`https://127.0.0.1:5000/oai2d?verb=ListRecords&metadataPrefix=oai_dc`](https://127.0.0.1:5000/oai2d?verb=ListRecords&metadataPrefix=oai_dc){:target="_blank"}.

## ``Resumption tokens``
Resumption tokens are only valid for 1 minute per default. In case a token expired, you will receive a `422 Unprocessable Entity` HTTP error.

## ``Rate limit``
The OAI-PMH API is rated limited like the REST API - i.e. you will receive a `429 Too Many Requests` HTTP error if you exceed the limit.

## ``Metadata formats``
Metadata for each record is currently available in the following formats:

`oai_dc`

Mandatory Dublin Core metadata format without qualification ([ref](http://www.openarchives.org/OAI/2.0/openarchivesprotocol.htm#dublincore){:target="_blank"}).

## ``Sets``
Currently, there is no support for sets. It is a feature that is being worked on and will be available in an upcoming version.

## ``Configuration``
#### OAI ID Prefix
The prefix that will be applied to the generated OAI-PMH ids. Should be set to the domain of the repository (f.e. `inveniordm.docs.cern.ch`):
```conf
OAISERVER_ID_PREFIX = 'inveniordm.docs.cern.ch': 
```

#### Admin Emails
The e-mail addresses of administrators of the repository. This should be set accordingly.
```conf
OAISERVER_ADMIN_EMAILS = [
    'info@inveniosoftware.org',
]:
```

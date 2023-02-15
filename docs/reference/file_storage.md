# File storage

There are two different concepts when handling file storage in InvenioRDM. One is the
backend, meaning the actual technology that is used to store it. For example, the local
file system or S3. You can find more information about storage backends in the
[customize](../customize/s3.md) section.

Moreover, the origin or method used to transport the files is also important. In InvenioRDM
there are three defined types.

- Local, which represents the files that are managed by the InvenioRDM instance,
independently of the backend.
- Fetch, these are files that are not managed by the instance but will be transported.
This means that they will eventually become _local_ files.
- Remote, these are represented by a reference to an external storage system. Since
the files are not managed by the instance there is no possible way to guarantee their
availability or integrity. At the moment this type of files are **not supported** by
InvenioRDM.

These file types are stored in the `storage_class` attribute of the file model, and
represented by a one character encoding:

|  Type  | Representation |
|:------:|:--------------:|
| Local  |       L        |
| Fetch  |       F        |
| Remote |       R        |

## Local files (L)

Local files are managed as defined in the
[records and drafts reference](rest_api_drafts_records.md) section.

## Files fetching (F)

_Introduced in InvenioRDM v11_

!!! warning "Experimental feature"

    The file fetching mechanism in InvenioRDM v11 has a few limitations. Be aware that
    future releases of InvenioRDM might introduce breaking changes. We will document them
    as extensively as possible.

    **Use it at your own risk!**

Fetched files accept two more arguments than a local files on their
[initialization](rest_api_drafts_records.md#start-draft-file-uploads): _storage\_class_, and
_uri_:

**Parameters**

| Name            | Type   | Location | Description                |
| --------------- | ------ | -------- | -------------------------- |
| `storage_class` | string | body     | "L"                        |
| `uri`           | string | body     | URL to fetch the file from |

The `uri` must be a URL, accessible from the server's network and resolving to a file
that can be fetched. No authentication mechanism (e.g. `Authorization` header) is
supported for the request process, so any authentication has to be part of the URL itself
(e.g. a token passed in a query string).

**Request**

```http
POST /api/records/{id}/draft/files HTTP/1.1
Content-Type: application/json

[
    {
        "key": "dataset.zip",
        "uri": "https://example.org/files/dataset.zip?token=<auth token>",
        "storage_class": "F",
    },
    ...
]
```

**Response**

```http
HTTP/1.1 201 CREATED
Content-Type: application/json

{
  "enabled": true,
  "default_preview": null,
  "order": [],
  "entries": [
    {
      "key": "dataset.zip",
      "updated": "2020-11-27 11:17:11.002624",
      "created": "2020-11-27 11:17:10.998919",
      "metadata": null,
      "status": "pending",
      "storage_class": "F",
      "uri": "https://example.org/files/dataset.zip?token=<auth token>",
      "links": {
        "content": "/api/records/{id}/draft/files/dataset.zip/content",
        "self": "/api/records/{id}/draft/files/dataset.zip",
        "commit": "/api/records/{id}/draft/files/dataset.zip/commit"
      },
    }
  ],
  "links": {
    "self": "/api/records/{id}/draft/files"
  },
}
```

At this point an asynchronous task will be launched and the file will be transported into
the InvenioRDM instance. Once the file transfer is completed, the status field will be
changed to `completed`. At this point the `storage_class` of the files has also changed
to `L`. The status can be checked using the _files_ url (`/api/records/{id}/draft/files`).
Note, until all the files have been transferred (i.e. their status is `completed`) the
record cannot be published.

More over, while files are being transferred requests to the `content` and `commit`
endpoints are not allowed (disabled).

### Security

By default file fetching will be refused. Files can only be fetched from a configurable
list of trusted domains, which can be configured in the `invenio.cfg` file.

```python
RECORDS_RESOURCES_FILES_ALLOWED_DOMAINS = [
    "example.org",
    "mystoragehosting.com",
]
```

## Remote files (R)

!!! info "Not supported"

    Remote files are currently not supported.

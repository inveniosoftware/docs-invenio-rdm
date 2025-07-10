# File transfer

Two different concepts are involved in the storing of files in InvenioRDM. One is the
**backend**, meaning the actual technology that is used to store a file. For example, the local
file system or [S3](../operate/customize/file-uploads/s3.md). The other concept is the **origin** ,
also known as **method** used to transport the files. There are three such defined methods.

- *Local*, which represents the files that are managed by the InvenioRDM instance,
independently of the backend.
- *Fetch*, these are files that are not immediately managed by the instance as they need to be downloaded first.
This means that they will eventually become _local_ files.
- *Multipart*, these are files that are uploaded in parts. Users can upload parts
in parallel or can retransmit each part if the upload fails, for example due to
network errors. After upload, the parts are assembled into a single file and the
file becomes a _local_ file.
- *Remote*, these are represented by a reference to an external storage system. Since
the files are not managed by the instance there is no possible way to guarantee their
availability or integrity.

These types of transfer mechanisms are stored in the `transfer.type` attribute of the file model, and
represented by a one character encoding:

|    Type    | Representation |
|:----------:|:--------------:|
| Local      |       L        |
| Fetch      |       F        |
| Multipart  |       M        |
| Remote     |       R        |

Example of selecting transfer type on file creation:

```http
POST /api/records/{id}/draft/files
Content-Type: application/json

[{
    "key": "dataset.zip",
    "transfer": {
      "type": "F",
      "url": "https://example.org/files/dataset.zip?token=<auth token>"
    }
    "metadata": {...}
}]
```

## Local files (L)

Local files are managed as defined in the
[records and drafts reference](rest_api_drafts_records.md) section.

## Files fetching (F)

During initialization, fetched files are created using [the same protocol as local files](rest_api_drafts_records.md#start-draft-file-uploads).
Additionally you need to provide a `transfer` object with `type` and `url` fields.

**Parameters**

| Name            | Type   | Location | Description                |
| --------------- | ------ | -------- | -------------------------- |
| `type`          | string | body     | "F"                        |
| `url`           | string | body     | URL to fetch the file from |

The `url` must be a URL, accessible from the server's network and resolving to a file
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
        "transfer": {
          "type": "F",
          "url": "https://example.org/files/dataset.zip?token=<auth token>",
        }
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
      "transfer": {
        "type": "F",
      },
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

**Note**: The response does not contain the URL of the fetched file. This is intentional
as the URL might contain sensitive information (e.g. a token) that should not be exposed
to users.

At this point an asynchronous task will be launched and the file will be transported into
the InvenioRDM instance. Once the file transfer is completed, the status field will be
changed to `completed`. At this point the `transfer.type` of the files has also changed
to `L`. The status can be checked using the _files_ url (`/api/records/{id}/draft/files`).
Note, until all the files have been transferred (i.e. their status is `completed`) the
record cannot be published.

Moreover, while files are being transferred requests to the `content` and `commit`
endpoints are not allowed (disabled).

### Error handling

If the file fetching fails, the status of the file will be set to `failed`
and the error message will be stored in the `transfer.error` field.

### Security

By default file fetching will be refused. Files can only be fetched from a configurable
list of trusted domains, which can be configured in the `invenio.cfg` file.

```python
RECORDS_RESOURCES_FILES_ALLOWED_DOMAINS = [
    "example.org",
    "mystoragehosting.com",
]
```

As fetching large files from external sources can take a long time and may deplete
the pool of workers, this type of file uploads are restricted to trusted users only.
By default, only users with the superuser access can add this type of files.

You can change this behavior in your `invenio.cfg` file:

```python
from invenio_records_resources.services.files.generators import IfTransferType
from invenio_records_resources.services.files.transfer import FETCH_TRANSFER_TYPE
from invenio_administration.generators import Administration

class MyRepositoryPermissionPolicy(RDMRecordPermissionPolicy):
  can_draft_create_files = RDMRecordPermissionPolicy.can_draft_transfer_files + [
        IfTransferType(FETCH_TRANSFER_TYPE, Administration())
  ]

RDM_PERMISSION_POLICY = MyRepositoryPermissionPolicy
```

## Remote files (R)

To link to a remote file, the `transfer` section must contain the `type=R` and `url` fields.

**Request**

```http
POST /api/records/{id}/draft/files HTTP/1.1
Content-Type: application/json

[
    {
        "key": "dataset.zip",
        "size": 1234567,
        "checksum": "md5:1234567890abcdef1234567890abcdef",
        "transfer": {
          "type": "R",
          "url": "https://mystoragehosting.org/files/dataset.zip",
        }
    },
    ...
]
```

**Note:** The `size` and `checksum` fields are optional, but they are recommended to
ensure that users can verify the integrity of the downloaded file.

There is no need to call the `commit` endpoint for remote files. The file is considered
committed as soon as it is created.

### Accessing remote files

Later on, when user tries to access the file, a 302 redirect will be returned to the
`url` provided in the request.

**Request**

```http
GET /api/records/{id}/draft/files/dataset.zip/content HTTP/1.1
```

**Response**

```http
HTTP/1.1 302 FOUND
Location: https://mystoragehosting.org/files/dataset.zip
```

### Security

When a `302` redirect is sent to the user, they will retrieve the file directly
by following the returned URL. Therefore, you must ensure:

1. **Network Access**: The file’s URL is reachable from the user’s network.
2. **No Sensitive Data**: The URL does not include any sensitive information (such as tokens).

By default, InvenioRDM refuses references to external files. Files can only be referenced
from a “trusted domains” list, which you can configure in your `invenio.cfg` file:

```python
RECORDS_RESOURCES_FILES_ALLOWED_REMOTE_DOMAINS = [
    "mystoragehosting.org",
]
```

Since the repository cannot guarantee a remote file’s availability or integrity,
file uploads are also restricted to trusted users only. By default, only users with
the superuser access can upload remote files.

You can change this behavior in your `invenio.cfg` file:

```python
from invenio_records_resources.services.files.generators import IfTransferType
from invenio_records_resources.services.files.transfer import REMOTE_TRANSFER_TYPE
from invenio_administration.generators import Administration

class MyRepositoryPermissionPolicy(RDMRecordPermissionPolicy):
  can_draft_create_files = RDMRecordPermissionPolicy.can_draft_transfer_files + [
        IfTransferType(REMOTE_TRANSFER_TYPE, Administration())
  ]

RDM_PERMISSION_POLICY = MyRepositoryPermissionPolicy
```

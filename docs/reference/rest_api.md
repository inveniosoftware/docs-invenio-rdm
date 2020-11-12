# REST API reference

**Summary**

The following document is a reference guide for all the REST APIs that InvenioRDM exposes.

**Intended audience**

This guide is intended for advanced users, and developers of InvenioRDM that have some experience with using REST APIs and are aware of the expected functionality a repository would be exposing.

## Authentication

The only authentication method supported at the moment for REST API calls is by using Bearer tokens that you can generate at the "Applications" section of your user account's settings of your InvenioRDM instance. There are two ways to pass the tokens in your requests.

**Authorization HTTP header (recommended)**

```shell
curl -H "Authorization: Bearer API-TOKEN" https://127.0.0.1:5000/api/records
```

**`access_token` HTTP query string parameter**

```shell
curl https://127.0.0.1:5000/api/records?access_token=API-TOKEN
```

### Scopes

!!! warning "Work in progress"

    The available scopes for generated token are subject to change when the access control mechanisms to records are finalized.

When you create your API token you can also specify **scopes** that control what kind of resources and actions you can access using your token.

| Scope        | Description                               |
| ------------ | ----------------------------------------- |
| `user:email` | Allows access to the user's email address |

## General information

### Timestamps

Timestamps are in UTC and formatted according to [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601).

### Pretty print JSON

If you are exploring the API via a browser, you can have the JSON formatted by
adding ``prettyprint=1`` in the query string.

**Example request**

```http
GET /api/records?prettyprint=1 HTTP/1.1
```

## Drafts

Used for interacting with unpublished or edited draft records.

!!! info "Authentication required"

    All requests to the draft-related REST API endpoints require authentication.

### Create a draft record

`POST /api/records`

**Parameters**

| Name       | Type   | Location | Description                                                  |
| ---------- | ------ | -------- | ------------------------------------------------------------ |
| `access`   | object | body     | [Access options](metadata.md#access-information) for the record. |
| `files`    | object | body     | Files options for the record. |
| `files.enabled` | boolean | body     | *Required*. Should files be attached to this record or not. |
| `metadata` | object | body     | [Metadata](metadata.md#metadata) of the record. |


**Request**

```http
POST /api/records HTTP/1.1
Content-Type: application/json

{
  "access": {
    "record": "public",
    "files": "public"
  },
  "files": {
    "enabled": true
  },
  "metadata": {
    "resource_type": { "type": "image", "subtype": "image-photo" },
    "title": "A Romans story",
    "publication_date": "2020-06-01",
    "creators": [
      {
        "person_or_org": {
          "family_name": "Brown",
          "given_name": "Troy",
          "type": "personal"
        }
      },
      {
        "person_or_org": {
          "family_name": "Collins",
          "given_name": "Thomas",
          "identifiers": [
            {"scheme": "orcid", "identifier": "0000-0002-1825-0097"}
          ],
          "name": "Collins, Thomas",
          "type": "personal"
        },
        "affiliations": [
          {
            "identifiers": [
              {"scheme": "ror", "identifier": "03yrm5c26"}
            ],
            "name": "Entity One"
          }
        ]
      }
    ]
  }
}
```

**Response**

```http
HTTP/1.1 201 CREATED
Content-Type: application/json

{
  "access": {
    "record": "public",
    "files": "public",
    "embargo": {
      "reason": null,
      "active": false
    }
  },
  "created": "2020-11-27 10:52:23.945755",
  "expires_at": "2020-11-27 10:52:23.945868",
  "files": {
    "enabled": true
  },
  "id": "{id}",
  "is_published": false,
  "links": {
    "latest": "{scheme+hostname}/api/records/{id}/versions/latest",
    "versions": "{scheme+hostname}/api/records/{id}/versions",
    "self_html": "{scheme+hostname}/uploads/{id}",
    "publish": "{scheme+hostname}/api/records/{id}/draft/actions/publish",
    "latest_html": "{scheme+hostname}/records/{id}/latest",
    "self": "{scheme+hostname}/api/records/{id}/draft",
    "files": "{scheme+hostname}/api/records/{id}/draft/files",
    "access_links": "{scheme+hostname}/api/records/{id}/access/links",
  },
  "metadata": {
    "resource_type": { "subtype": "image-photo", "type": "image" },
    "title": "A Romans story",
    "publication_date": "2020-06-01",
    "creators": [
      {
        "person_or_org": {
          "family_name": "Brown",
          "given_name": "Troy",
          "type": "personal"
        }
      },
      {
        "person_or_org": {
          "family_name": "Collins",
          "given_name": "Thomas",
          "identifiers": [
            {"scheme": "orcid", "identifier": "0000-0002-1825-0097"}
          ],
          "name": "Collins, Thomas",
          "type": "personal"
        },
        "affiliations": [
          {
            "identifiers": [
              {"scheme": "ror", "identifier": "03yrm5c26"}
            ],
            "name": "Entity One"
          }
        ]
      }
    ],
  },
  "parent": {
    "id": "{parent-id}",
    "access": {
      "owned_by": [
        {
          "user": {user-id}
        }
      ],
      "links": []
    }
  },
  "revision_id": 3,
  "updated": "2020-11-27 10:52:23.969244",
  "versions": {
    "index": 1,
    "is_latest": false,
    "is_latest_draft": true
  }
}
```


### Get a draft record

`GET /api/records/{id}/draft`

**Parameters**

| Name       | Type   | Location | Description                                                  |
| ---------- | ------ | -------- | ------------------------------------------------------------ |
| `id`       | string | path     | Identifier of the record, e.g.  `4d0ns-ntd89`                |
| `accept`   | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |

**Request**

```http
GET /api/records/{id}/draft HTTP/1.1
Accept: application/json
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "access": {
    "record": "public",
    "files": "public",
    "embargo": {
      "reason": null,
      "active": false
    }
  },
  "created": "2020-11-27 10:52:23.945755",
  "expires_at": "2020-11-27 10:52:23.945868",
  "files": {
    "enabled": true
  },
  "id": "{id}",
  "is_published": false,
  "links": {
    "latest": "{scheme+hostname}/api/records/{id}/versions/latest",
    "versions": "{scheme+hostname}/api/records/{id}/versions",
    "self_html": "{scheme+hostname}/uploads/{id}",
    "publish": "{scheme+hostname}/api/records/{id}/draft/actions/publish",
    "latest_html": "{scheme+hostname}/records/{id}/latest",
    "self": "{scheme+hostname}/api/records/{id}/draft",
    "files": "{scheme+hostname}/api/records/{id}/draft/files",
    "access_links": "{scheme+hostname}/api/records/{id}/access/links",
  },
  "metadata": {
    "resource_type": { "subtype": "image-photo", "type": "image" },
    "title": "A Romans story",
    "publication_date": "2020-06-01",
    "creators": [
      "person_or_org": {
        "family_name": "Brown",
        "given_name": "Troy",
        "type": "personal"
      },
      {
        "person_or_org": {
          "family_name": "Collins",
          "given_name": "Thomas",
          "identifiers": [
            {"scheme": "orcid", "identifier": "0000-0002-1825-0097"}
          ],
          "name": "Collins, Thomas",
          "type": "personal"
        },
        "affiliations": [
          {
            "identifiers": [
              {"scheme": "ror", "identifier": "03yrm5c26"}
            ],
            "name": "Entity One"
          }
        ]
      }
    ],
  },
  "parent": {
    "id": "{parent-id}",
    "access": {
      "owned_by": [
        {
            "user": {user-id}
        }
      ],
      "links": []
    }
  },
  "revision_id": 3,
  "updated": "2020-11-27 10:52:23.969244",
  "versions": {
    "index": 1,
    "is_latest": false,
    "is_latest_draft": true
  }
}
```

### Update a draft record

`PUT /api/records/{id}/draft`

**Parameters**

| Name       | Type   | Location | Description                                                  |
| ---------- | ------ | -------- | ------------------------------------------------------------ |
| `id`       | string | path     | Identifier of the record, e.g.  `4d0ns-ntd89`                |
| `access`   | object | body     | [Access options](metadata.md#access-information) for the record. |
| `files`    | object | body     | Files options for the record. |
| `files.enabled` | boolean | body     | *Required*. Should files be attached to this record or not. |
| `metadata` | object | body     | [Metadata](metadata.md#metadata) of the record. |

**Request**

```http
PUT /api/records/{id}/draft HTTP/1.1
Content-Type: application/json

{
  "access": {
    "record": "restricted",
    "files": "restricted"
  },
  "files": {
    "enabled": false,
  },
  "metadata": {
    "resource_type": { "type": "image", "subtype": "image-photo" },
    "title": "An Updated Romans story",
    "publication_date": "2020-06-01",
    "creators": [
      {
        "person_or_org": {
          "family_name": "Brown",
          "given_name": "Troy",
          "type": "personal"
        }
      },
      {
        "person_or_org": {
          "family_name": "Collins",
          "given_name": "Thomas",
          "identifiers": [
            {"scheme": "orcid", "identifier": "0000-0002-1825-0097"}
          ],
          "name": "Collins, Thomas",
          "type": "personal"
        },
        "affiliations": [
          {
            "identifiers": [
              {"scheme": "ror", "identifier": "03yrm5c26"}
            ],
            "name": "Entity One"
          }
        ]
      }
    ]
  }
}
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json


{
  "access": {
    "record": "restricted",
    "files": "restricted",
    "embargo": {
      "reason": null,
      "active": false
    }
  },
  "created": "2020-11-27 10:52:23.945755",
  "expires_at": "2020-11-27 10:52:23.945868",
  "files": {
    "enabled": false
  },
  "id": "{id}",
  "is_published": false,
  "links": {
    "latest": "{scheme+hostname}/api/records/{id}/versions/latest",
    "versions": "{scheme+hostname}/api/records/{id}/versions",
    "self_html": "{scheme+hostname}/uploads/{id}",
    "publish": "{scheme+hostname}/api/records/{id}/draft/actions/publish",
    "latest_html": "{scheme+hostname}/records/{id}/latest",
    "self": "{scheme+hostname}/api/records/{id}/draft",
    "files": "{scheme+hostname}/api/records/{id}/draft/files",
    "access_links": "{scheme+hostname}/api/records/{id}/access/links",
  },
  "metadata": {
    "resource_type": { "subtype": "image-photo", "type": "image" },
    "title": "An Updated Romans story",
    "publication_date": "2020-06-01",
    "creators": [
      "person_or_org": {
        "family_name": "Brown",
        "given_name": "Troy",
        "type": "personal"
      },
      {
        "person_or_org": {
          "family_name": "Collins",
          "given_name": "Thomas",
          "identifiers": [
            {"scheme": "orcid", "identifier": "0000-0002-1825-0097"}
          ],
          "name": "Collins, Thomas",
          "type": "personal"
        },
        "affiliations": [
          {
            "identifiers": [
              {"scheme": "ror", "identifier": "03yrm5c26"}
            ],
            "name": "Entity One"
          }
        ]
      }
    ],
  },
  "parent": {
    "id": "{parent-id}",
    "access": {
      "owned_by": [
        {
            "user": {user-id}
        }
      ],
      "links": []
    }
  },
  "revision_id": 3,
  "updated": "2020-11-27 10:52:23.969244",
  "versions": {
    "index": 1,
    "is_latest": false,
    "is_latest_draft": true
  }
}
```

### Publish a draft record

`POST /api/records/{id}/draft/actions/publish`

**Parameters**

| Name | Type   | Location | Description                                   |
| ---- | ------ | -------- | --------------------------------------------- |
| `id` | string | path     | Identifier of the record, e.g.  `4d0ns-ntd89` |

**Request**

```http
POST /api/records/{id}/draft/actions/publish HTTP/1.1
```

**Response**

```http
HTTP/1.1 202 ACCEPTED
Content-Type: application/json

{
  "access": {
    "record": "restricted",
    "files": "restricted",
    "embargo": {
      "reason": null,
      "active": false
    }
  },
  "created": "2020-11-27 10:52:23.945755",
  "expires_at": "2020-11-27 10:52:23.945868",
  "files": {
    "enabled": false
  },
  "id": "{id}",
  "is_published": true,
  "links": {
    "latest": "{scheme+hostname}/api/records/{id}/versions/latest",
    "versions": "{scheme+hostname}/api/records/{id}/versions",
    "self_html": "{scheme+hostname}/records/{id}",
    "latest_html": "{scheme+hostname}/records/{id}/latest",
    "self": "{scheme+hostname}/api/records/{id}",
    "files": "{scheme+hostname}/api/records/{id}/files",
    "access_links": "{scheme+hostname}/api/records/{id}/access/links",
  },
  "metadata": {
    "resource_type": { "subtype": "image-photo", "type": "image" },
    "title": "An Updated Romans story",
    "publication_date": "2020-06-01",
    "creators": [
      "person_or_org": {
        "family_name": "Brown",
        "given_name": "Troy",
        "type": "personal"
      },
      {
        "person_or_org": {
          "family_name": "Collins",
          "given_name": "Thomas",
          "identifiers": [
            {"scheme": "orcid", "identifier": "0000-0002-1825-0097"}
          ],
          "name": "Collins, Thomas",
          "type": "personal"
        },
        "affiliations": [
          {
            "identifiers": [
              {"scheme": "ror", "identifier": "03yrm5c26"}
            ],
            "name": "Entity One"
          }
        ]
      }
    ],
  },
  "parent": {
    "id": "{parent-id}",
    "access": {
      "owned_by": [
        {
            "user": {user-id}
        }
      ],
      "links": []
    }
  },
  "revision_id": 3,
  "updated": "2020-11-27 10:52:23.969244",
  "versions": {
    "index": 1,
    "is_latest": true,
    "is_latest_draft": true
  }
}
```

### Edit a published record (Create a draft record from a published record)

`POST /api/records/{id}/draft`

**Parameters**

| Name | Type   | Location | Description                                   |
| ---- | ------ | -------- | --------------------------------------------- |
| `id` | string | path     | Identifier of the record, e.g.  `4d0ns-ntd89` |

**Request**

```http
POST /api/records/{id}/draft HTTP/1.1
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json


{
  "access": {
    "record": "restricted",
    "files": "restricted",
    "embargo": {
      "reason": null,
      "active": false
    }
  },
  "created": "2020-11-27 10:52:23.945755",
  "expires_at": "2020-11-27 10:52:23.945868",
  "files": {
    "enabled": false
  },
  "id": "{id}",
  "is_published": false,
  "links": {
    "latest": "{scheme+hostname}/api/records/{id}/versions/latest",
    "versions": "{scheme+hostname}/api/records/{id}/versions",
    "self_html": "{scheme+hostname}/uploads/{id}",
    "publish": "{scheme+hostname}/api/records/{id}/draft/actions/publish",
    "latest_html": "{scheme+hostname}/records/{id}/latest",
    "self": "{scheme+hostname}/api/records/{id}/draft",
    "files": "{scheme+hostname}/api/records/{id}/draft/files",
    "access_links": "{scheme+hostname}/api/records/{id}/access/links",
  },
  "metadata": {
    "resource_type": { "subtype": "image-photo", "type": "image" },
    "title": "An Updated Romans story",
    "publication_date": "2020-06-01",
    "creators": [
      "person_or_org": {
        "family_name": "Brown",
        "given_name": "Troy",
        "type": "personal"
      },
      {
        "person_or_org": {
          "family_name": "Collins",
          "given_name": "Thomas",
          "identifiers": [
            {"scheme": "orcid", "identifier": "0000-0002-1825-0097"}
          ],
          "name": "Collins, Thomas",
          "type": "personal"
        },
        "affiliations": [
          {
            "identifiers": [
              {"scheme": "ror", "identifier": "03yrm5c26"}
            ],
            "name": "Entity One"
          }
        ]
      }
    ],
  },
  "parent": {
    "id": "{parent-id}",
    "access": {
      "owned_by": [
        {
            "user": {user-id}
        }
      ],
      "links": []
    }
  },
  "revision_id": 3,
  "updated": "2020-11-27 10:52:23.969244",
  "versions": {
    "index": 1,
    "is_latest": true,
    "is_latest_draft": true
  }
}
```

## Draft files

Used to manage a draft's files.

### List a draft's files

`GET /api/records/{id}/draft/files`

**Parameters**

| Name | Type   | Location | Description                                   |
| ---- | ------ | -------- | --------------------------------------------- |
| `id` | string | path     | Identifier of the record, e.g.  `4d0ns-ntd89` |

**Request**

```http
GET /api/records/{id}/draft/files HTTP/1.1
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "default_preview": null,
  "enabled": true,
  "entries": [],
  "links": {
    "self": "/api/records/{id}/draft/files"
  },
  "order": []
}
```

### Start draft file upload(s)

`POST /api/records/{id}/draft/files`

**Parameters**

| Name          | Type   | Location | Description                                                  |
| ------------- | ------ | -------- | ------------------------------------------------------------ |
| `id`          | string | path     | Identifier of the record, e.g.  `4d0ns-ntd89`                |
| `<top-level>` | array  | body     | Array of objects describing the file uploads to be initialized. |
| `[].key`      | string | body     | Name of the file to be uploaded.                             |

**Request**

```http
POST /api/records/{id}/draft/files HTTP/1.1
Content-Type: application/json

[
  {"key": "figure.png"},
  {"key": "article.pdf"},
  {"key": "data.zip"}
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
      "key": "figure.png",
      "updated": "2020-11-27 11:17:11.002624",
      "created": "2020-11-27 11:17:10.998919",
      "metadata": null,
      "status": "pending",
      "links": {
        "content": "/api/records/{id}/draft/files/figure.png/content",
        "self": "/api/records/{id}/draft/files/figure.png",
        "commit": "/api/records/{id}/draft/files/figure.png/commit"
      },
    },
        {
      "key": "article.pdf",
      "updated": "2020-11-27 11:17:11.002624",
      "created": "2020-11-27 11:17:10.998919",
      "metadata": null,
      "status": "pending",
      "links": {
        "content": "/api/records/{id}/draft/files/article.pdf/content",
        "self": "/api/records/{id}/draft/files/article.pdf",
        "commit": "/api/records/{id}/draft/files/article.pdf/commit"
      },
    },
    {
      "key": "data.zip",
      "updated": "2020-11-27 11:17:11.002624",
      "created": "2020-11-27 11:17:10.998919",
      "metadata": null,
      "status": "pending",
      "links": {
        "content": "/api/records/{id}/draft/files/data.zip/content",
        "self": "/api/records/{id}/draft/files/data.zip",
        "commit": "/api/records/{id}/draft/files/data.zip/commit"
      },
    }
  ],
  "links": {
    "self": "/api/records/{id}/draft/files"
  },
}
```

### Upload a draft file's content

`PUT /api/records/{id}/draft/files/{filename}/content`

**Parameters**

| Name             | Type    | Location | Description                                       |
| ---------------- | ------- | -------- | ------------------------------------------------- |
| `id`             | string  | path     | Identifier of the record, e.g.  `4d0ns-ntd89`     |
| `filename`       | string  | path     | Name of the file.                                 |
| `content-type`   | string  | header   | Should always be `application/octet-stream`.      |
| `content-length` | integer | header   | Size of the content in bytes (optional).          |
| `<content>`      | bytes   | body     | The raw bytes of the file content to be uploaded. |

**Request**

```http
PUT /api/records/{id}/draft/files/{filename}/content HTTP/1.1
Content-Type: application/octet-stream

<...file binary data...>
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "key": "{filename}",
  "updated": "2020-11-27 11:17:11.002624",
  "created": "2020-11-27 11:17:10.998919",
  "metadata": null,
	"status": "pending",
	"links": {
    "content": "/api/records/{id}/draft/files/{filename}/content",
    "self": "/api/records/{id}/draft/files/{filename}",
    "commit": "/api/records/{id}/draft/files/{filename}/commit"
  },
}
```

**Code sample**

```shell
curl \
  --request PUT \
  --header "Content-Type: application/octet-stream" \
  https://127.0.0.1:5000//api/records/{id}/draft/files/{filename}/content \
  --upload-file /path/to/file
```

### Complete a draft file upload

`POST /api/records/{id}/draft/files/{filename}/commit`

**Parameters**

| Name       | Type   | Location | Description                                   |
| ---------- | ------ | -------- | --------------------------------------------- |
| `id`       | string | path     | Identifier of the record, e.g.  `4d0ns-ntd89` |
| `filename` | string | path     | Name of the file.                             |

**Request**

```http
POST /api/records/{id}/draft/files/{filename}/commit HTTP/1.1
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "key": "{filename}",
  "updated": "2020-11-27 11:26:04.607831",
  "created": "2020-11-27 11:17:10.998919",
  "checksum": "md5:6ef4267f0e710357c895627e931f16cd",
  "mimetype": "image/png",
  "size": 89364.0,
  "status": "completed",
  "metadata": null,
  "file_id": "2151fa94-6dc3-4965-8df9-ec73ceb9175c",
  "version_id": "57ad8c66-b934-49c9-a46f-38bf5aa0374f",
  "bucket_id": "90b5b318-114a-4b87-bc9d-0d018b9363d3",
  "storage_class": "S",
  "links": {
    "content": "/api/records/{id}/draft/files/{filename}/content",
    "self": "/api/records/{id}/draft/files/{filename}",
    "commit": "/api/records/{id}/draft/files/{filename}/commit"
  },
}
```

### Get a draft file's metadata

`GET /api/records/{id}/draft/files/{filename}`

**Parameters**

| Name       | Type   | Location | Description                                   |
| ---------- | ------ | -------- | --------------------------------------------- |
| `id`       | string | path     | Identifier of the record, e.g.  `4d0ns-ntd89` |
| `filename` | string | path     | Name of the file.                             |

**Request**

```http
GET /api/records/{id}/draft/files/{filename} HTTP/1.1
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "key": "{filename}",
  "updated": "2020-11-27 11:26:04.607831",
  "created": "2020-11-27 11:17:10.998919",
  "checksum": "md5:6ef4267f0e710357c895627e931f16cd",
  "mimetype": "image/png",
  "size": 89364.0,
  "status": "completed",
  "metadata": null,
  "file_id": "2151fa94-6dc3-4965-8df9-ec73ceb9175c",
  "version_id": "57ad8c66-b934-49c9-a46f-38bf5aa0374f",
  "bucket_id": "90b5b318-114a-4b87-bc9d-0d018b9363d3",
  "storage_class": "S",
  "links": {
    "content": "/api/records/{id}/draft/files/{filename}/content",
    "self": "/api/records/{id}/draft/files/{filename}",
    "commit": "/api/records/{id}/draft/files/{filename}/commit"
  },
}
```

### Download a draft file

`GET /api/records/{id}/draft/files/{filename}/content`

**Parameters**

| Name       | Type   | Location | Description                                  |
| ---------- | ------ | -------- | -------------------------------------------- |
| `id`       | string | path     | Identifier of the record, e.g. `cbc2k-q9x58` |
| `filename` | string | path     | Name of a file                               |

**Request**

```http
GET /api/records/{id}/draft/files/{filename}/content HTTP/1.1
```

**Response**

```http
HTTP/1.1 200 OK
Content-Disposition: inline
Content-Length: 76122
Content-MD5: 71449104d017a6056ac1a5fb58754975
Content-Type: image/pdf
Date: Thu, 26 Nov 2020 18:35:33 GMT
ETag: "md5:71449104d017a6056ac1a5fb58754975"
Last-Modified: Thu, 26 Nov 2020 14:30:06 GMT

<...file binary data...>
```

### Delete a draft file

`DELETE /api/records/{id}/draft/files/{filename}`

**Parameters**

| Name       | Type   | Location | Description                                   |
| ---------- | ------ | -------- | --------------------------------------------- |
| `id`       | string | path     | Identifier of the record, e.g.  `4d0ns-ntd89` |
| `filename` | string | path     | Name of the file.                             |

**Request**

```http
DELETE /api/records/{id}/draft/files/{filename} HTTP/1.1
```

**Response**

```http
HTTP/1.1 204 No Content
Content-Type: application/json

{
  "key": "{filename}",
  "updated": "2020-11-27 11:26:04.607831",
  "created": "2020-11-27 11:17:10.998919",
  "checksum": "md5:6ef4267f0e710357c895627e931f16cd",
  "mimetype": "image/png",
  "size": 89364.0,
  "status": "completed",
  "metadata": null,
  "file_id": "2151fa94-6dc3-4965-8df9-ec73ceb9175c",
  "version_id": "57ad8c66-b934-49c9-a46f-38bf5aa0374f",
  "bucket_id": "90b5b318-114a-4b87-bc9d-0d018b9363d3",
  "storage_class": "S",
  "links": {
    "content": "/api/records/{id}/draft/files/{filename}/content",
    "self": "/api/records/{id}/draft/files/{filename}",
    "commit": "/api/records/{id}/draft/files/{filename}/commit"
  },
}
```

### Modify a draft's files options

Used for enabling/disabling files for drafts, setting the default previewed file, ordering files, etc.

`PUT /api/records/{id}/draft/files`

**Parameters**

| Name              | Type    | Location | Description                                                  |
| ----------------- | ------- | -------- | ------------------------------------------------------------ |
| `id`              | string  | path     | Identifier of the record, e.g.  `4d0ns-ntd89`                |
| `enabled`         | boolean | body     | Set to `false` to disable files for the record.              |
| `default_preview` | string  | body     | Filename of the file to be previewed by default on the published record. |

**Request**

```http
PUT /api/records/{id}/draft/files HTTP/1.1
Content-Type: application/json

{
  "enabled": true,
  "default_preview": "article.pdf",
}
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "default_preview": "article.pdf",
  "enabled": true,
  "entries": [
    {
      "key": "figure.png",
      "updated": "2020-11-27 11:17:11.002624",
      "created": "2020-11-27 11:17:10.998919",
      "metadata": null,
      "status": "pending",
      "links": {
        "content": "/api/records/{id}/draft/files/figure.png/content",
        "self": "/api/records/{id}/draft/files/figure.png",
        "commit": "/api/records/{id}/draft/files/figure.png/commit"
      },
    },
    {
      "key": "article.pdf",
      "updated": "2020-11-27 11:17:11.002624",
      "created": "2020-11-27 11:17:10.998919",
      "metadata": null,
      "status": "pending",
      "links": {
        "content": "/api/records/{id}/draft/files/article.pdf/content",
        "self": "/api/records/{id}/draft/files/article.pdf",
        "commit": "/api/records/{id}/draft/files/article.pdf/commit"
      },
    }
  ],
  "links": {
    "self": "/api/records/{id}/draft/files"
  },
  "order": []
}
```


## Records

Used for interacting with published records.

### Get a record

`GET /api/records/{id}`

**Parameters**

| Name     | Type   | Location | Description                                                  |
| -------- | ------ | -------- | ------------------------------------------------------------ |
| `id`     | string | path     | Identifier of the record, e.g. `cbc2k-q9x58`                 |
| `accept` | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |

**Request**

```http
GET /api/records/{id} HTTP/1.1
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "access": {
    "record": "restricted",
    "files": "restricted",
    "embargo": {
      "reason": null,
      "active": false
    }
  },
  "created": "2020-11-27 10:52:23.945755",
  "expires_at": "2020-11-27 10:52:23.945868",
  "files": {
    "enabled": true
  },
  "id": "{id}",
  "is_published": true,
  "links": {
    "latest": "{scheme+hostname}/api/records/{id}/versions/latest",
    "versions": "{scheme+hostname}/api/records/{id}/versions",
    "self_html": "{scheme+hostname}/records/{id}",
    "latest_html": "{scheme+hostname}/records/{id}/latest",
    "self": "{scheme+hostname}/api/records/{id}",
    "files": "{scheme+hostname}/api/records/{id}/files",
    "access_links": "{scheme+hostname}/api/records/{id}/access/links",
  },
  "metadata": {
    "resource_type": { "subtype": "image-photo", "type": "image" },
    "title": "An Updated Romans story",
    "publication_date": "2020-06-01",
    "creators": [
      "person_or_org": {
        "family_name": "Brown",
        "given_name": "Troy",
        "type": "personal"
      },
      {
        "person_or_org": {
          "family_name": "Collins",
          "given_name": "Thomas",
          "identifiers": [
            {"scheme": "orcid", "identifier": "0000-0002-1825-0097"}
          ],
          "name": "Collins, Thomas",
          "type": "personal"
        },
        "affiliations": [
          {
            "identifiers": [
              {"scheme": "ror", "identifier": "03yrm5c26"}
            ],
            "name": "Entity One"
          }
        ]
      }
    ],
  },
  "parent": {
    "id": "{parent-id}",
    "access": {
      "owned_by": [
        {
            "user": {user-id}
        }
      ],
      "links": []
    }
  },
  "revision_id": 3,
  "updated": "2020-11-27 10:52:23.969244",
  "versions": {
    "index": 1,
    "is_latest": true,
    "is_latest_draft": true
  }
}
```

### Search records

**Parameters**

| Name           | Type    | Location | Description                                                  |
| -------------- | ------- | -------- | ------------------------------------------------------------ |
| `q`            | string  | query    | Search query used to filter results based on [ElasticSearch's query string syntax](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax). |
| `sort`         | string  | query    | Sort search results.                                         |
| `size`         | integer | query    | Specify number of items in the results page (default: 10).   |
| `page`         | integer | query    | Specify the page of results.                                 |
| `allversions`  | boolean | query    | Specify if all versions should be included.                  |
| `accept`       | string  | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |

**Request**

```http
GET /api/records HTTP/1.1
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "aggregations": {...},
  "hits": {...},
  "links": {...},
  "sortBy": ...,
}
```

Each hit looks like a record above.

## Record files

### List a record's files

`GET /api/records/{id}/files`

**Parameters**

| Name     | Type   | Location | Description                                  |
| -------- | ------ | -------- | -------------------------------------------- |
| `id`     | string | path     | Identifier of the record, e.g. `cbc2k-q9x58` |
| `accept` | string | header   | - `application/json` (default)               |

**Request**

```http
GET /api/records/{id}/files HTTP/1.1
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "enabled": true,
  "default_preview": "article.pdf",
  "order": [],
  "entries": [
  	{
      "key": "article.pdf",
      "created": "2020-11-26 14:30:53.911912",
			"updated": "2020-11-26 14:30:53.920544",
      "checksum": "md5:71449104d017a6056ac1a5fb58754975",
      "mimetype": "application/pdf",
      "size": 76122,
      "status": "completed",
      "metadata": {...},
      "file_id": "...",
      "version_id": "...",
      "bucket_id": "...",
      "storage_class": "S",
      "links": {
        "content": "/api/records/{id}/files/article.pdf/content",
        "self": "/api/records/{id}/files/article.pdf"
      }
    }
  ]
  "links": {...},
}
```

### Get a record file's metadata

`GET /api/records/{id}/files/{filename}`

**Parameters**

| Name       | Type   | Location | Description                                  |
| ---------- | ------ | -------- | -------------------------------------------- |
| `id`       | string | path     | Identifier of the record, e.g. `cbc2k-q9x58` |
| `filename` | string | path     | Name of a file                               |
| `accept`   | string | header   | - `application/json` (default)               |

**Request**

```http
GET /api/records/{id}/files/{filename} HTTP/1.1
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "key": "{filename}",
  "created": "2020-11-26 14:30:53.911912",
  "updated": "2020-11-26 14:30:53.920544",
  "checksum": "md5:71449104d017a6056ac1a5fb58754975",
  "mimetype": "application/pdf",
  "size": 76122,
  "status": "completed",
  "metadata": {...},
  "file_id": "...",
  "version_id": "...",
  "bucket_id": "...",
  "storage_class": "S",
  "links": {
    "content": "/api/records/{id}/files/{filename}/content",
    "self": "/api/records/{id}/files/{filename}"
  }
}
```

### Download a record file

`GET /api/records/{id}/files/{filename}/content`

**Parameters**

| Name       | Type   | Location | Description                                  |
| ---------- | ------ | -------- | -------------------------------------------- |
| `id`       | string | path     | Identifier of the record, e.g. `cbc2k-q9x58` |
| `filename` | string | path     | Name of a file                               |

**Request**

```http
GET /api/records/{id}/files/{filename}/content HTTP/1.1
```

**Response**

```http
HTTP/1.1 200 OK
Content-Disposition: inline
Content-Length: 76122
Content-MD5: 71449104d017a6056ac1a5fb58754975
Content-Type: image/pdf
Date: Thu, 26 Nov 2020 18:35:33 GMT
ETag: "md5:71449104d017a6056ac1a5fb58754975"
Last-Modified: Thu, 26 Nov 2020 14:30:06 GMT

<...file binary data...>
```

## Versions

### Create a new version

`POST /api/records/{id}/versions`

**Parameters**

| Name | Type   | Location | Description                                   |
| ---- | ------ | -------- | --------------------------------------------- |
| `id` | string | path     | Identifier of the record, e.g.  `4d0ns-ntd89` |

**Request**

```http
POST /api/records/{id}/versions HTTP/1.1
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json


{
  "access": {
    "record": "restricted",
    "files": "restricted",
    "embargo": {
      "reason": null,
      "active": false
    }
  },
  "created": "2020-11-27 10:52:23.945755",
  "expires_at": "2020-11-27 10:52:23.945868",
  "files": {
    "enabled": true
  },
  "id": "{new-id}",
  "is_published": false,
  "links": {
    "latest": "{scheme+hostname}/api/records/{id}/versions/latest",
    "versions": "{scheme+hostname}/api/records/{id}/versions",
    "self_html": "{scheme+hostname}/uploads/{id}",
    "publish": "{scheme+hostname}/api/records/{id}/draft/actions/publish",
    "latest_html": "{scheme+hostname}/records/{id}/latest",
    "self": "{scheme+hostname}/api/records/{id}/draft",
    "files": "{scheme+hostname}/api/records/{id}/draft/files",
    "access_links": "{scheme+hostname}/api/records/{id}/access/links",
  },
  "metadata": {
    "resource_type": { "subtype": "image-photo", "type": "image" },
    "title": "An Updated Romans story",
    "creators": [
      "person_or_org": {
        "family_name": "Brown",
        "given_name": "Troy",
        "type": "personal"
      },
      {
        "person_or_org": {
          "family_name": "Collins",
          "given_name": "Thomas",
          "identifiers": [
            {"scheme": "orcid", "identifier": "0000-0002-1825-0097"}
          ],
          "name": "Collins, Thomas",
          "type": "personal"
        },
        "affiliations": [
          {
            "identifiers": [
              {"scheme": "ror", "identifier": "03yrm5c26"}
            ],
            "name": "Entity One"
          }
        ]
      }
    ],
  },
  "parent": {
    "id": "{parent-id}",
    "access": {
      "owned_by": [
        {
            "user": {user-id}
        }
      ],
      "links": []
    }
  },
  "revision_id": 3,
  "updated": "2020-11-27 10:52:23.969244",
  "versions": {
    "index": 2,
    "is_latest": false,
    "is_latest_draft": true
  }
}
```

Notice that a new draft is returned with `publication_date` and `version` removed (as those are typically replaced in a new version).
The `versions.index` is also incremented. The `{parent-id}` connects the different versions together.

Use (Publish a draft record)[#publish-a-draft-record] to publish it.

`POST /api/records`

**Parameters**

| Name       | Type   | Location | Description                                                  |
| ---------- | ------ | -------- | ------------------------------------------------------------ |
| `access`   | object | body     | [Access options](metadata.md#access-information) for the record. |
| `metadata` | object | body     | [Metadata](metadata.md#metadata) of the record. |


**Request**

```http
POST /api/records HTTP/1.1
Content-Type: application/json

{
  "access": {
    "record": "public",
    "files": "public"
  },
  "metadata": {
    "resource_type": { "type": "image", "subtype": "image-photo" },
    "title": "A Romans story",
    "publication_date": "2020-06-01",
    "creators": [
      "person_or_org": {
        "family_name": "Brown",
        "given_name": "Troy",
        "type": "personal"
      },
      {
        "person_or_org": {
          "family_name": "Collins",
          "given_name": "Thomas",
          "identifiers": [
            {"scheme": "orcid", "identifier": "0000-0002-1825-0097"}
          ],
          "name": "Collins, Thomas",
          "type": "personal"
        },
        "affiliations": [
          {
            "identifiers": [
              {"scheme": "ror", "identifier": "03yrm5c26"}
            ],
            "name": "Entity One"
          }
        ]
      }
    ]
  }
}
```

**Response**

```http
HTTP/1.1 201 CREATED
Content-Type: application/json

{
  "access": {
    "record": "public",
    "files": "public",
    "embargo": {
      "reason": null,
      "active": false
    }
  },
  "created": "2020-11-27 10:52:23.945755",
  "expires_at": "2020-11-27 10:52:23.945868",
  "id": "{id}",
  "is_published": false,
  "links": {
    "latest": "{scheme+hostname}/api/records/{id}/versions/latest",
    "versions": "{scheme+hostname}/api/records/{id}/versions",
    "self_html": "{scheme+hostname}/uploads/{id}",
    "publish": "{scheme+hostname}/api/records/{id}/draft/actions/publish",
    "latest_html": "{scheme+hostname}/records/{id}/latest",
    "self": "{scheme+hostname}/api/records/{id}/draft",
    "files": "{scheme+hostname}/api/records/{id}/draft/files",
    "access_links": "{scheme+hostname}/api/records/{id}/access/links",
  },
  "metadata": {
    "resource_type": { "subtype": "image-photo", "type": "image" },
    "title": "A Romans story",
    "publication_date": "2020-06-01",
    "creators": [
      "person_or_org": {
        "family_name": "Brown",
        "given_name": "Troy",
        "type": "personal"
      },
      {
        "person_or_org": {
          "family_name": "Collins",
          "given_name": "Thomas",
          "identifiers": [
            {"scheme": "orcid", "identifier": "0000-0002-1825-0097"}
          ],
          "name": "Collins, Thomas",
          "type": "personal"
        },
        "affiliations": [
          {
            "identifiers": [
              {"scheme": "ror", "identifier": "03yrm5c26"}
            ],
            "name": "Entity One"
          }
        ]
      }
    ],
  },
  "parent": {
    "id": "{parent-id}",
    "access": {
      "owned_by": [
        {
            "user": {user-id}
        }
      ],
      "links": []
    }
  },
  "revision_id": 3,
  "updated": "2020-11-27 10:52:23.969244",
  "versions": {
    "index": 1,
    "is_latest": false,
    "is_latest_draft": true
  }
}
```

### Get latest version

Given a record, it returns its latest version.

`GET /api/records/{id}/versions/latest`

**Parameters**

| Name     | Type   | Location | Description                                                  |
| -------- | ------ | -------- | ------------------------------------------------------------ |
| `id`     | string | path     | Identifier of a record, e.g. `cbc2k-q9x58`                 |
| `accept` | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |

**Request**

```http
GET /api/records/{id}/versions/latest HTTP/1.1
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "access": {
    "record": "restricted",
    "files": "restricted",
    "embargo": {
      "reason": null,
      "active": false
    }
  },
  "created": "2020-11-27 10:52:23.945755",
  "expires_at": "2020-11-27 10:52:23.945868",
  "files": {
    "enabled": true
  },
  "id": "{latest-version-id}",
  "is_published": true,
  "links": {
    "latest": "{scheme+hostname}/api/records/{id}/versions/latest",
    "versions": "{scheme+hostname}/api/records/{id}/versions",
    "self_html": "{scheme+hostname}/records/{id}",
    "latest_html": "{scheme+hostname}/records/{id}/latest",
    "self": "{scheme+hostname}/api/records/{id}",
    "files": "{scheme+hostname}/api/records/{id}/files",
    "access_links": "{scheme+hostname}/api/records/{id}/access/links",
  },
  "metadata": {
    "resource_type": { "subtype": "image-photo", "type": "image" },
    "title": "An Updated Romans story",
    "publication_date": "2020-06-01",
    "creators": [
      "person_or_org": {
        "family_name": "Brown",
        "given_name": "Troy",
        "type": "personal"
      },
      {
        "person_or_org": {
          "family_name": "Collins",
          "given_name": "Thomas",
          "identifiers": [
            {"scheme": "orcid", "identifier": "0000-0002-1825-0097"}
          ],
          "name": "Collins, Thomas",
          "type": "personal"
        },
        "affiliations": [
          {
            "identifiers": [
              {"scheme": "ror", "identifier": "03yrm5c26"}
            ],
            "name": "Entity One"
          }
        ]
      }
    ],
  },
  "parent": {
    "id": "{parent-id}",
    "access": {
      "owned_by": [
        {
            "user": {user-id}
        }
      ],
      "links": []
    }
  },
  "revision_id": 3,
  "updated": "2020-11-27 10:52:23.969244",
  "versions": {
    "index": 2,
    "is_latest": true,
    "is_latest_draft": true
  }
}
```


## Access links

Access links are URLs that can be shared with others to give them access and permissions to a record/draft.

### Create an access link

`POST /api/records/{id}/access/links`

**Parameters**

| Name     | Type   | Location | Description                                                  |
| -------- | ------ | -------- | ------------------------------------------------------------ |
| `id`     | string | path     | Identifier of the record, e.g. `cbc2k-q9x58`                 |
| `accept` | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |
| `expires_at`     | string | body     | Date time string. When the link expires.                 |
| `permission`     | string | body     | Required. Action that can be undertaken with the link.             |


**Request**

```http
POST /api/records/{id}/access/links HTTP/1.1
Content-Type: application/json

{
  "permission": "read"
}
```

**Response**

```http
HTTP/1.1 201 CREATED
Content-Type: application/json

{
  "permission": "read",
  "created_at": "2021-03-25T21:06:29.563235",
  "token": "eyJhbGciOiJIUzUxMiJ9.eyJpZCI6IjNkMzMyMGVhLTA3NTUtNGQ5My1hNzZlLWUyZjJmYzY1NWQyYSIsImRhdGEiOnt9LCJyYW5kb20iOiI2NzZhYTk3OTczMzgwMjkyNTJiM2MwZDBjNjliMTVkYSJ9.dBqk7YzIZ7kwG4oijNgH1VU-cjQmBiQlMQKMoB2y-YjVWmgnZetFAESsqRP6VpGTtaKdftrtob1PVZJF4YGpfg",
  "id": "3d3320ea-0755-4d93-a76e-e2f2fc655d2a",
  "expires_at": null
}
```

### Get an access link

`GET /api/records/{id}/access/links/{link-id}`

**Parameters**

| Name     | Type   | Location | Description                                                  |
| -------- | ------ | -------- | ------------------------------------------------------------ |
| `id`     | string | path     | Identifier of the record, e.g. `cbc2k-q9x58`                 |
| `link-id`     | string | path     | Identifier of the link, e.g. `3d3320ea-0755-4d93-a76e-e2f2fc655d2a` |
| `accept` | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |

**Request**

```http
GET /api/records/{id}/access/links/{link-id} HTTP/1.1
Content-Type: application/json
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "permission": "read",
  "created_at": "2021-03-25T21:06:29.563235",
  "token": "eyJhbGciOiJIUzUxMiJ9.eyJpZCI6IjNkMzMyMGVhLTA3NTUtNGQ5My1hNzZlLWUyZjJmYzY1NWQyYSIsImRhdGEiOnt9LCJyYW5kb20iOiI2NzZhYTk3OTczMzgwMjkyNTJiM2MwZDBjNjliMTVkYSJ9.dBqk7YzIZ7kwG4oijNgH1VU-cjQmBiQlMQKMoB2y-YjVWmgnZetFAESsqRP6VpGTtaKdftrtob1PVZJF4YGpfg",
  "id": "3d3320ea-0755-4d93-a76e-e2f2fc655d2a",
  "expires_at": null
}
```

### Update an access link

`PATCH /api/records/{id}/access/links/{link-id}`

**Parameters**

| Name     | Type   | Location | Description                                                  |
| -------- | ------ | -------- | ------------------------------------------------------------ |
| `id`     | string | path     | Identifier of the record, e.g. `cbc2k-q9x58`                 |
| `link-id`     | string | path     | Identifier of the link, e.g. `3d3320ea-0755-4d93-a76e-e2f2fc655d2a` |
| `accept` | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |
| `expires_at`     | string | body     | Date time string. When the link expires.                 |
| `permission`     | string | body     | Required. Action that can be undertaken with the link.             |

**Request**

```http
PATCH /api/records/{id}/access/links/{link-id} HTTP/1.1
Content-Type: application/json

{
  "permission": "manage",
  "expires_at": "2121-03-25T21:06:29.563235"
}
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "permission": "manage",
  "created_at": "2021-03-25T21:06:29.563235",
  "token": "eyJhbGciOiJIUzUxMiJ9.eyJpZCI6IjNkMzMyMGVhLTA3NTUtNGQ5My1hNzZlLWUyZjJmYzY1NWQyYSIsImRhdGEiOnt9LCJyYW5kb20iOiI2NzZhYTk3OTczMzgwMjkyNTJiM2MwZDBjNjliMTVkYSJ9.dBqk7YzIZ7kwG4oijNgH1VU-cjQmBiQlMQKMoB2y-YjVWmgnZetFAESsqRP6VpGTtaKdftrtob1PVZJF4YGpfg",
  "id": "3d3320ea-0755-4d93-a76e-e2f2fc655d2a",
  "expires_at": "2121-03-25T21:06:29.563235"
}
```

### Delete an access link

`DELETE /api/records/{id}/access/links/{link-id}`

**Parameters**

| Name     | Type   | Location | Description                                                  |
| -------- | ------ | -------- | ------------------------------------------------------------ |
| `id`     | string | path     | Identifier of the record, e.g. `cbc2k-q9x58`                 |
| `link-id`     | string | path     | Identifier of the link, e.g. `3d3320ea-0755-4d93-a76e-e2f2fc655d2a` |
| `accept` | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |

**Request**

```http
DELETE /api/records/{id}/access/links/{link-id} HTTP/1.1
Content-Type: application/json
```

**Response**

```http
HTTP/1.1 204 NO CONTENT
Content-Type: application/json
```

### List access links

`GET /api/records/{id}/access/links`

**Parameters**

| Name     | Type   | Location | Description                                                  |
| -------- | ------ | -------- | ------------------------------------------------------------ |
| `id`     | string | path     | Identifier of the record, e.g. `cbc2k-q9x58`                 |
| `accept` | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |

**Request**

```http
GET /api/records/{id}/access/links HTTP/1.1
Content-Type: application/json
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "hits": {
    "hits": [
      {
        "permission": "read",
        "id": "140f69c9-a8a5-41d4-8ae2-3dfbfe0e2796",
        "created_at": "2021-03-25T21:48:03.289198",
        "expires_at": null,
        "token": "eyJhbGciOiJIUzUxMiJ9.eyJpZCI6IjE0MGY2OWM5LWE4YTUtNDFkNC04YWUyLTNkZmJmZTBlMjc5NiIsImRhdGEiOnt9LCJyYW5kb20iOiI2NzE3MmY4MTNkYzhkNGJjZDAwOWFlOTlhOWM3NjU1MSJ9.1O9MwTmt_nfvsCm4qvlkUH0Rpe5bK3hT422A879DJSblOCONsNxPe_feNHrgTV3s6ZA6t6vLziXjhAwgKjHhIQ"
      }
    ],
    "total": 1
  }
}
```

## User Records

### List your draft or published records

`GET /api/user/records`

**Parameters**

| Name     | Type    | Location | Description                                                  |
| -------- | ------- | -------- | ------------------------------------------------------------ |
| `q`      | string  | query    | Search query used to filter results based on [ElasticSearch's query string syntax](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax). |
| `sort`   | string  | query    | Sort search results.                                         |
| `size`   | integer | query    | Specify number of items in the results page (default: 10).   |
| `page`   | integer | query    | Specify the page of results.                                 |
| `allversions`  | boolean | query    | Specify if all versions should be included.                  |
| `accept` | string  | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |

**Request**

```http
GET /api/user/records HTTP/1.1
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "aggregations": {...},
  "hits": {...},
  "links": {...},
  "sortBy": ...,
}
```

## Vocabularies

Used for accessing vocabulary records. Currently the following vocabularies
are supported:

- Languages (ISO 639-3 language codes)
- Licenses (SPDX licenses)

### Search vocabularies

**Parameters**

| Name     | Type    | Location | Description                                                  |
| -------- | ------- | -------- | ------------------------------------------------------------ |
| `type`   | string  | path     | Vocabulary (one of ``languages`` or ``licenses``)            |
| `q`      | string  | query    | Search query used to filter results based on [ElasticSearch's query string syntax](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax). |
| `suggest`| string  | query    | One or more words used to suggest records as the user types (i.e. auto-complete). |
| `tags`   | string  | query    | Filter results to the tag                                    |
| `sort`   | string  | query    | Sort search results.                                         |
| `size`   | integer | query    | Specify number of items in the results page (default: 10).   |
| `page`   | integer | query    | Specify the page of results.                                 |
| `accept` | string  | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |

Specifically for the `application/vnd.inveniordm.v1+json` format:

| Name     | Type   | Location | Description                                                  |
| -------- | ------ | -------- | ------------------------------------------------------------ |
| `ln`     | string | query     | Locale used to localize the title and description (e.g. `en` or `en_US`) |
| `accept-language` | string | header   | Locale used to localize the title and description (e.g. `en` or `en_US`) |

The API uses a locale matching algorithm, that will do it's best effort to translate the vocabulary record's title and description.

**Request**

```http
GET /api/vocabularies/{type} HTTP/1.1
```

**Response**

For all vocabularies:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "aggregations": {...},
  "hits": {...},
  "links": {...},
  "sortBy": ...,
}
```

Each hit looks like a vocabulary record below.

### Get a vocabulary record

`GET /api/vocabularies/{type}/{id}`

**Parameters**

| Name     | Type   | Location | Description                                                  |
| -------- | ------ | -------- | ------------------------------------------------------------ |
| `type`   | string | path     | Vocabulary (one of `languages` or `licenses`)            |
| `id`     | string | path     | Identifier of the record, e.g. `eng`                        |
| `accept` | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |
| `accept-language` | string | header   | For- `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |

Specifically for the `application/vnd.inveniordm.v1+json` format:

| Name     | Type   | Location | Description                                                  |
| -------- | ------ | -------- | ------------------------------------------------------------ |
| `ln`     | string | query     | Locale used to localize the title and description (e.g. `en` or `en_US`) |
| `accept-language` | string | header   | Locale used to localize the title and description (e.g. `en` or `en_US`) |

The API uses a locale matching algorithm, that will do it's best effort to translate the vocabulary record's title and description.

**Request**

```http
GET /api/vocabularies/{type}/{id} HTTP/1.1
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{

  "id": "{id}",
  "type": "{type}",
  "created": "2020-11-26T19:20:39",
  "updated": "2020-11-26T19:20:39",
  "revision_id": 1,
  "title": {
    "en": "..."
  },
  "description": {
    "en": "..."
  },
  "icon": "...",
  "props": { ... },
  "tags": [...],
  "links": { ... }
}
```


## Communities (Preview)

### Create a Community

`POST /api/communities`

**Parameters**

| Name       | Type   | Location | Description                                                  |
| ---------- | ------ | -------- | ------------------------------------------------------------ |
| `accept`   | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |

**Request**

```http
POST /api/communities HTTP/1.1
Accept: application/json

{
  "access": {
    "visibility": "public",
    "member_policy": "open",
    "record_policy": "open",
  },
  "id": "my_community_id",
  "metadata": {
    "title": "My Community",
    "description": "This is an example Community.",
    "type": "event",
    "alternate_identifiers": [{"scheme": "ror", "identifier": "03yrm5c26"}],
    "curation_policy": "This is the kind of records we accept.",
    "page": "Information for my community.",
    "website": "https://www.my_community.org",
    "domains": ["biology", "chemistry"],
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
}
```

**Response**

```http
HTTP/1.1 201 CREATED
Content-Type: application/json

{
  "access": {
    "visibility": "public",
    "member_policy": "open",
    "record_policy": "open",
  },
  "created": "2020-11-27 10:52:23.945755",
  "updated": "2020-11-27 10:52:23.945755",
  "id": "my_community_id",
  "links": {
    "self": "{scheme+hostname}/api/communities/my_community_id"
  },
  "metadata": {
    "title": "My Community",
    "description": "This is an example Community.",
    "type": "event",
    "alternate_identifiers": [{"scheme": "ror", "identifier": "03yrm5c26"}],
    "curation_policy": "This is the kind of records we accept.",
    "page": "Information for my community.",
    "website": "https://www.my_community.org",
    "domains": ["biology", "chemistry"],
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
}
```

### Update a Community

`PUT /api/communities/<comid>`

**Parameters**

| Name       | Type   | Location | Description                                                  |
| ---------- | ------ | -------- | ------------------------------------------------------------ |
| `comid`       | string | path     | Identifier of the community, e.g.  `my_community`                |
| `accept`   | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |

**Request**

```http
PUT /api/communities/<comid> HTTP/1.1
Accept: application/json

{
  "access": {
    "visibility": "public",
    "member_policy": "open",
    "record_policy": "open",
  },
  "id": "my_community_id",
  "metadata": {
    "title": "My Updated Community",
    "description": "This is an example Community.",
    "type": "event",
    "alternate_identifiers": [{"scheme": "ror", "identifier": "03yrm5c26"}],
    "curation_policy": "This is the kind of records we accept.",
    "page": "Information for my community.",
    "website": "https://www.my_community.org",
    "domains": ["biology", "chemistry"],
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
    }],
  }
}
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "access": {
    "visibility": "public",
    "member_policy": "open",
    "record_policy": "open",
  },
  "created": "2020-11-27 10:52:23.945755",
  "updated": "2020-11-27 10:55:23.945868",
  "id": "my_community_id",
  "links": {
    "self": "{scheme+hostname}/api/communities/my_community_id"
  },
  "metadata": {
    "title": "My Updated Community",
    "description": "This is an example Community.",
    "type": "event",
    "alternate_identifiers": [{"scheme": "ror", "identifier": "03yrm5c26"}],
    "curation_policy": "This is the kind of records we accept.",
    "page": "Information for my community.",
    "website": "https://www.my_community.org",
    "domains": ["biology", "chemistry"],
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
}
```

### Delete a Community

`DELETE /api/communities/<comid>`

**Parameters**

| Name       | Type   | Location | Description                                                  |
| ---------- | ------ | -------- | ------------------------------------------------------------ |
| `comid`       | string | path     | Identifier of the community, e.g.  `my_community`                |
| `accept`   | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |

**Request**

```http
DELETE /api/communities/<comid> HTTP/1.1
Accept: application/json

```

**Response**

```http
HTTP/1.1 204 No Content
Content-Type: application/json

{}
```

### Get a Community

`GET /api/communities/<comid>`

 **Parameters**

| Name       | Type   | Location | Description                                                  |
| ---------- | ------ | -------- | ------------------------------------------------------------ |
| `comid`       | string | path     | Identifier of the community, e.g.  `my_community`                |
| `accept`   | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |

**Request**

```http
GET /api/communities/<comid> HTTP/1.1
Accept: application/json
```

Response:
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "access": {
    "visibility": "public",
    "member_policy": "open",
    "record_policy": "open",
  },
  "created": "2020-11-27 10:52:23.945755",
  "updated": "2020-11-27 10:52:23.945868",
  "id": "my_community_id",
  "links": {
    "self": "{scheme+hostname}/api/communities/my_community_id"
  },
  "metadata": {
    "title": "My Community",
    "description": "This is an example Community.",
    "type": "event",
    "alternate_identifiers": [{"scheme": "ror", "identifier": "03yrm5c26"}],
    "curation_policy": "This is the kind of records we accept.",
    "page": "Information for my community.",
    "website": "https://www.my_community.org",
    "domains": ["biology", "chemistry"],
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
}
```


### Search Communities

**Parameters**

| Name           | Type    | Location | Description                                                  |
| -------------- | ------- | -------- | ------------------------------------------------------------ |
| `q`            | string  | query    | Search query used to filter results based on [ElasticSearch's query string syntax](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax). |
| `sort`         | string  | query    | Sort search results.                                         |
| `size`         | integer | query    | Specify number of items in the results page (default: 10).   |
| `page`         | integer | query    | Specify the page of results.                                 |               |
| `accept`       | string  | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |


**Request**

```http
GET /api/communities HTTP/1.1
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "aggregations": {...},
  "hits": {...},
  "links": {...},
  "sortBy": ...,
}
```

Each hit looks like a community above.

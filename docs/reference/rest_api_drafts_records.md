# Drafts and Records

## Drafts

Used for interacting with unpublished or edited draft records.

!!! info "Authentication required"

    All requests to the draft-related REST API endpoints require authentication.

### Create a draft record

`POST /api/records`

**Parameters**

| Name       | Type   | Location | Description                                                  |
| ---------- | ------ | -------- | ------------------------------------------------------------ |
| `access`   | object | body     | [Access options](metadata.md#access) for the record. |
| `files`    | object | body     | Files options (see below) for the record. |
| `metadata` | object | body     | [Metadata](metadata.md#metadata) of the record. |
| `custom_fields` | object | body     | [Custom fields](../customize/metadata/custom_fields/records.md#declaring-custom-fields) metadata for the record. (v10 and newer) |

#### Files Options

| Name       | Type   | Location | Description                                                  |
| ---------- | ------ | -------- | ------------------------------------------------------------ |
| `enabled`  | boolean | body     | *Required*. Should (and can) files be attached to this record or not. |
| `default_preview` &nbsp;  | string | body     | Filename of file to be previewed by default. |
| `order`    | array | body     | Array of filename strings in display order. |

A file must be uploaded to the draft before it can be used as the default
preview. See "[Start a draft file upload](#start-draft-file-uploads)" below.

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
            "id": "01ggx4157",
            "name": "Entity One"
          }
        ]
      }
    ],
    "publication_date": "2020-06-01",
    "resource_type": { "id": "image-photo" },
    "title": "A Romans story",
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
    "access_links": "{scheme+hostname}/api/records/{id}/access/links"
  },
  "metadata": {
    "resource_type": {
      "id": "image-photo",
      "title": {
        "en": "Photo"
      }
    },
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
            "id": "01ggx4157",
            "name": "European Organization for Nuclear Research"
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
  "pids": {},
  "revision_id": 3,
  "updated": "2020-11-27 10:52:23.969244",
  "versions": {
    "index": 1,
    "is_latest": false,
    "is_latest_draft": true
  }
}
```

Note how if a name and id are given for an affiliation identifiers. The instance's name it has for the given id is used e.g. "Entity One" is replaced by "European Organization for Nuclear Research" above.

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
    "access_links": "{scheme+hostname}/api/records/{id}/access/links"
  },
  "metadata": {
    "resource_type": {
      "id": "image-photo",
      "title": {
        "en": "Photo"
      }
    },
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
            "id": "01ggx4157",
            "name": "European Organization for Nuclear Research"
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
  "pids": {},
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
| `access`   | object | body     | [Access options](metadata.md#access) for the record. |
| `files`    | object | body     | [Files options](#files-options) for the record. |
| `metadata` | object | body     | [Metadata](metadata.md#metadata) of the record. |
| `custom_fields` | object | body     | [Custom fields](../customize/metadata/custom_fields/records.md#declaring-custom-fields) metadata for the record. (v10 and newer) |

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
    "enabled": false
  },
  "metadata": {
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
            "id": "01ggx4157",
            "name": "Entity One"
          }
        ]
      }
    ],
    "publication_date": "2020-06-01",
    "resource_type": { "id": "image-photo" },
    "title": "An Updated Romans story"
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
    "access_links": "{scheme+hostname}/api/records/{id}/access/links"
  },
  "metadata": {
    "resource_type": {
      "id": "image-photo",
      "title": {
        "en": "Photo"
      }
    },
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
            "id": "01ggx4157",
            "name": "European Organization for Nuclear Research"
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
  "pids": {},
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
    "access_links": "{scheme+hostname}/api/records/{id}/access/links"
  },
  "metadata": {
    "resource_type": {
      "id": "image-photo",
      "title": {
        "en": "Photo"
      }
    },
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
            "id": "01ggx4157",
            "name": "European Organization for Nuclear Research"
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
  "pids": {},
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
HTTP/1.1 201 CREATED
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
    "access_links": "{scheme+hostname}/api/records/{id}/access/links"
  },
  "metadata": {
    "resource_type": {
      "id": "image-photo",
      "title": {
        "en": "Photo"
      }
    },
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
            "id": "01ggx4157",
            "name": "European Organization for Nuclear Research"
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
  "pids": {},
  "revision_id": 3,
  "updated": "2020-11-27 10:52:23.969244",
  "versions": {
    "index": 1,
    "is_latest": true,
    "is_latest_draft": true
  }
}
```

### Delete/discard a draft record

`DELETE /api/records/{id}/draft`

Deleting a draft for an unpublished record will remove the draft and associated
files from the system.

Deleting a draft for a published record will remove the draft but not the
published record.

**Parameters**

| Name       | Type   | Location | Description                                                  |
| ---------- | ------ | -------- | ------------------------------------------------------------ |
| `id`       | string | path     | Identifier of the record, e.g.  `4d0ns-ntd89`                |

**Request**

```http
DELETE /api/records/{id}/draft HTTP/1.1
```

**Response**

```http
HTTP/1.1 204 No Content
```

## Draft files

Used to manage a draft's files.

!!! info "Authentication required"

    All requests to the draft-related REST API endpoints require authentication.

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
  "metadata": {
    "width": 960,
    "height": 640
  },
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
    "self_iiif_manifest": "{scheme+hostname}/api/records/{id}/manifest",
    "self_iiif_sequence": "{scheme+hostname}/api/records/{id}/sequence/default",
    "files": "{scheme+hostname}/api/records/{id}/files",
    "access_links": "{scheme+hostname}/api/records/{id}/access/links",
    "communities": "{scheme+hostname}/api/records/{id}/communities",
    "requests": "{scheme+hostname}/api/records/{id}/requests",
    "communities-suggestions": "{scheme+hostname}/api/records/{id}/communities-suggestions"
  },
  "metadata": {
    "resource_type": {
      "id": "image-photo",
      "title": {
        "en": "Photo"
      }
    },
    "title": "An Updated Romans story",
    "publication_date": "2020-06-01",
    "creators": [
      {
        "person_or_org": {
          "given_name": "Troy",
          "type": "personal",
          "name": "Brown, Troy",
          "family_name": "Brown"
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
            "id": "01ggx4157",
            "name": "European Organization for Nuclear Research"
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
  "pids": {},
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
| `sort`         | string  | query    | Sort search results. Customizable. Built-in options are `"bestmatch"`, `"newest"`, `"oldest"`, `"updated-desc"`, `"updated-asc"`, `"version"`, `"mostviewed"`, `"mostdownloaded"` (default: `"bestmatch"` or `"newest"`).                                        |
| `size`         | integer | query    | Specify number of items in the results page (default: 10).   |
| `page`         | integer | query    | Specify the page of results.                                 |
| `allversions` &nbsp; | boolean | query    | Specify if all versions should be included (default: `False`, displays just latest version).   |
| `accept`       | string  | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |

Sort options for records can be configured using the `RDM_SORT_OPTIONS` config variable as described in the [search customization](../customize/search.md) section. Note that `"bestmatch"` is only available as a sort option on requests that provide a query string as a `q` parameter. Otherwise `"bestmatch"` is ignored and the default `"newest"` sort is used. Queries sorted by `"mostviewed"` and `"mostdownloaded"` are in descending order.

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

Used for interacting with files of published records.

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

Used for interacting with record versions.

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
HTTP/1.1 201 OK
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
    "access_links": "{scheme+hostname}/api/records/{id}/access/links"
    "communities": "{scheme+hostname}/api/records/{id}/communities",
    "requests": "{scheme+hostname}/api/records/{id}/requests",
    "communities-suggestions": "{scheme+hostname}/api/records/{id}/communities-suggestions"
  },
  "metadata": {
    "resource_type": {
      "id": "image-photo",
      "title": {
        "en": "Photo"
      }
    },
    "title": "An Updated Romans story",
    "creators": [
      "person_or_org": {
        "family_name": "Brown",
        "given_name": "Troy",
        "name": "Brown, Troy",
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
            "id": "01ggx4157",
            "name": "European Organization for Nuclear Research"
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
  "pids": {},
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
The new draft version has no files. However, it is possible to link files from the previous version (avoiding the need to re-upload, which would also cause duplication in the file store). See below.

Use [Publish a draft record](#publish-a-draft-record) to publish it.

### Link files from previous version

`POST /api/records/{id}/draft/actions/files-import`

Links all files from the previous version to the new record.

**Parameters**

| Name | Type   | Location | Description                                              |
| ---- | ------ | -------- | -------------------------------------------------------- |
| `id` | string | path     | Identifier of the new draft version, e.g., `1bc9x-3pq5x` |

**Request**

```http
POST /api/records/{id}/draft/actions/files-import HTTP/1.1
```

**Response**

```http
HTTP/1.1 201 CREATED
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
      "links": {...}
    }
  ]
  "links": {...},
}

```

Note this call links all files from the previous version. Any files to be removed or updated can be [deleted](#delete-a-draft-file) from the draft version and remain attached to the previous version.

### Get all versions

`GET /api/records/{id}/versions`

**Parameters**

| Name | Type   | Location | Description                                   |
| ---- | ------ | -------- | --------------------------------------------- |
| `id` | string | path     | Identifier of the record, e.g.  `4d0ns-ntd89` |

**Request**

```http
GET /api/records/{id}/versions HTTP/1.1
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "hits": {...},
  "sortBy": "version",
  "links": {...}
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
    },
    "status": "restricted"
  },
  "created": "2020-11-27 10:52:23.945755",
  "expires_at": "2020-11-27 10:52:23.945868",
  "files": {
    "enabled": true,
    "order": []
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
    "communities": "{scheme+hostname}/api/records/{id}/communities",
    "requests": "{scheme+hostname}/api/records/{id}/requests",
    "communities-suggestions": "{scheme+hostname}/api/records/{id}/communities-suggestions"
  },
  "metadata": {
    "resource_type": {
      "id": "image-photo",
      "title": {
        "en": "Photo"
      }
    },
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
            "id": "01ggx4157",
            "name": "European Organization for Nuclear Research"
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
  "pids": {},
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
| `expires_at`     | string | body     | `ISO 8601 Date`Format (YYYY-MM-DD) When the link expires.          |
| `permission`     | string | body     | Required. Action that can be undertaken with the link (``view``, ``preview`` or ``edit``). |


**Request**

```http
POST /api/records/{id}/access/links HTTP/1.1
Content-Type: application/json

{
  "permission": "view",
  "expires_at": "2024-11-06"
}
```

**Response**

```http
HTTP/1.1 201 CREATED
Content-Type: application/json

{
    "id": "07fb00f3-928c-4ce9-8d2e-8e9c4dca3092",
    "created_at": "2024-06-12T13:07:09.951029+00:00",
    "expires_at": "2024-11-06",
    "permission": "view",
    "description": "",
    "token": "eyJhbGciOiJIUzUxMiIsImlhdCI6MTcxODE5NzYyOSwiZXhwIjoxNzMwODUxMTk5fQ.eyJpZCI6IjA3ZmIwMGYzLTkyOGMtNGNlOS04ZDJlLThlOWM0ZGNhMzA5MiIsImRhdGEiOnt9LCJyYW5kb20iOiI1NzVjNzEwY2QwNWI3YWFhMTM2MzY3ZmMzZWFkYzA0MSJ9.GPfPBvrbvEu-JMddFXjb5MZKNWRnzAK53oTVOSgfdZOcMIoRfszO39GEglko74dohZiUcJ11jWXj0fwfdq1WnQ"
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
    "id": "61c2d20f-4c88-440d-9978-dd16a69bf97e",
    "created_at": "2024-06-12T13:23:11.271139+00:00",
    "expires_at": "2024-11-06",
    "permission": "view",
    "description": "",
    "token": "eyJhbGciOiJIUzUxMiIsImlhdCI6MTcxODE5ODU5MSwiZXhwIjoxNzMwODUxMTk5fQ.eyJpZCI6IjYxYzJkMjBmLTRjODgtNDQwZC05OTc4LWRkMTZhNjliZjk3ZSIsImRhdGEiOnt9LCJyYW5kb20iOiI2MWYwZTg4YjgzY2E2ZDhkMjJiMTY0MGFjNmIzMmEwZiJ9.AFEmgQ8_gtEj7dvlZ2MHD9qneKy0UEC1HMByo8J5xVGMYG8PXwuRsyUgeq_k_ZeHybO5W4_Do_P4NVGXsrjHyg"
}
```

### Update an access link

`PATCH /api/records/{id}/access/links/{link-id}`

**Parameters**

| Name     | Type   | Location | Description                                                  |
| -------- | ------ | -------- | ------------------------------------------------------------ |
| `id`     | string | path     | Identifier of the record, e.g. `cbc2k-q9x58`                               |
| `link-id`     | string | path     | Identifier of the link, e.g. `3d3320ea-0755-4d93-a76e-e2f2fc655d2a`   |
| `accept` | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |
| `expires_at`     | string | body     |  `ISO 8601 Date`Format (YYYY-MM-DD) When the link expires.         |
| `permission`     | string | body     | Required. Action that can be undertaken with the link.             |

**Request**

```http
PATCH /api/records/{id}/access/links/{link-id} HTTP/1.1
Content-Type: application/json

{
  "permission": "edit",
  "expires_at": "2024-11-06"
}
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": "df672812-6b23-411a-b40a-9bb22787f0a2",
    "created_at": "2024-06-12T12:48:43.724970+00:00",
    "expires_at": "2024-11-06",
    "permission": "edit",
    "description": "",
    "token": "eyJhbGciOiJIUzUxMiJ9.eyJpZCI6ImRmNjcyODEyLTZiMjMtNDExYS1iNDBhLTliYjIyNzg3ZjBhMiIsImRhdGEiOnt9LCJyYW5kb20iOiIwZWE3ZWQ5YTBiZTE3N2ZjMjE4YjNjYzY3M2RiOTI5OSJ9.kqJ_gTvgjEc_-1Jxv-XHqSCUmOpcQDdBzx-T5BP7ybvQItK91wGxmVT_gfHxyHHDQ_7e8_LH1A5TotAZCA8q_w"
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
HTTP/1.1 204 No Content
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
              "id": "61c2d20f-4c88-440d-9978-dd16a69bf97e",
              "created_at": "2024-06-12T13:23:11.271139+00:00",
              "expires_at": "2024-11-06",
              "permission": "edit",
              "description": "",
              "token": "eyJhbGciOiJIUzUxMiIsImlhdCI6MTcxODE5ODU5MSwiZXhwIjoxNzMwODUxMTk5fQ.eyJpZCI6IjYxYzJkMjBmLTRjODgtNDQwZC05OTc4LWRkMTZhNjliZjk3ZSIsImRhdGEiOnt9LCJyYW5kb20iOiI2MWYwZTg4YjgzY2E2ZDhkMjJiMTY0MGFjNmIzMmEwZiJ9.AFEmgQ8_gtEj7dvlZ2MHD9qneKy0UEC1HMByo8J5xVGMYG8PXwuRsyUgeq_k_ZeHybO5W4_Do_P4NVGXsrjHyg"
          }
      ],
      "total": 1
  }
}
```

## User Records

Used for interacting with the records and drafts you can edit.

### List your draft and published records

`GET /api/user/records`

**Parameters**

| Name     | Type    | Location | Description                                                  |
| -------- | ------- | -------- | ------------------------------------------------------------ |
| `q`      | string  | query    | Search query used to filter results based on [ElasticSearch's query string syntax](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax). |
| `sort`   | string  | query    | Sort search results. Customizable. Built-in options are `"bestmatch"`, `"newest"`, `"oldest"`, `"updated-desc"`, `"updated-asc"`, `"version"`, `"mostviewed"`, `"mostdownloaded"` (default: `"bestmatch"` or `"newest"`).                                        |
| `size`   | integer | query    | Specify number of items in the results page (default: 10).   |
| `page`   | integer | query    | Specify the page of results.                                 |
| `allversions` &nbsp; | boolean | query    | Specify if all versions should be included.      |
| `accept` | string  | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |

Sort options for records can be configured using the `RDM_SORT_OPTIONS` config variable as described in the [search customization](../customize/search.md) section. Note that `"bestmatch"` is only available as a sort option on requests that provide a query string as a `q` parameter. Otherwise `"bestmatch"` is ignored and the default `"newest"` sort is used. Queries sorted by `"mostviewed"` and `"mostdownloaded"` are in descending order.

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

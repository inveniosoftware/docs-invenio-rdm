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
| `custom_fields` | object | body     | [Custom fields](../operate/customize/metadata/custom_fields/records.md#declaring-custom-fields) metadata for the record. (v10 and newer) |
| `pids`     | object | body     | Optional. For providing your own external persistent identifiers (e.g., DOIs). See [Providing your own PID](#providing-your-own-pid). To mint a new DOI, use the [Reserve a DOI endpoint](#reserve-a-doi-for-a-draft-record) instead. |

#### Files Options

| Name       | Type   | Location | Description                                                  |
| ---------- | ------ | -------- | ------------------------------------------------------------ |
| `enabled`  | boolean | body     | *Required*. Should (and can) files be attached to this record or not. |
| `default_preview` &nbsp;  | string | body     | Filename of file to be previewed by default. |
| `order`    | array | body     | Array of filename strings in display order. |

A file must be uploaded to the draft before it can be used as the default
preview. See "[Start a draft file upload](#start-draft-file-uploads)" below.

#### Providing your own PID

You can provide your own external persistent identifier (PID) when creating a draft record by including the `pids` field:

```json
{
  "pids": {
    "doi": {
      "identifier": "10.1234/your.doi",
      "provider": "external"
    }
  }
}
```

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
      "owned_by": {
        "user": {user-id}
      },
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

### Reserve a DOI for a draft record

`POST /api/records/{id}/draft/pids/doi`

Reserves a DOI for a draft record. The DOI will be registered when the record is published.

**Parameters**

| Name | Type   | Location | Description                                   |
| ---- | ------ | -------- | --------------------------------------------- |
| `id` | string | path     | Identifier of the draft record, e.g. `4d0ns-ntd13` |

**Request**

```http
POST /api/records/{id}/draft/pids/doi HTTP/1.1
```

**Response**

```http
HTTP/1.1 201 CREATED
Content-Type: application/json

{
  "id": "{id}",
  "created": "2025-05-22T10:07:39.346289+00:00",
  "updated": "2025-05-22T12:50:44.591407+00:00",
  "links": {
    "self": "{scheme+hostname}/api/records/{id}/draft",
    "self_html": "{scheme+hostname}/uploads/{id}",
    "doi": "https://handle.stage.datacite.org/10.71775/kth.{id}",
    "publish": "{scheme+hostname}/api/records/{id}/draft/actions/publish",
    "files": "{scheme+hostname}/api/records/{id}/draft/files",
    "reserve_doi": "{scheme+hostname}/api/records/{id}/draft/pids/doi",
    "versions": "{scheme+hostname}/api/records/{id}/versions"
    // ...other links omitted for brevity...
  },
  "pids": {
    "doi": {
      "identifier": "10.71775/kth.{id}",
      "provider": "datacite",
      "client": "datacite"
    }
  },
  // ...rest of the draft record...
}
```

**Error responses**

If the DOI already exists:

```http
HTTP/1.1 400 BAD REQUEST
Content-Type: application/json

{
  "status": 400,
  "message": "A validation error occurred.",
  "errors": [
    {
      "field": "pids.doi",
      "messages": [
        "A PID already exists for type doi"
      ]
    }
  ]
}
```

### Delete a DOI from a draft record

`DELETE /api/records/{id}/draft/pids/doi`

Deletes a DOI that was previously reserved for a draft record.

**Parameters**

| Name | Type   | Location | Description                                   |
| ---- | ------ | -------- | --------------------------------------------- |
| `id` | string | path     | Identifier of the draft record, e.g. `4d0ns-ntd13` |


!!! note "Deleting external DOIs"

    This endpoint only deletes DOIs reserved via the InvenioRDM API. If you supplied an external DOI (`provider: "external"` in the `pids` field), remove it by updating the draft record to exclude the `pids` field, then reserve a new DOI if needed.

**Request**

```http
DELETE /api/records/{id}/draft/pids/doi HTTP/1.1
```

**Response**

```http
HTTP/1.1 204 NO CONTENT
```

**Error responses**

If the DOI does not exist:

```http
HTTP/1.1 404 NOT FOUND
Content-Type: application/json

{
  "status": 404,
  "message": "The persistent identifier does not exist."
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
      "owned_by": {
        "user": {user-id}
      },
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
| `custom_fields` | object | body     | [Custom fields](../operate/customize/metadata/custom_fields/records.md#declaring-custom-fields) metadata for the record. (v10 and newer) |

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
      "owned_by": {
        "user": {user-id}
      },
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
      "owned_by": {
        "user": {user-id}
      },
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
      "owned_by": {
        "user": {user-id}
      },
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
      "owned_by": {
        "user": {user-id}
      },
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

Sort options for records can be configured using the `RDM_SORT_OPTIONS` config variable as described in the [search customization](../operate/customize/search.md) section. Note that `"bestmatch"` is only available as a sort option on requests that provide a query string as a `q` parameter. Otherwise `"bestmatch"` is ignored and the default `"newest"` sort is used. Queries sorted by `"mostviewed"` and `"mostdownloaded"` are in descending order.

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

### Container files

_Introduced in v14_

Container files are archive files (e.g., ZIP) that InvenioRDM understands. You can browse, preview, and extract individual files from archives without downloading the entire archive. This feature is particularly useful for large datasets organized in directory structures.

For supported formats, two additional endpoints are available on a **published record's** files:
- List the archive contents in a hierarchical tree structure
- Download or preview individual files and directories from within the archive

!!! note "Published records only"
    Container file endpoints are available only for **published records**, not drafts. Use `/api/records/{id}/files/` (not `/draft/files/`).

See the [ZIP and container files configuration guide](../operate/customize/file-uploads/zip-and-container-files.md) for setup instructions and supported formats.

#### List the contents of a container file

`GET /api/records/{id}/files/{filename}/container`

List all entries and directories inside a container file. Returns a hierarchical tree structure that can be used to navigate the archive contents.

**Parameters**

| Name       | Type   | Location | Description                                           |
| ---------- | ------ | -------- | ----------------------------------------------------- |
| `id`       | string | path     | Identifier of the record, e.g. `cbc2k-q9x58`         |
| `filename` | string | path     | Name of a container file, e.g. `dataset.zip`         |

**Request**

```http
GET /api/records/{id}/files/dataset.zip/container HTTP/1.1
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "entries": [
    {
      // saved path inside the ZIP archive (used as container item key)
      "key": "test_zip/test1.txt",
      // other metadata fields can be added here and should be ignored by clients if not recognized
      // fields below come from the Python zipfile library
      "size": 12,
      "compressed_size": 14,
      "mimetype": "text/plain",
      "checksum": "crc:2962613731",
    },
  ],
  "directories": [
    {
      "key": "test_zip",
      "links": {
        "content": ".../api/records/abc123-yz89/files/demo_with_subdirectories.zip/container/test_zip",
      },
      "entries": [
        "test_zip/test1.txt",
      ],
    },
  ],
  "total": 1, // total number of entries
  "truncated": false, // true if the listing was truncated (e.g., too many entries)
}
```

#### List contents of a specific directory

`GET /api/records/{id}/files/{filename}/container/{path}`

List the contents of a specific directory inside the container file. The `{path}` parameter specifies the directory path within the archive.

**Parameters**

| Name       | Type   | Location | Description                                                                       |
| ---------- | ------ | -------- | --------------------------------------------------------------------------------- |
| `id`       | string | path     | Identifier of the record, e.g. `cbc2k-q9x58`                                     |
| `filename` | string | path     | Name of a container file, e.g. `dataset.zip`                                     |
| `path`     | string | path     | Path of the directory inside the archive, e.g. `data/regional/north`                |

**Request**

```http
GET /api/records/{id}/files/dataset.zip/container/data/regional HTTP/1.1
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "entries": [
    {
      "key": "data/regional/north/images.zip",
      "size": 1048576,
      "compressed_size": 524288,
      "mimetype": "application/zip",
      "checksum": "crc:1234567890",
    },
  ],
  "directories": [
    {
      "key": "data/regional/south",
      "links": {
        "content": "/api/records/{id}/files/dataset.zip/container/data/regional/south",
      },
      "entries": ["data/regional/south/data.csv"],
    },
  ],
  "total": 1,
  "truncated": false,
}
```

#### Download or preview a container item

`GET /api/records/{id}/files/{filename}/container/{path}`

Retrieve specific container items from the archive. This endpoint supports both downloading and previewing files inside the archive. When used with a file path, it streams the file content directly. When used with a directory path, it generates a ZIP archive of the directory contents on-the-fly.

**Parameters**

| Name       | Type   | Location | Description                                                                       |
| ---------- | ------ | -------- | --------------------------------------------------------------------------------- |
| `id`       | string | path     | Identifier of the record, e.g. `cbc2k-q9x58`                                     |
| `filename` | string | path     | Name of a container file, e.g. `dataset.zip`                                     |
| `path`     | string | path     | Path of the item inside the archive, e.g. `data/measurements.csv` or `data`      |

**Request (single file)**

```http
GET /api/records/{id}/files/dataset.zip/container/data/measurements.csv HTTP/1.1
```

**Response (single file)**

```http
HTTP/1.1 200 OK
Content-Disposition: attachment; filename="measurements.csv"
Content-Type: text/csv

<...file binary data...>
```

**Request (directory)**

```http
GET /api/records/{id}/files/dataset.zip/container/data HTTP/1.1
```

**Response (directory)**

```http
HTTP/1.1 200 OK
Content-Disposition: attachment; filename="data.zip"
Content-Type: application/zip

<...ZIP archive of directory contents, streamed...>
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
      "owned_by": {
        "user": {user-id}
      },
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
      "owned_by": {
        "user": {user-id}
      },
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

Sort options for records can be configured using the `RDM_SORT_OPTIONS` config variable as described in the [search customization](../operate/customize/search.md) section. Note that `"bestmatch"` is only available as a sort option on requests that provide a query string as a `q` parameter. Otherwise `"bestmatch"` is ignored and the default `"newest"` sort is used. Queries sorted by `"mostviewed"` and `"mostdownloaded"` are in descending order.

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

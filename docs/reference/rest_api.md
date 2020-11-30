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

## Records

Used for accessing published records.

### Search records

**Parameters**

| Name     | Type    | Location | Description                                                  |
| -------- | ------- | -------- | ------------------------------------------------------------ |
| `q`      | string  | query    | Search query used to filter results based on [ElasticSearch's query string syntax](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax). |
| `sort`   | string  | query    | Sort search results.                                         |
| `size`   | integer | query    | Specify number of items in the results page (default: 10).   |
| `page`   | integer | query    | Specify the page of results.                                 |
| `accept` | string  | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |

**Request**

```http
GET /api/records/ HTTP/1.1
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "aggregations": {...},
  "hits": {...},
}
```

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
  "id": "{id}",
  "conceptid": ...,
  "updated": "2020-11-26T19:20:39",
  "created": "2020-11-26T19:20:39",
  "revision_id": 2,
  "metadata": {...},
  "access": {...},
  "links": {...},
}
```

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

## Drafts

Used for accessing unpublished or edited draft records.

!!! info "Authentication required"

    All requests to the draft-related REST API endpoints require authentication.

### List draft records

`GET /api/user/records`

**Parameters**

| Name     | Type    | Location | Description                                                  |
| -------- | ------- | -------- | ------------------------------------------------------------ |
| `q`      | string  | query    | Search query used to filter results based on [ElasticSearch's query string syntax](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax). |
| `sort`   | string  | query    | Sort search results.                                         |
| `size`   | integer | query    | Specify number of items in the results page (default: 10).   |
| `page`   | integer | query    | Specify the page of results.                                 |
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
}
```

### Create a record draft

`POST /api/records`

**Parameters**

| Name       | Type   | Location | Description                                                  |
| ---------- | ------ | -------- | ------------------------------------------------------------ |
| `metadata` | object | body     | Metadata of the record (see metadata reference for examples). |
| `access`   | object | body     | Access options for the record (TBD).                         |

**Request**

```http
POST /api/records HTTP/1.1
Content-Type: application/json

{
  "metadata": {
    "resource_type": { "type": "image", "subtype": "image-photo" },
    "title": "A Romans story",
    "publication_date": "2020-06-01",
    "creators": [
      {
        "given_name": "Troy",
        "family_name": "Brown",
        "type": "personal"
      },
      {
        "given_name": "Phillip",
        "family_name": "Lester",
        "type": "personal",
        "identifiers": { "orcid": "0000-0002-1825-0097" },
        "affiliations": [
          { "name": "Carter-Morris", "identifiers": { "ror": "03yrm5c26" } }
        ]
      },
      {
        "given_name": "Steven",
        "family_name": "Williamson",
        "type": "personal",
        "identifiers": { "orcid": "0000-0002-1825-0097" },
        "affiliations": [
          { "name": "Ritter and Sons", "identifiers": { "ror": "03yrm5c26" } },
          { "name": "Montgomery, Bush and Madden", "identifiers": { "ror": "03yrm5c26" } }
        ]
      }
    ]
  },
  "access": {
    "metadata": false,
    "files": false,
    "owned_by": [1],
    "access_right": "open"
  }
}
```

**Response**

```http
HTTP/1.1 201 CREATED
Content-Type: application/json

{
  "id": "{id}",
  "conceptid": "{conceptid}",
  "updated": "2020-11-27 10:52:23.969244",
  "created": "2020-11-27 10:52:23.945755",
  "revision_id": 2,
  "expires_at": "2020-11-27 10:52:23.945868",
  "metadata": {
    "resource_type": { "subtype": "image-photo", "type": "image" },
    "title": "A Romans story",
    "publication_date": "2020-06-01",
    "creators": [
      {
        "name": "Brown, Troy",
        "type": "personal",
        "family_name": "Brown",
        "given_name": "Troy"
      },
      {
        "name": "Lester, Phillip",
        "type": "personal",
        "affiliations": [
          { "name": "Carter-Morris", "identifiers": { "ror": "03yrm5c26" } }
        ],
        "family_name": "Lester",
        "identifiers": { "orcid": "0000-0002-1825-0097" },
        "given_name": "Phillip"
      },
      {
        "name": "Williamson, Steven",
        "type": "personal",
        "affiliations": [
          { "name": "Ritter and Sons", "identifiers": { "ror": "03yrm5c26" } },
          { "name": "Montgomery, Bush and Madden", "identifiers": { "ror": "03yrm5c26" } }
        ],
        "family_name": "Williamson",
        "identifiers": { "orcid": "0000-0002-1825-0097" },
        "given_name": "Steven"
      }
    ],
  },
  "access": {
    "owned_by": [ 1 ],
    "access_right": "open",
    "metadata": false,
    "files": false
  },
  "links": {
    "publish": "/api/records/{id}/draft/actions/publish",
    "self": "/api/records/{id}/draft",
    "self_html": "/uploads/{id}",
    "files": "/api/records/{id}/draft/files"
  },
}
```

### Get a record draft

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
  "id": "{id}",
  "conceptid": "{conceptid}",
  "updated": "2020-11-27 10:52:23.969244",
  "created": "2020-11-27 10:52:23.945755",
  "revision_id": 2,
  "expires_at": "2020-11-27 10:52:23.945868",
  "metadata": {
    "resource_type": { "subtype": "image-photo", "type": "image" },
    "title": "A Romans story",
    "publication_date": "2020-06-01",
    "creators": [
      {
        "name": "Brown, Troy",
        "type": "personal",
        "family_name": "Brown",
        "given_name": "Troy"
      },
      {
        "name": "Lester, Phillip",
        "type": "personal",
        "affiliations": [
          { "name": "Carter-Morris", "identifiers": { "ror": "03yrm5c26" } }
        ],
        "family_name": "Lester",
        "identifiers": { "orcid": "0000-0002-1825-0097" },
        "given_name": "Phillip"
      },
      {
        "name": "Williamson, Steven",
        "type": "personal",
        "affiliations": [
          { "name": "Ritter and Sons", "identifiers": { "ror": "03yrm5c26" } },
          { "name": "Montgomery, Bush and Madden", "identifiers": { "ror": "03yrm5c26" } }
        ],
        "family_name": "Williamson",
        "identifiers": { "orcid": "0000-0002-1825-0097" },
        "given_name": "Steven"
      }
    ],
  },
  "access": {
    "owned_by": [ 1 ],
    "access_right": "open",
    "metadata": false,
    "files": false
  },
  "links": {
    "publish": "/api/records/{id}/draft/actions/publish",
    "self": "/api/records/{id}/draft",
    "self_html": "/uploads/{id}",
    "files": "/api/records/{id}/draft/files"
  },
}
```

### Update metadata of the draft

`PUT /api/records/{id}/draft`

**Parameters**

| Name       | Type   | Location | Description                                                  |
| ---------- | ------ | -------- | ------------------------------------------------------------ |
| `id`       | string | path     | Identifier of the record, e.g.  `4d0ns-ntd89`                |
| `metadata` | object | body     | Metadata of the record (see metadata reference for examples). |
| `access`   | object | body     | Access options for the record (TBD).                         |

**Request**

```http
PUT /api/records HTTP/1.1
Content-Type: application/json

{
  "metadata": {
    "resource_type": { "type": "image", "subtype": "image-photo" },
    "title": "A new Romans story",
    "publication_date": "2020-06-01",
    "creators": [
      {
        "given_name": "Troy",
        "family_name": "Brown",
        "type": "personal"
      },
      {
        "given_name": "Phillip",
        "family_name": "Lester",
        "type": "personal",
        "identifiers": { "orcid": "0000-0002-1825-0097" },
        "affiliations": [
          { "name": "Carter-Morris", "identifiers": { "ror": "03yrm5c26" } }
        ]
      },
      {
        "given_name": "Steven",
        "family_name": "Williamson",
        "type": "personal",
        "identifiers": { "orcid": "0000-0002-1825-0097" },
        "affiliations": [
          { "name": "Ritter and Sons", "identifiers": { "ror": "03yrm5c26" } },
          { "name": "Montgomery, Bush and Madden", "identifiers": { "ror": "03yrm5c26" } }
        ]
      }
    ]
  },
  "access": {
    "metadata": false,
    "files": false,
    "owned_by": [1],
    "access_right": "open"
  }
}
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "{id}",
  "conceptid": "{conceptid}",
  "updated": "2020-11-27 10:52:23.969244",
  "created": "2020-11-27 10:52:23.945755",
  "revision_id": 2,
  "expires_at": "2020-11-27 10:52:23.945868",
  "metadata": {
    "resource_type": { "subtype": "image-photo", "type": "image" },
    "title": "A new Romans story",
    "publication_date": "2020-06-01",
    "creators": [
      {
        "name": "Brown, Troy",
        "type": "personal",
        "family_name": "Brown",
        "given_name": "Troy"
      },
      {
        "name": "Lester, Phillip",
        "type": "personal",
        "affiliations": [
          { "name": "Carter-Morris", "identifiers": { "ror": "03yrm5c26" } }
        ],
        "family_name": "Lester",
        "identifiers": { "orcid": "0000-0002-1825-0097" },
        "given_name": "Phillip"
      },
      {
        "name": "Williamson, Steven",
        "type": "personal",
        "affiliations": [
          { "name": "Ritter and Sons", "identifiers": { "ror": "03yrm5c26" } },
          { "name": "Montgomery, Bush and Madden", "identifiers": { "ror": "03yrm5c26" } }
        ],
        "family_name": "Williamson",
        "identifiers": { "orcid": "0000-0002-1825-0097" },
        "given_name": "Steven"
      }
    ],
  },
  "access": {
    "owned_by": [ 1 ],
    "access_right": "open",
    "metadata": false,
    "files": false
  },
  "links": {
    "publish": "/api/records/{id}/draft/actions/publish",
    "self": "/api/records/{id}/draft",
    "self_html": "/uploads/{id}",
    "files": "/api/records/{id}/draft/files"
  },
}
```

### Publish a draft

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
  "id": "{id}",
  "conceptid": "{conceptid}",
  "updated": "2020-11-27 10:52:23.969244",
  "created": "2020-11-27 10:52:23.945755",
  "revision_id": 2,
  "expires_at": "2020-11-27 10:52:23.945868",
  "metadata": {
    "resource_type": { "subtype": "image-photo", "type": "image" },
    "title": "A new Romans story",
    "publication_date": "2020-06-01",
    "creators": [
      {
        "name": "Brown, Troy",
        "type": "personal",
        "family_name": "Brown",
        "given_name": "Troy"
      },
      {
        "name": "Lester, Phillip",
        "type": "personal",
        "affiliations": [
          { "name": "Carter-Morris", "identifiers": { "ror": "03yrm5c26" } }
        ],
        "family_name": "Lester",
        "identifiers": { "orcid": "0000-0002-1825-0097" },
        "given_name": "Phillip"
      },
      {
        "name": "Williamson, Steven",
        "type": "personal",
        "affiliations": [
          { "name": "Ritter and Sons", "identifiers": { "ror": "03yrm5c26" } },
          { "name": "Montgomery, Bush and Madden", "identifiers": { "ror": "03yrm5c26" } }
        ],
        "family_name": "Williamson",
        "identifiers": { "orcid": "0000-0002-1825-0097" },
        "given_name": "Steven"
      }
    ],
  },
  "access": {
    "owned_by": [ 1 ],
    "access_right": "open",
    "metadata": false,
    "files": false
  },
  "links": {
    "self": "/api/records/{id}",
    "self_html": "/records/{id}",
    "files": "/api/records/{id}/files",
  },

  },
}
```

### Edit a record draft

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
  "id": "{id}",
  "conceptid": "{conceptid}",
  "updated": "2020-11-27 10:52:23.969244",
  "created": "2020-11-27 10:52:23.945755",
  "revision_id": 2,
  "expires_at": "2020-11-27 10:52:23.945868",
  "metadata": {
    "resource_type": { "subtype": "image-photo", "type": "image" },
    "title": "A new Romans story"
    "publication_date": "2020-06-01",
    "creators": [
      {
        "name": "Brown, Troy",
        "type": "personal",
        "family_name": "Brown",
        "given_name": "Troy"
      },
      {
        "name": "Lester, Phillip",
        "type": "personal",
        "affiliations": [
          { "name": "Carter-Morris", "identifiers": { "ror": "03yrm5c26" } }
        ],
        "family_name": "Lester",
        "identifiers": { "orcid": "0000-0002-1825-0097" },
        "given_name": "Phillip"
      },
      {
        "name": "Williamson, Steven",
        "type": "personal",
        "affiliations": [
          { "name": "Ritter and Sons", "identifiers": { "ror": "03yrm5c26" } },
          { "name": "Montgomery, Bush and Madden", "identifiers": { "ror": "03yrm5c26" } }
        ],
        "family_name": "Williamson",
        "identifiers": { "orcid": "0000-0002-1825-0097" },
        "given_name": "Steven"
      }
    ],
  },
  "access": {
    "owned_by": [ 1 ],
    "access_right": "open",
    "metadata": false,
    "files": false
  },
  "links": {
    "publish": "/api/records/{id}/draft/actions/publish",
    "self": "/api/records/{id}/draft",
    "self_html": "/uploads/{id}",
    "files": "/api/records/{id}/draft/files"
  },
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
  "enabled": true,
  "links": {
    "self": "/api/records/{id}/draft/files"
  },
  "entries": [],
  "default_preview": null,
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
  "enabled": true,
  "default_preview": "article.pdf",
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
    }
  ],
  "links": {
    "self": "/api/records/{id}/draft/files"
  },
}
```

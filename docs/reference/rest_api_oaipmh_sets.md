## OAI PMH Sets

Used for managing OAI-PMH sets for selective harvesting.

!!! hint
    To access any of these endpoints, the `admin` role is needed.

### Search sets

`GET /api/oaipmh/sets`

**Parameters**

| Name              | Type    | Location | Description                                                  |
| --------          | ------- | -------- | ------------------------------------------------------------ |
| `sort`            | string  | query    | Sort search results.<br />- `name` (default)<br />- `spec`<br />- `created`<br />- `updated`|                                         |
| `sort_direction`  | string  | query    | Sort direction of search results.<br />- `asc` (default)<br />- `desc`|
| `size`            | integer | query    | Specify number of items in the results page (default: 10).   |
| `page`            | integer | query    | Specify the page of results.                                 |
| `accept`          | string  | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |

Specifically for the `application/vnd.inveniordm.v1+json` format:


**Request**

```http
GET /api/oaipmh/sets HTTP/1.1
```

**Response**

For all sets:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "hits": {
    "hits": [{
      "id": "{id}",
      "name": "RDM Conference",
      "spec": "rdm-conference"
      "query": "elasticsearch_query:to_match_records",
      "description": "Entries presented at RDM conference",
      "links": {
        "self": "https://127.0.0.1/api/oaipmh/sets/{id}",
        "oai-listrecords": "https://127.0.0.1/oai2d?verb=ListRecords&metadataPrefix=oai_dc&spec=rdm-conference",
        "oai-listidentifiers": "https://127.0.0.1/oai2d?verb=ListIdentifiers&metadataPrefix=oai_dc&spec=rdm-conference",
      },
      "created": "2022-03-21T10:20:39",
      "updated": "2022-03-21T20:20:39",
    },
    {
      ...
    },
    {
      ...
    }]
  "total": 14
  },
  "links": {
    "oai-listsets": "https://127.0.0.1/oai2d?verb=ListSets",
    "oai-listrecords": "https://127.0.0.1/oai2d?verb=ListRecords&metadataPrefix=oai_dc",
    "oai-listidentifiers": "https://127.0.0.1/oai2d?verb=ListIdentifiers&metadataPrefix=oai_dc",
    "oai-identify": "https://127.0.0.1/oai2d?verb=Identify",
  },
}
```

Each hit looks like a set entry below.


### Get a set

`GET /api/oaipmh/sets/{id}`

**Parameters**

| Name     | Type   | Location | Description                                                  |
| -------- | ------ | -------- | ------------------------------------------------------------ |
| `id`     | int    | path     | Identifier of the set, e.g. `1`                              |
| `accept` | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |


**Request**

```http
GET /api/oaipmh/sets/{id} HTTP/1.1
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "{id}",
  "name": "RDM Conference",
  "spec": "rdm-conference"
  "query": "elasticsearch_query:to_match_records",
  "description": "Entries presented at RDM conference",
  "links": {
    "self": "https://127.0.0.1/api/oaipmh/sets/{id}",
    "oai-listrecords": "https://127.0.0.1/oai2d?verb=ListRecords&metadataPrefix=oai_dc&spec=rdm-conference",
    "oai-listidentifiers": "https://127.0.0.1/oai2d?verb=ListIdentifiers&metadataPrefix=oai_dc&spec=rdm-conference",
  },
  "created": "2022-03-21T10:20:39",
  "updated": "2022-03-21T20:20:39",
}
```


### Create a set

`POST /api/oaipmh/sets`

**Parameters**

| Name          | Type   | Location | Description                                                                   |
| --------      | ------ | -------- | ------------------------------------------------------------------------------|
| `name`        | string | body     | name of the set, e.g. `RDM Conference`                                        |
| `spec`        | string | body     | spec of the set, e.g. `rdm-conference`. Used for OAI-PMH selective harvesting |
| `query`       | string | body     | elasticsearch query of the set, e.g. `elasticsearch_query:to_match_records`   |
| `description` | string | body     | description of the set, e.g. `Entries presented at RDM conference`            |
| `accept`      | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json`    |


**Request**

```http
POST /api/oaipmh/sets
```

**Response**

```http
HTTP/1.1 201 CREATED
Content-Type: application/json

{
  "id": "{id}",
  "name": "RDM Conference",
  "spec": "rdm-conference"
  "query": "elasticsearch_query:to_match_records",
  "description": "Entries presented at RDM conference",
  "links": {
    "self": "https://127.0.0.1/api/oaipmh/sets/{id}",
    "oai-listrecords": "https://127.0.0.1/oai2d?verb=ListRecords&metadataPrefix=oai_dc&spec=rdm-conference",
    "oai-listidentifiers": "https://127.0.0.1/oai2d?verb=ListIdentifiers&metadataPrefix=oai_dc&spec=rdm-conference",
  },
  "created": "2022-03-21T10:20:39",
  "updated": "2022-03-21T20:20:39",
}
```

### Update a set

`PUT /api/oaipmh/sets/{id}`

**Parameters**

| Name          | Type   | Location | Description                                                                   |
| --------------| ------ | -------- | ------------------------------------------------------------------------------|
| `id`          | int    | path     | Identifier of the set, e.g. `1`                              |
| `name`        | string | body     | name of the set, e.g. `RDM Conference`                                        |
| `query`       | string | body     | elasticsearch query of the set, e.g. `elasticsearch_query:to_match_records`   |
| `description` | string | body     | description of the set, e.g. `Entries presented at RDM conference`            |
| `accept`      | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json`    |

It is *not* allowed to update the spec of a set. The correct way of doing it is to delete it and create a new one.

**Request**

```http
PUT /api/oaipmh/sets
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "{id}",
  "name": "RDM Conference",
  "spec": "rdm-conference"
  "query": "elasticsearch_query:to_match_records",
  "description": "Entries presented at RDM conference",
  "links": {
    "self": "https://127.0.0.1/api/oaipmh/sets/{id}",
    "oai-listrecords": "https://127.0.0.1/oai2d?verb=ListRecords&metadataPrefix=oai_dc&spec=rdm-conference",
    "oai-listidentifiers": "https://127.0.0.1/oai2d?verb=ListIdentifiers&metadataPrefix=oai_dc&spec=rdm-conference",
  },
  "created": "2022-03-21T10:20:39",
  "updated": "2022-03-21T20:20:39",
}
```


### Delete a set

`DELETE /api/oaipmh/sets/{id}`

**Parameters**

| Name     | Type   | Location | Description                                                  |
| -------- | ------ | -------- | ------------------------------------------------------------ |
| `id`     | int    | path     | Identifier of the set, e.g. `1`                              |


**Request**

```http
DELETE /api/oaipmh/sets/{id}
```

**Response**

```http
HTTP/1.1 204 No Content
```


### Get metadata formats
Returns the available metadata formats, in which records can be retrieved via the OAI-PMH endpoint.

`GET /api/oaipmh/formats`

**Parameters**

| Name     | Type   | Location | Description                                                  |
| -------- | ------ | -------- | ------------------------------------------------------------ |
| `accept` | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |


**Request**

```http
GET /api/oaipmh/formats HTTP/1.1
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "hits": {
    "hits": [
      {
        'id': 'oai_dc',
        'schema': 'http://www.openarchives.org/OAI/2.0/oai_dc.xsd',
        'namespace': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
      },
      ...
    ],
    "total": 3
  }
}
```

# Names

Query and retrieve entries from the [**names** vocabulary](../customize/vocabularies/names.md).

### Search names

`GET /api/names`

**Parameters**

| Name     | Type   | Location | Description                          |
| -------- | ------ | -------- | ------------------------------------ |
| `q`      | string | query    | Search query used to filter results. |
| `sort` | string | query | Sort search results. Built-in options are `"bestmatch"`, `"name"`, `"newest"`, `"oldest"` (default: `"bestmatch"` or `"name"`).  |
| `size`    | integer | query    | Specify number of items in the results page (default: 10).                                                                                                                                                 |
| `page`    | integer | query    | Specify the page of results.                                                                                                                                                                               |
| `suggest` | string | query   | "Search as you type" query.          |
| `accept` | string | header   | - `application/json`                 |

Sort options for names are configured on the vocabulary service class. Note that `"bestmatch"` is only available as a sort option on requests that provide a query string as a `q` parameter. Otherwise `"bestmatch"` is ignored and the default `"name"` sort is used.

**Query string syntax**

The query string syntax is based on [ElasticSearch's query string syntax](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax), and can include the following search fields:

- `name`, `given_name`, `family_name`
- `affiliations.name`
- `identifiers.identifier`

**Request**

```http
GET /api/names?q=smith HTTP/1.1
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "hits": {
    "hits": [
      {
        "given_name": "John",
        "name": "Smith, John",
        "revision_id": 1,
        "identifiers": [
          {
            "scheme": "orcid",
            "identifier": "0000-0002-1825-0097"
          }
        ],
        "updated": "2022-06-02T14:15:09.373996+00:00",
        "family_name": "Smith",
        "created": "2022-06-02T14:15:09.361671+00:00",
        "id": "b31jy-24855",
        "links": {
          "self": "{scheme+hostname}/api/names/b31jy-24855"
        },
        "affiliations": [
          {
            "name": "Wesleyan University"
          }
        ]
      },
      {
        "given_name": "Lisa",
        "name": "Smith, Lisa",
        "revision_id": 1,
        "identifiers": [
          {
            "scheme": "orcid",
            "identifier": "0000-0001-5109-3700"
          }
        ],
        "updated": "2022-06-02T14:15:00.211948+00:00",
        "family_name": "Smith",
        "created": "2022-06-02T14:15:00.199450+00:00",
        "id": "nvr8m-sdt30",
        "links": {
          "self": "{scheme+hostname}/api/names/nvr8m-sdt30"
        },
        "affiliations": [
          {
            "name": "European Organization for Nuclear Research"
          }
        ]
      }
    ],
    "total": 2
  },
  "sortBy": "bestmatch",
  "links": {
    "self": "{scheme+hostname}/api/names?page=1&q=smith&size=25&sort=bestmatch"
  }
}
```

### Get a name

`GET /api/names/{id}`

**Parameters**

| Name     | Type   | Location | Description          |
| -------- | ------ | -------- | -------------------- |
| `id`     | string | path     | The name identifier. |
| `accept` | string | header   | - `application/json` |

**Request**

```http
GET /api/names/{id} HTTP/1.1
Accept: application/json
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "given_name": "Lisa",
  "name": "Smith, Lisa",
  "revision_id": 1,
  "identifiers": [
    {
      "scheme": "orcid",
      "identifier": "0000-0001-5109-3700"
    }
  ],
  "updated": "2022-06-02T14:15:00.211948+00:00",
  "family_name": "Smith",
  "created": "2022-06-02T14:15:00.199450+00:00",
  "id": "{id}",
  "links": {
    "self": "{scheme+hostname}/api/names/{id}"
  },
  "affiliations": [
    {
      "name": "European Organization for Nuclear Research"
    }
  ]
}
```

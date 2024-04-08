# Awards

Query and retrieve entries from the [**awards** vocabulary](../customize/vocabularies/funding.md).

### Search awards

`GET /api/awards`

**Parameters**

| Name     | Type   | Location | Description                          |
| -------- | ------ | -------- | ------------------------------------ |
| `q`      | string | query    | Search query used to filter results. |
| `sort`   | string | query    | Sort search results. Built-in options are `"bestmatch"`, `"title"`, `"newest"`, `"oldest"` (default: `"bestmatch"` or `"title"`).  |
| `size`    | integer | query    | Specify number of items in the results page (default: 10).                                                                                                                                                 |
| `page`    | integer | query    | Specify the page of results.                                                                                                                                                                               |
| `suggest` | string | query   | "Search as you type" query.          |
| `accept` | string | header   | - `application/json`                 |

Sort options for awards are configured on the vocabulary service class. Note that `"bestmatch"` is only available as a sort option on requests that provide a query string as a `q` parameter. Otherwise `"bestmatch"` is ignored and the default `"title"` sort is used.

**Query string syntax**

The query string syntax is based on [ElasticSearch's query string syntax](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax), and can include the following search fields:

- `title.*`
- `number`
- `acronym`
- `funder.id`, `funder.name`
- `identifiers.identifier`

**Request**

```http
GET /api/awards?q=physics HTTP/1.1
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "hits": {
    "hits": [
      {
        "created": "2022-06-07T15:10:22.159293+00:00",
        "id": "021nxhr62::7244408",
        "updated": "2022-06-07T15:10:22.169781+00:00",
        "funder": {
          "name": "National Science Foundation",
          "id": "021nxhr62"
        },
        "revision_id": 2,
        "number": "7244408",
        "links": {
          "self": "{scheme+hostname}/api/awards/021nxhr62%3A%3A7244408"
        },
        "title": {
          "en": "MATHEMATICAL PHYSICS"
        }
      },
      {
        "acronym": "RICOCHET",
        "created": "2022-06-07T15:17:47.733316+00:00",
        "funder": {
          "id": "00rbzpz17",
          "name": "Agence Nationale de la Recherche"
        },
        "id": "00rbzpz17::ANR-20-CE31-0006",
        "links": {
          "self": "{scheme+hostname}/api/awards/00rbzpz17%3A%3AANR-20-CE31-0006"
        },
        "number": "ANR-20-CE31-0006",
        "revision_id": 2,
        "title": {
          "en": "Searching for new physics with the future Ricochet experiment"
        },
        "updated": "2022-06-07T15:17:47.744915+00:00"
      },
      ...
    ],
    "total": 48
  },
  "aggregations": {
    "funders": {
      "buckets": [
        {
          "key": "021nxhr62",
          "doc_count": 40,
          "label": "National Science Foundation (US)",
          "is_selected": false
        },
        {
          "key": "00k4n6c32",
          "doc_count": 3,
          "label": "European Commission (BE)",
          "is_selected": false
        },
        {
          "key": "01cwqze88",
          "doc_count": 2,
          "label": "National Institutes of Health (US)",
          "is_selected": false
        },
        {
          "key": "00rbzpz17",
          "doc_count": 1,
          "label": "National Agency for Research (FR)",
          "is_selected": false
        },
        {
          "key": "00yjd3n13",
          "doc_count": 1,
          "label": "Swiss National Science Foundation (CH)",
          "is_selected": false
        },
        {
          "key": "013tf3c58",
          "doc_count": 1,
          "label": "FWF Austrian Science Fund (AT)",
          "is_selected": false
        }
      ],
      "label": "Funders"
    }
  },
  "sortBy": "bestmatch",
  "links": {
    "self": "{scheme+hostname}/api/awards?page=1&q=physics&size=25&sort=bestmatch",
    "next": "{scheme+hostname}/api/awards?page=2&q=physics&size=25&sort=bestmatch"
  }
}
```

### Get an award

`GET /api/awards/{id}`

**Parameters**

| Name     | Type   | Location | Description          |
| -------- | ------ | -------- | -------------------- |
| `id`     | string | path     | The award identifier. |
| `accept` | string | header   | - `application/json` |

**Request**

```http
GET /api/awards/{id} HTTP/1.1
Accept: application/json
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "revision_id": 2,
  "updated": "2022-06-07T15:17:47.744915+00:00",
  "number": "ANR-20-CE31-0006",
  "funder": {
    "id": "00rbzpz17",
    "name": "Agence Nationale de la Recherche"
  },
  "created": "2022-06-07T15:17:47.733316+00:00",
  "id": "{id}}",
  "links": {
    "self": "{scheme+hostname}/api/awards/{id}"
  },
  "title": {
    "en": "Searching for new physics with the future Ricochet experiment"
  },
  "acronym": "RICOCHET"
}
```

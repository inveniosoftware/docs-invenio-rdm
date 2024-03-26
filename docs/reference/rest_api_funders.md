# Funders

Query and retrieve entries from the [**funders** vocabulary](../customize/vocabularies/funding.md).

### Search funders

`GET /api/funders`

**Parameters**

| Name     | Type   | Location | Description                          |
| -------- | ------ | -------- | ------------------------------------ |
| `q`      | string | query    | Search query used to filter results. |
| `suggest` | string | query   | "Search as you type" query.          |
| `sort` | string | query | Sort search results. Built-in options are `"bestmatch"`, `"name"`, `"newest"`, `"oldest"` (default: `"bestmatch"` or `"name"`).  |
| `size`    | integer | query    | Specify number of items in the results page (default: 10).                                                                                                                                                 |
| `page`    | integer | query    | Specify the page of results.                                                                                                                                                                               |
| `accept` | string | header   | - `application/json`                 |

Sort options for funders are configured on the vocabulary service class. Note that `"bestmatch"` is only available as a sort option on requests that provide a query string as a `q` parameter. Otherwise `"bestmatch"` is ignored and the default `"name"` sort is used.

**Query string syntax**

The query string syntax is based on [ElasticSearch's query string syntax](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax), and can include the following search fields:

- `name`
- `country`
- `identifiers.identifier`

**Request**

```http
GET /api/funders?q=health HTTP/1.1
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "hits": {
    "hits": [
      {
        "name": "National Institutes of Health",
        "country": "US",
        "identifiers": [
          {
            "identifier": "01cwqze88",
            "scheme": "ror"
          }
        ],
        "created": "2022-06-02T14:14:49.783395+00:00",
        "id": "01cwqze88",
        "updated": "2022-06-02T14:14:49.882210+00:00",
        "revision_id": 2,
        "links": {
          "self": "{scheme+hostname}/api/funders/01cwqze88"
        },
        "title": {
          "en": "National Institutes of Health"
        }
      },
      {
        "name": "Canadian Institutes of Health Research",
        "country": "CA",
        "identifiers": [
          {
            "identifier": "01gavpb45",
            "scheme": "ror"
          }
        ],
        "created": "2022-06-02T14:14:49.704849+00:00",
        "id": "01gavpb45",
        "updated": "2022-06-02T14:14:49.790375+00:00",
        "revision_id": 2,
        "links": {
          "self": "{scheme+hostname}/api/funders/01gavpb45"
        },
        "title": {
          "en": "Canadian Institutes of Health Research"
        }
      },
      {
        "name": "National Health and Medical Research Council",
        "country": "AU",
        "identifiers": [
          {
            "identifier": "011kf5r70",
            "scheme": "ror"
          }
        ],
        "created": "2022-06-02T14:14:49.790124+00:00",
        "id": "011kf5r70",
        "updated": "2022-06-02T14:14:49.877488+00:00",
        "revision_id": 2,
        "links": {
          "self": "{scheme+hostname}/api/funders/011kf5r70"
        },
        "title": {
          "en": "National Health and Medical Research Council"
        }
      }
    ],
    "total": 3
  },
  "sortBy": "bestmatch",
  "links": {
    "self": "{scheme+hostname}/api/funders?page=1&q=health&size=25&sort=bestmatch"
  }
}
```

### Get a funder

`GET /api/funders/{id}`

**Parameters**

| Name     | Type   | Location | Description          |
| -------- | ------ | -------- | -------------------- |
| `id`     | string | path     | The funder identifier. |
| `accept` | string | header   | - `application/json` |

**Request**

```http
GET /api/funders/{id} HTTP/1.1
Accept: application/json
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "name": "National Institutes of Health",
  "revision_id": 2,
  "identifiers": [
    {
      "scheme": "ror",
      "identifier": "01cwqze88"
    }
  ],
  "updated": "2022-06-02T14:14:49.882210+00:00",
  "country": "US",
  "created": "2022-06-02T14:14:49.783395+00:00",
  "id": "{id}",
  "links": {
    "self": "{scheme+hostname}/api/funders/{id}"
  },
  "title": {
    "en": "National Institutes of Health"
  }
}
```

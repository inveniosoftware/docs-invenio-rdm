## Vocabularies

Used for accessing vocabulary records. Currently the following vocabularies
are supported:

- Languages (ISO 639-3 language codes)
- Licenses (SPDX licenses)
- Resource types (custom)

### Search vocabularies

`GET /api/vocabularies/{type}`

**Parameters**

| Name      | Type    | Location | Description                                                                                                                                                                                                |
|-----------|---------|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `type`    | string  | path     | Vocabulary (one of `languages`, `licenses` or `resourcetypes`)                                                                                                                                             |
| `q`       | string  | query    | Search query used to filter results based on [ElasticSearch's query string syntax](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax). |
| `suggest` | string  | query    | One or more words used to suggest records as the user types (i.e. auto-complete).                                                                                                                          |
| `tags`    | string  | query    | Filter results to the tag                                                                                                                                                                                  |
| `sort`    | string  | query    | Sort search results. Unless overridden by a specific vocabulary, the built-in options are `"bestmatch"`, `"title"`, `"newest"`, `"oldest"` (default: `"bestmatch"` or `"title"`). |                                                                                                                                                                                       |
| `size`    | integer | query    | Specify number of items in the results page (default: 10).                                                                                                                                                 |
| `page`    | integer | query    | Specify the page of results.                                                                                                                                                                               |
| `accept`  | string  | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json`                                                                                                                                 |

Specifically for the `application/vnd.inveniordm.v1+json` format:

| Name     | Type   | Location | Description                                                  |
| -------- | ------ | -------- | ------------------------------------------------------------ |
| `ln`     | string | query     | Locale used to localize the title and description (e.g. `en` or `en_US`) |
| `accept-language` | string | header   | Locale used to localize the title and description (e.g. `en` or `en_US`) |

The API uses a locale matching algorithm, that will do its best effort to translate the vocabulary record's title and description.

The sort options available vary depending on the vocabulary being searched. These cannot presently be configured via config variables but are set in the service configuration for each vocabulary service. The default sort options are used where a vocabulary service has not defined its own.

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
| `type`   | string | path     | Vocabulary (one of `languages`, `licenses` or `resourcetypes`)            |
| `id`     | string | path     | Identifier of the record, e.g. `eng` for `type` `languages`                       |
| `accept` | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |

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

### Specific vocabularies

Some vocabularies have their own endpoints because their size and structure is different from the vocabularies above.
We refer to these vocabularies as "specific vocabularies".

Their search and get endpoints have the following shape:

**Search**

`GET /api/{type}`

**Get**

`GET /api/{type}/{id}`

Their **Parameters** are the same. Their responses are similar but have fields dependent on the specific vocabulary.

Supported `type`s so far are: `affiliations`, `names`, `funders`, `awards`, and `subjects`.

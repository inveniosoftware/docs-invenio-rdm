# Groups

## Groups

Query and manage groups.

!!! info "Authentication required"

    Requests to search REST API endpoints require authentication. Results sets
    are limited to max 10 results per query (i.e. pagination is not supported).

### Search groups

Search for groups

`GET /api/groups`

**Parameters**

| Name     | Type   | Location | Description                          |
| -------- | ------ | -------- | ------------------------------------ |
| `q`      | string | query    | Search query used to filter results. |
| `accept` | string | header   | - `application/json`                 |

**Query string syntax**

The query string syntax is based on [ElasticSearch's query string syntax](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax).

**Request**

```http
GET /api/groups?q=admin HTTP/1.1
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "hits": {
    "hits": [
      {
        "id": "admin",
        "revision_id": 1,
        "created": "2022-05-23T11:48:27.205711+00:00",
        "updated": "2022-05-23T11:49:14.411568+00:00",
        "name": null,
        "is_managed": true,
        "links": {
          "avatar": "https://127.0.0.1:5000/api/groups/admin/avatar.svg",
          "self": "https://127.0.0.1:5000/api/groups/admin"
        }
      }
    ],
    "total": 1
  },
  "links": {
    "self": "https://127.0.0.1:5000/api/groups?page=1&size=10&sort=name"
  },
  "sortBy": "name"
}
```

### Get a group

`GET /api/group/{id}`

Both authenticated and unauthenticated access is possible.

**Parameters**

| Name     | Type   | Location | Description          |
| -------- | ------ | -------- | -------------------- |
| `id`     | string | path     | The group identifier. |
| `accept` | string | header   | - `application/json` |

**Errors**

- **403**: The group does not exists.

**Request**

```http
GET /api/groups/{id} HTTP/1.1
Accept: application/json
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": "admin",
    "revision_id": 1,
    "created": "2022-05-23T11:48:27.205711+00:00",
    "updated": "2022-05-23T11:49:14.411568+00:00",
    "name": null,
    "is_managed": true,
    "links": {
        "avatar": "https://127.0.0.1:5000/api/groups/admin/avatar.svg",
        "self": "https://127.0.0.1:5000/api/groups/admin"
    }
}
```


### Get avatar for group

`GET /api/groups/{id}/avatar.svg`

Both authenticated and unauthenticated access is possible.

**Parameters**

| Name | Type   | Location | Description          |
| ---- | ------ | -------- | -------------------- |
| `id` | string | path     | The group identifier. |

**Errors**

- **403**: The group does not exists.

**Request**

```http
GET /api/groups/{id}/avatar.svg HTTP/1.1
```

**Response**

```http
HTTP/1.1 200 OK
Content-Disposition: inline; filename=avatar.svg
Content-Length: 351
Content-Type: image/svg+xml; charset=utf-8
ETag: "L#f06292"
...

 <svg width="256" height="256" xmlns="http://www.w3.org/2000/svg">
    <circle cx="125" cy="125" r="125" fill="#f06292" stroke="grey" />
    <text x="48%" y="53%" dominant-baseline="middle" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="125" fill="#f9f9f9" stroke="grey" stroke-width="2">
            L
    </text>
  </svg>
```

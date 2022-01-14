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
Content-Type: application/json

{
  "access": {
    "visibility": "public",
    "member_policy": "open",
    "record_policy": "open"
  },
  "id": "my_community_id",
  "metadata": {
    "title": "My Community",
    "description": "This is an example Community.",
    "type": "event",
    "curation_policy": "This is the kind of records we accept.",
    "page": "Information for my community.",
    "website": "https://www.my_community.org",
    "organizations": [{
      "name": "CERN",
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
    "owned_by": [
      {
          "user": {user-id}
      }
    ],
  },
  "created": "2020-11-27 10:52:23.945755",
  "updated": "2020-11-27 10:52:23.945755",
  "id": "my_community_id",
  "revision_id": 1,
  "links": {
    "self": "{scheme+hostname}/api/communities/my_community_id",
    "self_html": "{scheme+hostname}/communities/my_community_id"
  },
  "metadata": {
    "title": "My Community",
    "description": "This is an example Community.",
    "type": "event",
    "curation_policy": "This is the kind of records we accept.",
    "page": "Information for my community.",
    "website": "https://www.my_community.org",
    "organizations": [{
      "name": "CERN",
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
Content-Type: application/json

{
  "access": {
    "visibility": "public",
    "member_policy": "open",
    "record_policy": "open"
  },
  "id": "my_community_id",
  "metadata": {
    "title": "My Updated Community",
    "description": "This is an example Community.",
    "type": "event",
    "curation_policy": "This is the kind of records we accept.",
    "page": "Information for my community.",
    "website": "https://www.my_community.org",
    "organizations": [{
      "name": "CERN",
    }]
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
    "owned_by": [
      {
          "user": {user-id}
      }
    ]
  },
  "created": "2020-11-27 10:52:23.945755",
  "updated": "2020-11-27 10:55:23.945868",
  "id": "my_community_id",
  "revision_id": 2,
  "links": {
    "self": "{scheme+hostname}/api/communities/my_community_id",
    "self_html": "{scheme+hostname}/communities/my_community_id"
  },
  "metadata": {
    "title": "My Updated Community",
    "description": "This is an example Community.",
    "type": "event",
    "curation_policy": "This is the kind of records we accept.",
    "page": "Information for my community.",
    "website": "https://www.my_community.org",
    "organizations": [{
      "name": "CERN",
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
```

### Get a Community

`GET /api/communities/<comid>`

 **Parameters**

| Name       | Type   | Location | Description                                                  |
| ---------- | ------ | -------- | ------------------------------------------------------------ |
| `comid`    | string | path     | Identifier of the community, e.g.  `my_community`                |
| `accept`   | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |

**Request**

```http
GET /api/communities/<comid> HTTP/1.1
Accept: application/json
```

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "access": {
    "visibility": "public",
    "member_policy": "open",
    "record_policy": "open",
    "owned_by": [
      {
          "user": {user-id}
      }
    ]
  },
  "created": "2020-11-27 10:52:23.945755",
  "updated": "2020-11-27 10:52:23.945868",
  "id": "my_community_id",
  "revision_id": 1,
  "links": {
    "self": "{scheme+hostname}/api/communities/my_community_id",
    "self_html": "{scheme+hostname}/communities/my_community_id"
  },
  "metadata": {
    "title": "My Community",
    "description": "This is an example Community.",
    "type": "event",
    "curation_policy": "This is the kind of records we accept.",
    "page": "Information for my community.",
    "website": "https://www.my_community.org",
    "organizations": [{
      "name": "CERN",
    }]
  }
}
```


### Search Communities

`GET /api/communities`

**Parameters**

| Name           | Type    | Location | Description                                                  |
| -------------- | ------- | -------- | ------------------------------------------------------------ |
| `q`            | string  | query    | Search query used to filter results based on [ElasticSearch's query string syntax](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax). |
| `sort`         | string  | query    | Sort search results (default: newest).                                         |
| `size`         | integer | query    | Specify number of items in the results page (default: 10).   |
| `page`         | integer | query    | Specify the page of results.                                 |
| `type`         | string  | query    | Specify community type as one of organization, event, topic or project. |
| `accept`       | string  | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |


**Request**

```http
GET /api/communities HTTP/1.1
Accept: application/json
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "aggregations": {
    "type": {
      "buckets": [
      {
        "doc_count": 4,
        "key": "event"
      },
      {
        ...
      }],
    "doc_count_error_upper_bound": 0,
    "sum_other_doc_count": 0
    }
  },
  "hits": {
    "hits": [{
      "access": {
        "owned_by": [
          {
            "user": {user-id}
          }
        ],
        "visibility": "public"
      },
      "created": "2021-04-23T14:02:53.385481+00:00",
      "id": "my_comm_id",
      "links": {
        "self": "{scheme+hostname}/api/communities/my_comm_id",
        "self_html": "{scheme+hostname}/communities/my_comm_id"
      },
      "metadata": {"title": "Title", "type": "project"},
      "revision_id": 1,
      "updated": "2021-04-23T14:02:53.398976+00:00"
    },
    {
      ...
    },
    {
      ...
    }]
  "total": 16
  },
  "links": {
    "self": "{scheme+hostname}/api/communities?{params}"
  },
  "sortBy": "newest"
}
```

Each hit looks like a community above.

### Search User Communities

Same as `GET /api/communities` but with the authenticated user's communities in the search results.

`GET /api/user/communities`

**Parameters**

| Name           | Type    | Location | Description                                                  |
| -------------- | ------- | -------- | ------------------------------------------------------------ |
| `q`            | string  | query    | Search query used to filter results based on [ElasticSearch's query string syntax](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax). |
| `sort`         | string  | query    | Sort search results (default: newest).                                         |
| `size`         | integer | query    | Specify number of items in the results page (default: 10).   |
| `page`         | integer | query    | Specify the page of results.                                 |
| `type`         | string  | query    | Specify community type as one of organization, event, topic or project. |
| `accept`       | string  | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |


**Request**

```http
GET /api/user/communities HTTP/1.1
Accept: application/json
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "aggregations": {...},
  "hits": {...},
  "links": {...},
  "sortBy": "newest"
}
```


### Rename a Community

`POST /api/communities/<comid>/rename`

**Parameters**

| Name       | Type   | Location | Description                                                  |
| ---------- | ------ | -------- | ------------------------------------------------------------ |
| `accept`   | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |

**Request**

```http
POST /api/communities/<comid>/rename HTTP/1.1
Content-Type: application/json

{
  "access": {
    "visibility": "public",
    "member_policy": "open",
    "record_policy": "open"
  },
  "id": "my_new_community_id",
  "metadata": {
    "title": "My Community",
    "description": "This is an example Community.",
    "type": "event",
    "curation_policy": "This is the kind of records we accept.",
    "page": "Information for my community.",
    "website": "https://www.my_community.org",
    "organizations": [{
      "name": "CERN",
    }]
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
    "owned_by": [
      {
          "user": {user-id}
      }
    ],
  },
  "created": "2020-11-27 10:52:23.945755",
  "updated": "2020-11-27 10:52:23.945755",
  "id": "my_new_community_id",
  "revision_id": 2,
  "links": {
    "self": "{scheme+hostname}/api/communities/my_new_community_id",
    "self_html": "{scheme+hostname}/communities/my_new_community_id"
  },
  "metadata": {
    "title": "My Community",
    "description": "This is an example Community.",
    "type": "event",
    "curation_policy": "This is the kind of records we accept.",
    "page": "Information for my community.",
    "website": "https://www.my_community.org",
    "organizations": [{
      "name": "CERN",
    }]
  }
}
```

### Update Community Logo

`PUT api/communities/<comid>/logo`

**Parameters**

| Name             | Type    | Location | Description                                       |
| ---------------- | ------- | -------- | ------------------------------------------------- |
| `comid`          | string  | path     | Community name                                    |
| `content-type`   | string  | header   | Should always be `application/octet-stream`.      |
| `accept`         | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |

**Request**

```http
PUT api/communities/<comid>/logo HTTP/1.1
Content-Type: application/octet-stream

<...file binary data...>
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "bucket_id": "d3c493fd",
  "checksum": "md5:96d6f2e7e1f705ab5e59c84a6dc009b2",
  "created": "2021-04-26 10:52:23.945755",
  "file_id": "d2a7adb5",
  "key": "logo",
  "links": {"self": "{scheme+hostname}/api/communities/<comid>/logo"},
  "metadata": None,
  "mimetype": "application/octet-stream",
  "size": file_size,
  "status": "completed",
  "storage_class": "S",
  "updated": "2021-04-26 10:52:24.562652",
  "version_id": "b95ead95"
 }
```

### Get Community Logo
{scheme+hostname}
`GET api/communities/<comid>/logo`

**Parameters**

| Name             | Type    | Location | Description                                       |
| ---------------- | ------- | -------- | ------------------------------------------------- |
| `comid`          | string  | path     | Community name                                    |

**Request**

```http
GET api/communities/<comid>/logo HTTP/1.1

```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "data": <...file binary data...>
}
```

### Delete Community Logo

`DELETE api/communities/<comid>/logo`

**Parameters**

| Name             | Type    | Location | Description                                       |
| ---------------- | ------- | -------- | ------------------------------------------------- |
| `comid`          | string  | path     | Community name                                    |

**Request**

```http
DELETE api/communities/<comid>/logo HTTP/1.1

```

**Response**

```http
HTTP/1.1 204 No Content
```


### Error Responses of Community

`POST /api/communities`

**Parameters**

| Name       | Type   | Location | Description                                                  |
| ---------- | ------ | -------- | ------------------------------------------------------------ |
| `accept`   | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |

**Request**

```http
POST /api/communities HTTP/1.1
Content-Type: application/json

{
  "access": { },
  "id": "comm_id",
  "metadata": { }
}
```

**Response**

```http
HTTP/1.1 400 BAD REQUEST
Content-Type: application/json

{
  "errors": [
    {
      "field": "metadata",
      "messages": [
        "Missing data for required field."
      ]
    },
    {
      "field": "access",
      "messages": [
        "Missing data for required field."
      ]
    }
  ],
 "message": "A validation error occurred.",
 "status": 400
}
```

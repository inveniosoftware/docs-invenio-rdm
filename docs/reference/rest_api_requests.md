# Requests

## Requests

Used for interacting with requests.

### Get a request

`GET /api/requests/{request_id}`

**Parameters**

| Name           | Type   | Location | Description                                                  |
| -------------- | ------ | -------- | ------------------------------------------------------------ |
| `request_id`   | string | path     | The request's public identifier. |
| `accept`       | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` (not yet) |

**Request**

```http
GET /api/requests/{request_id} HTTP/1.1
Accept: application/json
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "created": "2020-11-27 10:52:23.945755",
  "created_by": {"user": "1"},
  "expires_at": null,
  "id": "{request_id}",
  "is_closed": False,
  "is_expired": False,
  "is_open": False,
  "links": {
    "self": "{scheme+hostname}/api/requests/{request_id}",
    "actions": {
      "accept": "{scheme+hostname}/api/requests/{request_id}/actions/accept",
      "cancel": "{scheme+hostname}/api/requests/{request_id}/actions/cancel",
      "decline": "{scheme+hostname}/api/requests/{request_id}/actions/decline",
      "submit": "{scheme+hostname}/api/requests/{request_id}/actions/submit"
    },
  },
  "number": "1",
  "receiver": {"user": "2"},
  "revision_id": 1,
  "status": "draft",
  "title": "Foo bar",
  "topic": {"record": {record_id}},
  "type": "default-request",
  "updated": "2020-11-27 10:52:23.969244",
}
```

### Update a request

!!! warning "Updating a request is not supported yet."

    Because only some properties of a request can be updated manually, updating a request is disabled
    until it can be handled properly.

`PUT /api/requests/{request_id}`

**Parameters**

| Name         | Type   | Location | Description                                                  |
| ------------ | ------ | -------- | ------------------------------------------------------------ |
| `request_id` | string | path     | The request's public identifier. |
| `accept`     | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` (not yet) |


**Request**

```http
PUT /api/requests/{request_id} HTTP/1.1
Content-Type: application/json

{
  "created_by": {"user": "1"},
  "expires_at": null,
  "id": "{request_id}",
  "number": "{request_number}",
  "receiver": {"user": "2"},
  "revision_id": 1,
  "status": "draft",
  "title": "A new title",
  "topic": {"record": "abcd-1234"},
  "type": "default-request",
}
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "created": "2020-11-27 10:52:23.945755",
  "created_by": {"user": "1"},
  "expires_at": null,
  "id": "{request_id}",
  "is_closed": False,
  "is_expired": False,
  "is_open": False,
  "links": {
    "self": "{scheme+hostname}/api/requests/{request_id}",
    "actions": {
      "accept": "{scheme+hostname}/api/requests/{request_id}/actions/accept",
      "cancel": "{scheme+hostname}/api/requests/{request_id}/actions/cancel",
      "decline": "{scheme+hostname}/api/requests/{request_id}/actions/decline",
      "submit": "{scheme+hostname}/api/requests/{request_id}/actions/submit"
    }
  },
  "number": "{request_number}",
  "receiver": {"user": "2"},
  "revision_id": 2,
  "status": "draft",
  "title": "A new title",
  "topic": {"record": "abcd-1234"},
  "type": "default-request",
  "updated": "2020-11-28 10:52:23.969244",
}
```

### Search requests

Used for listing all requests you can interact with.

`GET /api/requests`

**Parameters**

| Name           | Type    | Location | Description                                                  |
| -------------- | ------- | -------- | ------------------------------------------------------------ |
| `q`            | string  | query    | Search query used to filter results based on [ElasticSearch's query string syntax](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax). |
| `sort`         | string  | query    | Sort search results.                                         |
| `size`         | integer | query    | Specify number of items in the results page (default: 10).   |
| `page`         | integer | query    | Specify the page of results.                                 |
| `accept`       | string  | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |

**Request**

```http
GET /api/requests HTTP/1.1
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "hits": {
    "hits": [
      {
        "created": "2020-11-27 10:52:23.945755",
        "created_by": {"user": "1"},
        "expires_at": null,
        "id": "{request_id}",
        "is_closed": False,
        "is_expired": False,
        "is_open": False,
        "links": {
          "self": "{scheme+hostname}/api/requests/{request_id}",
          "actions": {
            "accept": "{scheme+hostname}/api/requests/{request_id}/actions/accept",
            "cancel": "{scheme+hostname}/api/requests/{request_id}/actions/cancel",
            "decline": "{scheme+hostname}/api/requests/{request_id}/actions/decline",
            "submit": "{scheme+hostname}/api/requests/{request_id}/actions/submit"
          }
        },
        "number": "{request_number}",
        "receiver": {"user": "2"},
        "revision_id": 2,
        "status": "draft",
        "title": "A new title",
        "topic": {"record": "abcd-1234"},
        "type": "default-request",
        "updated": "2020-11-28 10:52:23.969244",
      }
      ...
    ],
    "total": 2
  },
  "links": {
    "self": "{scheme+hostname}/api/requests?page=1&size=25&sort=newest"
  }
}
```

## Request Actions

Used for interacting with a request's lifecyle.

!!! info "Request submission"

    A request is submitted via the [draft and record APIs](rest_api_drafts_records.md).

### Accept a request

!!! info "Reviewer-only"

    Only a request's reviewer can accept it.

`POST /api/requests/{request_id}/actions/accept`

**Parameters**

| Name                | Type   | Location | Description                                   |
| ------------------- | ------ | -------- | --------------------------------------------- |
| `request_id` &nbsp; | string | path     | The request's public identifier.              |
| `payload`           | object | body     | The data associated with the comment. See [Comment Payload](#comment-payload). |
| `accept`            | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` (not yet) |

**Request**

```http
POST /api/requests/{request_id}/actions/accept HTTP/1.1
{
  "payload": {"content": "You are in!", "format": "html"}
}
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "created": "2020-11-27 10:52:23.945755",
  "created_by": {"user": "1"},
  "expires_at": null,
  "id": "{request_id}",
  "is_closed": True,
  "is_expired": False,
  "is_open": False,
  "links": {
    "self": "{scheme+hostname}/api/requests/{request_id}",
    "actions": {
      "accept": "{scheme+hostname}/api/requests/{request_id}/actions/accept",
      "cancel": "{scheme+hostname}/api/requests/{request_id}/actions/cancel",
      "decline": "{scheme+hostname}/api/requests/{request_id}/actions/decline",
      "submit": "{scheme+hostname}/api/requests/{request_id}/actions/submit"
    }
  },
  "number": "{request_number}",
  "receiver": {"user": "2"},
  "revision_id": 2,
  "status": "accepted",
  "title": "A new title",
  "topic": {"record": "abcd-1234"},
  "type": "default-request",
  "updated": "2020-11-28 10:52:23.969244",
}
```

### Cancel a request

!!! info "Creator-only"

    Only a request's creator can cancel it. A request's reviewer can decline though.

`POST /api/requests/{request_id}/actions/cancel`

**Parameters**

| Name         | Type   | Location | Description                                   |
| ------------ | ------ | -------- | --------------------------------------------- |
| `request_id` | string | path     | The request's public identifier.              |
| `payload`    | object | body     | The data associated with the comment. See [Comment Payload](#comment-payload). |
| `accept`     | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` (not yet) |

**Request**

```http
POST /api/requests/{request_id}/actions/cancel HTTP/1.1
{
  "payload": {"content": "Didn't mean to do that!", "format": "html"}
}
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "created": "2020-11-27 10:52:23.945755",
  "created_by": {"user": "1"},
  "expires_at": null,
  "id": "{request_id}",
  "is_closed": True,
  "is_expired": False,
  "is_open": False,
  "links": {
    "self": "{scheme+hostname}/api/requests/{request_id}",
    "actions": {
      "accept": "{scheme+hostname}/api/requests/{request_id}/actions/accept",
      "cancel": "{scheme+hostname}/api/requests/{request_id}/actions/cancel",
      "decline": "{scheme+hostname}/api/requests/{request_id}/actions/decline",
      "submit": "{scheme+hostname}/api/requests/{request_id}/actions/submit"
    }
  },
  "number": "{request_number}",
  "receiver": {"user": "2"},
  "revision_id": 2,
  "status": "cancelled",
  "title": "A new title",
  "topic": {"record": "abcd-1234"},
  "type": "default-request",
  "updated": "2020-11-28 10:52:23.969244",
}
```

### Decline a request

!!! info "Reviewer-only"

    Only a request's reviewer can decline it. A request's creator can cancel it though.

`POST /api/requests/{request_id}/actions/decline`

**Parameters**

| Name         | Type   | Location | Description                                   |
| ------------ | ------ | -------- | --------------------------------------------- |
| `request_id` | string | path     | The request's public identifier.              |
| `payload`    | object | body     | The data associated with the comment. See [Comment Payload](#comment-payload). |
| `accept`     | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` (not yet) |

**Request**

```http
POST /api/requests/{request_id}/actions/decline HTTP/1.1
{
  "payload": {"content": "You are not in!", "format": "html"}
}
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "created": "2020-11-27 10:52:23.945755",
  "created_by": {"user": "1"},
  "expires_at": null,
  "id": "{request_id}",
  "is_closed": True,
  "is_expired": False,
  "is_open": False,
  "links": {
    "self": "{scheme+hostname}/api/requests/{request_id}",
    "actions": {
      "accept": "{scheme+hostname}/api/requests/{request_id}/actions/accept",
      "cancel": "{scheme+hostname}/api/requests/{request_id}/actions/cancel",
      "decline": "{scheme+hostname}/api/requests/{request_id}/actions/decline",
      "submit": "{scheme+hostname}/api/requests/{request_id}/actions/submit"
    }
  },
  "number": "{request_number}",
  "receiver": {"user": "2"},
  "revision_id": 2,
  "status": "declined",
  "title": "A new title",
  "topic": {"record": "abcd-1234"},
  "type": "default-request",
  "updated": "2020-11-28 10:52:23.969244",
}
```


## Request Events

Used for interacting with request events.

### Submit a comment on a request

`POST /api/requests/{request_id}/comments`

**Parameters**

| Name           | Type   | Location | Description                                                  |
| -------------- | ------ | -------- | ------------------------------------------------------------ |
| `request_id`   | string | path     | The request's public identifier. |
| `payload`      | object | body     | The data associated with the comment. See [Comment Payload](#comment-payload). |
| `accept`       | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` (not yet) |

#### Comment Payload

| Name       | Type   | Location | Description                                                  |
| ---------- | ------ | -------- | ------------------------------------------------------------ |
| `content`  | string | body     | The comment's textual content. |
| `format`   | string | body     | The format of the textual content. Only `"html"` accepted for now. |


**Request**

```http
POST /api/requests/{request_id}/comments HTTP/1.1
Content-Type: application/json

{
  "payload": {
    "content": "I would use these subject terms to align the record with others in the community.",
    "format": "html"
  }
}
```

**Response**

```http
HTTP/1.1 201 CREATED
Content-Type: application/json

{
  "created_by": {"user": "1"},
  "created": "2020-11-27 10:52:23.945755",
  "id": "{comment_id}",
  "links": {
    "self": "{scheme+hostname}/api/requests/{rquest_id}/comments/{comment_id}"
  },
  "payload": {
    "content": "I would use these subject terms to align the record with others in the community.",
    "format": "html"
  },
  "revision_id": 1,
  "type": "C",
  "updated": "2020-11-27 10:52:23.969244",
}
```

!!! info "The event type"

    Comments are a kind of event related to a request. All events follow the same pattern: they have a
    `type` field identifying their type and a `payload` field with their specific data.


### Get a comment

`GET /api/requests/{request_id}/comments/{comment_id}`

**Parameters**

| Name         | Type   | Location | Description                                                  |
| ------------ | ------ | -------- | ------------------------------------------------------------ |
| `request_id` | string | path     | The request's public identifier. |
| `comment_id` | string | path     | The comment's public identifier                |
| `accept`     | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` (not yet) |

**Request**

```http
GET /api/requests/{request_id}/comments/{comment_id} HTTP/1.1
Accept: application/json
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "created": "2020-11-27 10:52:23.945755",
  "created_by": {"user": "1"},
  "id": "{comment_id}",
  "links": {
    "self": "{scheme+hostname}/api/requests/{rquest_id}/comments/{comment_id}"
  },
  "payload": {
    "content": "I would use these subject terms to align the record with others in the community.",
    "format": "html"
  },
  "revision_id": 1,
  "type": "C",
  "updated": "2020-11-27 10:52:23.969244",
}
```

### Update a comment

`PUT /api/requests/{request_id}/comments/{comment_id}`

**Parameters**

| Name         | Type   | Location | Description                                                  |
| ------------ | ------ | -------- | ------------------------------------------------------------ |
| `request_id` | string | path     | The request's public identifier. |
| `comment_id` | string | path     | The comment's public identifier                |
| `payload`    | object | body     | The data associated with the comment. See above. |
| `accept`     | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` (not yet) |

**Request**

```http
PUT /api/requests/{request_id}/comments/{comment_id} HTTP/1.1
Content-Type: application/json

{
  "payload": {
    "content": "I would use these subject terms to align this record and the other one with others in the community.",
    "format": "html"
  }
}
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json


{
  "created": "2020-11-27 10:52:23.945755",
  "created_by": {"user": "1"},
  "id": "{comment_id}",
  "links": {
    "self": "{scheme+hostname}/api/requests/{rquest_id}/comments/{comment_id}"
  },
  "payload": {
    "content": "I would use these subject terms to align this record and the other one with others in the community.",
    "format": "html"
  },
  "revision_id": 2,
  "type": "C",
  "updated": "2020-11-27 10:55:23.969244",
}
```

### Delete a comment

`DELETE /api/requests/{request_id}/comments/{comment_id}`

Deleting a comment will clear its content and mark it as a "deleted comment event". You can only delete your own comments unless you are a request's reviewer or admin.

**Parameters**

| Name       | Type   | Location | Description                                                  |
| ---------- | ------ | -------- | ------------------------------------------------------------ |
| `request_id`   | string | path     | The request's public identifier. |
| `comment_id`   | string | path     | The comment's public identifier                |
| `accept`   | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` (not yet) |

**Request**

```http
DELETE /api/requests/{request_id}/comments/{comment_id} HTTP/1.1
```

**Response**

```http
HTTP/1.1 204 No Content
```

### Get a request's timeline

`GET /api/requests/{request_id}/timeline`

**Parameters**

| Name                | Type   | Location | Description                                                  |
| ------------------- | ------ | -------- | ------------------------------------------------------------ |
| `request_id` &nbsp; | string | path     | The request's public identifier.                             |
| `q`            | string  | query    | Search query used to filter results based on [ElasticSearch's query string syntax](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax). |
| `sort`         | string  | query    | Sort search results.                                         |
| `size`         | integer | query    | Specify number of items in the results page (default: 10).   |
| `page`         | integer | query    | Specify the page of results.                                 |
| `accept`       | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` (not yet) |

**Request**

```http
GET /api/requests/{request_id}/timeline HTTP/1.1
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "hits": {
    "hits": [
      {
        "created": "2020-11-27 10:52:23.945755",
        "created_by": {"user": "1"},
        "id": "{comment_id}",
        "links": {
          "self": "{scheme+hostname}/api/requests/{rquest_id}/comments/{comment_id}"
        },
        "payload": {
          "content": "I would use these subject terms to align this record and the other one with others in the community.",
          "format": "html"
        },
        "revision_id": 2,
        "type": "C",
        "updated": "2020-11-27 10:55:23.969244",
      },
      ...
    ],
    "total": 2
  },
  "links": {
    "self": "{scheme+hostname}/api/requests/{request_id}/timeline?page=1&size=25&sort=oldest"
  }
}
```

!!! info "Advanced timeline search"

    The timeline endpoint can be searched, sorted, filtered, paginated etc., like any other InvenioRDM search endpoint.

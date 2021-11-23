# Requests REST API

## Requests

Used for interacting with requests.

## Request Events

Used for interacting with request events.

### Submit a comment on a request

`POST /api/requests/{request_id}/comments`

**Parameters**

| Name       | Type   | Location | Description                                                  |
| ---------- | ------ | -------- | ------------------------------------------------------------ |
| `request_id`   | string | path     | The request's public identifier. |
| `payload`    | object | body     | The data associated with he comment. See below. |
| `accept`   | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` (not yet) |

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

| Name       | Type   | Location | Description                                                  |
| ---------- | ------ | -------- | ------------------------------------------------------------ |
| `request_id`   | string | path     | The request's public identifier. |
| `comment_id`       | string | path     | The comment's public identifier                |
| `accept`   | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` (not yet) |

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

| Name       | Type   | Location | Description                                                  |
| ---------- | ------ | -------- | ------------------------------------------------------------ |
| `request_id`   | string | path     | The request's public identifier. |
| `accept`   | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` (not yet) |

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

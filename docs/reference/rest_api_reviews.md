# Reviews

## Draft reviews

!!! info "Working with review requests"

    Review requests are based on the [request APIs](rest_api_requests.md).
    Check their documentation to see how you can
    [post comments](rest_api_requests.md#request-events) and
    [manage](rest_api_requests.md#request-actions) your review request.

### Get a review request

`GET /api/records/{id}/draft/review`

**Parameters**

| Name     | Type   | Location | Description                                   |
|----------|--------|----------|-----------------------------------------------|
| `id`     | string | path     | Identifier of the record, e.g.  `4d0ns-ntd89` |
| `accept` | string | header   | - `application/json`                          |

**Request**

```http
GET /api/records/{id}/draft/review HTTP/1.1
Accept: application/json
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "created": "2022-05-23T14:36:33.538187+00:00",
  "created_by": {
    "user": "3"
  },
  "expires_at": null,
  "id": "{request_id}",
  "is_closed": false,
  "is_expired": false,
  "is_open": false,
  "links": {
    "actions": {
      "submit": "{scheme+hostname}/api/requests/{request_id}/actions/submit"
    },
    "comments": "{scheme+hostname}/api/requests/{request_id}/comments",
    "self": "{scheme+hostname}/api/requests/{request_id}",
    "timeline": "{scheme+hostname}/api/requests/{request_id}/timeline"
  },
  "number": "2",
  "receiver": {
    "community": "{community_id}"
  },
  "revision_id": 2,
  "status": "created",
  "title": "",
  "topic": {
    "record": "{id}"
  },
  "type": "community-submission",
  "updated": "2022-05-23T14:36:33.556820+00:00"
}
```

### Create/update a review request

`PUT /api/records/{id}/draft/review`

**Parameters**

| Name       | Type   | Location | Description                                   |
|------------|--------|----------|-----------------------------------------------|
| `id`       | string | path     | Identifier of the record, e.g.  `4d0ns-ntd89` |
| `accept`   | string | header   | - `application/json`                          |
| `receiver` | object | body     | Receiving entity.                             |
| `type`     | string | body     | Type of the request: - `community-submission` |

**Request**

```http
PUT /api/records/{id}/draft/review HTTP/1.1
Accept: application/json

{
  "receiver": {
    "community": "{community_id}"
  },
  "type": "community-submission"
}
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "created": "2022-05-23T14:36:33.538187+00:00",
  "created_by": {
    "user": "3"
  },
  "expires_at": null,
  "id": "{request_id}",
  "is_closed": false,
  "is_expired": false,
  "is_open": false,
  "links": {
    "actions": {
      "submit": "{scheme+hostname}/api/requests/{request_id}/actions/submit"
    },
    "comments": "{scheme+hostname}/api/requests/{request_id}/comments",
    "self": "{scheme+hostname}/api/requests/{request_id}",
    "timeline": "{scheme+hostname}/api/requests/{request_id}/timeline"
  },
  "number": "2",
  "receiver": {
    "community": "{community_id}"
  },
  "revision_id": 2,
  "status": "created",
  "title": "",
  "topic": {
    "record": "{id}"
  },
  "type": "community-submission",
  "updated": "2022-05-23T14:36:33.556820+00:00"
}
```

### Delete a review request

`DELETE /api/records/{id}/draft/review`

**Parameters**

| Name     | Type   | Location | Description                                   |
|----------|--------|----------|-----------------------------------------------|
| `id`     | string | path     | Identifier of the record, e.g.  `4d0ns-ntd89` |
| `accept` | string | header   | - `application/json`                          |

**Request**

```http
DELETE /api/records/{id}/draft/review HTTP/1.1
Accept: application/json
```

**Response**

```http
HTTP/1.1 204 No Content
```

### Submit a record for review

`POST /api/records/{id}/draft/actions/submit-review`

**Parameters**

| Name      | Type   | Location | Description                                                                                           |
|-----------|--------|----------|-------------------------------------------------------------------------------------------------------|
| `id`      | string | path     | Identifier of the record, e.g.  `4d0ns-ntd89`                                                         |
| `accept`  | string | header   | - `application/json`                                                                                  |
| `payload` | object | body     | Data associated with the review request. See [Comment Payload](rest_api_requests.md#comment-payload). |

**Request**

```http
POST /api/records/{id}/draft/actions/submit-review HTTP/1.1
Accept: application/json

{
  "payload": {
    "content": "Thank you in advance for the review.",
    "format": "html"
  }
}
```

**Response**

```http
HTTP/1.1 202 ACCEPTED
Content-Type: application/json
```

# Users

## Users

Query and manage users.

Only users fulfilling the conditions below will be present in the REST API.

- User MUST have a confirmed email address.
- User MUST be active.
- User MUST have set the profile visibility to public.

!!! info "Authentication required"

    Requests to search REST API endpoints require authentication. Results sets
    are limited to max 10 results per query (i.e. pagination is not supported).

### Search users

Search for users

`GET /api/users`

**Parameters**

| Name     | Type   | Location | Description                          |
| -------- | ------ | -------- | ------------------------------------ |
| `q`      | string | query    | Search query used to filter results. |
| `accept` | string | header   | - `application/json`                 |

**Query string syntax**

The query string syntax is based on [ElasticSearch's query string syntax](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax).

The following search fields:

- ``username``
- ``email``
- ``name`` or ``full_name`` or ``fullname``
- ``affiliation`` or ``affiliations``

**Request**

```http
GET /api/users?q=cern HTTP/1.1
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json


{
  "hits": {
    "hits": [
      {
        "email": "jose.benito.gonzalez@cern.ch",
        "id": "4",
        "is_current_user": false,
        "links": {
          "avatar": "https://127.0.0.1:5000/api/users/4/avatar.svg",
          "self": "https://127.0.0.1:5000/api/users/4"
        },
        "profile": {
          "affiliations": "CERN",
          "full_name": "Jose Benito Gonzalez Lopez"
        },
        "username": "jbenito"
      },
      {
        "active": true,
        "confirmed": true,
        "created": "2022-05-23T12:03:48.466772+00:00",
        "email": "lars.holm.nielsen@cern.ch",
        "id": "3",
        "is_current_user": true,
        "links": {
          "avatar": "https://127.0.0.1:5000/api/users/3/avatar.svg",
          "self": "https://127.0.0.1:5000/api/users/3"
        },
        "preferences": {
          "email_visibility": "public",
          "visibility": "public"
        },
        "profile": {
          "affiliations": "CERN",
          "full_name": "Lars Holm Nielsen"
        },
        "revision_id": 5,
        "updated": "2022-05-23T12:04:16.204875+00:00",
        "username": "lnielsen"
      }
    ],
    "total": 2
  },
  "links": {
    "self": "https://127.0.0.1:5000/api/users"
  },
  "sortBy": "bestmatch"
}
```

### Get a user

`GET /api/users/{id}`

Both authenticated and unauthenticated access is possible.

The following object-level fields are only accessible for the authenticated user
themselves:

- ``revision_id``
- ``created``
- ``updated``
- ``active``
- ``confirmed``
- ``preferences``

The following fields are only accessible for if email visibility is set to
public:

- ``email``

**Parameters**

| Name     | Type   | Location | Description          |
| -------- | ------ | -------- | -------------------- |
| `id`     | string | path     | The user identifier. |
| `accept` | string | header   | - `application/json` |

**Errors**

- **403**: The user does not exists or the profile is not public.

**Request**

```http
GET /api/users/{id} HTTP/1.1
Accept: application/json
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "3",
  "revision_id": 5,
  "created": "2022-05-23T12:03:48.466772+00:00",
  "updated": "2022-05-23T12:04:16.204875+00:00",
  "active": true,
  "confirmed": true,
  "is_current_user": true,
  "username": "lnielsen",
  "email": "lars.holm.nielsen@cern.ch",
  "profile": {
    "affiliations": "CERN",
    "full_name": "Lars Holm Nielsen"
  },
  "preferences": {
    "email_visibility": "public",
    "visibility": "public"
  },
  "links": {
    "avatar": "https://127.0.0.1:5000/api/users/3/avatar.svg",
    "self": "https://127.0.0.1:5000/api/users/3"
  }
}
```


### Get avatar for user

`GET /api/users/{id}/avatar.svg`

Both authenticated and unauthenticated access is possible.

**Parameters**

| Name | Type   | Location | Description          |
| ---- | ------ | -------- | -------------------- |
| `id` | string | path     | The user identifier. |

**Errors**

- **403**: The user does not exists or the profile is not public.

**Request**

```http
GET /api/users/{id}/avatar.svg HTTP/1.1
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

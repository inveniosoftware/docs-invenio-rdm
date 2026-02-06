# Groups

## Groups

Query and manage groups (roles).

!!! info "Authentication required"

    Requests to search REST API endpoints require authentication.
    Creation, update and deletion all require authentication as administrator or superuser.
    Access to **managed** groups is restricted to user administrators (see
    [Managed vs unmanaged groups](#managed-vs-unmanaged-groups) below).

### Managed vs unmanaged groups

- **Managed groups**: Created via the admin UI or REST API and fully
  controllable by admin users with administration moderation permission (e.g.
  administrators and superusers). They support the usual CRUD operations unless
  their names are protected (e.g. `admin`, `superuser-access`).
- **Unmanaged groups**: Typically synced or created by the system (for example
  through identity providers). They are readable by authenticated users but are
  not editable through the REST API or admin UI unless you are a superuser.

### Search groups

`GET /api/groups`

**Parameters**

| Name   | Type    | Location | Description |
|--------|---------|----------|-------------|
| `q`    | string  | query    | Search query used to filter results. |
| `accept` | string | header | - `application/json` |
| `sort` | string  | query    | Sort search results. Built-in options are `"bestmatch"`, `"name"`, `"name_desc"`, `"managed"`, `"unmanaged"`. Default is `"bestmatch"` when `q` is present, otherwise `"name"`. |
| `size` | integer | query    | Items per page (default: `20`, max: `50`). |
| `page` | integer | query    | Page number (default: `1`). |
| `is_managed` | boolean | query | Filter by management state (`true` or `false`). |

**Query string syntax**

The query string syntax is based on [ElasticSearch's query string syntax](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax).

**Request**

```http
GET /api/groups?q=admin&sort=managed&is_managed=true HTTP/1.1
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
                "created": "2026-02-04T09:29:59.790372+00:00",
                "updated": "2026-02-04T09:30:23.892939+00:00",
                "links": {
                    "self": "https://127.0.0.1:5000/api/groups/admin",
                    "avatar": "https://127.0.0.1:5000/api/groups/admin/avatar.svg"
                },
                "revision_id": 1770197423,
                "name": "admin",
                "description": null,
                "is_managed": true
            }
        ],
        "total": 1
    },
    "aggregations": {
        "is_managed": {
            "buckets": [
                {
                    "key": "true",
                    "doc_count": 1,
                    "label": "Managed",
                    "is_selected": true
                }
            ],
            "label": "Management state"
        }
    },
    "sortBy": "managed",
    "links": {
        "self": "https://127.0.0.1:5000/api/groups?is_managed=true&page=1&q=admin&size=20&sort=managed"
    }
}
```

### Get a group

`GET /api/groups/{id}`

Authenticated users can access **unmanaged** groups. Managed groups are only
visible to user administrators or superusers.

**Parameters**

| Name     | Type   | Location | Description |
|----------|--------|----------|-------------|
| `id`     | string | path     | The group identifier (UUID). |
| `accept` | string | header   | - `application/json` |

**Errors**

- **403**: The group is not accessible to the caller.

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
    "id": "bbe66a83-6925-44b9-80e6-eba824b5c9e7",
    "created": "2026-02-04T10:17:11.029064+00:00",
    "updated": "2026-02-04T10:17:11.029082+00:00",
    "links": {
        "self": "https://127.0.0.1:5000/api/groups/bbe66a83-6925-44b9-80e6-eba824b5c9e7",
        "avatar": "https://127.0.0.1:5000/api/groups/bbe66a83-6925-44b9-80e6-eba824b5c9e7/avatar.svg"
    },
    "revision_id": 1770200231,
    "name": "data-stewards",
    "description": "Local data steward team",
    "is_managed": true
}
```

### Create a group

`POST /api/groups`

**Parameters**

| Name           | Type   | Location | Description |
|----------------|--------|----------|-------------|
| `name`         | string | body     | Required. Must start with a letter and contain only letters, numbers, hyphens or underscores (max 80 chars). |
| `description`  | string | body     | Optional. Max 255 chars. |
| `accept`       | string | header   | - `application/json` |

**Errors**

- **400**: Validation error (invalid name or description length).
- **403**: Caller lacks `user_management_action` permissions or tries to create a protected group name.

**Request**

```http
POST /api/groups HTTP/1.1
Content-Type: application/json

{
  "name": "data-stewards",
  "description": "Local data steward team"
}
```

**Response**

```http
HTTP/1.1 201 CREATED
Content-Type: application/json

{
    "id": "bbe66a83-6925-44b9-80e6-eba824b5c9e7",
    "created": "2026-02-04T10:17:11.029064+00:00",
    "updated": "2026-02-04T10:17:11.029082+00:00",
    "links": {
        "self": "https://127.0.0.1:5000/api/groups/bbe66a83-6925-44b9-80e6-eba824b5c9e7",
        "avatar": "https://127.0.0.1:5000/api/groups/bbe66a83-6925-44b9-80e6-eba824b5c9e7/avatar.svg"
    },
    "revision_id": 1770200231,
    "name": "data-stewards",
    "description": "Local data steward team",
    "is_managed": true
}
```

### Update a group

`PUT /api/groups/{id}`

**Parameters**

| Name          | Type   | Location | Description |
|---------------|--------|----------|-------------|
| `id`          | string | path     | The group identifier (UUID). |
| `name`        | string | body     | Optional. Must satisfy the same pattern as creation. |
| `description` | string | body     | Optional. Max 255 chars. |
| `accept`      | string | header   | - `application/json` |

**Errors**

- **400**: Validation error (e.g. description too long).
- **403**: The group is not accessible to the caller.

**Request**

```http
PUT /api/groups/bbe66a83-6925-44b9-80e6-eba824b5c9e7 HTTP/1.1
Content-Type: application/json

{
  "description": "Updated description"
}
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": "bbe66a83-6925-44b9-80e6-eba824b5c9e7",
    "created": "2026-02-04T10:17:11.029064+00:00",
    "updated": "2026-02-04T10:26:45.322262+00:00",
    "links": {
        "self": "https://127.0.0.1:5000/api/groups/bbe66a83-6925-44b9-80e6-eba824b5c9e7",
        "avatar": "https://127.0.0.1:5000/api/groups/bbe66a83-6925-44b9-80e6-eba824b5c9e7/avatar.svg"
    },
    "revision_id": 1770200805,
    "name": "data-stewards",
    "description": "Updated description",
    "is_managed": true
}
```

### Delete a group

`DELETE /api/groups/{id}`

**Parameters**

| Name     | Type   | Location | Description |
|----------|--------|----------|-------------|
| `id`     | string | path     | The group identifier (UUID). |
| `accept` | string | header   | - `application/json` |

**Errors**

- **403**: The group is not accessible to the caller.

**Request**

```http
DELETE /api/groups/2d3b5de5-5d64-4f9d-9c4c-2fd70047f90a HTTP/1.1
```

**Response**

```http
HTTP/1.1 204 No Content
```

### Get avatar for group

`GET /api/groups/{id}/avatar.svg`

**Parameters**

| Name | Type   | Location | Description |
|------|--------|----------|-------------|
| `id` | string | path     | The group identifier (UUID). |

**Errors**

- **403**: The group is not accessible to the caller.

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

### Permissions and protected names

- Only identities with the user management action permission (e.g. user with
  `administration-moderation` role) or the system process can create, update, or delete managed
  groups.
- Some identifiers are protected (e.g. `admin`, `superuser-access`,
  `administration`, `administration-moderation`) and cannot be created or
  modified via the REST API. They can only be changed by system processes.
- Unmanaged groups remain visible to authenticated users but cannot be mutated
  by administrators unless they are superusers.

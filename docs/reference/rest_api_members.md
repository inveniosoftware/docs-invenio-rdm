## Community members

The members API allows you to manage members of a community.

!!! info "Read vs. write separation"

    The members REST API separates writes from reads. This means all state
    changing requests (``POST``, ``PUT`` or ``DELETE``) does not return any
    results (i.e. 204 HTTP response code). You must issue a ``GET`` request to
    retrieve the updated object. Changes are applied asynchronously so you may
    get outdated information if you query right after an update. Changes a
    normally applied within seconds.

The following general restrictions apply to the member API:

- Owners can manage all roles including owners (except themselves).
- Managers can managed all roles except owners (except themselves).
- A community MUST always have at least one owner.
- User can leave a community.
- Members can change their own visibility to both public/hidden.
- Owners/managers can change visibility of members to hidden.

### Search members

`GET /api/communities/{id}/members`

**Parameters**

| Name         | Type    | Location | Description                                                              |
| ------------ | ------- | -------- | ------------------------------------------------------------------------ |
| `id`         | string  | path     | Community UUID identifier                                                |
| `accept`     | string  | header   | - `application/json`                                                     |
| `q`          | string  | query    | Search query used to filter results.                                     |
| `sort`       | string  | query    | Sort search results.                                                     |
| `size`       | integer | query    | Specify number of items in the results page (default: 10).               |
| `page`       | integer | query    | Specify the page of results.                                             |
| `role`       | string  | query    | Filter by role (one of ``reader``, ``curator``, ``manager``, ``owner``). |
| `visibility` | boolean | query    | Filter by visibility (one of ``true``, ``false``)                        |

**Request**

```http
GET /api/communities/bd647379-23ea-477a-970f-201512ae5624/members HTTP/1.1
Accept: application/json
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "hits": {
        "hits": [
            {
                "member": {
                    "type": "user",
                    "id": "4",
                    "name": "Jose Benito Gonzalez Lopez",
                    "description": "CERN",
                    "avatar": "https://127.0.0.1:5000/api/users/4/avatar.svg"
                },
                "id": "4730bf2b-f440-454f-b205-d79842ea809f",
                "updated": "2022-05-23T15:18:11.969226+00:00",
                "permissions": {
                    "can_leave": false,
                    "can_delete": true,
                    "can_update_role": true,
                    "can_update_visible": false
                },
                "role": "reader",
                "created": "2022-05-23T15:17:14.618960+00:00",
                "revision_id": 3,
                "visible": false,
                "is_current_user": false
            },
            {
                "member": {
                    "type": "user",
                    "id": "3",
                    "name": "Lars Holm Nielsen",
                    "description": "CERN",
                    "avatar": "https://127.0.0.1:5000/api/users/3/avatar.svg"
                },
                "id": "3e78d5d1-c162-46b4-8f3c-da2edc8f1192",
                "updated": "2022-05-23T12:42:08.763029+00:00",
                "permissions": {
                    "can_leave": true,
                    "can_delete": false,
                    "can_update_role": false,
                    "can_update_visible": true
                },
                "role": "owner",
                "created": "2022-05-23T12:06:20.437809+00:00",
                "revision_id": 3,
                "visible": true,
                "is_current_user": true
            }
        ],
        "total": 2
    },
    "aggregations": {
        "role": {
            "buckets": [
                {
                    "key": "owner",
                    "doc_count": 1,
                    "label": "Owner",
                    "is_selected": false
                },
                {
                    "key": "reader",
                    "doc_count": 1,
                    "label": "Reader",
                    "is_selected": false
                }
            ],
            "label": "Role"
        },
        "visibility": {
            "buckets": [
                {
                    "key": "false",
                    "doc_count": 1,
                    "label": "Hidden",
                    "is_selected": false
                },
                {
                    "key": "true",
                    "doc_count": 1,
                    "label": "Public",
                    "is_selected": false
                }
            ],
            "label": "Visibility"
        }
    },
    "sortBy": "name",
    "links": {
        "self": "https://127.0.0.1:5000/api/communities/bd647379-23ea-477a-970f-201512ae5624/members?page=1&q=&size=25&sort=name"
    }
}
```

### Search public members

`GET /api/communities/{id}/members/public`

**Parameters**

| Name     | Type    | Location | Description                                                |
| -------- | ------- | -------- | ---------------------------------------------------------- |
| `id`     | string  | path     | Community UUID identifier                                  |
| `accept` | string  | header   | - `application/json`                                       |
| `q`      | string  | query    | Search query used to filter results.                       |
| `size`   | integer | query    | Specify number of items in the results page (default: 10). |
| `page`   | integer | query    | Specify the page of results.                               |

**Request**

```http
GET /api/communities/bd647379-23ea-477a-970f-201512ae5624/members/public HTTP/1.1
Accept: application/json
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "hits": {
        "hits": [
            {
                "member": {
                    "type": "user",
                    "id": "3",
                    "name": "Lars Holm Nielsen",
                    "description": "CERN",
                    "avatar": "https://127.0.0.1:5000/api/users/3/avatar.svg"
                },
                "id": "3e78d5d1-c162-46b4-8f3c-da2edc8f1192"
            }
        ],
        "total": 1
    },
    "sortBy": "name",
    "links": {
        "self": "https://127.0.0.1:5000/api/communities/bd647379-23ea-477a-970f-201512ae5624/members?page=1&q=&size=25&sort=name"
    }
}
```


### Search invitations

`GET /api/communities/{id}/invitations`

**Parameters**

| Name      | Type    | Location | Description                                                                                     |
| --------- | ------- | -------- | ----------------------------------------------------------------------------------------------- |
| `id`      | string  | path     | Community UUID identifier                                                                       |
| `accept`  | string  | header   | - `application/json`                                                                            |
| `q`       | string  | query    | Search query used to filter results.                                                            |
| `sort`    | string  | query    | Sort search results.                                                                            |
| `size`    | integer | query    | Specify number of items in the results page (default: 10).                                      |
| `page`    | integer | query    | Specify the page of results.                                                                    |
| `role`    | string  | query    | Filter by role (one of ``reader``, ``curator``, ``manager``, ``owner``).                        |
| `status`  | string  | query    | Filter by status (one of ``submitted``, ``accepted``, ``declined``, ``expired``, ``cancelled``) |
| `is_open` | boolean | query    | Filter by open/closed (one of ``true``, ``false``)                                              |

**Request**

```http
GET /api/communities/bd647379-23ea-477a-970f-201512ae5624/invitations HTTP/1.1
Accept: application/json
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "hits": {
        "hits": [
            {
                "member": {
                    "type": "user",
                    "id": "4",
                    "name": "Jose Benito Gonzalez Lopez",
                    "description": "CERN",
                    "avatar": "https://127.0.0.1:5000/api/users/4/avatar.svg"
                },
                "id": "252df09b-8fab-4818-8553-a5bf09abfab3",
                "updated": "2022-05-23T12:41:40.779087+00:00",
                "permissions": {
                    "can_cancel": false,
                    "can_update_role": false
                },
                "request": {
                    "is_open": false,
                    "id": "c4381dc0-a395-4291-b4cf-5164f01f1778",
                    "expires_at": "2022-06-22T12:41:19.353850",
                    "status": "accepted"
                },
                "role": "reader",
                "created": "2022-05-23T12:41:19.403553+00:00",
                "revision_id": 1,
                "visible": false,
                "is_current_user": false
            },
            {
                "member": {
                    "type": "user",
                    "id": "4",
                    "name": "Jose Benito Gonzalez Lopez",
                    "description": "CERN",
                    "avatar": "https://127.0.0.1:5000/api/users/4/avatar.svg"
                },
                "id": "4730bf2b-f440-454f-b205-d79842ea809f",
                "updated": "2022-05-23T15:18:11.973365+00:00",
                "permissions": {
                    "can_cancel": false,
                    "can_update_role": false
                },
                "request": {
                    "is_open": false,
                    "id": "9033a8d5-6fa2-4685-87c7-e20c527535d8",
                    "expires_at": "2022-06-22T15:17:14.550679",
                    "status": "accepted"
                },
                "role": "reader",
                "created": "2022-05-23T15:17:14.618960+00:00",
                "revision_id": 1,
                "visible": false,
                "is_current_user": false
            }
        ],
        "total": 2
    },
    "aggregations": {
        "role": {
            "buckets": [
                {
                    "key": "reader",
                    "doc_count": 2,
                    "label": "Reader",
                    "is_selected": false
                }
            ],
            "label": "Role"
        },
        "status": {
            "buckets": [
                {
                    "key": "accepted",
                    "doc_count": 2,
                    "label": "Accepted",
                    "is_selected": false
                }
            ],
            "label": "Status"
        },
        "is_open": {
            "buckets": [
                {
                    "key": "false",
                    "doc_count": 2,
                    "label": "Closed",
                    "is_selected": true
                }
            ],
            "label": "Status"
        }
    },
    "sortBy": "name",
    "links": {
        "self": "https://127.0.0.1:5000/api/communities/bd647379-23ea-477a-970f-201512ae5624/members?is_open=false&page=1&q=&size=10&sort=name"
    }
}
```

### Add group members

`POST /api/communities/{id}/members`

Note, only groups can be added directly as member of a community.
Users must be invited.

The Python programmatic API supports adding users without inviting them via the
system identity.

**Parameters**

| Name           | Type    | Location | Description                                                                 |
| -------------- | ------- | -------- | --------------------------------------------------------------------------- |
| `id`           | string  | path     | Community UUID identifier                                                   |
| `content-type` | string  | header   | - `application/json`                                                        |
| `members`      | object  | body     | List of group members to add.                                               |
| `role`         | string  | body     | Set role of group (one of ``reader``, ``curator``, ``manager``, ``owner``). |
| `visible`      | boolean | body     | Set visibility (one of ``true``, ``false``)                                 |

**Request**

```http
POST /api/communities/acc9058e-b034-49d0-a008-af971a69c34d/members HTTP/1.1
Content-Type: application/json

{
    "members": [
        {
            "id": "admin",
            "type": "group"
        }
    ],
    "role": "curator"
}
```

**Response**

```http
HTTP/1.1 204 NO CONTENT
```

### Invite user members

`POST /api/communities/{id}/invitations`

Note, only users can be invited. Groups must be added directly.

**Parameters**

| Name           | Type    | Location | Description                                                                 |
| -------------- | ------- | -------- | --------------------------------------------------------------------------- |
| `id`           | string  | path     | Community UUID identifier                                                   |
| `content-type` | string  | header   | - `application/json`                                                        |
| `members`      | object  | body     | List of group members to add.                                               |
| `role`         | string  | body     | Set role of group (one of ``reader``, ``curator``, ``manager``, ``owner``). |
| `visible`      | boolean | body     | Set visibility (one of ``true``, ``false``)                                 |
| `message`      | string  | body     | A message to the user being invited.                                        |

**Request**

```http
POST /api/communities/acc9058e-b034-49d0-a008-af971a69c34d/invitations HTTP/1.1
Content-Type: application/json

{
    "members":[
        {
            "id":"4",
            "type":"user"
        }
    ],
    "role":"curator",
    "message":"<p>Hi</p>"
}
```

**Response**

```http
HTTP/1.1 204 NO CONTENT
```

### Remove members / leave community

`DELETE /api/communities/{id}/members`

**Parameters**

| Name           | Type   | Location | Description                      |
| -------------- | ------ | -------- | -------------------------------- |
| `id`           | string | path     | Community UUID identifier        |
| `content-type` | string | header   | - `application/json`             |
| `members`      | object | body     | List of group members to delete. |

**Request**

```http
DELETE /api/communities/acc9058e-b034-49d0-a008-af971a69c34d/members HTTP/1.1
Content-Type: application/json

{
    "members": [
        {
            "type": "user",
            "id": "3"
        }
    ]
}
```

**Response**

```http
HTTP/1.1 204 NO CONTENT
```

### Update members

`PUT /api/communities/{id}/members`

**Parameters**

| Name           | Type    | Location | Description                                                                 |
| -------------- | ------- | -------- | --------------------------------------------------------------------------- |
| `id`           | string  | path     | Community UUID identifier                                                   |
| `content-type` | string  | header   | - `application/json`                                                        |
| `members`      | object  | body     | List of group members to add.                                               |
| `role`         | string  | body     | Set role of group (one of ``reader``, ``curator``, ``manager``, ``owner``). |
| `visible`      | boolean | body     | Set visibility (one of ``true``, ``false``)                                 |


**Request**

```http
PUT /api/communities/acc9058e-b034-49d0-a008-af971a69c34d/members HTTP/1.1
Content-Type: application/json

{
    "members": [
        {
            "id": "admin",
            "type": "group"
        },
        {
            "id": "3",
            "type": "user"
        }
    ],
    "visible": false
    "role": "reader"
}
```

**Response**

```http
HTTP/1.1 204 NO CONTENT
```

### Update invitations

`PUT /api/communities/{id}/invitations`

**Parameters**

| Name           | Type    | Location | Description                                                                 |
| -------------- | ------- | -------- | --------------------------------------------------------------------------- |
| `id`           | string  | path     | Community UUID identifier                                                   |
| `content-type` | string  | header   | - `application/json`                                                        |
| `members`      | object  | body     | List of group members to add.                                               |
| `role`         | string  | body     | Set role of group (one of ``reader``, ``curator``, ``manager``, ``owner``). |
| `visible`      | boolean | body     | Set visibility (one of ``true``, ``false``)                                 |

**Request**

```http
PUT /api/communities/acc9058e-b034-49d0-a008-af971a69c34d/invitations HTTP/1.1
Content-Type: application/json

{
    "members": [
        {
            "id": "3",
            "type": "user"
        }
    ],
    "role": "reader"
}
```

**Response**

```http
HTTP/1.1 204 NO CONTENT
```

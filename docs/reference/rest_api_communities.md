## Communities

### Create a Community

`POST /api/communities`

**Parameters**

| Name       | Type   | Location | Description                                                                                                       |
|------------|--------|----------|-------------------------------------------------------------------------------------------------------------------|
| `accept`   | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json`                                        |
| `access`   | object | body     | [Access](#community-access) of the community.                                                                     |
| `slug`     | string | body     | Required, url-compatible, max 100 char. The identifier of the community that will be used in the community's URL. |                                                  |
| `metadata` | object | body     | [Metadata](#community-metadata) of the community.                                                                 |

### Community access

| Name            | Type   | Location | Description                                                                                                                  |
|-----------------|--------|----------|------------------------------------------------------------------------------------------------------------------------------|
| `visibility`    | string | body     | Required, one of `"public"` or `"restricted"`. Visible by the public or restricted to those who have access.                 |
| `member_policy` | string | body     | Required, one of `"open"` or `"closed"`. Can people ask to be part of the community (open) or not (closed)?                  |
| `record_policy` | string | body     | Required, one of `"open"` or `"closed"` or `"restricted"`. Can records be submitted to the community (open) or not (closed)? |
| `owned_by`      | array  | body     | Array of Objects of the form: `{"user": <user_id> }`. Community owners (admins).                                             |

### Community metadata

| Name              | Type   | Location | Description                                                                                                       |
|-------------------|--------|----------|-------------------------------------------------------------------------------------------------------------------|
| `title`           | string | body     | Required, max 250 char. Human readable title of the community.                                                    |
| `description`     | string | body     | Max 2000 char. Short description of the community.                                                                |
| `curation_policy` | string | body     | Max 2000 char, html allowed. Description of how records are curated for this community.                           |
| `type`            | object | body     | Object with an id and optionally a title, in the form `{"id": "event", "title: { "en": "example_title"}}`         |
| `website`         | string | body     | URL. URL to external website.                                                                                     |
| `organizations`   | array  | body     | Array of Objects of the form: `{"id": <ROR id>}` or `{"name": <string>}`. Organizations related to the community. |


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
    "slug": "my_community_identifier",
    "metadata": {
            "title": "My Community",
            "description": "This is an example Community.",
            "type": {
                "id": "event"
            },
            "curation_policy": "This is the kind of records we accept.",
            "page": "Information for my community.",
            "website": "https://inveniosoftware.org/",
            "organizations": [{
                    "name": "My Org"
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
  "slug": "my_community_identifier",
  "id": "399a3cdc-d2ba-4f63-8b3a-9c2c977a5dd3",
  "revision_id": 1,
  "links": {
    "self": "{scheme+hostname}/api/communities/{community_id}",
    "self_html": "{scheme+hostname}/communities/{community_slug}",
    "settings_html": "{scheme+hostname}/communities/{community_slug}/settings",
    "logo": "{scheme+hostname}/communities/{community_id}/logo",
    "rename": "{scheme+hostname}/communities/{community_id}",
    "members": "{scheme+hostname}/communities/{community_id}/members",
    "public_members": "{scheme+hostname}/communities/{community_id}/members/public",
    "invitations": "{scheme+hostname}/communities/{community_id}/invitations",
    "requests": "{scheme+hostname}/communities/{community_id}/requests"
  },
  "metadata": {
    "title": "My Community",
    "description": "This is an example Community.",
    "type": {
        "id": "event"
    },
    "curation_policy": "This is the kind of records we accept.",
    "page": "Information for my community.",
    "website": "https://inveniosoftware.org/",
    "organizations": [{
      "name": "CERN",
    }]
  }
}
```

### Update a Community

`PUT /api/communities/<com_slug>`

**Parameters**

| Name       | Type   | Location | Description                                                                |
|------------|--------|----------|----------------------------------------------------------------------------|
| `com_slug` | string | path     | Identifier of the community, e.g.  `my_community`                          |
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
  "slug": "my_community_identifier",
  "metadata": {
    "title": "My Updated Community",
    "description": "This is an example Community.",
    "type": {
        "id": "event"
    },
    "curation_policy": "This is the kind of records we accept.",
    "page": "Information for my community.",
    "website": "https://inveniosoftware.org/",
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
    "record_policy": "open"
  },
  "created": "2020-11-27 10:52:23.945755",
  "updated": "2020-11-27 10:55:23.945868",
  "slug": "my_community_identifier",
  "id": "399a3cdc-d2ba-4f63-8b3a-9c2c977a5dd3",
  "revision_id": 2,
  "links": {
    "self": "{scheme+hostname}/api/communities/{community_id}",
    "self_html": "{scheme+hostname}/communities/{community_slug}",
    "settings_html": "{scheme+hostname}/communities/{community_slug}/settings",
    "logo": "{scheme+hostname}/communities/{community_id}/logo",
    "rename": "{scheme+hostname}/communities/{community_id}",
    "members": "{scheme+hostname}/communities/{community_id}/members",
    "public_members": "{scheme+hostname}/communities/{community_id}/members/public",
    "invitations": "{scheme+hostname}/communities/{community_id}/invitations",
    "requests": "{scheme+hostname}/communities/{community_id}/requests"
  },
  "metadata": {
    "title": "My Updated Community",
    "description": "This is an example Community.",
    "type": {
        "id": "event"
    },
    "curation_policy": "This is the kind of records we accept.",
    "page": "Information for my community.",
    "website": "https://inveniosoftware.org/",
    "organizations": [{
      "name": "CERN"
    }]
  }
}
```

### Delete a Community

`DELETE /api/communities/<com_slug>`

**Parameters**

| Name       | Type   | Location | Description                                                                |
|------------|--------|----------|----------------------------------------------------------------------------|
| `com_slug` | string | path     | Identifier of the community, e.g.  `my_community`                          |
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

`GET /api/communities/<com_id>`

 **Parameters**

| Name     | Type   | Location | Description                                                                |
|----------|--------|----------|----------------------------------------------------------------------------|
| `com_id` | string | path     | UUID of the community e.g.  `399a3cdc-d2ba-4f63-8b3a-9c2c977a5dd3`         |
| `accept` | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |

**Request**

```http
GET /api/communities/<com_id> HTTP/1.1
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
    "record_policy": "open"
  },
  "created": "2020-11-27 10:52:23.945755",
  "updated": "2020-11-27 10:55:23.945868",
  "slug": "my_community_identifier",
  "id": "399a3cdc-d2ba-4f63-8b3a-9c2c977a5dd3",
  "revision_id": 2,
  "links": {
    "self": "{scheme+hostname}/api/communities/{community_id}",
    "self_html": "{scheme+hostname}/communities/{community_slug}",
    "settings_html": "{scheme+hostname}/communities/{community_slug}/settings",
    "logo": "{scheme+hostname}/communities/{community_id}/logo",
    "rename": "{scheme+hostname}/communities/{community_id}",
    "members": "{scheme+hostname}/communities/{community_id}/members",
    "public_members": "{scheme+hostname}/communities/{community_id}/members/public",
    "invitations": "{scheme+hostname}/communities/{community_id}/invitations",
    "requests": "{scheme+hostname}/communities/{community_id}/requests",
    "featured": "{scheme+hostname}/communities/{community_id}/featured"
  },
  "metadata": {
    "title": "My Updated Community",
    "description": "This is an example Community.",
    "type": {
        "id": "event"
    },
    "curation_policy": "This is the kind of records we accept.",
    "page": "Information for my community.",
    "website": "https://inveniosoftware.org/",
    "organizations": [{
      "name": "CERN"
    }]
  }
}
```


### Search Communities

`GET /api/communities`

**Parameters**

| Name     | Type    | Location | Description                                                                                                                                                                                                |
|----------|---------|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `q`      | string  | query    | Search query used to filter results based on [ElasticSearch's query string syntax](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax). |
| `sort`   | string  | query    | Sort search results (default: newest).                                                                                                                                                                     |
| `size`   | integer | query    | Specify number of items in the results page (default: 10).                                                                                                                                                 |
| `page`   | integer | query    | Specify the page of results.                                                                                                                                                                               |
| `type`   | string  | query    | Specify community type as one of organization, event, topic or project.                                                                                                                                    |
| `accept` | string  | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json`                                                                                                                                 |


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
        "visibility": "public",
        "member_policy": "open",
        "record_policy": "open"
      },
      "created": "2020-11-27 10:52:23.945755",
      "updated": "2020-11-27 10:55:23.945868",
      "slug": "my_community_identifier",
      "id": "399a3cdc-d2ba-4f63-8b3a-9c2c977a5dd3",
      "revision_id": 2,
      "links": {
        "self": "{scheme+hostname}/api/communities/{community_id}",
        "self_html": "{scheme+hostname}/communities/{community_slug}",
        "settings_html": "{scheme+hostname}/communities/{community_slug}/settings",
        "logo": "{scheme+hostname}/communities/{community_id}/logo",
        "rename": "{scheme+hostname}/communities/{community_id}",
        "members": "{scheme+hostname}/communities/{community_id}/members",
        "public_members": "{scheme+hostname}/communities/{community_id}/members/public",
        "invitations": "{scheme+hostname}/communities/{community_id}/invitations",
        "requests": "{scheme+hostname}/communities/{community_id}/requests"
      },
      "metadata": {
        "title": "My Updated Community",
        "description": "This is an example Community.",
        "type": {
            "id": "event"
        },
        "curation_policy": "This is the kind of records we accept.",
        "page": "Information for my community.",
        "website": "https://inveniosoftware.org/",
        "organizations": [{
          "name": "CERN"
        }]
      }
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

| Name     | Type    | Location | Description                                                                                                                                                                                                |
|----------|---------|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `q`      | string  | query    | Search query used to filter results based on [ElasticSearch's query string syntax](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax). |
| `sort`   | string  | query    | Sort search results (default: newest).                                                                                                                                                                     |
| `size`   | integer | query    | Specify number of items in the results page (default: 10).                                                                                                                                                 |
| `page`   | integer | query    | Specify the page of results.                                                                                                                                                                               |
| `type`   | string  | query    | Specify community type as one of organization, event, topic or project.                                                                                                                                    |
| `accept` | string  | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json`                                                                                                                                 |


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

`POST /api/communities/<com_id>/rename`

**Parameters**

| Name     | Type   | Location | Description                                                                |
|----------|--------|----------|----------------------------------------------------------------------------|
| `accept` | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |
 | `com_id` | string | path     | UUID of the community e.g.  `399a3cdc-d2ba-4f63-8b3a-9c2c977a5dd3`         |

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
  "slug": "my_new_community_identifier",
  "metadata": {
    "title": "My Community",
    "description": "This is an example Community.",
    "type": "event",
    "curation_policy": "This is the kind of records we accept.",
    "page": "Information for my community.",
    "website": "https://inveniosoftware.org/",
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
  "slug": "my_new_community_identifier",
  "id": "399a3cdc-d2ba-4f63-8b3a-9c2c977a5dd3",
  "revision_id": 2,
  "links": {
    "self": "{scheme+hostname}/api/communities/{community_id}",
    "self_html": "{scheme+hostname}/communities/{community_slug}",
    "settings_html": "{scheme+hostname}/communities/{community_slug}/settings",
    "logo": "{scheme+hostname}/communities/{community_id}/logo",
    "rename": "{scheme+hostname}/communities/{community_id}",
    "members": "{scheme+hostname}/communities/{community_id}/members",
    "public_members": "{scheme+hostname}/communities/{community_id}/members/public",
    "invitations": "{scheme+hostname}/communities/{community_id}/invitations",
    "requests": "{scheme+hostname}/communities/{community_id}/requests"
  },
  "metadata": {
    "title": "My Community",
    "description": "This is an example Community.",
    "type": "event",
    "curation_policy": "This is the kind of records we accept.",
    "page": "Information for my community.",
    "website": "https://inveniosoftware.org/",
    "organizations": [{
      "name": "CERN",
    }]
  }
}
```

### Update Community Logo

`PUT api/communities/<com_id>/logo`

**Parameters**

| Name           | Type   | Location | Description                                                                |
|----------------|--------|----------|----------------------------------------------------------------------------|
| `com_id`       | string | path     | UUID of the community e.g.  `399a3cdc-d2ba-4f63-8b3a-9c2c977a5dd3`         |
| `content-type` | string | header   | Should always be `application/octet-stream`.                               |
| `accept`       | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |

**Request**

```http
PUT api/communities/<com_id>/logo HTTP/1.1
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
`GET api/communities/<com_id>/logo`

**Parameters**

| Name     | Type   | Location | Description                                                        |
|----------|--------|----------|--------------------------------------------------------------------|
| `com_id` | string | path     | UUID of the community e.g.  `399a3cdc-d2ba-4f63-8b3a-9c2c977a5dd3` |

**Request**

```http
GET api/communities/<com_id>/logo HTTP/1.1

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

`DELETE api/communities/<com_id>/logo`

**Parameters**

| Name     | Type   | Location | Description                                                        |
|----------|--------|----------|--------------------------------------------------------------------|
| `com_id` | string | path     | UUID of the community e.g.  `399a3cdc-d2ba-4f63-8b3a-9c2c977a5dd3` |

**Request**

```http
DELETE api/communities/<com_id>/logo HTTP/1.1

```

**Response**

```http
HTTP/1.1 204 No Content
```


### Error Responses of Community

`POST /api/communities`

**Parameters**

| Name     | Type   | Location | Description                                                                |
|----------|--------|----------|----------------------------------------------------------------------------|
| `accept` | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |

**Request**

```http
POST /api/communities HTTP/1.1
Content-Type: application/json

{
  "access": { },
  "slug": "my_community_identifier",
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
      "field": "metadata.title",
      "messages": [
        "Missing data for required field."
      ]
    },
  ],
 "message": "A validation error occurred.",
 "status": 400
}
```


## Featured Communities
The goal of featured communities is to increase the level of awareness for a community. This could be due to special research output, because a community is new or any other reason a community should be put in the spotlight.

!!! hint
    Only public communities may be featured, as they can be accessed by everyone.
    
    Only the search is available to any user. Other endpoints require the `system_process` permission need.

### Search Featured Communities

`GET /api/communities/featured`

**Parameters**

| Name           | Type    | Location | Description                                                  |
| -------------- | ------- | -------- | ------------------------------------------------------------ |
| `q`            | string  | query    | Search query used to filter results based on [ElasticSearch's query string syntax](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax). |
| `size`         | integer | query    | Specify number of items in the results page (default: 10).   |
| `page`         | integer | query    | Specify the page of results.                                 |
| `type`         | string  | query    | Specify community type as one of organization, event, topic or project. |
| `accept`       | string  | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json` |

Only communities with a featured timestamp before the current time are retrieved.
They are sorted by the begin of their latest featured timestamp (e.g. A is featured starting with 2022-06-01, B is featured starting with 2022-06-03 then the order will be [B, A]).

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
  "hits": {
    "hits": [
      {
        "created": "2022-06-03T10:04:14.837956+00:00",
        "links": {
          "self": "{scheme+hostname}/api/communities/21c0c843-c3c1-40df-9bcd-225b9a4f9021",
          "self_html": "{scheme+hostname}/communities/c2-id",
          "settings_html": "{scheme+hostname}/communities/c2-id/settings",
          "logo": "{scheme+hostname}/api/communities/21c0c843-c3c1-40df-9bcd-225b9a4f9021/logo",
          "rename": "{scheme+hostname}/api/communities/21c0c843-c3c1-40df-9bcd-225b9a4f9021/rename",
          "members": "{scheme+hostname}/api/communities/21c0c843-c3c1-40df-9bcd-225b9a4f9021/members",
          "public_members": "{scheme+hostname}/api/communities/21c0c843-c3c1-40df-9bcd-225b9a4f9021/members/public",
          "invitations": "{scheme+hostname}/api/communities/21c0c843-c3c1-40df-9bcd-225b9a4f9021/invitations",
          "requests": "{scheme+hostname}/api/communities/21c0c843-c3c1-40df-9bcd-225b9a4f9021/requests"
        },
        "metadata": {
          "title": "My Community"
        },
        "id": "21c0c843-c3c1-40df-9bcd-225b9a4f9021",
        "updated": "2022-06-03T10:04:14.852380+00:00",
        "access": {
          "member_policy": "open",
          "record_policy": "open",
          "visibility": "public"
        },
        "revision_id": 2,
        "slug": "c2-id"
      },
      {
        "created": "2022-06-03T10:04:14.659785+00:00",
        "links": {
          "self": "{scheme+hostname}/api/communities/9b44aa91-de2b-4551-97ff-8a9cb25e5752",
          "self_html": "{scheme+hostname}/communities/1654243454-614428",
          "settings_html": "{scheme+hostname}/communities/1654243454-614428/settings",
          "logo": "{scheme+hostname}/api/communities/9b44aa91-de2b-4551-97ff-8a9cb25e5752/logo",
          "rename": "{scheme+hostname}/api/communities/9b44aa91-de2b-4551-97ff-8a9cb25e5752/rename",
          "members": "{scheme+hostname}/api/communities/9b44aa91-de2b-4551-97ff-8a9cb25e5752/members",
          "public_members": "{scheme+hostname}/api/communities/9b44aa91-de2b-4551-97ff-8a9cb25e5752/members/public",
          "invitations": "{scheme+hostname}/api/communities/9b44aa91-de2b-4551-97ff-8a9cb25e5752/invitations",
          "requests": "{scheme+hostname}/api/communities/9b44aa91-de2b-4551-97ff-8a9cb25e5752/requests"
        },
        "metadata": {
          "title": "My Community"
        },
        "id": "9b44aa91-de2b-4551-97ff-8a9cb25e5752",
        "updated": "2022-06-03T10:04:14.685074+00:00",
        "access": {
          "member_policy": "open",
          "record_policy": "open",
          "visibility": "public"
        },
        "revision_id": 2,
        "slug": "1654243454-614428"
      }
    ],
    "total": 2
  },
  "aggregations": {
    "type": {
      "buckets": [],
      "label": "Type"
    },
    "visibility": {
      "buckets": [
        {
          "key": "public",
          "doc_count": 2,
          "label": "Public",
          "is_selected": false
        }
      ],
      "label": "Visibility"
    }
  },
  "sortBy": "featured",
  "links": {
    "self": "{scheme+hostname}/api/communities/featured?page=1&size=25&sort=featured"
  }
}

```
### Create a Featured Community Entry

`POST /api/communities/<community_id>/featured`

**Parameters**

| Name          | Type   | Location | Description                                                  |
| ----------    | ------ | -------- | ------------------------------------------------------------ |
| `accept`      | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json`                    |
| `community_id`| string | path     | ID of the community.                                                                          |
| `start_date`  | string | body     | Required, datetime in iso format. Community will be featured from this point in time onwards. |


**Request**

```http
POST /api/communities/<community_id>/featured HTTP/1.1
Content-Type: application/json

{
  "start_date": "2022-06-03 10:52:23.945755"
}
```

**Response**

```http
HTTP/1.1 201 CREATED
Content-Type: application/json

{
  "start_date": "2022-06-03 10:52:23.945755"
  "id": 1
}
```

### Get Featured Community Entries

`GET /api/communities/<community_id>/featured`

**Parameters**

| Name          | Type   | Location | Description                                                  |
| ----------    | ------ | -------- | ------------------------------------------------------------ |
| `accept`      | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json`                  |
| `community_id`| string | path     | ID of the community.                                                                        |


**Request**

```http
GET /api/communities/<community_id>/featured HTTP/1.1
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "hits": {
    "hits": [
      {
        "start_date": "2022-06-03T10:32:42.207652",
        "id": 8
      },
      {
        "start_date": "2022-06-04T10:32:42.207662",
        "id": 9
      }
    ],
    "total": 2
  }
}
```


### Update a Featured Community Entry

`PUT /api/communities/<community_id>/featured/<featured_entry_id>`

**Parameters**

| Name                | Type   | Location | Description                                                  |
| ----------          | ------ | -------- | ------------------------------------------------------------ |
| `accept`            | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json`              |
| `community_id`      | string | path     | ID of the community.                                                                    |
| `featured_entry_id` | string | path     | ID of the featured entry.                                                               |
| `start_date`  | string | body     | Required, datetime in iso format. Community will be featured from this point in time onwards. |


**Request**

```http
PUT /api/communities/<community_id>/featured/<featured_entry_id> HTTP/1.1
Content-Type: application/json

{
  "start_date": "2022-06-03 10:52:23.945755"
}
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "start_date": "2022-06-03 10:52:23.945755"
  "id": <featured_entry_id>
}
```

### Delete a Featured Community Entry

`DELETE /api/communities/<community_id>/featured/<featured_entry_id>`

**Parameters**

| Name                | Type   | Location | Description                                                  |
| ----------          | ------ | -------- | ------------------------------------------------------------ |
| `accept`            | string | header   | - `application/json` (default)<br />- `application/vnd.inveniordm.v1+json`                  |
| `community_id`      | string | path     | ID of the community.                                                                        |
| `featured_entry_id` | string | path     | ID of the featured entry.                                                                   |


**Request**

```http
DELETE /api/communities/<community_id>/featured/<featured_entry_id> HTTP/1.1
```

**Response**

```http
HTTP/1.1 204 No Content
```

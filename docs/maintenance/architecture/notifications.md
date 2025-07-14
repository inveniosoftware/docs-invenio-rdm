# Notifications

_Introduced in v12_

The notification system in InvenioRDM is provided via the [`invenio-notifications`](https://github.com/inveniosoftware/invenio-notifications) module.


## Service Level

Notifications are registered at the service level in the unit of work and send off to a celery task - which takes care of further processing. When dispatching this notification in the service, the context shall be as minimal as possible, to reduce passing huge chunks of data.
The implications of sending all of the required immediately would be a hit on performance and higher memory usage.
As the notification operations are registered during methods of the service level, it would increase response time for requests using these methods.
As we can offload the extension of the notification to a worker, the initial request can be processed quicker and save some precious time - leading to faster response times.

This is an example of creating a notification
```py
n = Notification(type="community-submission", context={"request": request.id})
```

After it is build, it can be dumped and send to a background task for further processing. The serialized notification will look like this
```py
{
    "type": "community-submission",
    "context": {
        "request": 1
    }
}
```


## Notification Manager

A notification manager is created, which will rely on certain [configuration values](../../operate/customize/notifications_modify.md#configuration-values) and provide logic to send notifications. Its task is also to call respective methods to resolve the notification context, generate recipients, filter recipients and generate the backend ids for further processing. With all information created, it will then dispatch further tasks to relay the notification to the backend, which will take care of sending the actual notification.

<details>
<summary>A recipient entity could look like this</summary>

```py
{
  "data": {
    "id": "5",
    "created": "2023-08-03T12:37:24.353656+00:00",
    "updated": "2023-08-03T12:37:24.971301+00:00",
    "links": {
      "self": "https://127.0.0.1:5000/api/users/5",
      "avatar": "https://127.0.0.1:5000/api/users/5/avatar.svg"
    },
    "revision_id": 5,
    "active": true,
    "confirmed": true,
    "is_current_user": false,
    "email": "newuser@newuser.org",
    "username": null,
    "profile": {
      "full_name": "New User",
      "affiliations": "CERN"
    },
    "preferences": {
      "visibility": "public",
      "email_visibility": "restricted",
      "locale": "en",
      "timezone": "Europe/Zurich",
      "notifications": {
        "enabled": true
      }
    }
  }
}
```
</details>

<details>
<summary>After resolving all entities, a notification could look like this</summary>

```py
{
  "type": "community-invitation.submit",
  "context": {
    "request": {
      "id": "372cd107-7b76-4a45-9c10-c339f4c2a3ac",
      "created": "2023-08-03T12:32:06.251565+00:00",
      "updated": "2023-08-03T12:32:06.260397+00:00",
      "links": {
        "actions": {
          "accept": "https://127.0.0.1:5000/api/requests/372cd107-7b76-4a45-9c10-c339f4c2a3ac/actions/accept",
          "decline": "https://127.0.0.1:5000/api/requests/372cd107-7b76-4a45-9c10-c339f4c2a3ac/actions/decline",
          "cancel": "https://127.0.0.1:5000/api/requests/372cd107-7b76-4a45-9c10-c339f4c2a3ac/actions/cancel",
          "expire": "https://127.0.0.1:5000/api/requests/372cd107-7b76-4a45-9c10-c339f4c2a3ac/actions/expire"
        },
        "self": "https://127.0.0.1:5000/api/requests/372cd107-7b76-4a45-9c10-c339f4c2a3ac",
        "self_html": "https://127.0.0.1:5000/requests/372cd107-7b76-4a45-9c10-c339f4c2a3ac",
        "comments": "https://127.0.0.1:5000/api/requests/372cd107-7b76-4a45-9c10-c339f4c2a3ac/comments",
        "timeline": "https://127.0.0.1:5000/api/requests/372cd107-7b76-4a45-9c10-c339f4c2a3ac/timeline"
      },
      "revision_id": 2,
      "type": "community-invitation",
      "title": "Invitation to join \"My Community\"",
      "description": "You will join as \"Reader\".",
      "number": "2",
      "status": "submitted",
      "is_closed": false,
      "is_open": true,
      "expires_at": "2023-09-02T12:32:06.239340+00:00",
      "is_expired": false,
      "created_by": {
        "id": "232d2ae9-ac03-4359-bc8e-9fa95e66ced0",
        "created": "2023-08-03T12:32:05.556911+00:00",
        "updated": "2023-08-03T12:32:05.595929+00:00",
        "links": {
          "featured": "https://127.0.0.1:5000/api/communities/232d2ae9-ac03-4359-bc8e-9fa95e66ced0/featured",
          "self": "https://127.0.0.1:5000/api/communities/232d2ae9-ac03-4359-bc8e-9fa95e66ced0",
          "self_html": "https://127.0.0.1:5000/communities/public",
          "settings_html": "https://127.0.0.1:5000/communities/public/settings",
          "logo": "https://127.0.0.1:5000/api/communities/232d2ae9-ac03-4359-bc8e-9fa95e66ced0/logo",
          "rename": "https://127.0.0.1:5000/api/communities/232d2ae9-ac03-4359-bc8e-9fa95e66ced0/rename",
          "members": "https://127.0.0.1:5000/api/communities/232d2ae9-ac03-4359-bc8e-9fa95e66ced0/members",
          "public_members": "https://127.0.0.1:5000/api/communities/232d2ae9-ac03-4359-bc8e-9fa95e66ced0/members/public",
          "invitations": "https://127.0.0.1:5000/api/communities/232d2ae9-ac03-4359-bc8e-9fa95e66ced0/invitations",
          "requests": "https://127.0.0.1:5000/api/communities/232d2ae9-ac03-4359-bc8e-9fa95e66ced0/requests",
          "records": "https://127.0.0.1:5000/api/communities/232d2ae9-ac03-4359-bc8e-9fa95e66ced0/records"
        },
        "revision_id": 2,
        "slug": "public",
        "metadata": {
          "title": "My Community"
        },
        "access": {
          "visibility": "public",
          "member_policy": "open",
          "record_policy": "open",
          "review_policy": "closed"
        },
        "custom_fields": {}
      },
      "receiver": {
        "id": "5",
        "created": "2023-08-03T12:32:05.683922+00:00",
        "updated": "2023-08-03T12:32:06.366896+00:00",
        "links": {
          "self": "https://127.0.0.1:5000/api/users/5",
          "avatar": "https://127.0.0.1:5000/api/users/5/avatar.svg"
        },
        "revision_id": 6,
        "active": true,
        "confirmed": true,
        "is_current_user": false,
        "email": "newuser@newuser.org",
        "username": null,
        "profile": {
          "full_name": "New User",
          "affiliations": "CERN"
        },
        "preferences": {
          "visibility": "public",
          "email_visibility": "restricted",
          "locale": "en",
          "timezone": "Europe/Zurich",
          "notifications": {
            "enabled": true
          }
        }
      },
      "topic": {
        "community": "232d2ae9-ac03-4359-bc8e-9fa95e66ced0"
      }
    },
    "role": "Reader",
    "message": null
  }
}
```
</details>

# How to modify notifications
This guide will show you how you can configure and modify all things related to notifications.

## Templates

In order to provide your own customized templates or override parts of existing ones, templates can be placed in the `<my-site>/templates/semantic-ui/invenio_notifications` folder. The file name then has to match the base template name (e.g. `community-submission.submitted.jinja`). So we end up with

```
<my-site>/templates/semantic-ui/invenio_notifications/community-submission.submitted.jinja
```

Let's have a look at a base template and then customize parts of it for our own needs.

Assume a notification context like this:

```py
{
    "request": {
        "links": {
            "self_html": "<link to the request>",
        },
        "created_by": {
            "id": 3,
            "username": "Chris the Creator",
        },
        "receiver": {
            "id":  "3fc4fcaa-ce2c-4ec7-97cd-4b29ca204035",
            "metadata": {
                "title": "Notification Community",
            },
            "links": {
                "self_html": "<link to the community>",
            }
        },
        "topic": {
            "id": "49e72dea-f14a-4774-a52d-a3d581fed86e",
            "metadata": {
                "title": "My Submitted Record",
            },
        }
    }
}
```

```jinja
{# notifications/community-submission.submitted.jinja #}

{%- block subject -%}
New record submission for your community {{ notification.context.get("request").get("receiver").get("metadata").get("title") }} submitted by {{ notification.context.get("request").get("created_by").get("username") }}
{%- endblock subject -%}

{%- block html_body -%}
<p>The record "{{ notification.context.get("request").get("topic").get("metadata").get("title") }}" was submitted to your community {{ notification.context.get("request").get("receiver").get("metadata").get("title") }} by {{ notification.context.get("request").get("created_by").get("username") }}.</p>

<a href="{{ notification.context.get("request").get("links").get("self_html") }}" class="button">Review the request</a>
{%- endblock html_body -%}

{%- block plain_body -%}
The record "{{ notification.context.get("request").get("topic").get("metadata").get("title") }}" was submitted to your community {{ notification.context.get("request").get("receiver").get("metadata").get("title") }} by {{ notification.context.get("request").get("created_by").get("username") }}.

Review the request: {{ notification.context.get("request").get("links").get("self_html") }}
{%- endblock plain_body -%}

{# Markdown for Slack/Mattermost/chat #}
{%- block md_body -%}
The record "{{ notification.context.get("request").get("topic").get("metadata").get("title") }}" was submitted to your community {{ notification.context.get("request").get("receiver").get("metadata").get("title") }} by {{ notification.context.get("request").get("created_by").get("username")}}.

[Review the request]({{ notification.context.get("request").get("links").get("self_html") }})
{%- endblock md_body -%}

```

We are pretty happy with most of the content, but want to override the `html_body` to include a link to the community and all requests.
To do this, we will create a file with the same name, copy the file content from the base file and then adapt the block we want to modify.

```jinja
{# notifications/community-submission.submitted.jinja #}

{%- block subject -%}
New record submission for your community {{ notification.context.get("request").get("receiver").get("metadata").get("title") }} submitted by {{ notification.context.get("request").get("created_by").get("username") }}
{%- endblock subject -%}

{% block html_body %}

<p>The record "{{ notification.context.get("request").get("topic").get("metadata").get("title") }}" was submitted to your community {{ notification.context.get("request").get("receiver").get("metadata").get("title") }} by {{ notification.context.get("request").get("created_by").get("username") }}.</p>

<a href="{{ notification.context.get("request").get("receiver").get("links").get("self_html") }}" class="button">Check out the community"</a>

<a href="{{ notification.context.get("request").get("links").get("self_html") }}" class="button">Review the request</a>

<a href="{{ notification.context.get("request").get("receiver").get("links").get("self_html") + "/requests" }}" class="button">Check out all community requests</a>

{% endblock %}

{%- block plain_body -%}
The record "{{ notification.context.get("request").get("topic").get("metadata").get("title") }}" was submitted to your community {{ notification.context.get("request").get("receiver").get("metadata").get("title") }} by {{ notification.context.get("request").get("created_by").get("username") }}.

Review the request: {{ notification.context.get("request").get("links").get("self_html") }}
{%- endblock plain_body -%}

{# Markdown for Slack/Mattermost/chat #}
{%- block md_body -%}
The record "{{ notification.context.get("request").get("topic").get("metadata").get("title") }}" was submitted to your community {{ notification.context.get("request").get("receiver").get("metadata").get("title") }} by {{ notification.context.get("request").get("created_by").get("username")}}.

[Review the request]({{ notification.context.get("request").get("links").get("self_html") }})
{%- endblock md_body -%}

```

If you want to provide a template for a specific backend, you can do that too! Assume we want to add a specific template for the email backend. We know that the `id` of the email backend is `email`. Following the same steps as above and adding the backend id to the path, we end up with a file to be placed in

```
<my-site>/templates/semantic-ui/invenio_notifications/email/community-submission.submitted.jinja
```

In a backend specific file, you only have to provide blocks needed by this specific backend (but feel free to include other blocks). The email relies on the `subject`, `plain_body` and `html_body` blocks.
In our case, we are happy with the content in the general template and _only_ want to modify the `html_body`block (as in the example before). Now, we can take advantage of the base template by extending it.

```jinja

{% extends "invenio_notifications/community-submission.submitted.html" %}

{% block html_body %}

<p>The record "{{ notification.context.get("request").get("topic").get("metadata").get("title") }}" was submitted to your community {{ notification.context.get("request").get("receiver").get("metadata").get("title") }} by {{ notification.context.get("request").get("created_by").get("username") }}.</p>

<a href="{{ notification.context.get("request").get("receiver").get("links").get("self_html") }}" class="button">Check out the community"</a>

<a href="{{ notification.context.get("request").get("links").get("self_html") }}" class="button">Review the request</a>

<a href="{{ notification.context.get("request").get("receiver").get("links").get("self_html") + "/requests" }}" class="button">Check out all community requests</a>

{% endblock %}
```

Only the specified blocks will be overriden. Other blocks stay as they are in the base template.




## Build your own
This will show you can build your own notification classes.

### Notification Backend
Building your own notification backend can be achieved in a few steps. For instance, you can provide an implementation for your institution's preferred communication tool and send notifications via this backend. For this, simply extend the `NotificationBackend` class and implement the `send` method.

```py
from invenio_notifications.backends import JinjaTemplateLoaderMixin, NotificationBackend,

class InstitutationalBackend(NotificationBackend, JinjaTemplateLoaderMixin):
    """Base class for notification backends."""

    id = "institutional-backend"
    """Unique id of the backend."""

    def send(self, notification, recipient):
        """Send the notification message as markdown to a user."""
        template = self.render_template(notification=notification, recipient=recipient)
        institutation_communication_tool.send_message(user_id=recipient.data["id"], template["md_body"])
```

### Notification Builder
Let us assume that you want to override who will get notified in the event of a community record submission (community curator and owner) and add the previously defined backend (so recipients will get notified via whatever the base class has defined and via the `InstitutationalBackend`).
To do this, we will create a custom builder, which will inherit most of the properties from the existing base class.

```py
from institutational_package.notifications import InstitutationalBackend
from invenio_communities.notifications.generators import CommunityMembersRecipient
from invenio_rdm_records.notifications.builders import CommunityInclusionSubmittedNotificationBuilder

class CustomSubmissionBuilder(CommunityInclusionSubmittedNotificationBuilder):

    # properties not overwritten will keep their base value
    recipients = [
        CommunityMembersRecipient(key="request.receiver", roles=["curator", "owner"]),
    ]

    recipient_backends = CommunityInclusionSubmittedNotificationBuilder.recipient_backends + [
        InstitutationalBackend(),
    ]
```

## Configuration Values

Configuration values used in the `invenio-notifications` module can be overriden, in order to adapt instances to specific needs.


### NOTIFICATION_BACKENDS

This config variable allows to specify the available backends. For a detailed description on backends, checkout the respective [reference section](../../reference/notifications.md#backends).
For instance, you can provide an implementation for your institution's preferred communication tool and send notifications via this backend.

As an example, take the backend shown in [build your own backend](#notification-backend). Then you only have to specify it in the config variable (e.g. in `invenio.cfg`).

```py
NOTIFICATION_BACKENDS = {
    EmailNotificationBackend.id: EmailNotificationBackend,
    InstitutationalBackend.id: InstitutationalBackend,
}
```

### NOTIFICATION_BUILDERS

Specifies [notification builders](#notification-builder) to be used for certain types of notifications. When a notification is handled by the manager, it will lookup the type in this variable and build the notification with the provided builder class.

As an example, take the backend shown in [build your own builder](#notification-builder). Then you only have to specify it in the config variable (e.g. in `invenio.cfg`).

```py
NOTIFICATIONS_BUILDERS = {
    CustomSubmissionBuilder.type: CustomSubmissionBuilder,
}
```

Since the custom builder uses the same `type` as the builder we want to override, we can use either `type` as key for the entry. The following snippet will have the same effect, but it is more clear what will be overriden.

```py
NOTIFICATIONS_BUILDERS = {
    CommunityInclusionSubmittedNotificationBuilder.type: CustomSubmissionBuilder,
}
```


### NOTIFICATIONS_ENTITY_RESOLVERS

Specifies entity resolvers to be used for resolving the notification context. These are usually `ServiceResultResolver` objects, which provide functionality to dump an object to a reference dictionary and later on use the dump to fetch information as seen on the API/service level (i.e. fully resolved objects with links for easy access).

```py
NOTIFICATIONS_ENTITY_RESOLVERS = [
    RDMRecordServiceResultResolver(),
    ServiceResultResolver(service_id="users", type_key="user"),
    ServiceResultResolver(service_id="communities", type_key="community"),
    ServiceResultResolver(service_id="requests", type_key="request"),
    ServiceResultResolver(service_id="request_events", type_key="request_event"),
]
```

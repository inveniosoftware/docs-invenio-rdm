# Notifications

_Introduced in InvenioRDM v12_

The notification system in InvenioRDM is provided via the [`invenio-notifications`]() module.
This module provides customization possibilities for notification backends, notification builders and resolvers.
A notification manager is created, which will rely on these configuration values and provide logic to send notifications. Its task is also to call respective methods to resolve the notification context, generate recipients, filter recipients and generate the backend ids for further processing. With all information created, it will then dispatch further tasks to relay the notification to the backend, which will take care of sending the actual notification.

Notifications are registered at the service level in the unit of work and send off to a celery task - which takes care of further processing.

## Base Entities

Let's first have a look at the base entities provided.

### Models

#### Notification

A notification is a simple dataclass, holding information about its type and the context.

```py
@dataclass
class Notification:

    type: str
    context: dict
```

The context attribute of the notification holds information relevant for further processing and will be expanded throughout the workflow.
When dispatching this notification in the service, the context shall be as minimal as possible, to reduce passing huge chunks of data.

An example creation of a notification object could be:

```py

n = Notification(type="community-submission", context='{"request": request.id}')
```

#### Recipient

A recipient is a simple dataclass, holding information about a recipient.

```py
@dataclass
class Recipient:
    data: dict
```

The data attribute holds information required for contact purposes (i.e. for a user, this means information about the name, email and notification preferences).
An example creation of a recipient object could be:

```py

u = current_user_service.read(...)
r = Recipient(data=u.to_dict())
```

### Builders, Filters, Generators

A few classes are in place, to provide a general interface for processing a notification and generate all necessary information.

#### ContextGenerator

A context generator is supposed to be doing work on as well as extend/expand the notification context.
As an example, this could mean adding a new key/value pair to the context.

It specifies a callable method expecting the notification, which can be modified in place.

_EntityResolve_

This is a discrete implementation of the context generator, using the registered entity resolvers of the `invenio-notifications` module to expand the context. It will take a key to do a dictionary look-up and store the resolved entity at the index of the key.

```py
class EntityResolve(ContextGenerator):
    """Payload generator for a notification using the entity resolvers."""

    def __init__(self, key):
        """Ctor."""
        self.key = key

    def __call__(self, notification):
        """Update required recipient information and add backend id."""
        entity_ref = dict_lookup(notification.context, self.key)
        entity = EntityResolverRegistry.resolve_entity(entity_ref)
        dict_set(notification.context, self.key, entity)
        return notification
```

#### RecipientGenerator

A recipient generator will get the fully expanded notification and the recipients from previously ran recipient generators. The task of this generator is to generate recipients (i.e. users, groups) based on the context and add them to the previous recipients.

The recipients received is a map:

```py
recipients = {
    "3": {
        "name": "Admin the admin",
        "email": "admin@invenio.ch",
        ...
     },
     ...
}
```

Based on the recipients key, this takes care of duplicate entries (i.e. if user with id 3 is added twice, the old value will be overwritten).

_UserRecipientGenerator_

This is a discrete implementation of the recipient generator. Based on the provided key, it will do a lookup in the notification context to get the user data dump. With this information, a new recipient will be created and added to the recipients.

```py
class UserRecipient(RecipientGenerator):
    """User recipient generator for a notification."""

    def __init__(self, key):
        """Ctor."""
        self.key = key

    def __call__(self, notification, recipients):
        """Update required recipient information and add backend id."""
        user = dict_lookup(notification.context, self.key)
        recipients[user["id"]] = Recipient(data=user)
        return recipients
```

#### RecipientFilter

A recipient filter will get the fully expanded notification and all created recipients. The task of the filter is to filter recipients in place, which do not fulfill a certain requirement.c

_UserPreferencesRecipientFilter_

This is a discrete implementation of the recipient filter. It will remove recipients, which do not have notifications enabled via their preferences.

```py
class UserPreferencesRecipientFilter(RecipientFilter):
    """Recipient filter for notifications being enabled at all."""

    def __call__(self, notification, recipients):
        """Filter recipients."""
        for key in list(recipients.keys()):
            r = recipients[key]
            if not (
                r.data.get("preferences", {})
                .get("notifications", {})
                .get("enabled", False)
            ):
                del recipients[key]

        return recipients
```

#### RecipientBackendGenerator

A recipient backend generator will get the fully expanded notification, a single recipient and previously created backend ids. The task of this generator is to return the id of the backend, it wants to send the notification to. Additionally, if the backend depends on information, not yet available in the recipient, it can modify the recipient in place and provide this information.

_UserEmailBackend_

This is a discrete implementatio of the recipient backend generator. When called, it will add the id of the email backend to the backends parameter. Since all information needed for sending mails are already available in the recipient, it does not have to do any additonal work.

```py
class UserEmailBackend(RecipientBackendGenerator):
    """User related email backend generator for a notification."""

    def __call__(self, notification, recipient, backends):
        """Add backend id to backends."""
        backend_id = EmailNotificationBackend.id
        backends.append(backend_id)
        return backend_id
```

#### NotificationBuilder

A notification builder has following class attributes:

- `context`: List of [ContextGenerator](#contextgenerator)
- `recipients`: List of [RecipientBuilder](#recipientgenerator)
- `recipient_filters`: List of [RecipientFilter](#recipientfilter)
- `recipient_backends`: List of [RecipientBackendGenerator](#recipientbackendgenerator)
- `type`: Name of the notification it shall build.

Additionally, class methods take care of creating all needed information for sending a notification. Each method will iterate over their respective attribute and return the cumulative result.

### Backends

A notification backend is responsible for the actual sending of the notification to a recipient. To complete this task, its `send` method will receive all information required from the notification system. A backend shall not perform any queries. It may render templates based on its own needs and with the notification content provided.

Each backend shall have an `id`, to distinguish it from others. Backends are registered in the notification manager.

#### JinjaTemplateLoaderMixin

`JinjaTemplateLoaderMixin` is supposed to make handling jinja templates easier. It already takes care of loading templates and rendering the blocks inside of them. This mixin will also take care of factoring in the locale and the backend id when choosing the template (i.e. a more specific template will take precedence over a general template).

#### EmailNotificationBackend

This is a discrete implemenation of a notification backend. With the help of a [JinjaTemplateLoaderMixin](#jinjatemplateloadermixin), it will render a notification template based on the notification type provided.

```py
class EmailBackend(Backend):

    id = "email"

    def send(self, notification: Notification, recipient: Recipient):
        """Mail sending implementation."""
        content = self.render_template(notification, recipient)
        resp = send_email({
            "subject": content["subject"],
            "html_body": content["html_body"],
            "plain_body": content["plain_body"],
            "recipients": [f"{recipient.name} <{recipient.email}>"],
            "sender": current_app.config["MAIL_DEFAULT_SENDER"],
        })
        return resp
```

## Templates

The Jinja templates provided shall include all parts of the notification that are subject to special formatting by a backend (e.g. subject, HTML/plaintext/markdown body, etc.) in separate Jinja blocks.
Additional backends should provide their own templates, to be as specific as possible.

This is an example notifitication

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

## Configuration Values

Configuration values used in the `invenio-notifications` module can be overriden, in order to adapt instances to specific needs.

### NOTIFICATION_BACKENDS

Specifies available [notification backends](#notification_backends) for sending notifications.

```py
NOTIFICATIONS_BACKENDS = {
    "email": EmailBackend,
    "cern": CERNNotificationsBackend,
    "slack": SlackBackend,
    }
```

### NOTIFICATION_BUILDERS

Specifies [notification builders](#notification_builders) to be used for certain types of notifications. When a notification is handled by the manager, it will lookup the type in this variable and build the notification with the provided builder class.

```py
NOTIFICATIONS_BUILDERS = {
    "community_submission_create": CommunitySubmissionCreate,
    "community_submission_accept": CommunitySubmissionAccept,
    "community_submission_reject": CommunitySubmissionReject,
    "member_invitation_create": CommunityMemberInvitationCreate,
    "member_invitation_accept": CommunityMemberInvitationAccept,
    "member_invitation_reject": CommunityMemberInvitationReject,
    "request_comment_create": RequestCommentCreate,
}
```

### NOTIFICATIONS_ENTITY_RESOLVERS

Specifies entity resolvers (not to be confused with [EntityResolve](#entityresolve)) to be used for resolving the notification context. These are usually `ServiceResultResolver` objects, which provide functionality to dump an object to a reference dictionary and later on use the dump to fetch information as seen on the API/service level (i.e. fully resolved objects with links for easy access).

```py
NOTIFICATIONS_ENTITY_RESOLVERS = [
    RDMRecordServiceResultResolver(),
    ServiceResultResolver(service_id="users", type_key="user"),
    ServiceResultResolver(service_id="communities", type_key="community"),
    ServiceResultResolver(service_id="requests", type_key="request"),
    ServiceResultResolver(service_id="request_events", type_key="request_event"),
]
```

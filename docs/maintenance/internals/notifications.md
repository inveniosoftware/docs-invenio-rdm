# Notifications

_Introduced in v12_

## Models

### Notification

A notification is a simple dataclass, holding information about its type and the context.

#### Attributes

- `type` specifies the notification type and is used for template selection as well as the key for notification builders.
- `context` holds information relevant for further processing and will be expanded throughout the workflow.

#### Methods
- `dumps(self)`: Dumps the object as dict.


### Recipient

Simple dataclass, holding information about a recipient.

#### Attributes

- `data` attribute holds information required for contact purposes (i.e. for a user, this means information about the name, email and notification preferences).
An example creation of a recipient object could be:


#### Methods
- `dumps(self)`: Dumps the object as dict.


## Builders, Filters, Generators

A few classes are in place, to provide a general interface for processing a notification and generate all necessary information.

### ContextGenerator

A context generator is doing work on as well as extend/expand the notification context.


### RecipientGenerator

A recipient generator will get the fully expanded notification and the recipients from previously ran recipient generators. The task of this generator is to generate recipients (i.e. users, groups) based on the context and add them to the previous recipients.


### RecipientFilter

A recipient filter will get the fully expanded notification and all created recipients. The task of the filter is to filter recipients in place, based on specified certain criterias.


### RecipientBackendGenerator

A recipient backend generator will get the fully expanded notification, a single recipient and previously created backend ids. The task of this generator is to return the id of the backend, it wants to send the notification to. Additionally, if the backend depends on information, not yet available in the recipient, it can modify the recipient in place and provide this information.


### NotificationBuilder

Based on specified attributes, it takes care of building the context, recipients, recipient backends and filter recipients.

#### Attributes

- `context`: List of [ContextGenerator](#contextgenerator)
- `recipients`: List of [RecipientBuilder](#recipientgenerator)
- `recipient_filters`: List of [RecipientFilter](#recipientfilter)
- `recipient_backends`: List of [RecipientBackendGenerator](#recipientbackendgenerator)
- `type`: Name of the notification it shall build.

#### Methods

Class methods take care of creating all needed information for sending a notification. Each method will iterate over their respective attribute and return the cumulative result.

- `build(cls, **kwargs)`: Build notification based on type and additional context.
- `resolve_context(cls, notification)`: Resolve all references in the notification context.
- `build_recipients(cls, notification)`: Return a dictionary of unique recipients for the notification.
- `filter_recipients(cls, notification, recipients)`: Apply filters to the recipients.
- `build_recipient_backends(cls, notification, recipient)`: Return the backends for recipient.

## Backends

### Notification Backend
A notification backend is responsible for the actual sending of the notification to a recipient.

#### Attributes

- `id`: Identifier of the backend.

#### Methods

- `send(self, notification, recipient)`: Send the notification message to a recipient and perform any additional tasks required to do so.

### JinjaTemplateLoaderMixin

`JinjaTemplateLoaderMixin` is supposed to make handling jinja templates easier. It already takes care of loading templates and rendering the blocks inside of them. This mixin will also take care of factoring in the locale and the backend id when choosing the template (i.e. a more specific template will take precedence over a general template).

#### Attributes
- `template_folder` specifies the folder for template lookup.

#### Methods
- `render_template(self, notification, recipient)`: Render template for a notification. Fetch the template based on the notification type and return the template blocks. More specific templates take precedence over less specific ones. Rendered template will also take the locale into account.

### EmailNotificationBackend

This is a discrete implemenation of a notification backend. With the help of a [JinjaTemplateLoaderMixin](#jinjatemplateloadermixin), it will render a notification template based on the notification type provided.

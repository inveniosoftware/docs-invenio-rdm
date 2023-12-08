# Event handling

The InvenioRDM backend is not event driven. At the time of writing (v11) there is no
support for event handling, although there is work being done to implement an
_event bus_ ([RFC](https://github.com/inveniosoftware/rfcs/pull/56)).

Nonetheless, there are several addressed use cases that would benefit from an event bus
and will be refactored to use it once it is implemented.

In the following sections these specific use cases will be described with more detail.
However, they all share a similar architecture.

## Emitter

The object in charge of sending/triggering the "event". The lack of an event bus leaves
freedom of implementation on the emitter. For example, they could be emitted from the
views, after unit of work (record) commit, etc. These events are written to case-specific
message queues.

The important factor to have into account is the decoupling of the _happening_ of the
action and creating the _event about it happening_. For example, notifying about record
creation should be done after the record has been committed. This would avoid
inconsistencies such as failing to commit a record because the event failed to be created,
or sending a notification about something that was not committed yet and might fail to do
so. This leads to the question of _what happens if after commit I cannot create the event?_
and other corner cases. Addressing these cases is out of the scope of the current
implementations and will be solved by the event bus.

## Handler

For every event there is one or more operations that need to be executed. In the following
examples the logic is implemented in case-specific tasks that run periodically (celery
beat).

When processing events it is important to _eventually_ arrive to the same state. For example,
if all events where to be reprocessed (e.g. _event sourcing_) several times, the final
state should be the same. In addition, if one or more events were processed more than once
the final state should also be the same, this means that event processing must be
idempotent.

Moreover, processing events can take a long time. If this effects the user experience _eager read derivation_ could be used. However, this comes at a cost of having to handle rollbacks and potential data inconsistency.

## Events

Since there is no defined event API, the current use cases define case-specific payloads
and formats.

## Examples

### Change notifications

The full design details can be found in the [RFC](https://github.com/inveniosoftware/rfcs/blob/master/rfcs/framework-0062-change-notification.md).

InvenioRDM uses polyglot persistence: PostgreSQL and OpenSearch. Due to data retrieval and
search requirements data is denormalized in OpenSearch. This means that when some
entities  are updated (e.g. user profiles) objects containing their denormalized
information also need to be updated too (e.g. membership requests reflecting the user's
username).

To achieve this, the events or _change notifications_ are registered in the unit of work.
On an operation that will trigger an asynchronous Celery task with a custom payload on
`post_commit`. This task will enrich the payload and trigger all the handlers registered
for the record type that was changed. These handlers are service methods with custom
signatures, and are configurable in the `invenio.cfg` file. The records have a revision id
and use optimistic concurrency, therefore idempotence can be guaranteed.

### Statistics

Statistics such as record view or file downloads are calculated using events. These
events are emitted on the resources/views, by registering a message with a custom payload in a specific queue. Event indexers will then read these messages and
carry out the appropriate operations (e.g. aggregations). Event indexers are running as
celery beat tasks. To guarantee idempotence each event contains a unique identifier (e.g.
timestamp + User-agent + IP address + URL), which guarantees that the event is captured/persisted only once.

### Mail notifications

This feature has not been fully implemented yet. But progress can be followed and the full
design details can be found in the [RFC](https://github.com/inveniosoftware/rfcs/pull/66).

### Webhooks

!!! info "Not supported"

    This feature has not been implemented yet

In order to enable interoperability and for other applications to build on top of
InvenioRDM we can deliver webhook notifications to user-configured 3rd-party applications.
These webhooks can be configured/filtered on the level of specific events (and their
properties, e.g. "send a webhook for all records of type `software` added to the community
`astronomy`").

### Audit log

!!! info "Not supported"

    This feature has not been implemented yet

For many operations it's useful to keep an audit log, so that administrators, community
curators/managers, and users, can review past actions. This is both a security and
"inspection" feature. Events can be mapped to actions, and logging them could be
implemented via event handlers.

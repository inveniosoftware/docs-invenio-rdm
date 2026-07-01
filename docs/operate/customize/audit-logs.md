# Audit logs

_Introduced in v13_

**Audience**: Instance staff / Content managers / Site administrators

InvenioRDM can store audit log events of actions performed by the end-users.

Currently, the following audit log actions are supported out of the box:

- Creating/updating/deleting a draft
- Publishing a record
- Creating a new version of a record
- Adding/Removing a file to a draft
- Adding/updating/deleting the access settings of a record/draft
- Adding/updating/deleting a secret link for sharing a record/draft

You will be able to view all actions performed in your instance and query actions performed on resources.

You can learn about its internals [here](../../maintenance/internals/audit-logs.md).

## Enabling audit logs
To enable audit logs, you need to set the following configuration in your `invenio.cfg`:

```python
# Enable the feature flag
AUDIT_LOGS_ENABLED = True
```

## Add your actions
To track more actions on resources in InvenioRDM using audit logs, follow these steps to add new actions:

### 1. Define the action

Create a new class that inherits from `AuditLogAction`.
Define your action by specifying:

- **id**: A unique name that identifies the action.
- **context** (optional): A list of context resolver classes to resolve additional information for the log entry.
- **resource_type** (optional): The type of resource the action affects (like "record" or "draft").
- **metadata_schema** (optional): A custom marshmallow schema describing any additional fields to store in the audit log entry.

These attributes help your log entry capture just the right information for your needs.

```python
from invenio_audit_logs.services import AuditLogAction

class CustomActionAuditLog(AuditLogAction):
    """Audit log for a custom action."""

    id = "custom.action"
    message_template = "User {user_id} performed a custom action on {resource_id}."
    context = [
        CustomContext(),
    ]
    resource_type = "custom_resource"
    metadata_schema = {
        "custom_audit_metadata": fields.Nested(
            CustomAuditMetadataSchema,
            required=True,
        ),
    }
```

### 2. Add context (optional)

If the action requires additional context, extend the context attribute with resolvers.

For example:

```python
class CustomContext(object):
    """Payload generator to update audit log data."""

    def __call__(self, data, **kwargs):
        ...
```

### 3. Register the action

Ensure the new action class is registered in the appropriate entry point.

```cfg
invenio_audit_logs.actions =
    custom.action = your_module.actions:CustomActionAuditLog

```

### 4. Use the action in your module

To log the action in your module, register it with the Unit of Work (UoW) using the `AuditLogOp` operation. This ensures the action is logged as part of the transactional workflow.

```python
from invenio_audit_logs.services import AuditLogOp
from your_module.actions import CustomActionAuditLog

uow.register(AuditLogOp(CustomActionAuditLog.build(identity, resource_id, ...)))
```

By following these steps, you can extend the audit logging system to include custom actions tailored to your instance's needs.

## Opt out of certain actions

If you want to not log certain actions, you can set the following configuration in your `invenio.cfg`:

```python
AUDIT_LOGS_DISABLED_ACTIONS = {"draft.edit"}
```

To find all the available actions, check the entry points in the `invenio_audit_logs.actions` group.
```python
>>> from invenio_base.utils import entry_points
>>> [ep.name for ep in entry_points(group="invenio_audit_logs.actions")]
```

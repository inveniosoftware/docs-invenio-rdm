# Audit logs

_Introduced in InvenioRDM v13_

## Summary

This document serves as a developer guide to the Audit logging feature, detailing its functionality.

## Intended Audience

This guide is designed for developers working with InvenioRDM.

## Overview

The Audit logging feature provides a mechanism to track actions performed within the InvenioRDM framework. It integrates with the existing service layers, ensuring that the relevant operations are logged.

## Storage

Audit logs are stored in the database, leveraging the existing record storage mechanisms provided by Invenio. Each log entry is treated as a record, allowing for efficient querying and management.

Additionally, audit logs are indexed in the econfigured search backend to support advanced search capabilities and fast retrieval. The indexing process is handled automatically through the Unit of Work (UoW) operations, ensuring that database and search indexes remain synchronized.

## Implementation

InvenioRDM implements audit log entries as records, leveraging InvenioRDM's existing record management infrastructure. Consistency between storage backends, such as the database and the search backend, is maintained using the Unit of Work (UoW) pattern. This ensures that all operations on audit logs, including creation and indexing, are handled transactionally.

### Service Layer

The service layer provides the core functionality for managing audit logs, including creating, searching, and retrieving log entries from the DB and Search backend.

### Permissions

Access to audit logs is controlled via the Invenio permissions system.

### Resource layer

Additionally, the audit logs feature includes a resource layer that defines RESTful API endpoints. These endpoints allow users to search and retrieve audit log entries via URL routes, enabling seamless integration with external systems and user interfaces.

## Administration Panel

The administration panel provides an interface for managing audit logs. Administrators can search, filter, and view log entries directly from the panel.

## How to add new actions

To add new actions to the audit logging system, follow these steps:

1. **Define the Action**: Create a new class that inherits from `AuditLogAction` or a base class like `RecordBaseAuditLog`.
Specify the id (action name), message_template, and optionally, the context and resource_type.

```python
from invenio_audit_logs.services import AuditLogAction

class CustomActionAuditLog(AuditLogAction):
    """Audit log for a custom action."""

    id = "custom.action"
    message_template = "User {user_id} performed a custom action on {resource_id}."
    context = [
        CustomContext(),
    ]
    resource_type = "custom_resource
```

2. **Add Context (Optional)**

If the action requires additional context, extend the context attribute with resolvers.

For example:

```python
class CustomContext(object):
    """Payload generator to update audit log data."""

    def __call__(self, data, **kwargs):
        ...
```

3. **Register the action**

Ensure the new action class is registered in the appropriate entry point.

```cfg
invenio_audit_logs.actions =
    custom.action = your_module.actions.py:CustomActionAuditLog

```

4. **Use the action in your module**

To log the action in your module, register it with the Unit of Work (UoW) using the `AuditLogOp` operation. This ensures the action is logged as part of the transactional workflow.

```python
from invenio_audit_logs.services import AuditLogOp
from your_module.actions import CustomActionAuditLog

uow.register(AuditLogOp(CustomActionAuditLog.build(identity, resource_id, ...)))
```

By following these steps, you can extend the audit logging system to include custom actions tailored to your instance's needs.

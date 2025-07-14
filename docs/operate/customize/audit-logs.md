# Audit logs

_Introduced in v13_

**Audience**: Instance staff / Content managers / Site administrators

InvenioRDM can store audit log events of actions performed by the end-users.

In v13, InvenioRDM logs the following actions:

- Creating a draft
- Updating a draft
- Publishing a record
- Deleting a draft
- Creating a new version of a record

You will be able to view all actions performed in your instance and query actions performed on resources.

The feature can be enabled by setting the `AUDIT_LOGS_ENABLED` flag to `True`.

## Administration panel

When the audit logging feature is enabled, you will be able to see when a user created a draft and then published it as a record. Only site-administrators can access the logs via the administration panel (`<domain>/administration/audit-logs`).

You can also check the changes in the new version of the record via the administration panel.

You will be able to view all actions performed in your instance and query actions performed on resources.

![Administration Panel](./imgs/audit-logs.png)

## Add new actions

You can extend the functionalities of audit logs by adding new actions. Follow [this guide](../../maintenance/internals/audit-logs.md#how-to-track-more-actions) to learn how.

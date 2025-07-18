# Audit logs

_Introduced in v13_

## Summary

This document serves as a developer reference to the Audit logging feature, detailing its functionality.

## Overview

The Audit logging feature provides a mechanism to track actions performed within the InvenioRDM framework. It integrates with the existing service layers, ensuring that the relevant operations are logged.

For example, audit logs allow admins to track resource actions like creating/editing/deleting a draft and publishing a record.

## Implementation

InvenioRDM implements Audit logs as records, leveraging the framework's existing record management infrastructure. This approach ensures efficient querying, indexing, and management of log entries.

### Storage

The Unit of Work (UoW) pattern is used to maintain consistency across storage backends, such as the database and the configured search backend (e.g., OpenSearch). This ensures that all operations, including creation, updates, and indexing, are handled transactionally, keeping the database and search index synchronized.

### Service Layer

The service layer provides the core functionality for managing audit logs, including creating, searching, and retrieving log entries from the DB and Search backend.

### Permissions

Access to audit logs is controlled via the Invenio permissions system. Currently only the System User can create audit logs and administrators can read them. The permissions can be updated in the permission policy class to, for example, provide read access to other user roles.

### Resource layer

Additionally, the audit logs feature includes a resource layer that defines RESTful API endpoints. These endpoints allow users to search and retrieve audit log entries via URL routes, enabling seamless integration with external systems and user interfaces.

**Key Endpoints:**

- **Search Logs**: _GET_ `/api/audit-logs?q=abcd-1234`
  Allows users to perform a query over audit log entries.

- **Retrieve Log Entry**: _GET_ `/api/audit-logs/<id>`
  Enables retrieval of a specific audit log entry by its unique identifier.

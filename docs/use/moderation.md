# Moderation of users and records

_Introduced in InvenioRDM v12_

**Audience**: Instance staff / Content managers / Site administrators

The administration panel is a feature in InvenioRDM introduced in v10 that provides a graphical user interface for managing users and records. It is designed to be used by administrators and superusers to moderate the content of the repository.
For more technical details you can read the [developer guide to the InvenioRDM administration panel](../maintenance/internals/administration_panel.md), detailing its programmatic interface and usage.

![The User Management](imgs/user-management.png){ loading=lazy }


The administration panel now includes a "User management" section to deactivate, block, and delete users, as well as undo all those actions. Below is a table summarizing the hierarchy of user moderation states and their effects:

| User state       | Can create records | Can sign in  | Records can be seen  |
|------------------|--------------------|--------------|----------------------|
| In good standing | ✅                 | ✅           | ✅                   |
| Deactivated      | ❌                 | ✅           | ✅                   |
| Blocked          | ❌                 | ❌           | ✅                   |
| Deleted          | ❌                 | ❌           | ❌ (Tombstones)      |

- **Deactivated users**: Temporarily prevented from creating records but can still sign in and appeal their deactivation.
- **Blocked users**: Cannot sign in anymore, but their records remain visible.
- **Deleted users**: Their records are removed from public view and replaced with a tombstone page indicating the user has been deleted.

Records can also be deleted (with a grace period for appeal or undoing) which empowers administrators to enforce institutional policies and fight spam. This leaves a [tombstone page](../reference/metadata.md#tombstone) in place of the record landing page. See the [Concept DOIs section](../operate/customize/dois.md#doi-registration) for a screenshot.

Associated JSON APIs (e.g. `/api/domains`) have been added. Bulk versions of these are in the works.

# File modification

_Introduced in v14_

Admins can now modify the files of all records on their instance by default and, with configuration, you can also allow users to edit their own published records within a certain time period.

## Files modification by users

By default, only admins can modify files. To enable file modification for users, you need to add a relevant policy. Out of the box there is a time-based policy which you can use to allow users to edit their records within a certain period (by default this is 30 days). To enable this, add the following to your config:

```python
from invenio_rdm_records.services.request_policies import (
    FileModificationGracePeriodPolicy,
    FileModificationAdminPolicy,
)
RDM_IMMEDIATE_FILE_MODIFICATION_POLICIES = [
    FileModificationGracePeriodPolicy(),
    FileModificationAdminPolicy(),
]
```

To change the default allowed time, set:

```python
RDM_IMMEDIATE_FILE_MODIFICATION_POLICIES = [
    FileModificationGracePeriodPolicy(grace_period=timedelta(days=7))),
    FileModificationAdminPolicy(),
]
```

You can also block administrators from editing files and only allow users by removing the corresponding policy:

```diff
RDM_IMMEDIATE_FILE_MODIFICATION_POLICIES = [
    FileModificationGracePeriodPolicy(grace_period=timedelta(days=7))),
-   FileModificationAdminPolicy(),
]
```

## Disable

If you would like to disable file modification for all users including admins, add the following to your `invenio.cfg`.

```
RDM_IMMEDIATE_FILE_MODIFICATION_ENABLED = False
```

### Configure policies

Using the default grace periods, here is how file modification works from the submitter's perspective:

1. When a submitter creates a draft, they have an unlimited time to edit the files before publishing.
2. After publication, the submitter has 30 days from publication to edit the files
  * The time to unlock the files is configured via passing a custom timedelta to the policy, e.g. `FileModificationGracePeriodPolicy(timedelta(days=30))`
3. After editing the files, the submitter has 45 days from publication to upload the files and publish the changes
  * The time in which to publish the changes, which should be greater than the grace period, is configured in your config via `RDM_FILE_MODIFICATION_PERIOD = timedelta(days=30 + 15)`

The second time period of 45 days exists to prevent users from repeatedly editing files and leaving them editable indefinitely.

!!! info

  Short time periods are recommended for the file modification period as there is a risk of submitters treating records as file storage, and not respecting that a DOI has been minted for this digital object.

## Configure out of policy messages

Unlike [record deletion](record_deletion.md), users who are outside the file modification policy cannot submit a request to modify files. Such requests must be handled through your instance's regular support channels (for example: email, support ticket, or direct contact). You should either provide guidance on how to request help or clearly state that no exceptions will be made.

Unless disables, administrator can manually unlock the record so the user can make changes, and then publish the updated record on their behalf.

There are two user-facing messages you should customize to reflect your support process.

First, the user facing message when they try to unlock the files outside of policy is a React component that should be [overridden](../customize/look-and-feel/override_components.md) using your `mapping.js`. For example,

```js
import { ModalContent } from "semantic-ui-react";
const ModificationMessage = () => {
  return (
    <ModalContent>
      <p>
        {i18next.t(
          "Please contact us to request file modification, including the" +
            " record URL and a detailed justification in your message."
        )}
      </p>
    </ModalContent>
  );
};

export const overriddenComponents = {
  "InvenioAppRdm.Deposit.ModificationModal.message": ModificationMessage,
};
```

Second, the message which is returned to the user when they have run out of time to publish can be overriden via changing the [translation](../../community/translations/i18n.md). The default message key is:

> "File modification grace period has passed. Please discard this draft to make any changes."

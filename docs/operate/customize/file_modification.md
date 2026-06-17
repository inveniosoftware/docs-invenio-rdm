# File modification

_Introduced in vNext_

Admins can now modify the files of all records on their instance by default and, with configuration, you can also allow users to edit their own published records within a certain time period.

## Disable

If you would like to disable file modification for all users including admins, add the following to your `invenio.cfg`.

```
RDM_IMMEDIATE_FILE_MODIFICATION_ENABLED = False
```

## User file modification

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

To use a custom grace period, pass a custom timedelta like `FileModificationGracePeriodPolicy(grace_period=timedelta(days=7)))` here instead. And if you remove the admin policy then only users will able to edit files of records.

### Configure policies

Using the default grace periods, here is how file modification works from a user perspective:

1. I create a draft, I have an unlimited time to edit the files before publishing
2. After publishing, I have 30 days from publication to edit the files
    * The time to unlock the files is configured via passing a custom timedelta to the policy, e.g. `FileModificationGracePeriodPolicy(timedelta(days=30))`
3. After editing the files, I have 45 days from publication to upload my files and publish my changes 
    * The time in which to publish the changes, which should be greater than the grace period, is configured in your config via `RDM_FILE_MODIFICATION_PERIOD = timedelta(days=30 + 15)`

The second time period of 45 days is to prevent people from editing the files, and leaving the files editable for an unknown date in the future.

!!! info

    Short time periods are recommended for the file modification period as there is a risk of users treating records as file storage, and not respecting that a DOI has been minted for this digital object.

## Configure out of policy messages

Unlike [record deletion](record_deletion.md) in which users outside of policy can "request" deletion, users are **not** similarly allowed to request file modification when they are outside of policy. Instead this request should be made via established channels relevant for your instance (whether by email, in person communication, official support ticket, etc) or you should communicate that no concessions will be made (and if they have an unpublishable draft it should be discarded). If you would like to satisfy the users request, you can unlock the record for them (in the same way they would) and then publish for them once they have made the changes.

There are two messages which should be customized based upon how your instance handles support.

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

Second, the message which is returned to the user when they have run out of time to publish can be overriden via changing the [translation](../../community/translations/i18n.md). The default message is:

> "File modification grace period has passed. Please discard this draft to make any changes."

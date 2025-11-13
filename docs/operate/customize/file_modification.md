# File modification

_Introduced in vNext_

Admins can now modify the files of all records on their instance by default and, with configuration, you can also allow users to edit their own published records within a certain time period.

## Disable

If you would like to disable file modification for all users including admins, add the following to your `invenio.cfg`.

```
RDM_IMMEDIATE_FILE_MODIFICATION_ENABLED = False
```

## User file modification

To enable user file modification, there is a default time-based policy which allows users to edit their records within a certain period. To enable this, add the following to your config:

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

### Configure policies

The time periods of the grace period policy are configured in two places, both in your config.

First, the time to unlock the files is configured via passing a custom timedelta to the policy, e.g. `FileModificationGracePeriodPolicy(timedelta(days=30))`

Second, the time in which to publish the changes, which should be greater than the grace period, is configured in your config via `RDM_FILE_MODIFICATION_PERIOD = timedelta(days=30 + 15)`

!!! info

    Short time periods are recommended for the file modification period as there is a risk of users treating records as file storage, and not respecting that a DOI has been minted for this digital object.

## Configure out of policy messages

Unlike record deletion in which users outside of policy can "request" deletion, users are **not** similarly allowed to request file modification when they are outside of policy. Instead this request should be made via established channels relevant for your instance (whether by email, in person communication, official support ticket, etc) or you should communicate that no concessions will be made (and if they have an unpublishable draft it should be discarded). If you would like to satisfy the users request, you can unlock the bucket for them (in the same way they would) and then publish for them once they have made the changes.

There are two messages which should be customised based upon how your instance handles support.

First, the user facing message when they try to unlock the files outside of policy is a React compontent that should be [overridden](../customize/look-and-feel/override_components.md) using your `mapping.js`. For example,

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

Second, the message which is returned to the user when they have run out of time to publish is defined via your config:

```
RDM_FILE_MODIFICATION_VALIDATION_ERROR_MESSAGE = _(
    "File modification grace period has passed. Please discard this draft to make any changes."
)
```

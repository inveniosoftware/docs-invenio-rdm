# Compliance information when publishing

_Introduced in v13_

InvenioRDM lets you customize the confirmation information shown to users when publishing records, such as terms of service, data policy, or other compliance requirements. This flexibility supports custom publishing workflows and helps ensure users acknowledge your organization's policies.

## Configure checkboxes
InvenioRDM requires users to confirm compliance both when submitting a record for review and when publishing directly. Each interface can be configured independently, allowing you to tailor the compliance workflow to your organization's needs.

In your `mapping.js`, parametrize your UI components by adding a new `extraCheckboxes` parameter in the following format:

```javascript
import React from "react";
import { i18next } from "@translations/invenio_app_rdm/i18next";
import { PublishModal } from "@js/invenio_rdm_records";
import { parametrize } from "react-overridable";

const parameters = {
  extraCheckboxes: [
    {
      fieldPath: "acceptTermsOfService",  // give it a unique name
      text: i18next.t(
        "I confirm that this record complies with the data policy and terms of service."
      ),  // define the text to show
    },
  ],
};

const PublishModalComponent = parametrize(PublishModal, parameters);

export const overriddenComponents = {
  // applied only to the confirmation box when publishing directly
  "InvenioRdmRecords.PublishModal.container": PublishModalComponent,
};
```

![Publish modal with checkbox](imgs/compliance_checkboxes.png)

### Configure extra messages
You can also show information messages before and after the compliance checkboxes section. In your `mapping.js`, define:

```javascript
import React from "react";
import { SubmitReviewModal } from "@js/invenio_rdm_records";
import { parametrize } from "react-overridable";

const LegalDisclaimer = () => (
  <>
    <p>
      By publishing, you agree to our <a href="/terms">terms of service</a>.
    </p>
    <p>This action is irreversible.</p>
  </>
);

const parameters = {
  beforeContent: () => <><p>Please review before continuing:</p><p>{/*Kept empty for spacing */}</p></>,
  afterContent: () => <LegalDisclaimer />,
};

const SubmitReviewModalComponent = parametrize(SubmitReviewModal, parameters);

export const overriddenComponents = {
  // applied only to the confirmation box when submitting for review
  "InvenioRdmRecords.SubmitReviewModal.container": SubmitReviewModalComponent,
};
```

![Submit Review modal with extra content](imgs/compliance_content.png)

Don't forget to re-build the assets for the changes to take effect.

```sh
invenio-cli assets build
```

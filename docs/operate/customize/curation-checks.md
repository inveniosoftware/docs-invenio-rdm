# Curation checks

_Introduced in v13_

> For the mental model of how checks are structured conceptually, refer to the [Maintain and Develop](../../maintenance/architecture/curation.md) documentation.

## Enabling checks

To enable checks, you need to set the following configuration in your `invenio.cfg` file:

```python
# Hook into community request actions
from invenio_rdm_records.checks import requests as checks_requests
RDM_COMMUNITY_SUBMISSION_REQUEST_CLS = checks_requests.CommunitySubmission
RDM_COMMUNITY_INCLUSION_REQUEST_CLS = checks_requests.CommunityInclusion

# Enable the feature flag
CHECKS_ENABLED = True
```

## Configuring checks

!!! warning "Community settings for checks"
    The UI for managing checks is not yet available in InvenioRDM
    v13. Checks are currently managed programmatically via the Python shell.

Checks are added to a community like so:

```python
from invenio_checks.models import CheckConfig, Severity

check_config = CheckConfig(
    community_id=<community-uuid>,
    check_id="metadata",
    params={ ... },
    severity=Severity.INFO,
    enabled=True,
)
db.session.add(check_config)
db.session.commit()
```

To run the checks, submit a draft or record to a community and open the corresponding request.

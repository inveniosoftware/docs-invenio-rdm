# Requests

Configure the requests system in InvenioRDM, including the reviewers feature for enhanced review workflows.

## Requests reviewers

_Introduced in v13.1_

The reviewers feature enables assignment of external experts, collaborators, or community members to provide feedback on requests without granting them the possibility of accepting or declining a request.

### Enable

```python
# Enable the reviewers feature (default: True)
REQUESTS_REVIEWERS_ENABLED = True
```

### Configure limits

Control the maximum number of reviewers that can be assigned to a single request. This helps preventing overwhelming requests with too many reviewers.

```python
# Maximum number of reviewers per request (default: 10)
REQUESTS_REVIEWERS_MAX_NUMBER = 5
```

### Group reviewers

Enable the assignment of user groups as reviewers, allowing entire teams or committees to be assigned to review requests collectively.


```python
# Enable groups, and their assignment as reviewers
USERS_RESOURCES_GROUPS_ENABLED = True
```
then you will be able to use them as request reviewers. All members of the assigned group receive access to view and comment on the request. Group members may receive notifications based on the user's notification settings.

By default, reviewers can be added or removed by Owners, Managers and Curators. Readers cannot assign reviewers but can be assigned as reviewers.

## Require reviews for each record version

By default, only the first version of a record submitted to a community is subject to a review request (depending on the community's settings).
You can change this to also require reviews for new record versions.

In your `invenio.cfg`, set:

```python
from invenio_rdm_records.services.review.policy import AllRecordVersionsReviewPolicy

RDM_NEW_RECORD_VERSION_REVIEW_POLICY = AllRecordVersionsReviewPolicy
```

### Advanced customizations

You can implement custom logic to determine when a review is necessary for each record version. For example, you can require reviews only for specific communities.
To do so, implement your custom policy class:

```python
from flask import current_app

class CustomVersionReviewPolicy:
    """Policy override."""

    @classmethod
    def requires_review(cls, identity, draft) -> bool:
        """Returns whether the new record version requires review."""
        default_community = draft.parent.communities.default
        if default_community is None:
            return False

        # Define which communities require review for all record versions
        communities_requiring = current_app.config.get(
            "COMMUNITIES_REQUIRING_REVIEW_FOR_ALL_VERSIONS", []
        )
        return (
            str(default_community.id) in communities_requiring
        )
```

Then, add the following to your `invenio.cfg`:

```python
RDM_NEW_RECORD_VERSION_REVIEW_POLICY = CustomVersionReviewPolicy

COMMUNITIES_REQUIRING_REVIEW_FOR_ALL_VERSIONS = ["10e21709-1795-4858-a068-f41135c5ab9b"]  # community id
```

## Related configuration

See also:

- [Communities](../../use/communities.md#requests) - User guide for requests and reviewers
- [Architecture documentation](../../maintenance/architecture/requests.md) - Technical overview of the requests system

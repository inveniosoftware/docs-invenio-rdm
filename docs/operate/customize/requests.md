# Requests

_Introduced in v14_

Configure the requests system in InvenioRDM, including the reviewers feature for enhanced review workflows.

## Reviewers configuration

The reviewers feature enables assignment of external experts, collaborators, or community members to provide feedback on requests without granting them the possibility of accepting or declining a request.

### Enable/Disable reviewers

```python
# Enable the reviewers feature (default: True)
REQUESTS_REVIEWERS_ENABLED = True
```

### Reviewer limits

Control the maximum number of reviewers that can be assigned to a single request. This helps manage workflow complexity and ensures review processes remain manageable.

```python
# Maximum number of reviewers per request (default: 10)
REQUESTS_REVIEWERS_MAX_NUMBER = 5
```

- **Purpose**: Prevents overwhelming requests with too many reviewers
- **Considerations**: Balance between comprehensive review and manageable workflow

### Group reviewers

Enable the assignment of user groups as reviewers, allowing entire teams or committees to be assigned to review requests collectively. If you allow
groups to be defined in your instance, i.e.

```python
# Enable assignment of groups as reviewers (requires invenio-users-resources)
USERS_RESOURCES_GROUPS_ENABLED = True
```
then you will be able to use them as request reviewers.

- **Use cases**: 
    - Institutional Review Boards
    - Editorial committees
    - Subject matter expert panels
    - Department review teams
- **Behavior**: All members of the assigned group receive access to view and comment on the request
- **Notifications**: Group members may receive notifications based on your notification configuration

## Usage

When enabled, community curators, managers and owners can:

- Assign individual users or groups as reviewers to any request
- Share requests with external experts outside the community
- Grant access to community members who normally wouldn't see requests (e.g., readers)
- Allow multiple reviewers to provide independent feedback
- Track all reviewer interactions in the request timeline

Reviewers can view the request, participate in conversations, and provide recommendations, but cannot accept or decline the request.

## Permissions

By default, reviewers can be added or removed by community members with roles:

- **Owners** and **Managers** can assign/remove reviewers
- **Curators** can assign/remove reviewers

Community members with the role **Reader** cannot assign reviewers but can be assigned as reviewers.

## Require reviews for each record version

By default, only the first version of a record submitted to a community is subject to a review request (depending on the community's settings).
This can be changed to also require reviews for new record versions.

To do so, you need to override the [`NewRecordVersionPolicy`](https://github.com/inveniosoftware/invenio-rdm-records/blob/master/invenio_rdm_records/services/review/policy.py#L7) class in your instance.
This class contains one method that is called when the user clicks the "New version" button, and is passed the new version draft as well as the identity of the user.
This method can contain any custom logic that returns a boolean value, indicating whether the new version draft should be subject to a review.

New version reviews can only be created for the **default community of the record**.

For example, you can use a config variable to specify communities that require a review for all record versions:

```python
# record_version_policy.py

from flask import current_app
from invenio_rdm_records.services.review import NewRecordVersionReviewPolicy

class CustomVersionReviewPolicy(NewRecordVersionReviewPolicy):
    """Policy override."""

    @classmethod
    def requires_review(cls, identity, draft) -> bool:
        """Returns whether the new record version requires review."""
        default_community = draft.parent.communities.default
        if default_community is None:
            return False

        communities_requiring = current_app.config.get(
            "COMMUNITIES_REQUIRING_REVIEW_FOR_ALL_VERSIONS", []
        )
        return (
            str(default_community.id) in communities_requiring
        )
```

Then, add the overridden policy to your instance's configuration:

```python
# invenio.cfg

from record_version_policy import CustomVersionReviewPolicy

RDM_NEW_RECORD_VERSION_REVIEW_POLICY = CustomVersionReviewPolicy
COMMUNITIES_REQUIRING_REVIEW_FOR_ALL_VERSIONS = ["10e21709-1795-4858-a068-f41135c5ab9b"]
```

## Related configuration

See also:

- [Communities](../../use/communities.md#requests) - User guide for requests and reviewers
- [Architecture documentation](../../maintenance/architecture/requests.md) - Technical overview of the requests system

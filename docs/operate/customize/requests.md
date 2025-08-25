# Requests

_Introduced in InvenioRDM v14_

Configure the requests system in InvenioRDM, including the reviewers feature for enhanced review workflows.

## Reviewers Configuration

The reviewers feature enables assignment of external experts, collaborators, or community members to provide feedback on requests without granting them decision-making authority.

### Enable/Disable Reviewers

```python
# Enable the reviewers feature (default: True)
REQUESTS_REVIEWERS_ENABLED = True
```

### Reviewer Limits

Control the maximum number of reviewers that can be assigned to a single request. This helps manage workflow complexity and ensures review processes remain manageable.

```python
# Maximum number of reviewers per request (default: 10)
REQUESTS_REVIEWERS_MAX_NUMBER = 5
```

- **Purpose**: Prevents overwhelming requests with too many reviewers
- **Considerations**: Balance between comprehensive review and manageable workflow

### Group Reviewers

Enable the assignment of user groups as reviewers, allowing entire teams or committees to be assigned to review requests collectively.

```python
# Enable assignment of groups as reviewers (requires invenio-users-resources)
USERS_RESOURCES_GROUPS_ENABLED = True
```

- **Requirements**: Requires the `invenio-users-resources` module to be installed and configured
- **Use cases**: 
  - Institutional Review Boards (IRBs)
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

Reviewer assignment requires appropriate community permissions:
- **Owners** and **managers** can assign/remove reviewers
- **Curators** can assign/remove reviewers (if configured)
- **Reviewers** can view and comment on assigned requests
- **Readers** cannot assign reviewers but can be assigned as reviewers

## Related Configuration

See also:
- [Communities](../../use/communities.md#requests) - User guide for requests and reviewers
- [Architecture documentation](../../maintenance/architecture/requests.md) - Technical overview of the requests system
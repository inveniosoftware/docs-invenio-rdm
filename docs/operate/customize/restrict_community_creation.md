# Restrict who can create communities

You can control who can create communities by defining custom permissions. You can find below an example approach using custom roles to restrict community creation to a specific role, named `community-curator`.

To implement this, follow these steps:

1- Create permission generators:

```python
from flask import current_app
from flask_principal import RoleNeed
from invenio_administration.generators import Administration
from invenio_communities.permissions import CommunityPermissionPolicy
from invenio_records_permissions.generators import Generator, SystemProcess

class CommunityCreator(Generator):
    """Grant permissions to custom community-creator role"""
    def needs(self, record=None, **kwargs):
        return [RoleNeed("community-creator")]


class CustomCommunitiesPermissionPolicy(CommunityPermissionPolicy):
    """
    Custom permission policy for communities.

    This class overrides the default `CommunityPermissionPolicy` to provide
    a tailored permission model for community-related actions.

    This policy demonstrates how to grant specific permissions for community creation actions:

    - Community creation (`can_create`) is allowed for:
        - Users with the custom 'community-creator' role
        - Users with administration role
        - System processes

    - Direct inclusion of records (`can_include_directly`) is allowed for:
        - Users with administration role
        - System processes
    """
    can_create = [CommunityCreator(), Administration(), SystemProcess()]
    can_include_directly = [Administration(), SystemProcess()]
```

2- Configure in `invenio.cfg`:

```python
from yourmodule.permissions import CustomCommunitiesPermissionPolicy
# Apply custom permissions
COMMUNITIES_PERMISSION_POLICY = CustomCommunitiesPermissionPolicy
```

3- Create and assign roles via CLI:

```bash
# Create role (name must match `community-creator`)
# You only need to create this role once for your instance
invenio roles create community-curator
```

4- To assign the role to a user, run:

```bash
invenio roles add <useremail> community-curator
```

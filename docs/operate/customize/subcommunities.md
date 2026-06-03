_Introduced in v13_

Subcommunities let you link one community as a child of another, so that a parent community can group related communities under it. A university could keep a community per department, all linked under a single university community. A research institute could do the same for its laboratories and research groups.

## Overview

A subcommunity relationship connects a parent community to a child community. The relationship goes one way and can only be one level deep. A community is either a parent or a child, never both. A parent cannot also be someone else's child, and a child cannot have children of its own.

A community with two child communities would look something like this:

- University of Example (parent)
    - Department of Physics (child)
    - Department of History (child)

The link is established through a request, and there are two kinds depending on who starts it. With a _subcommunity request_, the owner of a community asks to have it added under a parent. With a _subcommunity invitation_, the owner of a parent invites another community to join as a child, and the invitation expires after 45 days if the invited community does not respond.

Only the subcommunity request has a user interface today (see [Communities](../../use/communities.md#subcommunities)). The invitation flow exists as a request type and service method, but has no end-user interface yet, so it has to be driven programmatically.

Linking is opt-in on the parent's side. A community accepts children only after an administrator enables it, and any request or invitation targeting a parent that has not enabled children is rejected.

## Enabling a community to accept subcommunities

A community accepts children only when its `children.allow` field is set to `True`. This field defaults to `False`, there is no setting in the community's interface to change it, and community owners cannot change it themselves. Only the system process can, so you set it from the instance shell (or a script running with the system identity).

```python
from invenio_access.permissions import system_identity
from invenio_communities.proxies import current_communities

service = current_communities.service

# Resolve the parent community by its slug
parent = service.read(system_identity, "my-parent-community")

# Enable it to accept children
service.update(
    system_identity,
    "my-parent-community",
    data={**parent.data, "children": {"allow": True}},
)
```

The community is reindexed as part of the update, so no extra step is needed. Once enabled, the parent shows a "Browse" page listing its subcommunities, and members of other communities can request to join it.

## How children get linked to a parent

Both request types have the same outcome. When the request is accepted, the child community's `parent` is set to the parent community. In a default InvenioRDM instance that is the only effect of accepting. It does not retroactively move or re-index the child's existing records, merge memberships, or change either community's settings. The two communities keep their own members and records.

Records still end up browsable under the parent, but through a separate mechanism. When a record is added to a community that has a parent, the parent community is also added to that record. So once a child community is linked to its parent, records included into the child from then on are associated with the parent too and show up in the parent's record listing. Records that were already in the child community before the link are not propagated automatically.

### Child requests to join a parent

The owner of the child community sends a subcommunity request to the parent. The parent's owners or managers then accept or decline it from their community's "Requests" tab. On acceptance, the child's parent is set.

Programmatically, the request is created through the subcommunities service:

```python
from invenio_communities.proxies import current_communities

subcommunities_service = current_communities.subcommunity_service

# `identity` must own (or be allowed to act for) the child community
request = subcommunities_service.join(
    identity,
    "my-parent-community",  # the parent's slug or id
    data={"community_id": "<child_community_id>"},
)
```

You can also create the child community inline by passing a `community` object with a `slug` and `title` instead of `community_id`.

If the same identity owns both the parent and the child community, the request is accepted automatically with no separate approval step.

### Parent invites a child

The owner of the parent community creates a subcommunity invitation targeting the community it wants to add. The invited community's owners or managers accept or decline it. On acceptance, the invited community's parent is set, the same as for a subcommunity request. An invitation that is not answered within 45 days expires.

This flow has no user interface, so it is created through the service:

```python
from invenio_communities.proxies import current_communities

subcommunities_service = current_communities.subcommunity_service

subcommunities_service.create_subcommunity_invitation_request(
    identity,
    parent_community_id="<parent_community_id>",
    child_community_id="<child_community_id>",
    data={},
)
```

## Customizing what acceptance does

The request types, their actions, and the request schema are all configurable, so an instance can change what happens when a subcommunity link is accepted. The relevant settings are:

```python
# Request type used when a community asks to join a parent
COMMUNITIES_SUB_REQUEST_CLS = "..."

# Request type used when a parent invites a child
COMMUNITIES_SUB_INVITATION_REQUEST_CLS = "..."

# Marshmallow schema used to validate the join request payload
COMMUNITIES_SUB_SERVICE_SCHEMA = "..."
```

A common customization is to also add the child community's existing records to the parent on acceptance, so that records published before the link also show up under the parent. You do this by subclassing the accept action and adding the extra behavior. For example, a parent community that wants its children's records to also appear in its own listing:

```python
from invenio_access.permissions import system_identity
from invenio_communities.subcommunities.services.request import (
    AcceptSubcommunity,
    SubCommunityRequest,
)
from invenio_rdm_records.proxies import (
    current_community_records_service,
    current_rdm_records,
)


class AddRecordsAcceptAction(AcceptSubcommunity):
    """Accept a subcommunity and copy its records into the parent."""

    def execute(self, identity, uow):
        child_id = self.request.topic.resolve().id
        parent_id = self.request.receiver.resolve().id
        super().execute(identity, uow)

        # Add the child community's records to the parent community
        records = current_community_records_service.search(
            system_identity, community_id=child_id, scan=True
        )
        current_rdm_records.record_communities_service.bulk_add(
            system_identity, parent_id, (r["id"] for r in records), uow=uow
        )


class MyParentRequest(SubCommunityRequest):
    """Subcommunity request that copies records on acceptance."""

    available_actions = {
        **SubCommunityRequest.available_actions,
        "accept": AddRecordsAcceptAction,
    }
```

```python
# invenio.cfg
COMMUNITIES_SUB_REQUEST_CLS = "my_site.subcommunities:MyParentRequest"
```

Keep these side effects in mind when you unlink a subcommunity, since they are not undone automatically.

## Unlinking a subcommunity

To detach a child from its parent, set the child's `parent` to `None`. There is no helper for this, and the action requires the `manage_parent` permission, which by default is granted only to administrators and the system process. So this is done from the shell:

```python
from invenio_access.permissions import system_identity
from invenio_communities.proxies import current_communities

service = current_communities.service

child = service.read(system_identity, "my-child-community")
service.update(
    system_identity,
    "my-child-community",
    data={**child.data, "parent": None},
)
```

Unlinking only clears the parent link. It does not undo anything else. Records that gained the parent community while the link was in place keep it, whether they got there automatically (included into the child while linked) or through a customized accept action that copied existing records over. Those inclusions stay after unlinking and have to be removed separately if you do not want them.

## Browsing subcommunities

A parent community's subcommunities are listed on its "Browse" page, at `/communities/<community_slug>/browse/subcommunities`. This is the same Browse page that lists a community's [collections](collections.md), and it is shown using the `COMMUNITIES_SHOW_BROWSE_MENU_ENTRY` setting documented in the [Collections](collections.md#display-settings) page.

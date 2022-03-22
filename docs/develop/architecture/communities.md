# Communities

**Intended audience**

This guide is intended for maintainers and developers of InvenioRDM itself.

**Scope**

The guide provides a high-level architectural overview of the communities
module for InvenioRDM.

## Community roles

An InvenioRDM defines a set of community roles that applies globally to all
communities to ensure a consistent user experience across all communities in an
InvenioRDM instance.

A community roles translates into a set of permissions. The roles are
configurable to ensure that they can be tailored to the needs of an instance,
as well as allow for customizations - e.g. one instance might want to use
"curator" and another instance wants to use "editor" as a role because it makes
sense in their setting.

The default instance defines the following community roles:

- Owner: Can do all actions
- Managers: Can manage community members (except owners)
- Curators: Can accept/decline submission requests and edit records.
- Readers: Can view restricted records in the community.

Technically a community must have an owner role (can be named differently).

## Member types

A community has two member types:

- Users
- Groups

Groups are by default added to a community, whereas users are invited to a
community (i.e. requires the user to confirm their membership). It's done like
this because groups may not have a person to address the invitation request to.
Users are not added directly for privacy reason.

## Memberships and invitations

A user or group can be a member of a community. Each membership is associated
with a community role and a visibility

- Community
- Member
- Role
- Visibility

The "visibility" property defines a value public or hidden, to determine if a
community membership is visible to everyone or only to other members of the
community. We allow only members themselves (and the system identity) to set
their visibility to public (again for privacy reason). Owners and managers can
however set hidden visibility of all members.

Invitations to join a community is stored in the same table using two extra
properties:

- Active
- Request

The property "active" is meant to only be used solely for invitations. For
instance, it's not meant to temporarily inactive an existing membership (the
membership should simply be deleted instead).

The property "request" links to the associated request sent to the user being
invited.

A result of this data model is that a user can only be invited once to a
community.

### Business rules

The memberships business rules can be somewhat complex. They are essentially
divided into permissions and pre-conditions.

**A community must always have an owner**

A community must always have an owner so that someone can manage the community.
A community should be removed if an sole owner wants to leave it.

**No self role change**

You cannot change your own role. THis prevents owners and managers from loosing
their access, as they'll have to ask another manager/owner to perform the
change.

**Visibility can be changed by members themselves**

For privacy reasons only members themselves can set their visibility to public.

**Visibility cannot be changed to public by managers/owners**

To allow owners/managers to manage how the community looks, they can decide
to hide certain members from a community.

**Users can leave a community**

All users are allowed to leave a community if they so desire. If a user
is a member of group that's associated with a community, then however they
have to be removed from that group (possibly in an external system) to be fully
removed from a community.

**System identity can do everything**

We allow the system identity to perform all actions independent of other
permissions, to ensure that we can support data migration uses cases where you
want to load data from another system where e.g. users may have already given
their consent.

### Members Command and Query Responsibility Segregation (CQRS)

All state changing commands such as add, invite, update and delete
performs only the required changed, but does not return any results.

Instead to retrieve the list of members the caller must perform a query to one
of the search endpoints.

The reason for this design is because we denormalize data required for the
views (such as the user's name/affiliation etc) into the search index that is
not available if we immediately returned a result. Also, it ensures that all
querying happens on the search index.

Note that all state changes are done directly in the database in order to
ensure relevant integrity checks are with the transaction boundary.

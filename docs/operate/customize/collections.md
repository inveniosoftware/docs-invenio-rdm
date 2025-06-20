_Introduced in v13_

Collections provide a powerful way to curate and organize records within your InvenioRDM instance. They define sets of records based on search filters and can be organized hierarchically to create meaningful groupings of content.

## Overview

Collections are dynamic, query-based groupings of records that automatically include all records matching a specified search filter. They enable you to:

- **Organize records thematically** - Group records by subject, resource type, funding program, or any metadata field
- **Create hierarchical structures** - Build nested collections to guide users in browsing records
- **Display curated content** - Present collections on dedicated pages within communities or globally

Each collection is stored in the database with a search query string that dynamically fetches matching records. This approach ensures collections stay current as new records are added to your repository.

!!! info "Architecture Details"
    For technical implementation details, see [RFC0079](https://github.com/inveniosoftware/rfcs/blob/master/rfcs/rdm-0079-collections.md).

## Configuration

To enable displaying the communities "Browse" tab in your InvenioRDM instance, add to your `invenio.cfg`:

```python
COMMUNITIES_SHOW_BROWSE_MENU_ENTRY = True
```

## Managing Collections

Collections are organized within **Collection Trees** - hierarchical structures that allow you to create logical groupings and nested relationships. Collection trees serve as the root containers for your collections and can be:

- **Community-specific** - Scoped to records of a particular community
- **Global** - Scoped across records of your entire instance

!!! info "Global collections"
    Global collections display is not yet implemented in InvenioRDM v13.

Before creating collections, you need:

1. **Access to Python shell** - Collections are currently managed via `invenio shell`
2. **A community with sub-communities enabled** - Collections can be scoped to communities, so you need at least one community. That community must have `children.allow: true` set, which allows it to have sub-communities (and thus display the "Browse" tab).

!!! bug "Requirement on enabled sub-communities"
    Having a community with `children.allow: true` is a limitation of the current "Browse" tab implementation in InvenioRDM v13. This will be patched to allow communities that might only have collections (and not sub-communities enabled) to still display the "Browse" tab.

!!! warning "Administration UI for Collections"
    The administration UI for managing collections is not yet available in InvenioRDM v13. Collections are currently managed programmatically via the Python shell.

### Create a Collection Tree

First, create a collection tree to serve as the root container:

```python
from invenio_collections.api import CollectionTree

COMMUNITY_ID = "<community_id>"  # Replace with your community's UUID

# Create a collection tree for a subjects-based hiearchy
ctree = CollectionTree.create(
    title="Subjects",
    slug="subjects",  # Used in URLs
    community_id=COMMUNITY_ID,  # `None` for global trees
    order=10  # Controls display order (lower numbers appear first)
)
```

### Create top-level Collections

Create your first collections within the tree:

```python
from invenio_collections.proxies import current_collections
from invenio_access.permissions import system_identity

collections_service = current_collections.service

# Create a collection for records classified under the "Natural sciences" subject
natural_sciences_col = collections_service.create(
    system_identity,
    COMMUNITY_ID,
    tree_slug="subjects",
    slug="natural-sciences",  # URL slug for the collection
    title="Natural Sciences",  # Displayed title
    query='metadata.subjects.subject:"Natural Sciences"',  # Search filter
    order=10  # Display order within the tree (lower numbers appear first)
)
social_sciences_col = collections_service.create(
    system_identity,
    COMMUNITY_ID,
    tree_slug="subjects",
    slug="social-sciences",
    title="Social Sciences",
    query='metadata.subjects.subject:"Social Sciences"',
    order=20
)
```

### Create nested Collections

Add two sub-collections to the "Natural Sciences" top-level collection:

```python
math_col = collections_service.add(
    system_identity,
    collection=natural_sciences_col._collection,
    slug="mathematics",
    title="Mathematics",
    query='metadata.subjects.subject:"Mathematics"',
    order=10
)
compsci_col = collections_service.add(
    system_identity,
    collection=natural_sciences_col._collection,
    slug="computer-science",
    title="Computer and Information Sciences",
    query='metadata.subjects.subject:"Computer and Information Sciences"',
    order=20
)
```

You now have a collection tree with the following structure:

- Subjects (tree)
    - Natural Sciences (query: `metadata.subjects.subject:"Natural Sciences"`)
        - Mathematics (query: `metadata.subjects.subject:"Mathematics"`)
        - Computer and Information Sciences (query: `metadata.subjects.subject:"Computer and Information Sciences"`)
    - Social Sciences (query: `metadata.subjects.subject:"Social Sciences"`)

### Collections query inheritance

Nested collections automatically inherit their parent's search criteria, combining queries with the `AND` boolean operator. Child collections show only records that match both their own query and all parent queries.

!!! example "Example Subjects Hierarhy"

    Given the following collection hierarchy:

    - Research Fields
        - Natural Sciences (query: `metadata.subjects.subject:"Natural sciences"`)
            - Mathematics (query: `metadata.subjects.subject:"Mathematics"`)
            - Physical Sciences (query: `metadata.subjects.subject:"Physical sciences"`)
        - Social Sciences (query: `metadata.subjects.subject:"Social sciences"`)
            - Psychology (query: `metadata.subjects.subject:"Psychology"`)

    The effective queries for each collection would be:

    - **Natural Sciences**: `metadata.subjects.subject:"Natural sciences"`
    - **Mathematics**: `metadata.subjects.subject:"Natural sciences" AND metadata.subjects.subject:"Mathematics"`
    - **Physical Sciences**: `metadata.subjects.subject:"Natural sciences" AND metadata.subjects.subject:"Physical sciences"`
    - **Psychology**: `metadata.subjects.subject:"Social sciences" AND metadata.subjects.subject:"Psychology"`

## Accessing Collections

!!! note "TODO: Move to Use > Communities section of docs"
    This section is aimed mostly at end-users, but we don't have currently the
    "Communities" section in the docs.

Once created, individual collections are accessible through dedicated pages that display all records matching the collection's search criteria. Communities have a "Browse" page that provides an overview of all available collections.

### Community "Browse" page

Communities with configured collections, feature a browse page that provides an overview of all available collection trees and their contained collections hierarchy, along with the total number of records contained within each collection level. This serves as the main entry point for users to discover and navigate collections within a community.

![Community browse page showing multiple collection tree hierarchies](imgs/collection-browse.png)
/// caption
The collection "Browse" page gives users an overview of all available collections organized by collection trees.
///

The community "Browse" page is accessible at `/communities/<community_slug>/browse`.

The record totals for each collection level are updated automatically every 1 hour by the `invenio_collections.tasks.update_collections_size` Celery tasks.

### Collection pages

Each Collection has a dedicated page showing its hierarchy and a standard record search page, pre-filtered based on the collection search criteria.

![Collection page showing "Mathematics" records with search filters and results](imgs/collection-page.png)
/// caption
A collection page displays all records matching the search criteria, with breadcrumb navigation showing the collection hierarchy.
///

Collection pages are accessible at `/communities/<community_slug>/collections/<collection_tree>/<collection_slug>`.

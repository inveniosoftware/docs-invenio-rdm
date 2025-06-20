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

## Managing Collections

Collections are organized within **Collection Trees** - hierarchical structures that allow you to create logical groupings and nested relationships. Collection trees serve as the root containers for your collections and can be:

- **Community-specific** - Scoped to records of a particular community
- **Global** - Scoped across records of your entire instance

!!! info "Global collections"
    Global collections display is not yet implemented in InvenioRDM v13.

Before creating collections, you need:

1. **Access to Python shell** - Collections are currently managed via `invenio shell`
2. **A community** - Collections can be scoped to communities, so you need at least one community created

!!! warning "Administration UI for Collections"
    The administration UI for managing collections is not yet available in InvenioRDM
    v13. Collections are currently managed programmatically via the Python shell.

### Step 1: Create a Collection Tree

First, create a collection tree to serve as the root container:

```python
from invenio_collections.api import CollectionTree

COMMUNITY_ID = "<community_id>"  # Replace with your actual community UUID

# Create a collection tree for a subjects-based hiearchy
ctree = CollectionTree.create(
    title="Subjects",
    slug="subjects",  # Used in URLs
    community_id=COMMUNITY_ID,  # `None` for global trees
    order=10  # Controls display order (lower numbers appear first)
)
```

### Step 2: Create a top-level Collection

Create your first collection within the tree:

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
    query='metadata.subjects.id:"natural-sciences"',  # Search filter
    order=10  # Display order within the tree (lower numbers appear first)
)
```

### Step 3: Create nested Collections

Add two sub-collections to the top-level collection:

```python
math_col = collections_service.add(
    system_identity,
    collection=natural_sciences_col._collection,
    slug="mathematics",
    title="Mathematics",
    query="metadata.subjects.id:\"mathematics\"",
    order=10
)
compsci_col = collections_service.add(
    system_identity,
    collection=natural_sciences_col._collection,
    slug="computer-science",
    title="Computer and Information Sciences",
    query="metadata.subjects.id:\"computer-science\"",
    order=20
)
```

## Collection Query Inheritance

Nested collections automatically inherit their parent's search criteria, combining queries with AND logic. Child collections show only records that match both their own query and all parent queries.

### Example: EU Funding Programs

```
Funding Programs (tree)
├── Horizon Europe (query: metadata.funding.program:"horizon europe")
├── Horizon 2020 (query: metadata.funding.program:"horizon 2020")
│   └── Open Data (query: access.record:public)
│       └── Datasets (query: metadata.resource_type.id:dataset)
└── FP7 (query: metadata.funding.program:fp7)
```

**Effective queries:**
- Horizon Europe: `metadata.funding.program:"horizon europe"`
- Horizon 2020: `metadata.funding.program:"horizon 2020"`
- Open Data: `metadata.funding.program:"horizon 2020" AND access.record:public`
- Datasets: `metadata.funding.program:"horizon 2020" AND access.record:public AND metadata.resource_type.id:dataset`
- FP7: `metadata.funding.program:fp7`

### Example: Fields of Science

```
Research Fields (tree)
├── Natural Sciences (query: metadata.subjects.subject:"Natural sciences")
│   ├── Mathematics (query: metadata.subjects.subject:"Mathematics")
│   └── Physical Sciences (query: metadata.subjects.subject:"Physical sciences")
│       └── Astronomy (query: metadata.subjects.subject:"Astronomy")
└── Engineering (query: metadata.subjects.subject:"Engineering and technology")
```

**Effective queries:**
- Natural Sciences: `metadata.subjects.subject:"Natural sciences"`
- Mathematics: `metadata.subjects.subject:"Natural sciences" AND metadata.subjects.subject:"Mathematics"`
- Physical Sciences: `metadata.subjects.subject:"Natural sciences" AND metadata.subjects.subject:"Physical sciences"`
- Astronomy: `metadata.subjects.subject:"Natural sciences" AND metadata.subjects.subject:"Physical sciences" AND metadata.subjects.subject:"Astronomy"`
- Engineering: `metadata.subjects.subject:"Engineering and technology"`

## Accessing Collections

!!! note "TODO: Move to Use > Communities section of docs"
    This section is aimed mostly at end-users, but we don't have currently the
    "Communities" section in the docs.

Once created, collections are accessible through dedicated pages that display all records matching the collection's search criteria.

### Collection Pages

Collections appear as filtered views of records with clear navigation and context. The page shows the collection title, description (if provided), and all matching records with standard search and filtering options.

![Collection page showing Horizon 2020 records with search filters and results](placeholder-collection-page.png)

*A collection page displays all records matching the search criteria, with breadcrumb navigation showing the collection hierarchy.*

### Nested Collection Navigation

For hierarchical collections, users can navigate between parent and child collections using breadcrumb navigation. Each level in the hierarchy maintains its own filtered view while showing the relationship to parent collections.

![Nested collection page with breadcrumb navigation showing path from Programs > Horizon 2020 > Open Access](placeholder-nested-collection.png)

*Nested collections show breadcrumb navigation and allow users to move between different levels of the hierarchy.*

### Collection Browser

Communities with collections enabled feature a browse page that provides an overview of all available collection trees and their contained collections. This serves as the main entry point for users to discover and navigate collections within a community.

![Community browse page showing multiple collection trees with expandable sections](placeholder-collection-browser.png)

*The collection browser gives users an overview of all available collections organized by collection trees.*

Collections are accessible at these URL patterns:
- Root collection: `/communities/<community_slug>/collections/<tree_slug>/<collection_slug>`
- Nested collection: `/communities/<community_slug>/collections/<tree_slug>/<parent_slug>/<child_slug>`
- Collection browser: `/communities/<community_slug>/browse`

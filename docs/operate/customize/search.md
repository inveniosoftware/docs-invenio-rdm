# Change facets and sorting

InvenioRDM comes out of the box with facets for:

- Publication date (histogram with publication years, slider and default search filters)
- Access status (Open, Embargoed, Restricted or Metadata-only)
- Is published (Published, Unpublished)
- Languages
- Resource types (nested)
- Subjects (both plain and nested supported)
- File type

Similarly for sorting multiple fields are supported:

- Best match (makes sense with a search query)
- Newest
- Oldest
- Version index
- Most recently updated
- Least recently updated
- Most viewed
- Most downloaded

!!! tip

    Let us know which other facets/sort options you'd like to see out of the box.

## Configure

**Change facets and sort options**

To change the default facets, you need to edit your ``invenio.cfg``, and add one or
more of the following variables:

- ``RDM_SEARCH`` - Controls facets/sorting on ``/search`` and ``/api/records``.
- ``RDM_SEARCH_DRAFTS`` - Controls facets/sorting on ``/uploads`` and ``/api/user/records``.
- ``RDM_SEARCH_VERSIONING`` - - Controls facets/sorting on ``/api/records/:id/versions``.

For instance:

```python
RDM_SEARCH = {
    # Supported values: publication_date, access_status, is_published,
    # language, resource_type, subject, subject_nested, file_type
    "facets": ["publication_date", "access_status", "file_type", "resource_type"],

    # Supported values: bestmatch, newest, oldest, version, updated-desc,
    # updated-asc, mostviewed, mostdownloaded
    "sort": [
        "bestmatch",
        "newest",
        "oldest",
        "version",
        "mostviewed",
        "mostdownloaded",
    ],
}
```

Each variable has two keys:

- ``facets``: The list of facets in the order they are displayed. The name must
  have been defined in ``RDM_FACETS`` (defined in [invenio-rdm-records](https://github.com/inveniosoftware/invenio-rdm-records/blob/master/invenio_rdm_records/config.py)).
- ``sort``: The list of sort fields. The first element in the list is the
  default sort option used with a query. The second element is the default sort
  option used with an empty query. The sort fields must have been defined in
  ``RDM_SORT_OPTIONS`` (defined in [invenio-rdm-records](https://github.com/inveniosoftware/invenio-rdm-records/blob/master/invenio_rdm_records/config.py)).


**Defining a new sort option**

You can define new sort options yourself for your search interface.

To do this, add the ``RDM_SORT_OPTIONS`` to your ``invenio.cfg``.

If you'd like to completely replace the existing sort options, simply override the
variable like this:

```python
RDM_SORT_OPTIONS = {
    "bestmatch": dict(
        title=_('Best match'),
        fields=['_score'],
    ),
    "newest": dict(
        title=_('Newest'),
        fields=['-created'],
    ),
}
```

If you'd like to instead just add new options, you'll need to update the
existing list like this:

```python
from invenio_rdm_records.config import RDM_SORT_OPTIONS
RDM_SORT_OPTIONS.update({
    "title": dict(
        title=_('Title'),
        fields=['metadata.title'],
    ),
})
```

Note, that this only defines a new sort option. You still need to change e.g.
``RDM_SEARCH`` to use it.

The sort option is defined by:

- ``title`` - The title displayed in the user interface.
- ``fields`` - The search index fields to perform the sorting on (multiple
  fields allowed.)

### Configure date range facets

_Introduced in v14_

slider. The built-in ``publication_date`` facet is defined in
[invenio-rdm-records](https://github.com/inveniosoftware/invenio-rdm-records/blob/master/invenio_rdm_records/services/facets.py) and
enabled by default in ``RDM_SEARCH`` and ``RDM_SEARCH_DRAFTS``:

```python
# invenio_rdm_records/services/facets.py
publication_date = DateFacet(
    field="metadata.publication_date_range",
    label=_("Publication date"),
    interval="year",
    separator="..",
)

# invenio_rdm_records/config.py — RDM_FACETS
"publication_date": {
    "facet": facets.publication_date,
    "ui": {"field": "publication_date", 
    "type": "date", 
    "separator": ".."},
},
```

<figure>
  <img src="../imgs/publication-date-range-facet.png" alt="Publication date range facet" width="400" />
</figure>

To add a custom date range facet, register a ``DateFacet`` in ``RDM_FACETS`` and
mark the UI configuration with ``"type": "date"``:

```python
from invenio_i18n import lazy_gettext as _
from invenio_records_resources.services.records.facets import DateFacet
from invenio_rdm_records.config import RDM_FACETS

RDM_FACETS = {
    **RDM_FACETS,
    "created_date": {
        "facet": DateFacet(
            field="created",
            label=_("Created"),
            interval="month",
            separator="..",
        ),
        "ui": {
            "field": "created",
            "type": "date",
            "separator": "..",
        },
    },
}

RDM_SEARCH = {
    "facets": ["created_date", "publication_date", "access_status"],
    "sort": ["bestmatch", "newest", "oldest"],
}
```

In this configuration:

- ``facet`` configures backend aggregation and filtering via ``DateFacet``. Its
  ``field`` must be a date or date range field in the search index.
- ``ui`` configures the frontend. ``"type": "date"`` renders a ``RangeFacet``
  instead of a checkbox facet.
- ``separator`` in ``DateFacet`` and ``ui`` must match.

### Customize publication date facet UI

InvenioRDM renders date facets via ``ContribSearchAppFacets`` in
[invenio-search-ui](https://github.com/inveniosoftware/invenio-search-ui).
By default, preset and custom date filters are enabled:

```js
<RangeFacet
    title={agg.title}
    agg={agg}
    rangeSeparator={agg.separator || ".."}
    defaultRanges={[
        { label: i18next.t("Last 6 months"), type: "months", value: 6 },
        { label: i18next.t("Last 1 year"), type: "years", value: 1 },
        { label: i18next.t("Last 5 years"), type: "years", value: 5 },
    ]}
    enableCustomRange
    dateRangeToLabel={i18next.t("to")}
/>
```

``defaultRanges`` entries use ``type: "years"`` or ``type: "months"`` with a
numeric ``value``. Without these props, ``RangeFacet`` defaults to no presets and
no custom input (histogram and slider only).

To change or disable the optional filters, override ``RangeFacet`` in your
``mapping.js``. ``parametrize`` props take precedence over those passed by
``ContribSearchAppFacets``:

```js
import { RangeFacet } from "react-searchkit";
import { parametrize } from "react-overridable";

export const overriddenComponents = {
  RangeFacet: parametrize(RangeFacet, {
    defaultRanges: [],
    enableCustomRange: false,
  }),
};
```

See [Override React components](look-and-feel/override_components.md) and the
[RangeFacet documentation](https://inveniosoftware.github.io/react-searchkit/docs/components/range-facet).

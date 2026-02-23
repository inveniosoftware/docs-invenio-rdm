# Change facets and sorting

InvenioRDM comes out of the box with facets for:

- Publication date (Histogram with publication years, slider and default search filters)
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
    # Supported values: access_status, is_published, language, resource_type,
    # subject, subject_nested, file_type
    "facets": ["access_status", "file_type", "resource_type"],

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

### Customize publication date facet

By default, some optional filters are enabled.

```js
<RangeFacet
    title={agg.title}
    agg={agg}
    rangeSeparator={agg.separator || ".."}
    // optional
    defaultRanges={[
        { label: i18next.t("Last 1 year"), type: "years", value: 1 },
        { label: i18next.t("Last 5 years"), type: "years", value: 5 },
        { label: i18next.t("Last 6 months"), type: "months", value: 6 },
    ]}
    enableCustomRange={true}
    dateRangeToLabel={i18next.t("to")}
    customDatesLabel={i18next.t("Custom Dates")}
    datePlaceholders={{ YYYY: i18next.t("YYYY"), MM: i18next.t("MM"), DD: i18next.t("DD") }}
/>
```

If you want to configure or disable optional filters, you can parameterize them in your instance:

```js
import { RangeFacet } from "react-searchkit";
import { parametrize } from "react-overridable";

export const parameters = {
  defaultRanges: [],
  enableCustomRange: false,
};

export const MyRDMRangeFacet = parametrize(RangeFacet, parameters);
```

For more information about the facet, see the [RangeFacet documentation](https://inveniosoftware.github.io/react-searchkit/docs/components/range-facet).
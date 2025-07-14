# Usage statistics

_Introduced in v12_

The record usage statistics in InvenioRDM are implemented with the
[`Invenio-Stats`](https://invenio-stats.readthedocs.io/en/latest/) module and they are
designed to be compatible with the [COUNTER Code of Practice Release 4](https://www.projectcounter.org/code-of-practice-sections/archived-code-of-practice-release-4/).

!!! info "Persisted in the search indices"
    All information related to statistics (i.e. the raw events and aggregations) are stored
    exclusively in search indices and not in the database, which makes search engine backups
    much more relevant.
    Some recommendations are given in the [how-to section](../../operate/ops/backup_search_indices.md).

## Inner workings

The following sections aim to give you some insights into how usage statistics are collected under the hood.

### Raw events

Usage **events** are generated in the resources (for the REST API) and view functions (for the web interface).
The basic events are filtered and enriched via **event builders** that usually capture
information only present in the request context at the time of the event (e.g. IP address, user agent, etc.).
After their build process is finalized, they are sent off to a message queue.

!!! warning "Deduplication of events"
    Events that "look" the same (except for the timestamp) and are less than a second
    apart from each other will be deduplicated and counted as only one single event.
    So when somebody hits refresh on a landing page very quickly, not every page load
    will be counted.

A periodic background task will pick up pending events from the message queues,
process them further with the configured **preprocessors** (e.g. user anonymization)
and index them into the events indices.
This task can be called on demand via the CLI command `invenio stats events process`.

An indexed `record-view` statistics event looks like the following:

```json
{
  "_index": "my-site-events-stats-record-view-2023-04-04",
  "_id": "2023-04-04T09:26:30-951a582a144b51479477fc89a1ca96ab8891a10d",
  "_score": 1,
  "_source": {
    "timestamp": "2023-04-04T08:26:30",
    "recid": "fq14q-7ja92",
    "parent_recid": "n5qej-kaz30",
    "referrer": "https://127.0.0.1:5000/",
    "via_api": false,
    "is_robot": false,
    "country": null,
    "visitor_id": "10ac3a4737efabc81e12e8fbaeb2aab0d25f23c7d5731f6387461528",
    "unique_session_id": "f75b509f9aad420811b965d867940e1675296a7b5e95eb72fe0733be",
    "unique_id": "ui_fq14q-7ja92"
  }
}
```

The mappings for newly created event indices are automatically registered as defined
in the configured index **templates**.

### Event aggregations

While using all the raw usage events to calculate the statistics is possible,
it can be very expensive — especially when this is a frequent operation.
So to save some calculations, the raw events are periodically consolidated
into intermediate **aggregations** that can be used for querying statistics rather than
the raw events.

A periodic background task will check if there are any new events since the last run
and if there are, it will aggregate them into intermediate results ready for querying.
A bookmark mechanism is used to keep track of the periods for which events have
already been aggregated and which may contain new events to aggregate.
This task can be called on demand via the CLI command `invenio stats aggregations process`.

An indexed events aggregation over `record-view` events looks like the following:

```json
{
  "_index": "my-site-stats-record-view-2023-04",
  "_id": "ui_fq14q-7ja92-2023-04-04",
  "_score": 1,
  "_source": {
    "timestamp": "2023-04-04T00:00:00",
    "unique_id": "ui_fq14q-7ja92",
    "count": 2,
    "unique_count": 1,
    "recid": "fq14q-7ja92",
    "parent_recid": "n5qej-kaz30",
    "via_api": false
  }
}
```

### Querying statistics

`Invenio-Stats` provides **query** classes that can be used to calculate the finalized
statistics, e.g. by fetching the relevant intermediate aggregations from the search indices
and summing them up.

A query result for the `record-view` statistics of a record in Python looks like the following:

```python
{
    "start_date": None,
    "end_date": None,
    "recid": "fq14q-7ja92",
    "parent_recid": "n5qej-kaz30",
    "views": 13.0,
    "unique_views": 6.0
}
```

### Final record usage statistics

The final usage statistics for a record include the *record views* and *file downloads*
for both the *selected record version* as well as across *all of its versions*.
InvenioRDM turns them into the following shape:

```python
{
    "this_version": {
        "views": 10,
        "unique_views": 6,
        "downloads": 7,
        "unique_downloads": 7,
        "data_volume": 123.456,
    },
    "all_versions": {
        "views": 30,
        "unique_views": 16,
        "downloads": 23,
        "unique_downloads": 21,
        "data_volume": 345.678,
    }
}
```

#### Putting the stats into the records

Every record has usage statistics available via a transient `stats` property that's
lazy-loaded only when it is accessed.

For consistency between the search results and the landing pages (and a bit of caching),
the primary source for the collected record statistics is the records search index.
As a fallback, the statistics are fetched directly via several queries from the
aggregations' search indices.

!!! info "Outdated statistics?"
    A special **search dumper extension** for records will take care of updating the
    statistics before indexing the record in the search engine.
    The upshot here is that when the statistics seem to be outdated, you should
    try to reindex the record.

## REST API endpoint

`Invenio-Stats` provides a [REST API endpoint](../../reference/rest_api_statistics.md) for querying the statistics.
The required permissions to access this endpoint are determined by the `query_stats` entry
in the permissions policy.

!!! info "Disabled per default"
    Per default, access to this specific API endpoint is disabled to prevent
    attackers from overloading the system with too many or heavy queries.
    When enabling access to the system, it should be limited to certain groups of users
    (e.g. authenticated users, administrators, etc.) and/or rate-limiting should be
    put in place.

    However, the system will still include a record's usage statistics in the
    web interface as well as the API endpoints for records.

## Additional information

### Unique views and downloads

If it seems like the view and download counts on the landing page are a bit low, that's
probably because the landing page shows the _unique views/downloads_ per default.
They deduplicate events for each record that are coming from the same source.
This is simply the more honest metric, even if it can be a little bit disappointing.

### Only records have stats

Out of the box, InvenioRDM only collects statistics for records but not drafts.
As a consequence, only the record search supports the display of and sorting by views
and downloads.

### Only UI visits are counted as "view" events

Currently, InvenioRDM will generate but immediately discard `record-view` events
generated via REST API accesses.
Thus, only landing page visits will count as record views.

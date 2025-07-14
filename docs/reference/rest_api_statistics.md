# Statistics

_Introduced in v12_

Query for one or multiple statistics.

## Get statistics

`POST /api/stats`

**Parameters**

| Name                  | Type   | Location | Description                                          |
| --------------------- | ------ | -------- | ---------------------------------------------------- |
| `{query_name}`        | object | body     | Key-value pairs for 0-N queries and their options.   |
| `{query_name}.stat`   | string | body     | Configured query to execute.                         |
| `{query_name}.params` | object | body     | Arguments/parameters for the query, e.g. the `recid` |

### Request

```http
POST /api/stats HTTP/1.1
Content-Type: application/json

{
  "views": {
    "stat": "record-view",
    "params": {
      "recid": "abcd-1234"
    }
  },
  "views-all-versions": {
    "stat": "record-view-all-versions",
    "params": {
      "parent_recid": "qwer-1234"
    }
  },
  "views-with-date-range": {
    "stat": "record-view",
    "params": {
      "start_date": "2023-01-01",
      "end_date": "2023-01-10",
      "recid": "abcd-1234"
    }
  },
}
```

The top-level keys in the request body determine the names of the statistics queries and
will be used in the response.
They can be chosen freely.

Each query needs to have the values for `stat` and `params`.
The `stat` value determines the type of query to use and needs to match one of the configured
`STATS_QUERIES` keys.

The contents of the `params` object will be passed to the query and thus enable querying
for the statistics of certain objects.
Please note that every kind of query has a different set of parameters it accepts and/or
requires, as defined by the configuration.

#### Default queries

The following queries are available per default:

| Query name                     | Parameters                |
| ------------------------------ | ------------------------- |
| `record-view`                  | `recid` (required)        |
| `record-view-all-versions`     | `parent_recid` (required) |
| `record-download`              | `recid` (required)        |
| `record-download-all-versions` | `parent_recid` (required) |

All queries accept optional `start_date` and `end_date` parameters to limit the timespan
for which to report results.

### Response
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "views": {
    "end_date": null,
    "parent_recid": "n5qej-kaz30",
    "recid": "fq14q-7ja92",
    "start_date": null,
    "unique_views": 4.0,
    "views": 7.0
  },
  "views-all-versions": {
    "end_date": null,
    "parent_recid": "n5qej-kaz30",
    "start_date": null,
    "unique_views": 10.0,
    "views": 18.0
  },
  "views-with-date-range": {
    "end_date": "2023-01-01T00:00:00",
    "start_date": "2023-01-10T00:00:00",
    "unique_views": 0.0,
    "views": 0.0
  }
}
```

The result for each of the statistics queries is returned under the name chosen in the request.

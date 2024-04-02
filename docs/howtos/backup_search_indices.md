# Back up search indices

Starting with InvenioRDM v12, not all search indices can be recreated from the database
anymore.
In order to not lose any data when something goes wrong with the search indices, they
should be backed up regularly.

!!! info "Search indices: that's a lot of data"
    To give you an idea about the order of magnitude for search index sizes and what's
    on the line:
    In January 2020, [Zenodo](https://zenodo.org) got approximately **3M** visits
    (total, from harvesters and users), which produced approximately **10Gb** of
    usage statistics data.


## Non-exhaustive list of methods

There are several tools and approaches to pick from when it comes to preserving your
indexed data in Elasticsearch or OpenSearch.
Here is a small selection:

- [Elasticdump](https://github.com/taskrabbit/elasticsearch-dump#readme):
  A simple and straight-forward tool for moving and saving indices.
  Works with Elasticsearch as well as OpenSearch.
- Snapshots in [Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshot-restore.html)
  and [OpenSearch](https://opensearch.org/docs/2.6/tuning-your-cluster/availability-and-recovery/snapshots/index/):
  A method for taking incremental snapshots of the entire search cluster or individual indices.
- Raw file system backups: Of course, you can always just keep a backup of the file system
  for each of the cluster's nodes.
  However, we don't recommend this strategy.

Of course there's more possibilities out there (e.g. [Curator](https://github.com/elastic/curator)
for Elasticsearch), but this should give you an idea where to start.


## Elasticdump

For the sake of brevity, this guide only deals with `elasticdump` as it is a very simple
tool to use and works with both Elasticsearch and OpenSearch.

!!! info "Make sure to back up all indices"
    Please note that the given example only deals with backing up and restoring one single index.
    In your instance, you should make sure to back up *all* relevant indices regularly!


### Backup

All it takes to back up a search index are two commands, one for saving the mappings
and one for saving the data.
With the following commands, you'll create the files `stats-record-view-2023-04.mappings.json`
and `stats-record-view-2023-04.data.json` that hold each part:

```bash
$ elasticdump \
>       --input http://localhost:9200/my-site-stats-record-view-2023-04 \
>       --output stats-record-view-2023-04.mappings.json \
>       --type mapping
Tue, 04 Apr 2023 17:00:39 GMT | starting dump
Tue, 04 Apr 2023 17:00:39 GMT | got 1 objects from source elasticsearch (offset: 0)
Tue, 04 Apr 2023 17:00:39 GMT | sent 1 objects to destination file, wrote 1
Tue, 04 Apr 2023 17:00:39 GMT | got 0 objects from source elasticsearch (offset: 1)
Tue, 04 Apr 2023 17:00:39 GMT | Total Writes: 1
Tue, 04 Apr 2023 17:00:39 GMT | dump complete

$ elasticdump \
>       --input http://localhost:9200/my-site-stats-record-view-2023-04 \
>       --output stats-record-view-2023-04.data.json \
>       --type data
Tue, 04 Apr 2023 17:00:53 GMT | starting dump
Tue, 04 Apr 2023 17:00:53 GMT | got 2 objects from source elasticsearch (offset: 0)
Tue, 04 Apr 2023 17:00:53 GMT | sent 2 objects to destination file, wrote 2
Tue, 04 Apr 2023 17:00:53 GMT | got 0 objects from source elasticsearch (offset: 2)
Tue, 04 Apr 2023 17:00:53 GMT | Total Writes: 2
Tue, 04 Apr 2023 17:00:53 GMT | dump complete
```

!!! warning "Don't forget to back up the mappings!"
    In addition to the data itself, you will also have to back up the **index mappings**
    in order to be able to restore the data properly!
    Otherwise, the mapping types may be inferred automatically by the search engine,
    which can have a negative impact on the usability of the index, e.g. for search or
    filtering.

In order to emulate some kind of disruption (e.g. a malicious attack), you can simply
delete the index that was just backed up:

```bash
$ curl -X DELETE http://localhost:9200/my-site-stats-record-view-2023-04
{"acknowledged":true}
```

And just like that, the record view statistics for all of April 2023 are gone.


### Restore

Luckily, the restore is just as simple as the backup was.
All you need to do is to restore the mappings first, and the data afterwards.
The commands are nearly identical to the backup, just with the values for `--input` and
`--output` swapped out:

```bash
$ elasticdump \
>       --input stats-record-view-2023-04.mappings.json \
>       --output http://localhost:9200/my-site-stats-record-view-2023-04 \
>       --type mapping
Tue, 04 Apr 2023 17:01:19 GMT | starting dump
Tue, 04 Apr 2023 17:01:19 GMT | got 1 objects from source file (offset: 0)
Tue, 04 Apr 2023 17:01:20 GMT | sent 1 objects to destination elasticsearch, wrote 4
Tue, 04 Apr 2023 17:01:20 GMT | got 0 objects from source file (offset: 1)
Tue, 04 Apr 2023 17:01:20 GMT | Total Writes: 4
Tue, 04 Apr 2023 17:01:20 GMT | dump complete

$ elasticdump \
>       --input stats-record-view-2023-04.data.json \
>       --output http://localhost:9200/my-site-stats-record-view-2023-04 \
>       --type data
Tue, 04 Apr 2023 17:01:40 GMT | starting dump
Tue, 04 Apr 2023 17:01:40 GMT | got 2 objects from source file (offset: 0)
Tue, 04 Apr 2023 17:01:40 GMT | sent 2 objects to destination elasticsearch, wrote 2
Tue, 04 Apr 2023 17:01:40 GMT | got 0 objects from source file (offset: 2)
Tue, 04 Apr 2023 17:01:40 GMT | Total Writes: 2
Tue, 04 Apr 2023 17:01:40 GMT | dump complete
```

Now, the index is fully restored including the mappings as well as the data!

# v9.0: migrate to OpenSearch

With the release of InvenioRDM v10, the usage of Elasticsearch v7 is deprecated due to the [change of license](https://www.elastic.co/pricing/faq/licensing), and the migration to OpenSearch is highly recommended. The last version of Elasticsearch that can be installed, before the license change, is `v7.10`.

However, this version of Elasticsearch is affected by the security vulnerability [Log4Shell](https://www.elastic.co/security-labs/analysis-of-log4shell-cve-2021-45046).

Users of InvenioRDM v9 LTS release can seamlessly migrate to OpenSearch v1. The first available version not affected by the `Log4Shell` security issue is [OpenSearch v1.2.1](https://opensearch.org/blog/releases/2021/12/update-to-1-2-1/).

After careful analysis on how to enable OpenSearch integration in InvenioRDM v9, we recommend to run OpenSearch in compatibility mode, which will emulate Elasticsearch.

## Setup OpenSearch cluster

To set up the new OpenSearch v1 cluster, follow the **first** step in the InvenioRDM v10 [upgrade guide](../upgrading/upgrade-v10.0.md#migrate-to-opensearch). When following the guide, do not continue to step 2, do not change or upgrade any Python package.

In your new cluster, make sure that you enable the `compatibility` flag: `compatibility.override_main_response_version: true`.

```yaml
search:
    image: opensearchproject/opensearch:1.3.6
    environment:
      - "compatibility.override_main_response_version=true"
      ...
```

 This will instruct the cluster to return version 7.10.2 rather than its actual version, so that it will behave as an Elasticsearch cluster. For more information, see the [official documentation](https://opensearch.org/docs/latest/clients/agents-and-ingestion-tools/index/).

To ensure that the flag has been taken into account, check the version displayed when you visit <http://localhost:9200/>:

```json
{
  "name" : "...",
  ...
  "version" : {
    "number" : "7.10.2",
    ...
  },
  "tagline" : "The OpenSearch Project: https://opensearch.org/"
}
```

For reference, see the [OpenSearch 1.0 Backwards Compatibility FAQ](https://opensearch.org/blog/technical-posts/2021/06/opensearch-backwards-compatibility-faq/).

## Check Python dependencies

Make sure that your InvenioRDM v9 uses Elasticsearch Python dependencies:

```shell
# invenio-search should be < 2.0.0
$ pipenv run pip show invenio-search
Name: invenio-search
Version: 1.4.2

# elasticsearch should be < 7.14
$ pipenv run pip show elasticsearch
Name: elasticsearch
Version: 7.13.4
```

The Elasticsearch Python library [v7.14](https://github.com/elastic/elasticsearch-py/pull/1623) introduces a version check that **does not allow** to use other clusters than Elasticsearch.

## Re-index data

In your new cluster, re-index all data, as described in InvenioRDM v10 upgrade guide:

1. [Re-index data](../upgrading/upgrade-v10.0.md#re-index-data)
2. [Complete re-indexing](../upgrading/upgrade-v10.0.md#complete-re-indexing)

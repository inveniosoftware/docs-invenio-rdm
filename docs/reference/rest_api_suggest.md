# Suggest API
_Introduced in v13_

The `suggest` API endpoint (`/api/{resource}?suggest={search_input}`) provides an interface for real-time search suggestions. It leverages OpenSearch's `multi_match` query to search across multiple fields within a specified index, returning relevant suggestions based on user input.

## Endpoint structure

**URL:** `/api/{resource}?suggest={search_input}`
**Method:** GET

Each index in InvenioRDM can have its own configuration to customize how the `suggest` API behaves. This includes defining which fields are searchable and other settings provided by the `multi_match` query API.

## How to use the `suggest` API?

InvenioRDM's `suggest` API is designed to provide search suggestions by using a `multi_match` query. It can be configured for all the indices using the `SuggestQueryParser` class that can be imported from `invenio-records-resources` module. The fields are analyzed using custom analyzers at index time which apply filters like `asciifolding` for accent search and `edge_ngram` for prefix search.

Check the [official documentation](https://opensearch.org/docs/2.0/opensearch/ux/) and, if you are a core InvenioRDM developer, the [internals section](../maintenance/internals/search.md#tokenizers-and-token-filters) for more context on the `edge_ngram` filter and custom analyzers.

## When to use the `suggest` API

- **Typo Tolerance & Auto-completion:** Helps correct typos (using `fuzziness` at search time analyzing) and completes partial inputs.
- **Large, Diverse Datasets:** Useful for datasets with a wide variety of terms, like names or titles.
- **Pre-query Optimization:** Reduces unnecessary searches by suggesting relevant terms.

## When not to use the `suggest` API

- **Small or Specific Datasets:** Less beneficial for well-defined datasets.
- **Performance Constraints:** Because the suggest API creates large amounts of tokens using the `edge_ngram` filter, it is important to observe how it affects the index size.
  - A reasonable trade-off might involve an index size increase of up to 20-30% if it significantly improves search speed and relevance.
  - A 10-20% improvement in response times might justify a moderate increase in index size.

For more information check the [official documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/tune-for-disk-usage.html).

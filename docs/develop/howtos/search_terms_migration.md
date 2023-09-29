# Create search terms mappings

*Introduced in InvenioRDM v11*

This guide describes the process to create search terms mappings in the application layer.

This is particularly useful when a certain search term is not supported anymore by the search engine or we want to simplify a search term (e.g. nested field), in favor of a new term.

The query is parsed in the application layer and the old term is replaced with the new one before passing the query to the search engine.

!!! warning "Terms not in the mapping are not considered!"
    When a search term mapping is defined, other terms (not present in the mapping) are not used by the search engine.
    E.g. if a mapping is defined with a single term "description" that matches "metadata.description", all the other terms such as "metadata.title" will not work anymore.
    Proceed with caution.

## Steps

- Identify the search term to be mapped (e.g. `q=old_term:"value"`).
- Identify the new, equivalent search term (e.g. `q=new_term:"value"`)
- Add or edit the following configuration variable in your application `invenio.cfg` file:
    ```python
    RDM_SEARCH = {
        "query_parser_cls": QueryParser.factory(
            tree_transformer_factory=SearchFieldTransformer.factory(
                mapping={
                    "old_term": "new_term"
                }
            ),
        )
    }
    ```

## Examples

- The term `resource_type.subtype` was deprecated in favor of `metadata.resource_type.props.subtype`. Therefore, the following configuration was added to `invenio.cfg`:

    ```python
    RDM_SEARCH = {
        "query_parser_cls": QueryParser.factory(
            tree_transformer_factory=SearchFieldTransformer.factory(
                mapping={
                    "resource_type.subtype": "metadata.resource_type.props.subtype"
                }
            ),
        )
    }
    ```

    The query  `/api/records/q=resource_type.subtype` is transformed into `/api/records/q=metadata.resource_type.props.subtype:<subtype>`.

- Simplify a query for a nested field. This example maps `parent.communities.ids` into a shorter term `communities`:

    ```python
    RDM_SEARCH = {
        "query_parser_cls": QueryParser.factory(
            tree_transformer_factory=SearchFieldTransformer.factory(
                mapping={
                    "communities": "parent.communities.ids"
                }
            ),
        )
    }
    ```

    The query  `/api/records/q=communities:<community_id>` is transformed into `/api/records/q=parent.communities.ids:<community_id>`.

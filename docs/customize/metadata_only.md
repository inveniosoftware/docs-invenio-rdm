# Metadata-only records

Depending on your instance needs, you might want to disable the option for metadata-only records, and thus by default require that users include files in their uploads in order to publish.

To do so you can set in your `invenio.cfg` the following config:

```python
RDM_ALLOW_METADATA_ONLY_RECORDS = False
```

!!! note

    Superusers of your instance will still be able to disable files for draft uploads.

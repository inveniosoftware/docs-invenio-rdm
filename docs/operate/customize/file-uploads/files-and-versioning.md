# Files and record versioning

The record versioning feature in InvenioRDM allows for the tracking and management of changes made to records' files over time. With this feature, every time a file of a record is updated, a new version of the record is created, capturing the changes made to the files.

This record versioning system enables researchers, data managers, and administrators to maintain a complete history of changes made to records, providing transparency and accountability in the data management process. Each version of the record includes a timestamp, indicating when the change was made, and the user who made the update.

By utilizing record versioning in InvenioRDM, institutions can maintain a reliable audit trail of all modifications made to records, enhancing data integrity, and contributing to good data management practices. This feature is an essential component of maintaining the accuracy, reproducibility, and long-term accessibility of research data and associated metadata in InvenioRDM.

In some cases repository manager might need to chose to disable the file versioning, for example.

- Storage Space: Record file versioning can result in an accumulation of multiple versions of files, which can consume significant storage space over time. In scenarios where storage resources are limited, disabling file versioning can help conserve storage and reduce costs.

- Simplicity: Some users may prefer a simpler and cleaner file management system without multiple versions of files. By disabling versioning, the system becomes more straightforward to manage, especially for users who do not require version history.

- Security and Privacy concerns: In certain cases, keeping multiple versions of files might pose security or privacy risks. Disabling versioning can help mitigate these risks by ensuring that only the latest version of the file is available, reducing the potential exposure of sensitive or outdated information.

- User Preferences: Some users may find versioning unnecessary for their specific use case and may prefer a file management system without version history. By allowing users to disable file versioning, InvenioRDM offers flexibility to cater to individual preferences.

- Performance: Maintaining version history can impact system performance, especially when handling a large number of files and records. Disabling versioning can help improve system responsiveness and speed, particularly in resource-constrained environments.

In order to provide custom rules for unlocking the file edition without creating a new version, you need to implement a callable which evaluates the conditions to return a bool value:

```python
def lock_edit_record_published_files(service, identity, record=None, draft=None):
    """Custom conditions for file bucket lock."""
    if record:
        is_external_doi = record.get("pids", {}).get("doi", {}).get("provider") == "external"
        if is_external_doi:
            return False
    return True


RDM_LOCK_EDIT_PUBLISHED_FILES = lock_edit_record_published_files
"""Lock editing already published files (enforce record versioning)."""
```

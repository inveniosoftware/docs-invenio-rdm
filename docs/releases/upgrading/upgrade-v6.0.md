# Upgrading from v4.0 to v6.0


## Prerequisites

The steps listed in this article require an existing local installation of InvenioRDM 4.0, please make sure that this is given!
If unsure, run `invenio-cli install` from inside the instance directory before executing the listed steps.

**Note**: Do *not* delete the old Python virtual environment, or the database migration may complain about missing packages.

!!! warning "Backup"

    Always backup your database and files before you try to perform an upgrade.

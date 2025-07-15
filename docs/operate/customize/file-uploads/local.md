# Local storage

InvenioRDM can upload, store and serve files on the local filesystem of your server.

## Storage locations
A `location` defines a storage backend by specifying a name and a URI, which can reference either a local directory or a remote storage service. Locations determine where and how files are physically stored.

InvenioRDM offers a flexible storage architecture, allowing you to define multiple locations. Out-of-the-box, the system uses the location marked as `default`. If you wish to use multiple storage backends simultaneously (for example, both local storage and S3), you will need to implement custom logic to select which location to use for each file.

When you first install InvenioRDM, a default location named `default-location` is automatically created, with its URI pointing to your Python virtual environment’s base directory at `<venv>/var/instance/data`. Files will be stored there.

## Manage locations
You can use CLI commands to manage locations.

To list existing locations, run in your activated virtualenv:

```bash
$ invenio files location list
default-location /<venv>/var/instance/data as default True
```

To create new location, run:

```bash
$ invenio files location create myfolder /<path>/myfolder
Location myfolder /<path>/myfolder as default False stored in database
```

You can set the new location as default by passing `--default` when creating it, or by running:

```bash
$ invenio files location set-default myfolder
Location myfolder /<path>/myfolder set as default (True)
```

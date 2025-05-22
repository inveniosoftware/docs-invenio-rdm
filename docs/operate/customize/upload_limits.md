# Limiting File Uploads

Limiting the maximum size for file uploads can be desirable for a few reasons, e.g. to prevent a single record to fill up the entire disk space, and to make it more difficult for malicious users to upload a lot of data.


## Invenio Configuration

`Invenio-Files-REST` provides some [configuration values](https://invenio-files-rest.readthedocs.io/en/latest/configuration.html) that are relevant for limiting file uploads.
The most relevant ones are `FILES_REST_DEFAULT_MAX_FILE_SIZE` which limits the maximum size for *each* uploaded file (in bytes) and `FILES_REST_DEFAULT_QUOTA_SIZE` which limits the maximum overall size of *all* files uploaded per record (also in bytes).

For instance, consider the case that the maximum file size is set to 10GiB, and the default quota is set to 30GiB.
Then, the user can upload several files with a maximum size of 10GiB each.
The user could upload 3 files with 10GiB each, or several smaller ones, or anything in between.
However, the total size of all files deposited with a single record cannot exceed 30GiB.

**Note** that the Flask configuration option `MAX_CONTENT_LENGTH` is only applied for multi-part form uploads (e.g. community logos), but not for the files deposited with records.

For the InvenioRDM deposit form, restrictions are available for the total number of files and total file size (in decimal bytes). These are set by the `APP_RDM_DEPOSIT_FORM_QUOTA` variable which can be configured in `invenio.cfg`. For example, if you want to restrict users to a maximum upload of 30 GB and 100 files, you would add:

```
APP_RDM_DEPOSIT_FORM_QUOTA = {
    "maxFiles": 100,
    "maxStorage": 30*10**9,
}
```

## Nginx

While the above mentioned configuration would already prevent the backend from accepting files that are too large, an additional layer of defense can be added by configuring `nginx` to reject client requests above a certain size.

This can be achieved by setting the `client_max_size_body` for the REST API file content endpoint (`location ~ /api/records/.+/draft/files/.+/content`) to a desired value, e.g. `75G`.
The relevant file for this configuration on a default cookiecutter installation is [`docker/nginx/conf.d/default.conf`](https://github.com/inveniosoftware/cookiecutter-invenio-rdm/blob/master/%7B%7Bcookiecutter.project_shortname%7D%7D/docker/nginx/conf.d/default.conf#L118).


!!! info "Mind the multi-byte units!"
    The `nginx` configuration uses [binary units (KiB, MiB, GiB, ...) rather than decimal units (kB, MB, GB, ...)](https://en.wikipedia.org/wiki/Byte#Multiple-byte_units), i.e. `1M` is `1024K` rather than `1000K`.
    Given the example above, this means that `75G` would be equivalent to `75 * 1024^3` (= `80530636800`) bytes.
    This should be carefully considered while creating the configuration in all the various spots!

# FAIR Signposting

FAIR Signposting is a method for making research outputs more Findable, Accessible, Interoperable, and Reusable (FAIR). It involves adding specific links to the HTTP headers and/or HTML of a web page, which allows machines to easily discover metadata, related resources, and licensing information about the resource. This can greatly improve the discoverability and citability of your repository's content.

For more information, see [the official documentation](https://signposting.org/).

## Level 1

_Introduced in v13_

In order to increase discoverability, [FAIR Signposting level 1](https://signposting.org/FAIR/#level1) can be enabled in your `invenio.cfg`:

```python
APP_RDM_RECORD_LANDING_PAGE_FAIR_SIGNPOSTING_LEVEL_1_ENABLED = True
```

Once enabled, FAIR Signposting information will be directly included in the `Link` HTTP response header.

!!! warning
    Since enabling FAIR Signposting level 1 does increase the size of HTTP response headers, it is **recommended** to edit the `nginx` configuration and specify [`uwsgi_buffer_size`](https://nginx.org/en/docs/http/ngx_http_uwsgi_module.html#uwsgi_buffer_size) with a higher limit than the default values. If you have enabled `uwsgi_buffering on;`, then [`uwsgi_buffers`](https://nginx.org/en/docs/http/ngx_http_uwsgi_module.html#uwsgi_buffers) may also be adjusted.
    ```nginx
    server {
        # ...
        # Allow for larger HTTP response headers for FAIR Signposting level 1 support
        uwsgi_buffer_size 16k;
        # optional if uwsgi_buffering on;
        uwsgi_buffers 8 16k;

        # ...
    }
    ```

## Level 2
[FAIR Signposting level 2](https://signposting.org/FAIR/#level2) was already enabled by default since v12.
The response header of each record's landing page includes a `Link` header pointing to a JSON-based linkset which contains the FAIR Signposting information.

!!! info
    Please note that for records having many authors, files, or licenses, FAIR Signposting will fall back to level 2 only, in order to avoid generating excessively big HTTP response headers.

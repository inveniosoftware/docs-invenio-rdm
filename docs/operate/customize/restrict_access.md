# How to restrict access to pages

Sometimes it can be desirable to live by the motto "better safe than sorry", especially regarding potentially sensitive features like the administration panel (enabled in InvenioRDM v12).

This guide briefly describes how to narrow down access to subsets of the system.


## Restricting access for IP ranges via `nginx`

While most features in InvenioRDM are guarded by configurable permission policies, this isn't necessarily always the case.
For these exceptions, as well as extra precautions generally, it can be beneficial to restrict access on an `nginx` level.

!!! info "Current exceptions"
    At the time of writing, one of these exceptions is the administration panel which has a hard-coded check for the `administration-access` action.

An access restriction based on the client's IP address can be put into place via the `nginx` configuration, e.g. by adding nested `location` directives in the existing configuration:

```nginx
location / {
    uwsgi_pass ui_server;
    include uwsgi_params;
    # ... your configuration for the UI paths ...

    # restrict access to the administration panel UI to your network only
    location /administration/ {
      # action directives like `uwsgi_pass` aren't inherited like other configs
      uwsgi_pass ui_server;

      # allow your networks (replace with your IP ranges)
      allow 128.130.0.0/15;
      allow 192.35.240.0/22;
      allow 2001:629::/32;
      # etc.

      # also allow localhost and private networks (e.g. for local access through Docker)
      allow 127.0.0.1/8;
      allow ::1/128;
      allow 10.0.0.0/8;
      allow 172.16.0.0/12;
      allow 192.168.0.0/16;
      allow fd00::/8;

      # disallow anybody else
      deny all;
    }
}
```

!!! info "The `uwsgi_pass` directive doesn't get inherited"
    Note that the `uwsgi_pass` directive is part of a [class of directives that do not get inherited in nested locations](https://forum.nginx.org/read.php?2,243488,243488) and thus has to be specified explicitly again.

Restricting access to API endpoints follows a similar schema, but in the `location /api` block and with `uwsgi_pass api_server` instead.

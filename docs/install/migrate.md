# Migrate from another repository

You may want to import your existing records into your new InvenioRDM instance.
How to export your data is highly dependent on your existing repository. As of now, InvenioRDM provides no tooling for this. However, to import the records into your instance, the REST API is the current easiest mechanism to do so.

Beforehand, prepare your records to conform to the [REST API](../reference/rest_api_index.md).

Then you will want to POST to the API to create the records, but InvenioRDM rate limits the API usage. By default, we don't want our API to be abused or subject to denial-of-service attacks. For the period of time when records are being ingested, however, you will want to allow a greater request rate.

## Rate limiting

The Flask-Limiter library is used to control this via its [configuration options](https://flask-limiter.readthedocs.io/en/stable/#configuration). There you will find a range of configuration to adapt your strategy to your needs.

For our purposes, a couple of simple options are available:

### Option 1: RATELIMIT_ENABLED

Simply disable rate limiting completely:

In `invenio.cfg`:

```python
RATELIMIT_ENABLED = False
```

This disables ALL rate limiting. It's probably good to take your application unreachable from the outside during that time.

### Option 2: RATELIMIT_PER_ENDPOINT

Change the rate limit on the relevant endpoints for record (with files) creation / publication via `RATELIMIT_PER_ENDPOINT`:

In `invenio.cfg`:

```python
RATELIMIT_PER_ENDPOINT = {
    "records.create": "25000 per hour;500 per minute",
    "records.publish": "25000 per hour;500 per minute",
    "draft_files.create": "25000 per hour;500 per minute",
    "draft_files.update_content": "25000 per hour;500 per minute",
    "draft_files.create_commit": "25000 per hour;500 per minute"
}
```

Naturally, choose a rate that makes sense for you!

!!!info "Rate limit strings"
    Flask-Limiter outlines the [rate limit format](https://flask-limiter.readthedocs.io/en/stable/#rate-limit-string-notation) that you can use to tailor your throughput as you see fit.

Restart your instance so it picks up the changed configuration.

### Option 3: RATELIMIT_AUTHENTICATED_USER

Change the rate limit for authenticated users via `RATELIMIT_AUTHENTICATED_USER`. Its default is `"5000 per hour;100 per minute"`:

```python
RATELIMIT_AUTHENTICATED_USER = "25000 per hour;500 per minute"
```

Restart your instance so it picks up the changed configuration.

## Conclusion

When you are done importing your records, make sure to revert your rate limiting changes, by removing these configurations and restarting your instance.

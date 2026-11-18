# Rate limiting

Rate limiting restricts how many requests a client can send in a given time. It protects your instance from abuse, bots, scrapers and accidental overload.

InvenioRDM uses [Flask-Limiter](https://flask-limiter.readthedocs.io) through the Invenio-App module. It is **enabled by default**.

## Default limits

| Setting | Default | Applies to |
|---|---|---|
| `RATELIMIT_GUEST_USER` | `"1000 per hour;60 per minute"` | Visitors that are not logged in |
| `RATELIMIT_AUTHENTICATED_USER` | `"5000 per hour;100 per minute"` | Logged in users |
| `RATELIMIT_PER_ENDPOINT` | see below | Specific endpoints |

By default, the login, registration and password endpoints are limited to 10 requests per minute:

```python
RATELIMIT_PER_ENDPOINT = {
    "security.login": "10 per minute",
    "security.register": "10 per minute",
    "security.forgot_password": "10 per minute",
    "security.reset_password": "10 per minute",
}
```

When a client goes over the limit, it receives an HTTP `429 Too Many Requests` response. Rate limit headers (`RATELIMIT_HEADERS_ENABLED`) tell clients how many requests they have left.

## Change the limits

Set the values in your `invenio.cfg`. The format is described in the [Flask-Limiter documentation](https://flask-limiter.readthedocs.io/en/stable/#rate-limit-string-notation).

```python
RATELIMIT_GUEST_USER = "500 per hour;30 per minute"
RATELIMIT_AUTHENTICATED_USER = "5000 per hour;100 per minute"
```

To add or change a limit for one endpoint, **copy the full dictionary** and edit it, because your value replaces the default:

```python
RATELIMIT_PER_ENDPOINT = {
    "security.login": "5 per minute",
    "security.register": "5 per minute",
    "security.forgot_password": "5 per minute",
    "security.reset_password": "10 per minute",
    "invenio_search_ui.search": "30 per minute",  # example: add a limit for search
}
```

Run `invenio limiter limits` to list all routes that have a rate limit (see the [CLI reference](../../reference/cli_invenio.md)).

## Use a shared storage in production

By default, limits are counted in memory (`RATELIMIT_STORAGE_URI = "memory://"`). Each web process counts on its own, and counters are lost on restart. In production, use Redis so all processes share the same counters:

```python
RATELIMIT_STORAGE_URI = "redis://localhost:6379/3"
```

Set it with the environment variable `INVENIO_RATELIMIT_STORAGE_URI` if it contains credentials.

## Behind a proxy

Limits are counted per client IP address. If your instance runs behind a load balancer or reverse proxy, configure `PROXYFIX_CONFIG` correctly. Otherwise all users appear to come from the proxy and share one limit. See [`PROXYFIX_CONFIG`](../../reference/settings.md#proxyfix_config).

## Temporarily disable limits

For large imports, you may need higher limits. See [Migrate from another repository](../ops/migrate.md#rate-limiting). Remember to revert the change afterwards.

## Prefer limiting at the edge

Application limits are a good first layer, but heavy abuse is best stopped before it reaches the application. Add limits in your reverse proxy (for example the [Nginx `limit_req` module](https://nginx.org/en/docs/http/ngx_http_limit_req_module.html)) or load balancer. This is also the right place to block abusive bots and crawlers. See [Infrastructure architecture](../ops/infrastructure.md).

## Learn more

- [Flask-Limiter documentation](https://flask-limiter.readthedocs.io)
- [OWASP: Denial of Service Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Denial_of_Service_Cheat_Sheet.html)

# Security hardening

This page helps you secure your InvenioRDM instance. Use it as a **checklist before going live**, and again when you **upgrade** or review an existing instance.

!!! note
    This is not an exhaustive list. Security depends on your whole infrastructure. Follow established best practices, for example the [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org).

## Pre-launch checklist

Copy this list and tick the items as you go.

**Secrets and configuration**

- [ ] `SECRET_KEY`, `SECURITY_LOGIN_SALT` and `CSRF_SECRET_SALT` are long, random and unique per environment
- [ ] Secrets are set via environment variables and are **not** in Git
- [ ] `DEBUG` is off and the development default passwords from the template are changed
- [ ] `TRUSTED_HOSTS` lists only your domain names
- [ ] `PROXYFIX_CONFIG` matches the number of proxies in front of the application

**Network and transport**

- [ ] The site is only served over HTTPS with a valid certificate
- [ ] Only the load balancer or reverse proxy is reachable from the internet
- [ ] PostgreSQL, OpenSearch, Redis and RabbitMQ are **not** reachable from the internet
- [ ] Session cookies are secure (`SESSION_COOKIE_SECURE = True`, the default)

**Abuse protection**

- [ ] [Captcha (ALTCHA)](../customize/captcha.md) is enabled
- [ ] [Rate limiting](../customize/rate-limiting.md) uses a shared Redis storage
- [ ] Email confirmation is on (`SECURITY_CONFIRMABLE = True`)
- [ ] Limits are also set in the reverse proxy

**Access control**

- [ ] Admin access is given to as few users as possible
- [ ] The administration panel is [restricted to your network](../customize/restrict_access.md)
- [ ] Community creation and publishing policies match your needs

**Operations**

- [ ] Backups for the database, files and [statistics](./backup_search_indices.md) are in place and a restore was tested
- [ ] Logs and alerts are set up (see [Logs](./logging.md) and [Monitoring](./deploy.md#monitoring))
- [ ] You follow the [security announcements](../../releases/security-policy.md) and know how to upgrade

## Protect against bots and abuse

### Reduce spam on published content

- Use [curation checks](../customize/curation-checks.md) and [community reviews](../customize/require_community.md) so that new content is reviewed.
- Use [user quota](../customize/file-uploads/user-quota.md) and [upload limits](../customize/file-uploads/upload_limits.md) to limit storage abuse.

## Secrets and sessions

Use strong, random secrets, and **never** commit them. If a secret is leaked, change it immediately. For `SECRET_KEY`, use the [`invenio migrate-secret-key` command](../../reference/cli_invenio.md) so encrypted data stays readable.

See [Secret keys](../../reference/settings.md#secret-keys) and [Setting secrets and credentials](../customize/configuration.md#setting-secrets-and-credentials).

## Web security headers

Configure the [Content Security Policy](../../reference/settings.md#content-security-policy-csp) and other secure headers with `APP_DEFAULT_SECURE_HEADERS`. Keep the policy as strict as your features allow, and allow only the external domains you actually use.

## Files uploaded by users

Uploaded files can contain malicious content. To reduce the risk:

- Allow only the file types you need and do not let browsers run uploaded HTML or scripts.
- Serve files from a separate domain without sessions, when possible.
- Consider scanning uploads with an antivirus on your storage or proxy.

See [Deploy to production: Security](./deploy.md#security).

## Network and services

- Expose only the reverse proxy or load balancer to the internet.
- Use firewalls or private networks between services. Be careful with Docker: published ports can bypass host firewall rules. See [Docker packet filtering](https://docs.docker.com/engine/network/packet-filtering-firewalls/).
- Set passwords on PostgreSQL, OpenSearch, Redis and RabbitMQ, and use TLS where you can.
- Use an unprivileged database user for the application.

## Keep up to date

- Use a [supported version](../../releases/maintenance-policy.md) and read the [upgrade policy](../../releases/upgrade-policy.md).
- Follow the [release notes](../../releases/index.md) and apply upgrades regularly. Each major version has an upgrade guide.
- Update the operating system, Docker images and services too.
- Lock your JavaScript and Python dependencies. See [Deploy to production](./deploy.md#build-and-lock-assets).
- Report security issues privately. See the [security policy](../../releases/security-policy.md).

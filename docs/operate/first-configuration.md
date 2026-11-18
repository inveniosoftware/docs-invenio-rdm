# First configuration

This page lists the settings you should define when you set up a new InvenioRDM instance. It is a starting point, not the full list. For everything else, see [Configure everything](../customize/configuration.md).

!!! info "Where to set what"
    - Put **site-wide** settings in `invenio.cfg`.
    - Put **secrets and deployment-specific** settings (passwords, hosts, keys) in **environment variables** prefixed with `INVENIO_`.

    See [Configure everything](../customize/configuration.md) for details.

## 1. Identity of your site

| Setting | Description |
|---|---|
| `SITE_UI_URL` | Public URL of your instance, e.g. `https://repository.my-university.org`. |
| `SITE_API_URL` | Public URL of the API, e.g. `https://repository.my-university.org/api`. |
| `THEME_SITENAME` | Name of your site, shown in the header and emails. |
| `TRUSTED_HOSTS` | Domain names that can be served. See [`TRUSTED_HOSTS`](../../reference/settings.md#trusted_hosts). |
| `BABEL_DEFAULT_LOCALE`, `I18N_LANGUAGES` | Default and available languages. See [Languages](../customize/i18n-and-l10n.md). |

Also see [Change logo](../customize/look-and-feel/logo.md) and [Change theme](../customize/look-and-feel/theme.md).

## 2. Secrets

Generate a **long random value** for each secret and keep them out of Git. Use different values for each deployment (test, staging, production).

| Setting | Description |
|---|---|
| `SECRET_KEY` | Signs sessions and encrypts some database fields. |
| `SECURITY_LOGIN_SALT` | Used for login links and tokens. |
| `CSRF_SECRET_SALT` | Used for CSRF tokens. |

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

See [Secret keys](../../reference/settings.md#secret-keys).

## 3. Services

Point InvenioRDM to your services. These contain passwords, so set them via environment variables.

| Setting | Service |
|---|---|
| `SQLALCHEMY_DATABASE_URI` | PostgreSQL |
| `SEARCH_HOSTS` | OpenSearch |
| `CACHE_REDIS_URL`, `ACCOUNTS_SESSION_REDIS_URL` | Redis (cache and sessions) |
| `RATELIMIT_STORAGE_URI` | Redis (rate limiting). See [Rate limiting](../customize/rate-limiting.md). |
| `BROKER_URL`, `CELERY_RESULT_BACKEND` | Message queue and Celery |

See [Infrastructure architecture](./infrastructure.md) and [Deploy to production](./deploy.md).

## 4. Email

Users need email to confirm their account and reset their password.

```python
MAIL_SERVER = "smtp.my-university.org"
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_SUPPRESS_SEND = False
SECURITY_EMAIL_SENDER = "repository@my-university.org"
MAIL_DEFAULT_SENDER = "repository@my-university.org"
```

Set `MAIL_USERNAME` and `MAIL_PASSWORD` via environment variables. See [Emails](../customize/emails.md).

## 5. Users and registration

Decide who can create an account and how.

- Local accounts, institutional login (OAuth, SAML), or both: see [Authentication](../customize/authentication.md).
- Keep `SECURITY_CONFIRMABLE = True` so users must confirm their email.
- If registration is open, enable the [captcha](../customize/captcha.md).
- Create your first admin user: see the [pre-launch checklist](./deploy.md#pre-launch-checklist) and [Manage users and roles](../customize/users.md).

## 6. Files and storage

| Topic | Page |
|---|---|
| Where files are stored (local disk or S3) | [Local storage](../customize/file-uploads/local.md), [S3 compatible storage](../customize/file-uploads/s3.md) |
| Maximum file and record size | [Upload limits](../customize/file-uploads/upload_limits.md) |
| Storage per user | [User quota](../customize/file-uploads/user-quota.md) |

## 7. Persistent identifiers

If you want DOIs for your records, configure a provider and a prefix. See [DOI registration](../customize/dois.md).

## 8. Repository policies

Choose the behavior that fits your institution:

- [Metadata-only records](../customize/metadata/metadata_only.md)
- [Require a community to publish](../customize/require_community.md)
- [Restrict community creation](../customize/restrict_community_creation.md)
- [Record deletion](../customize/record_deletion.md)
- [Custom fields](../customize/metadata/custom_fields/records.md) and [vocabularies](../customize/vocabularies/index.md)

## Next steps

- Learn how you can [customize the look-and-feel](./customize/look-and-feel/index.md) of your instance.
- Review what you can [configure](./customize/configuration.md).
- Harden your instance and run through the [security hardening checklist](./ops/hardening.md).
- Follow [Deploy to production](./ops/deploy.md).

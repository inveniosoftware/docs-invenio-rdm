# Upgrade from v14 to v15

<!-- TODO: complete with the general upgrade steps (packages, database, search mappings, ...). -->

!!! warning "Backup"

    Always backup your database, [statistics indices](../../operate/ops/backup_search_indices.md) and files before you try to perform an upgrade.

## Update your configuration or infrastructure

**FIX-ME and make it way shorter**

### Switch from reCAPTCHA to ALTCHA

*Required for upgrade*: **Only if you customized the registration, forgot password or resend confirmation templates.** Otherwise it is recommended, but not required.

#### What changed and why

InvenioRDM used Google reCAPTCHA to protect the registration form. In v15 it is replaced by [ALTCHA](https://altcha.org), a self-hosted, proof-of-work captcha. The reasons:

- **Privacy**: reCAPTCHA sends your users' data to Google and uses cookies. ALTCHA runs entirely on your server.
- **Simpler setup**: no Google account and no API keys.
- **Better coverage**: ALTCHA also protects the forgot password and resend confirmation forms, not only registration.
- **Accessibility**: users do not need to solve image puzzles.

Learn more in the [Captcha documentation](../../operate/customize/captcha.md).

#### What happens if you do nothing

| Your situation | Result after upgrade |
|---|---|
| reCAPTCHA was not configured | Nothing changes. Captcha stays disabled. We recommend [enabling it](../../operate/customize/captcha.md#enable-altcha). |
| reCAPTCHA keys set, **default** templates | ALTCHA is enabled automatically. A deprecation warning is logged at startup. |
| reCAPTCHA keys set, **custom** templates | The forms may be **rejected**. Follow step 2 below. |

#### Step 1: update the configuration

In your `invenio.cfg` (or environment variables), remove the reCAPTCHA keys and enable ALTCHA:

```diff
- RECAPTCHA_PUBLIC_KEY = "..."
- RECAPTCHA_PRIVATE_KEY = "..."
+ ACCOUNTS_ALTCHA_ENABLED = True
```

Don't forget to remove `INVENIO_RECAPTCHA_PUBLIC_KEY` and `INVENIO_RECAPTCHA_PRIVATE_KEY` from your environment variables or secrets, if you used them.

Make sure that:

- `SECRET_KEY` is set to a strong random value. It is used to sign the challenges unless you set `ACCOUNTS_ALTCHA_HMAC_KEY`.
- `RATELIMIT_STORAGE_URI` points to a shared storage such as Redis in production. It prevents a solved challenge from being used twice. See [Rate limiting](../../operate/customize/rate-limiting.md#use-a-shared-storage-in-production).

#### Step 2: update your custom templates

Skip this step if you did not override these templates:

- `invenio_accounts/register_user.html`
- `invenio_accounts/forgot_password.html`
- `invenio_accounts/send_confirmation.html`

The ALTCHA widget needs two things in the template: the **field** and the **JavaScript bundle**. The simplest way is to start again from the new templates in [Invenio-Accounts](https://github.com/inveniosoftware/invenio-accounts/tree/master/invenio_accounts/templates/semantic-ui/invenio_accounts) and re-apply your changes.

If you prefer to update your template by hand:

**1. Render the field.** Replace the old reCAPTCHA field with the ALTCHA field, inside the `<form>`, before the submit button:

```diff
- {%- if form.recaptcha %}
-   <div class="grouped fields">{{ form.recaptcha() }}</div>
- {%- endif %}
+ {%- if form.altcha %}
+   <div class="field{% if form.altcha.errors %} error{% endif %}">
+     {{ form.altcha() }}
+     {%- for error in form.altcha.errors %}
+       <div class="ui pointing red basic label">{{ error }}</div>
+     {%- endfor %}
+   </div>
+ {%- endif %}
```

For the forgot password and resend confirmation pages, you can use the macro instead:

```jinja
{% from "invenio_accounts/_macros.html" import render_altcha %}
...
{{ render_altcha(forgot_password_form) }}
```

**2. Include the JavaScript bundle** at the end of the template:

```jinja
{%- block javascript %}
  {{ super() }}
  {%- if config.ACCOUNTS_ALTCHA_ENABLED %}
    {{ webpack['invenio-accounts-altcha.js'] }}
  {%- endif %}
{%- endblock javascript %}
```

!!! info "Temporary compatibility"
    On the registration page only, `form.recaptcha()` still renders the ALTCHA widget while the deprecated reCAPTCHA keys are set. This is temporary: update your template to use `form.altcha`.

#### Step 3: rebuild and test

1. Rebuild your assets (`invenio-cli assets build`, or rebuild your Docker image). The widget's JavaScript is a new bundle.
2. If you added Google domains (`www.google.com`, `www.gstatic.com`) to your Content Security Policy (`APP_DEFAULT_SECURE_HEADERS`) for reCAPTCHA, you can remove them.
3. Restart your instance and check that the startup logs do not show the reCAPTCHA deprecation warning.
4. Test these pages in a private browser window: sign up, forgot password and resend confirmation. Submit each form and check that it is accepted.

<!-- TODO: add screenshot of the widget while it is verifying -->

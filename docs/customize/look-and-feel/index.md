# Look-and-feel

This section covers how to change the look-and-feel of your instance. If you need to match your institution's look-and-feel, this section is for you.

Typically, this involves setting configuration values and placing files in expected locations.
Other sections, such as [Authentication](../authentication.md) or [Vocabularies](../vocabularies/index.md) deal with customizing content or adding features.

## Setting configuration values

### via `invenio.cfg`
When told to set a configuration variable or edit your instance's settings, this typically means editing
the `invenio.cfg` file:

```python
# invenio.cfg file

THEME_FRONTPAGE_TITLE = "RePo: the Repository about Potatoes"
```

Doing so overrides the `config.py` variables provided by
[Invenio modules](https://invenio.readthedocs.io/en/latest/documentation/bundles/index.html)
and their dependencies. The configuration values are interpreted as Python values. In fact, `invenio.cfg` is just a Python file.

### via environment variables

Sometimes, you will want to provide the configuration value via an environment variable (e.g. different values based on different deployment contexts). In that case, you will prefix the configuration key by `INVENIO_` and use the resulting variable name as the environment variable to set:

```bash
INVENIO_THEME_FRONTPAGE_TITLE="Stage RePo: the Repository about Potatoes"
```

!!! warning "Environment variables are interpreted as Python literals"

    The InvenioRDM environment variables loader will try to interpret values as Python literals. Quoting is thus recommended to get the right result.

    ❌ DON'T
    ```shell
    INVENIO_APP_ALLOWED_HOSTS=["127.0.0.1"] invenio-cli run
    ```
    `APP_ALLOWED_HOSTS` is interpreted as the string `"[127.0.0.1]"` because of shell substitution followed by Python literal conversion.

    ✅ DO
    ```shell
    INVENIO_APP_ALLOWED_HOSTS='["127.0.0.1"]' invenio-cli run
    ```
    `APP_ALLOWED_HOSTS` is interpreted as the list `["127.0.0.1"]` which is right.

    Another pitfall to avoid is when a value can be interpreted as the wrong type.

    ❌ DON'T
    ```shell
    INVENIO_DATACITE_PREFIX="10.5072" invenio-cli run
    ```
    `INVENIO_DATACITE_PREFIX` is interpreted as the float `10.5072` which is wrong.

    ✅ DO
    ```shell
    INVENIO_DATACITE_PREFIX='"10.5072"' invenio-cli run
    ```
    `INVENIO_DATACITE_PREFIX` is interpreted as the string `"10.5072"` which is right.

    Investigate how your system handles environment variable to avoid these issues.

## Placing files in expected locations

Your instance comes with a folder structure prepared to welcome new files:

- `assets/`  -- where custom JavaScript and LESS files go
- `static/`  -- where custom images and other static files go
- `templates/` -- where custom Jinja templates go

For Jinja templates, because the content of your `templates/` folder is consulted before the InvenioRDM modules' `templates/` folder, mimicking a template's expected path in your `templates/` folder won't require you to change any configuration values.

In the next sections, we go through common customizations and show you the workflow commands to use:

- [Change logo](logo.md)
- [Change templates](templates.md)
- [Change theme](theme.md)

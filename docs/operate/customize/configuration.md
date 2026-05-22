# Configure everything

InvenioRDM can be configured via:

- Configuration file (``invenio.cfg``)
- Environment variables

## Configuration file

In the created project folder you'll find the ``invenio.cfg`` configuration file.
It already has some options set and documented that you can change.

The ``invenio.cfg`` file is good for default and site-wide configuration - i.e. options that are the same no matter if you deploy in a test/sandbox system, a local installation or a production system. Examples include for instance the site name or the default language.

The ``invenio.cfg`` file is included in the Docker image, which means that if you change it, you will also have to rebuild the image.

!!! info
    The configuration file is a Python module, and thus follows standard Python syntax.

    - It doesn’t allow for Python syntax errors.
    - It can assign settings dynamically using normal Python syntax
    - It can import values from other configuration files.

## Environment variables

InvenioRDM can also be configured via environment variables. The environment variables are good for deployment specific options. Examples include the database host and credentials and the application's secret key.

To set an environment variable configuration, you should prefix the configuration variable with ``INVENIO_``. Below is an example of setting the ``SQLALCHEMY_DATABASE_URI`` variable:

```bash
export INVENIO_SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://my-site:my-site@localhost/my-site"
```

!!! info
    Environment variables take precedence over values in the ``invenio.cfg`` configuration file.

## Setting secrets and credentials

You should ALWAYS set secrets or credentials (e.g. database password etc.) in the configuration via environment variables.

In particular, you should NEVER set secrets or credentials in the configuration file, and you should NEVER commit that file to e.g. a Git source code repository.

The credentials you do find in the ``invenio.cfg`` file are for the default development server.

## Reference

InvenioRDM is a *large* project with many modules and many settings. We curated the feature flags and most notable settings on the [Notable Configuration Settings](../../reference/settings.md) page. To find other specialized settings, look for the `config.py` file in the [relevant InvenioRDM module](../../maintenance/modules.md)'s source code.

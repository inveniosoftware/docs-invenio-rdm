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

## Notable configuration settings

### ``TRUSTED_HOSTS``

Invenio has a configuration option called ``TRUSTED_HOSTS`` which controls which hosts/domain names can be served. A client request to a web server usually includes the domain name in the Host HTTP header:

```
GET /
Host: example.org
...
```

The web server uses that for instance to host several websites on the same domain. Also, the host header is usually used in a load balanced environment to generate links with the right domain name.

An attacker has full control of the host header and can thus change it to whatever they like, and for instance have the application generate links to a completely different domain.

Normally your load balancer/web server should only route requests with a white-listed set of hosts to your application. It is however very easy to misconfigure this in your web server, and thus Invenio includes a protective measure.

Simply set TRUSTED_HOSTS to a list of allowed hosts/domain names:

```
TRUSTED_HOSTS = ['www.example.org']
```

Failing to properly configure this variable will cause the error `Bad Request Host x.x.x.x is not trusted.` when starting the web app.

### ``WSGI_PROXIES``

Invenio is commonly used with both a load balancer and a web server in front of the application server. The load balancer and web server both work as proxies, which means that the clients remote address usually gets added in the X-Forwarded-For HTTP header. Invenio will automatically extract the clients IP address from the HTTP header, however to prevent clients from doing IP spoofing you need to specify exactly how many proxies you have in front of you application server:

```
WSGI_PROXIES = 2
```

### Secret keys

Probably the most important security measure is to have strong random secret keys set for your InvenioRDM instance.

Good practices:

- Never commit your secrets in the source code repository (or any other password for that sake).
- Use different secrets for different deployments (testing, staging, production).

List of secrets:

- `SECRET_KEY`: The secret key is used for instance to sign user session ids and encrypt certain database fields. The secret key must be kept secret. If the key is leaked or stolen somehow, you should immediately change it to a new key.
- `SECURITY_LOGIN_SALT`: The salt value is used when generating login links/tokens.
- `CSRF_SECRET_SALT`: The salt value is used when generating login CSRF tokens.

```python
SECRET_KEY = '..put a long random value here..'
SECURITY_LOGIN_SALT = '..put a long random value here..'
CSRF_SECRET_SALT = '..put a long random value here..'
```

### Content Security Policy (CSP)

Content Security Policy (CSP) is an added layer of security that helps to detect and mitigate certain types of attacks, including Cross-Site Scripting (XSS) and data injection attacks.
To configure such headers, change the var `APP_DEFAULT_SECURE_HEADERS` in ``invenio.cfg``:

```python
APP_DEFAULT_SECURE_HEADERS = {
    ...
}
```

### Citation styles

InvenioRDM supports citations styles defined in the [CSL 1.0.1 specifications](https://docs.citationstyles.org/en/v1.0.1/specification.html). You can find the list of all possible citation styles [here](https://github.com/citation-style-language/styles/tree/v1.0.1).

In the record landing page, you can display a subset of the available styles. In your `invenio.cfg` change:

```
RDM_CITATION_STYLES = [
     ('chicago-annotated-bibliography', _('Chicago')),
     ('ieee', _('IEEE')),
     ('science', _('Science')),
     ('apa', _('APA')),
     ('cell', _('Cell')),
]
```

By changing the list above, these styles will be visible in the record landing page and the user can click on them to change citation style.

You can change the default citation style used when loading the record landing page by setting:

```
RDM_CITATION_STYLES_DEFAULT = 'chicago-annotated-bibliography'
```

### Download all files button

*Introduced in InvenioRDM v11*

!!! warning "Blocking connection and large files"
     In contrast to other file-serving endpoints, this functionality does not offload the response to nginx, which means that for very large files and slower client connections these might become long-running blocking requests. You can mitigate these issues either via rate-limiting or setting up dedicated resources for serving this type of requests.

To enable/disable the UI button and backend functionality for being able to download all of a record's files as a single ZIP file, you can set in your `invenio.cfg` the following config:

```python
RDM_ARCHIVE_DOWNLOAD_ENABLED = True
```

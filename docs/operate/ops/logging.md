# Logs

## Retrieving logs

To get the logs if you are running a containerized environment, you will need to retrieve them from the corresponding containers. It can be done in two steps, first obtaining the container IDs and then getting their logs:

``` bash
docker ps -a
```
``` console
CONTAINER ID        IMAGE                                                     COMMAND                  CREATED             STATUS                           PORTS                                                                                        NAMES
5cb64814ed2a        my-site-frontend                                          "nginx -g 'daemon of…"   24 minutes ago      Up 1 minute                                                                                                                   mysite_frontend_1
39993dcbb84f        my-site                                                   "bash -c 'celery wor…"   24 minutes ago      Up 1 minute                                                                                                                   mysite_worker_1
ff9a589845e4        my-site                                                   "bash -c 'uwsgi /opt…"   24 minutes ago      Up 1 minute                      0.0.0.0:32810->5000/tcp                                                                      mysite_web-api_1
a99532c10a8b        my-site                                                   "bash -c 'uwsgi /opt…"   24 minutes ago      Up 1 minute                      0.0.0.0:32811->5000/tcp                                                                      mysite_web-ui_1
d9afc36a573c        redis                                                     "docker-entrypoint.s…"   24 minutes ago      Up 3 minute                      0.0.0.0:6379->6379/tcp                                                                       mysite_cache_1
cbdac8cbd6a9        rabbitmq:3-management                                     "docker-entrypoint.s…"   24 minutes ago      Up 3 minute                      4369/tcp, 5671/tcp, 0.0.0.0:5672->5672/tcp, 15671/tcp, 25672/tcp, 0.0.0.0:15672->15672/tcp   mysite_mq_1
38d63e050e6b        postgres:9.6                                              "docker-entrypoint.s…"   24 minutes ago      Up 3 minute                      0.0.0.0:5432->5432/tcp                                                                       mysite_db_1
30356839105a        docker.elastic.co/elasticsearch/elasticsearch-oss:7.2.0   "/usr/local/bin/dock…"   24 minutes ago      Up 3 minute (health: starting)   0.0.0.0:9200->9200/tcp, 0.0.0.0:9300->9300/tcp                                               mysite_es_1
```

The most interesting entries are the `web-ui` and `web-api` containers, which in this case have id `a99532c10a8b` and `ff9a589845e4` respectively. The logs can be obtained by using the `logs` command of `docker`. An example of a working instance of the `web-api` container would show the following (trimmed output for clarity):

``` bash
docker logs ff9a589845e4
```

``` console
[uWSGI] getting INI configuration from /opt/invenio/var/instance/uwsgi_rest.ini
*** Starting uWSGI 2.0.18 (64bit) on [Wed Jan  8 13:09:07 2020] ***
[...]
spawned uWSGI master process (pid: 1)
spawned uWSGI worker 1 (pid: 255, cores: 2)
spawned uWSGI worker 2 (pid: 257, cores: 2)
*** Stats server enabled on 0.0.0.0:9001 fd: 11 ***
```

## invenio-logging

InvenioRDM enhances its logging capabilities with the [`invenio-logging`](https://github.com/inveniosoftware/invenio-logging) module, improving the observability and reliability of your repository. This ensures a smoother operational experience for administrators and end-users alike.

[`invenio-logging`](https://github.com/inveniosoftware/invenio-logging) configures the Flask app logger, offering a standard Python logging interface for log creation and handler installation.

The following logger extensions exists:

**InvenioLoggingConsole**: Logs output to the console, useful for development environments.

**InvenioLoggingFS**: Logs are written to a file, ideal for production environments where log preservation is necessary.

**InvenioLoggingSentry**: Provides real-time error tracking and monitoring, allowing for immediate notification of issues.

## Logging Levels

InvenioRDM supports different logging levels for controlling the verbosity of logs. The available levels, in increasing order of severity, are:

- `DEBUG`: Detailed information for diagnosing issues.
- `INFO`: Confirmation that things are working as expected.
- `WARNING`: Indicating a potential issue that should be addressed.
- `ERROR`: A fault that caused a feature to fail but didn't cause a complete failure.
- `CRITICAL`: A serious error that caused a failure and should be investigated immediately.

You can set the desired logging level for your environment by configuring the `LOGGING_CONSOLE_LEVEL` and `LOGGING_FS_LEVEL` variables in your `invenio.cfg` file. For example, to set the console logging level to `DEBUG`, you can add the following line:

```python
LOGGING_CONSOLE_LEVEL = "DEBUG"
```

Setting the logging level to `DEBUG` can be particularly useful during development or when troubleshooting issues, as it provides more detailed information in the logs.

For more information on configuring logging levels and handlers, refer to the [`invenio-logging`](https://invenio-logging.readthedocs.io/en/latest/) documentation.

## File Logging

For file logging, you can configure the LOGGING_FS_LEVEL variable in a similar way:

```python
LOGGING_FS_LEVEL = "INFO"
```

This will set the file logging level to `INFO`, which is a good default for production environments.

The available logging levels are: `CRITICAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG`, or `NOTSET`.

## Python Warnings Logging

InvenioRDM can log Python warnings to the console and file logs. This behavior can be controlled using the `LOGGING_CONSOLE_PYWARNINGS` and `LOGGING_FS_PYWARNINGS` configuration variables.

## File Logging Configuration

The maximum size of log files can be set using `LOGGING_FS_MAXBYTES` (default: 100MB).
The number of rotated log files to keep can be set using `LOGGING_FS_BACKUPCOUNT` (default: 5).

Full configuration options can be found in [config.py](https://github.com/inveniosoftware/invenio-logging/blob/master/invenio_logging/config.py)

## Integrations

You can configure Celery, SQLAlchemy, and Redis to send logs to Sentry. This behavior can be controlled using the `LOGGING_SENTRY_CELERY`, `LOGGING_SENTRY_SQLALCHEMY`, and `LOGGING_SENTRY_REDIS` configuration variables, respectively.

## Sentry Integration

[Sentry](https://docs.sentry.io/) is a popular error tracking and monitoring tool that provides real-time error tracking and monitoring capabilities. InvenioRDM integrates with Sentry through the `invenio-logging` module, allowing you to seamlessly incorporate Sentry into your logging setup.

## Configuring Sentry

To enable Sentry integration, follow these steps:

- Install the Sentry SDK: In your `Pipfile`, under the `[packages]` section, add the `invenio-logging` package with the `sentry` extra:

```python
invenio-logging = {extras = ["sentry"]}
```

- Configure Logging Backends: In your `invenio.cfg` file, add the desired logging backends and configure the Sentry initialization options:

```python
# Invenio-logging Sentry
# ----------------------
LOGGING_SENTRY_INIT_KWARGS = {
    # Add Sentry SDK configuration options here, e.g.:
    # Instruct Sentry to send user data attached to the event
    "send_default_pii": True,
}
```

You can find the full configuration options at [Sentry configuration page](https://docs.sentry.io/platforms/python/configuration/)

- Set the Sentry DSN: In your `.env` file, override the SENTRY_DSN variable with your Sentry Data Source Name (DSN) to avoid CI errors:

```python
INVENIO_SENTRY_DSN = "https://<SENTRY_PROJECT_ID>@sentry.io/<SENTRY_PROJECT_ID>"
```

Replace <SENTRY_PROJECT_ID> with your actual Sentry project ID.

You can adjust any of the logging variables for Sentry like

```python
LOGGING_SENTRY_LEVEL = "DEBUG"
```

## Customizing the Sentry Extension

If needed, Additional options can be passed to the Sentry instance using the `LOGGING_SENTRY_INIT_KWARGS` configuration variable.

## Best Practices

**Environment-Specific Configuration**
Utilize different logging levels and backends for development, testing, and production environments to optimize performance and monitoring by switching the configurations above.

**Sensitive Information**
Ensure that logging does not capture sensitive information, adhering to privacy and security best practices.

# Install Locally

In the [Preview Section](../preview/index.md), we have been running all of the
application in docker containers. This saves you the trouble of installing the
instance on your host and gets something visible fast. Now, we will run the
application locally and the database and other services in containers. It's the
best compromise between getting up and running with relevant services fast, while
allowing you to iterate on your local instance quickly.

Before going on, let's move into the project directory:

``` bash
cd development-instance
```

## Install for development

To run the application locally, we will need to install it and its dependencies
first. For this release, we need to add `--pre`, since we do have to
install alpha releases. Be patient, it might take some time to build.

!!! info "Pre-requisite: FLASK_ENV is available via invenio-cli flags"
    You do not need to export `FLASK_ENV` anymore. Just call the commands with
    `--development` or `-d`.
    To be able to modify assets and work on dependent modules, the environment
    variable `FLASK_ENV` must be set to `development`. This will instruct the
    different commands to create symbolic links to your files so the changes
    are easily propagated. There are two operations that require this flag:
    `install` and `update`.

``` bash
invenio-cli install --pre --development
```

``` console
# Summarized output
Installing python dependencies...
Symlinking invenio.cfg...
Symlinking templates/...
Collecting statics and assets...
Installing js dependencies...
Copying project statics and assets...
Symlinking assets/...
Building assets...
Built webpack project.
```

As a result, the Python dependencies for the project have been installed in
a new virtualenv for the application and many of the files in your project
directory have been symlinked inside it.

#### Notes and Known Issues

- You may see `SystemError: Parent module 'setuptools' not loaded, cannot perform relative import`
  at the dependency locking step. This depends on your version of
  `setuptools` (bleeding edge causes this) and can be solved by setting an
  environment variable: `SETUPTOOLS_USE_DISTUTILS=stdlib`.
  [See more details](https://github.com/pypa/setuptools/blob/17cb9d6bf249cefe653d3bdb712582409035a7db/CHANGES.rst#v5000).
  This sudden upstream change will be addressed more systematically in future releases.


## Setup the database, Elasticsearch, Redis and RabbitMQ

We need to initialize the database, the indices and so on. For this, we use
the `services` command. The first time this command is run, the services will be
setup correctly and the containers running them will even restart upon a reboot
of your machine. If you stop and restart those containers, your data will still
be there. Upon running this command again, the initial setup is skipped.

``` bash
invenio-cli services setup
```

``` console
Making sure containers are up...
Creating network "development-instance_default" with the default driver
Creating development-instance_cache_1 ... done
Creating development-instance_es_1    ... done
Creating development-instance_db_1    ... done
Creating development-instance_mq_1    ... done
Creating database postgresql+psycopg2://development-instance:development-instance@localhost/development-instance
Creating all tables!
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
Created all tables!
Location default-location /your/path/to/var/instance/data as default True created
Role "admin" created successfully.
Creating indexes...
Putting templates...
```

In case you want to wipe out the data that was there (say to start fresh),
you can use `--force` and nuke the content!

``` bash
invenio-cli services setup --force
```

``` console
Making sure containers are up...
development-instance_mq_1 is up-to-date
development-instance_db_1 is up-to-date
development-instance_cache_1 is up-to-date
development-instance_es_1 is up-to-date
Cache cleared
Destroying database postgresql+psycopg2://development-instance:development-instance@localhost/development-instance
Destroying indexes...
Indexing queue has been initialized.
Indexing queue has been purged.
Creating database postgresql+psycopg2://development-instance:development-instance@localhost/development-instance
Creating all tables!
  [####################################]  100%
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
Created all tables!
Location default-location /your/path/to/var/instance/data as default True created
Role "admin" created successfully.
Creating indexes...
Putting templates...
```

## Populate DB

Demo records come now by default! If you want to avoid having them when setting up your instance pass the `--no-demo-data` flag to the `setup` command:

```bash
invenio-cli services setup --no-demo-data
```

# Build, setup and run

Now that we have created a project folder, we need to build and set up the InvenioRDM application.

As mentioned before, the application can be built and installed in two different ways:

- *Local development* (good for developers or for customizing your instance): The application is installed directly on your machine in a Python [virtual environment](../reference/virtualenvs.md) managed by the python package manager tool (by default ``uv``). Its services are containerized though.
- *Containerized preview* (good for quick preview): The application is built inside a Docker image and, it, along with the services are all containerized.

## Condensed version

For the impatient, here are the commands to build, setup and run InvenioRDM. For clarity, we have decomposed them into individual steps in the guide below. Follow the guide below for step-by-step details:

=== "Local development"

    ```shell
    # Install Python and Javascript packages
    invenio-cli install
    # Set up containerized database, cache, OpenSearch, etc.
    invenio-cli services setup
    # Serve the application locally through a development server
    invenio-cli run
    ```

=== "Containerized preview"

    ```shell
    invenio-cli containers start --lock --build --setup
    ```

!!! info
    If you run the above commands, you're all set for this section. If you would like to learn more about the build process,
    then follow the steps below instead.


## Python dependencies

First, we start by locking the Python dependencies, which ensures that you will always have the same versions of dependencies if you reinstall in the future. Locked dependencies are important for having reproducible installs.

This step is executed automatically by both the local development (under `invenio-cli install`) and containerized preview (`--lock` option) installation options, but here we run it explicitly.

It's the same command for either installation option. Let's try it:

```bash
cd my-site/
invenio-cli packages lock
```
```console
Locking dependencies... Allow pre-releases: False. Include dev-packages: False.
Locking python dependencies...
[...]
Dependencies locked successfully.
```

A new lock file (e.g., ``uv.lock``) has now been created with the locked dependencies.

Next, follow the *local development* option or *containerized preview* option according to your preferred installation method.

## Option 1: Local development

The local install is good for developers or if you like to customize InvenioRDM as it avoids the waiting time for building a new Docker image. For instance, changing the layout will be much faster with a local install.

### Build

The local build steps involve installing all the Python dependencies into a local Python virtual environment, as well as all the Javascript dependencies. The Javascript dependencies are defined in the Python packages. This is done with the command:

```bash
invenio-cli install
```
```console
Installing python dependencies... Please be patient, this operation might take some time...
[...]
Built webpack project.
Dependencies installed successfully.
```

The command does the following:

- Install Python dependencies (according to the lock file)
- Install JavaScript dependencies
- Build the JavaScript/CSS web assets

### Setup

We need to initialize the database, the indices and so on. For this, we use the services command. The first time this command is run, the services will be setup correctly and the containers running them will even restart upon a reboot of your machine. If you stop and restart those containers, your data will still be there. Upon running this command again, the initial setup is skipped.

```bash
invenio-cli services setup
```
```console
Making sure containers are up...
Creating network "my-site_default" with the default driver
Creating my-site_cache_1 ... done
Creating my-site_es_1    ... done
Creating my-site_db_1    ... done
Creating my-site_mq_1    ... done
Creating database postgresql+psycopg2://my-site:my-site@localhost/my-site
Creating all tables!
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
Created all tables!
Location default-location /your/path/to/var/instance/data as default True created
Role "admin" created successfully.
Creating indexes...
Putting templates...
```

!!! tip

    You can skip the creation of demo records by using the ``--no-demo-data`` option (``-N`` for short):

    ```shell
    invenio-cli services setup --no-demo-data
    ```

    You can forcefully redo the setup step with the ``--force`` option (``-f`` for short):

    ```shell
    invenio-cli services setup --force
    ```

### Run

You can now run the application locally:

```bash
invenio-cli run
```

Go and explore your InvenioRDM instance at [https://127.0.0.1:5000](https://127.0.0.1:5000). This is the default host and port configured in ``invenio.cfg``.


!!! tip "Change the host and port"
    By default, the host is `127.0.0.1` and the port is `5000`. Pass `--host` and `--port`
    to change them:

      `invenio-cli run --host 0.0.0.0 --port 443`

    It's a development server though, so don't use it for production.

!!! warning "Visit 127.0.0.1, not localhost"
    Due to Content Security Policy (CSP) headers it is important that you use ``127.0.0.1``, and not ``localhost``.

## Option 2: Containerized preview

The container install is good for a quick preview, or if you don't want all dependencies locally. It is not good for development or for customizing your instance, as it requires you to rebuild the Docker image for every change which can be time consuming.

### Build

For the container build, you first build the Docker application image using
the following command:

```bash
invenio-cli containers build
```
```console
Building images... Pull newer versions True, use cache True
Checking if dependencies are locked.
Dependencies are locked
Building images...

[...]

Successfully built f1fc95ce1037
Successfully tagged my-site:latest
Images built successfully.
```

The command will:

- Download the Docker images for the services (database, cache, search engine, etc.)
- Build the Docker image for the InvenioRDM application using the ``Dockerfile`` in your project.
- Install Python dependencies (according to the lock file)
- Install JavaScript dependencies
- Build the JavaScript/CSS web assets

### Setup

Once the Docker application image has been built, we need to initialize the database, the indices and so on. For this, we use again the ``containers`` command.

The first time this command is run, the services will be setup correctly and the containers running them will even restart upon a reboot of your machine. If you stop and restart those containers, your data will still be there. Upon running this command again, the initial setup is skipped.

```bash
invenio-cli containers setup
```
```console
Making sure containers are up...
Creating network "my-site_default" with the default driver
Creating my-site_cache_1 ... done
Creating my-site_es_1    ... done
Creating my-site_db_1    ... done
Creating my-site_mq_1    ... done
Creating database postgresql+psycopg2://my-site:my-site@localhost/my-site
Creating all tables!
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
Created all tables!
Location default-location /your/path/to/var/instance/data as default True created
Role "admin" created successfully.
Creating indexes...
Putting templates...
```

The command will:

- Create the database and Elasticsearch indexes.
- Load fixtures data into InvenioRDM.
- Create demo records.

!!! tip

    You can skip the creation of demo records by using the ``--no-demo-data`` option (``-N`` for short):

    ```shell
    invenio-cli containers setup --no-demo-data
    ```

    You can forcefully redo the setup step with the ``--force`` option (``-f`` for short):

    ```shell
    invenio-cli containers setup --force
    ```

### Run

You can now run the application container and related services:

```bash
invenio-cli containers start
```

Go and explore your InvenioRDM instance at [https://127.0.0.1](https://127.0.0.1).

!!! tip
    You can provide other configuration variables by setting them as environment variables with the ``INVENIO_`` prefix.

!!! warning "Visit 127.0.0.1, not localhost"
    Due to Content Security Policy (CSP) headers it is important that you visit ``127.0.0.1``, and not ``localhost`` unless you set ``INVENIO_SITE_UI_URL`` and ``INVENIO_SITE_API_URL`` to ``https://localhost`` and ``https://localhost/api`` respectively.

## Troubleshooting

- You may see the following error message `TypeError: Object.fromEntries is not a function`.
  This means you need to update your base Invenio docker image because Node.js 14+ is needed. Make sure the base Invenio image is up to date. You can re-build your instance image with `invenio-cli containers build --pull --no-cache` to make sure things are done from scratch.

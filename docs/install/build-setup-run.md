# Build, setup and run

Now, that we have created a project folder, we need to build and set up the InvenioRDM application.

The application can be built and installed in two different ways:

- Local (good for developers or for customizing your instance): The application is installed locally on your machine in a Python virtual environment managed by the ``pipenv`` tool.
- Container (good for quick preview): The application is built inside a Docker image.

## For the impatient

For the impatient, here are the commands to build, setup and run InvenioRDM. For clarity, we have decomposed them into individual steps in the guide below. Follow the guide below for step-by-step details:

Container:

```bash
invenio-cli containers start --lock --build --setup
```

Local:

```bash
invenio-cli install
invenio-cli services setup
invenio-cli run
```

!!! info
    If you run the above commands, you're all set for this section. If you like to learn more about the build process,
    then follow the steps below instead.


## Python dependencies

First, we start by locking the Python dependencies, which ensures that you will always have the same versions of dependencies if you reinstall in the future. Locked dependencies are important for having reproducible installs.

This step will normally be executed automatically by both the local and container installation options, but here we run it explicitly.

Let's try it:

```bash
cd my-site/
invenio-cli packages lock
```
```console
Locking dependencies... Allow pre-releases: False. Include dev-packages: False.
Locking python dependencies...
Creating a virtualenv for this project…
Pipfile: /Users/johnsmith/src/tmp/my-site/Pipfile
Using /Users/johnsmith/.virtualenvs/cli/bin/python3.8 (3.8.5) to create virtualenv…
⠇ Creating virtual environment...created virtual environment CPython3.8.5.final.0-64 in 542ms
  creator CPython3Posix(dest=/Users/johnsmith/.virtualenvs/my-site-0wtHqD1g, clear=False, global=False)
  seeder FromAppData(download=False, pip=bundle, setuptools=bundle, wheel=bundle, via=copy, app_data_dir=/Users/johnsmith/Library/Application Support/virtualenv)
    added seed packages: pip==21.0.1, setuptools==53.1.0, wheel==0.36.2
  activators BashActivator,CShellActivator,FishActivator,PowerShellActivator,PythonActivator,XonshActivator

✔ Successfully created virtual environment!
Virtualenv location: /Users/johnsmith/.virtualenvs/my-site-0wtHqD1g
Locking [dev-packages] dependencies…
Building requirements...
Resolving dependencies...
✔ Success!
Locking [packages] dependencies…
Building requirements...
Resolving dependencies...
✔ Success!
Updated Pipfile.lock (271a6d)!
Dependencies locked successfully.
```

A new file ``Pipfile.lock`` has now been created with the locked dependencies.

Next, choose option 1 or option 2 for your preferred installation method.

## Option 1: Container install

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
- Install Python dependencies (according the ``Pipfile.lock``)
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

    ```
    invenio-cli containers setup --no-demo-data
    ```

### Run

You can now run the application container and related services:

```bash
invenio-cli containers start
```

Go and explore your InvenioRDM instance at [https://127.0.0.1](https://127.0.0.1).

!!! warning "Visit 127.0.0.1, not localhost"
    Due to Content Security Policy (CSP) headers it is important that you visit ``127.0.0.1``, and not ``localhost`` unless you set ``INVENIO_SITE_UI_URL`` and ``INVENIO_SITE_API_URL`` to ``https://localhost`` and ``https://localhost/api`` respectively.

!!! tip
    You can provide other configuration variables by setting them as environment variables with the ``INVENIO_`` prefix.

## Option 2: Local install

The local install is good for developers or if you like to customize InvenioRDM as it avoids the waiting time for building a new Docker image. For instance, changing the layout will be much faster with a local install.

### Build

The local build steps involve installing all the Python dependencies into a local Python virtual environment. This is done with the command (the virtualenv is managed by ``pipenv``):

```bash
invenio-cli install
```
```console
Installing python dependencies... Please be patient, this operation might take some time...
Installing dependencies from Pipfile.lock (271a6d)…
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 200/200 — 00:02:00

[...]

Built webpack project.
Assets and statics updated.
Dependencies installed successfully.
```

Similar to the ``containers`` command, the command does the following:

- Install Python dependencies (according the ``Pipfile.lock``)
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

    ```
    invenio-cli services setup --no-demo-data
    ```


### Run

You can now run the application locally:

```bash
invenio-cli run
```

Go and explore your InvenioRDM instance at [https://127.0.0.1:5000](https://127.0.0.1:5000). This is the default host and port configured in ``invenio.cfg``.

!!! warning "Visit 127.0.0.1, not localhost"
    Due to Content Security Policy (CSP) headers it is important that you use ``127.0.0.1``, and not ``localhost``.

!!! tip "Change the host and port"
    By default, the host is `127.0.0.1` and the port is `5000`. Pass `--host` and `--port`
    to change them e.g.:

      `invenio-cli run --host 0.0.0.0 --port 443`

    It's a development server, so don't use it for production.

## Troubleshooting

- You may see the following error message `TypeError: Object.fromEntries is not a function`.
  This means you need to update your base Invenio docker image because Node.js 14+ is needed. Make sure the base Invenio image is up to date. You can re-build your instance image with `invenio-cli containers build --pull --no-cache` to make sure things are done from scratch.
- You may see `SystemError: Parent module 'setuptools' not loaded, cannot perform relative import`
  at the dependency locking step when running `invenio-cli containers start`. This depends on your version of `setuptools` (bleeding edge causes this)
  and can be solved by setting an environment variable: `SETUPTOOLS_USE_DISTUTILS=stdlib`. [See more details](https://github.com/pypa/setuptools/blob/17cb9d6bf249cefe653d3bdb712582409035a7db/CHANGES.rst#v5000). This sudden upstream change will be addressed more systematically in future releases.
- You may see the following error message  ``pkg_resources.ContextualVersionConflict: (setuptools 60.5.0 (...), Requirement.parse('setuptools<59.7.0,>=59.1.1'), {'celery'})`` when running ``invenio-cli install``. This happens when you recently installed or upgraded ``invenio-cli``. The problem can be fixed by adding ``setuptools = ">=59.1.1,<59.7.0"`` to the ``[dev-packages]`` section in your ``Pipfile``. The problem happens when virtualenv v20.13.1+ gets installed with Invenio-CLI and when Celery v5.2.3 gets is installed with InvenioRDM. Only Celery v5.2.3 causes this issue.

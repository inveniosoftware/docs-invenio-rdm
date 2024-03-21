# CLI reference

**Summary**

The following document is a reference guide to the commands provided by the
Invenio-CLI tool.

**Intended audience**

This guide is intended for system administrators and developers of InvenioRDM.

## Overview

Following is an overview of the root-level commands in Invenio-CLI:

| Command              | Description                                                                                   | Supported |
| :------------------- | :-------------------------------------------------------------------------------------------- | :-------: |
| `assets`             | Statics and assets management commands.                                                       |  v0.19.0  |
| `check-requirements` | Checks the system fulfills the pre-requirements.                                              |  v0.19.0  |
| `containers`         | Containers management commands.                                                               |  v0.19.0  |
| `destroy`            | Removes all associated resources (containers, images, virtual environment, etc.)              |  v0.19.0  |
| `init`               | Initializes the application according to the chosen flavour (Currently only RDM is available) |  v0.19.0  |
| `install`            | Installs the project locally.                                                                 |  v0.19.0  |
| `packages`           | Commands for package management.                                                              |  v0.19.0  |
| `pyshell`            | Python shell command.                                                                         |  v0.19.0  |
| `run`                | Starts the local development server.                                                          |  v0.19.0  |
| `services`           | Commands for services management.                                                             |  v0.19.0  |
| `shell`              | Shell command.                                                                                |  v0.19.0  |
| `translations`       | Extracts, initializes and compile message catalogs (i18n)                                     |  v1.0.12  |
| `upgrade`            | Upgrades the current application to the specified InvenioRDM version                          |     -     |

### Shell completion

Invenio-CLI provides support for tab completion of commands and options for Bash, Zsh and Fish shells. You can install the shell completion

For Bash, add this to `~/.bashrc`:

    eval "$(_INVENIO_CLI_COMPLETE=source_bash invenio-cli)"

For Zsh, add this to `~/.zshrc`:

    eval "$(_INVENIO_CLI_COMPLETE=source_zsh invenio-cli)"

For Fish, add this to `~/.config/fish/completions/invenio-cli.fish`:

    eval (env _INVENIO_CLI_COMPLETE=source_fish invenio-cli)

The above `eval` commands will invoke your application every time a shell is started.
This may slow down shell startup time.

Alternatively, create an activation script:

For Bash:

    _INVENIO_CLI_COMPLETE=source_bash invenio-cli > invenio-cli-complete.sh

For Zsh:

    _INVENIO_CLI_COMPLETE=source_zsh invenio-cli > invenio-cli-complete.sh

In `.bashrc` or `.zshrc`, source the script instead of the `eval` command:

    . /path/to/invenio-cli-complete.sh

For Fish, add the file to the completions directory:

    _INVENIO_CLI_COMPLETE=source_fish invenio-cli > ~/.config/fish/completions/invenio-cli-complete.fish

## General commands

### **`check-requirements`**

Checks the minimal system requirements are met.

**Options**

- `-d`, `--development` Check also development requirements (defaults to not checking development requirements).

### **`destroy`**

Removes all associated resources (containers, images, volumes, Python virtual environment).

All data in services are lost.

### **`init`**

Initializes the application skeleton for the chosen flavour. Currently only `rdm` flavour is supported and it is the default value.

**Options**

- `-t`, `--template` `TEXT` Path or git URL to the Cookiecutter template.
- `-c`, `--checkout` `TEXT` Branch, tag or commit to checkout if `--template` is a git URL.
- `--config .invenio`, Auto pre-filling of initialization questions from the .invenio file. Refer to `.invenio` for file structure within your instance for more info.

### **`install`**

Installs the project locally.

Installs Python dependencies, creates an instance directory, symlinks the `invenio.cfg`, templates, static files, assets, and finally builds front-end assets.

A python virtual environment is created if it does not already exist.

**Options**

- `--pre` If specified, allows the installation of alpha releases
- `-p`, `--production` / `-d`, `--development` Production mode copies statics/assets. Development mode symlinks statics/assets (default).

### `run`

Starts the local development server.

**Options**

- `-h`, `--host` TEXT The interface to bind to.
- `-p`, `--port` INTEGER The port to bind to.
- `-d`, `--debug` / `--no-debug` Debug mode enables Flask development mode, auto-reloading and more (default: enabled).
- `-s`, `--services` / `-n`, `--no-services` Run dockerized services along with the instance or not.

## Assets commands

Statics files and assets management commands.

| Command        | Description                                        | Supported |
| :------------- | :------------------------------------------------- | :-------: |
| `install`      | Install and link a React module.                   |  v0.19.0  |
| `build`        | Build the current application static/assets files. |  v0.19.0  |
| `watch`        | Statics and assets watch commands.                 |  v0.19.0  |
| `watch-module` | Watch a JavaScript/React module.                   |  v0.19.0  |

### **`assets install`**

Install and link the JavaScript/React package specified by the path. For example:

```bash
invenio-cli assets install ~/src/react-invenio-awesome/
```

### **`assets build`**

Build the current application's static/assets files.

The default behavior of the command is to:

- Remove any existing
  1. Static files
  2. Webpack project
  3. Installed Node modules
  - Collect
    1. Static files
    2. Assets for the Webpack project
    3. InvenioRDM's instance statics and assets.
- Install all Node modules specified by the Webpack project's `package.json`.
- Build the Webpack project.

The command by default symlinks the static files and assets. This enables you to
run the `watch`. If you build with `--production`, no symlinks are created,
and the `watch` will not detect changes to your local development files.

**Options**

- `-n`, `--no-wipe` Do not remove existing assets.
- `-p`, `--production` / `-d`, `--development` Production mode copies files. Development mode creates symbolic links, this allows to have real-time changes of the files. Defaults to `--development`.

### **`assets watch`**

Watches InvenioRDM's Webpack project for changes, and automatically rebuild the project if a file is changed.

This command is useful for instance if you're editing the LESS or JavaScript files in your InvenioRDM instance.

Note, if you run `assets build` with the `--production` option, then your local development files are not symlinked, and the
`assets watch` command will not detect edits of your local development files.

### **`assets watch-module`**

Watch a JavaScript/React package for changes, and automatically rebuild the package.

This command is useful if you are developing a React package (e.g. React-Searchkit).

Before watching a React package, it must be installed and linked. This can be done with the `assets install` command. If the package is not already installed and linked you can use the `-l`/`--link` option.

**Options**

- `-l`/`--link` Install and link the JavaScript/React package before watching for changes.

!!! info
The command `assets watch-module` only rebuilds the JavaScript/React package into InvenioRDM's Webpack project. However, before you can
see the changes, you must also rebuild InvenioRDM's Webpack project. Hence, you normally always use `assets watch-module` and `assets watch` in together:

        invenio-cli assets watch-module --link ~/src/react-invenio-deposit
        invenio-cli assets watch

## Container commands

Containers management commands.

The container management commands intends to bring up a full infrastructure environment for **development purposes** that looks similar to your production environment.

| Command | Description                                     | Supported |
| :------ | :---------------------------------------------- | :-------: |
| build   | Build application and service images.           |  v0.19.0  |
| destroy | Destroy containerized services and application. |  v0.19.0  |
| setup   | Setup containerized services.                   |  v0.19.0  |
| start   | Start containerized services and application.   |  v0.19.0  |
| status  | Checks if the services are up and running.      |  v0.19.0  |
| stop    | Stop containerized services and application.    |  v0.19.0  |

The container management commands uses Docker-Compose behind the scenes, and
specifically relies on the `docker-compose.full.yml` file.

### **`containers build`**

Build the application and service images.

**Options**

- `--pull` / `--no-pull` Download newer versions of the image. Defaults to pull.
- `--cache` / `--no-cache` Use or do not use the cache when building images. Defaults to using the cache.

### **`containers destroy`**

Destroy the containerized services and application.

### **`containers setup`**

Setup containerized services.

By default this command will build and boot all the containerized services (see `--stop-services` and `--no-services` options below to control this behaviour).

This command:

- Initialize and create the database, Elasticsearch indexes, cache and message queue.
- Create an admin role.
- Create a default location for files.

!!! warning "Error (psycopg2.OperationalError) FATAL: role "xxx" does not exist"

    To avoid misleading error messages like this, make sure Postgres is not installed locally (and using port 5432) when setting up the database container.

**Options**

- `-f`, `--force` Force recreation of database tables, Elasticsearch indexes and queues.
- `-n`, `--no-demo-data` Disable the creation of demo data.
- `--stop-services` Stop containers after setup.
- `-s`, `--services` / `-n`, `--no-services` Boot up or not the containerized services. Defaults to boot them up.

### **`containers start`**

Start the containerized services and application.

**Options**

- `--lock` / `--skip-lock` Lock Python dependencies (defaults to `--skip-lock`).
- `--build` / `--no-build` Build images (defaults to `--no-build`).
- `--setup` / `--no-setup` Setup services (defaults to `--no-setup`).
- `--demo-data` / `--no-demo-data` Create demo records if `--setup` is specified. (default=True).
- `-s`, `--services` / `-n`, `--no-services` Boot up or not the containerized services. Defaults to booting them up.

This command is intended to only start the containers needed to run a full containerised instance, for example:

```bash
invenio-cli containers start
```

However, for demo/preview purposes it allows to perform a full build and setup. For instance, if you have a freshly initialized instance you can build and boot it with:

```bash
invenio-cli containers start --lock --build --setup
```

Note, that `--lock` is done locally on your machine, and not inside the containers.

### **`containers status`**

Checks if the services are up and running.

!!! info "Supported services"
currently only ES, DB (postgresql/mysql) and redis are supported.

**Options**

- `-v`, `--verbose` Verbose mode will show all logs in the console.

### **`containers stop`**

Stop containerized services and application.

## Packages commands

Commands for Python package management.

| Command  | Description                                                        | Supported |
| :------- | :----------------------------------------------------------------- | :-------: |
| install  | Install one or a list of Python packages in the local environment. |  v0.19.0  |
| lock     | Lock Python dependencies.                                          |  v0.19.0  |
| outdated | Show outdated Python dependencies.                                 |     -     |
| update   | Update a single Python python package.                             |     -     |

### **`packages install`**

Install one or more Python packages as editable packages in the local Python virtual environment.

The primary intended purpose of this command is for developers to install a development version of an Invenio module they are working on.

!!! warning "Don't skip assets rebuild"

    The command by default rebuilds the assets afterwards (same as running ``assets build``). If you skip rebuilding the assets, you will likely have outdated files in InvenioRDM's Webpack project, and you are very likely going to have problems.

**Options**

- `-s`, `--skip-build` Do not rebuild the assets.

### **`packages lock`**

Lock Python dependencies.

This creates a `Pipfile.lock` in your instance with hashes and versions of all
Python packages. This ensures you have reproducible builds, and that you don't risk
having new patch-level versions of third-party Python packages break your build.

**Options**

- `--pre` Allows the installation of alpha releases.
- `--dev` Include development devepencies.

### **`packages outdated`**

!!! error "Not yet supported"

### **`packages update`**

!!! error "Not yet supported"

## Services commands

Commands for services management.

The services management commands intends to bring up a minimal infrastructure environment for **development purposes**.

| Command | Description                                | Supported |
| :------ | :----------------------------------------- | :-------: |
| destroy | Destroy development services.              |  v0.19.0  |
| setup   | Setup local services.                      |  v0.19.0  |
| start   | Start local services.                      |  v0.19.0  |
| status  | Checks if the services are up and running. |  v0.19.0  |
| stop    | Stop local services.                       |  v0.19.0  |

The services management commands uses Docker-Compose behind the scenes, and specifically relies on the `docker-compose.yml` file. The `containers` commands instead relies on the `docker-compose.full.yml` file.

### **`services destroy`**

Destroy development services and any data in them.

### **`services setup`**

Setup containerized services.

By default this command will build and boot all the containerized services (see `--stop-services` and `--no-services` options below to control this behaviour).

**Options**

- `-f`, `--force` Force recreation of database tables, Elasticsearch indices and queues.
- `-n`, `--no-demo-data` Disable the creation of demo data.
- `--stop-services` Stop containers after setup.
- `-s`, `--services` / `-n`, `--no-services` Boot up or not the containerized services. Defaults to boot them up.

### **`services start`**

Start the containerized services.

### **`services status`**

Checks if the services are up and running.

!!! info "Supported services"
Currently only Elasticsearch, databases (PostgreSQL/MySQL) and Redis are supported.

**Options**

- `-v`, `--verbose` Verbose mode will show all logs in the console.

### **`services stop`**

Stop containerized services.

The command does not destroy any data in the services.

## Shell commands

### **`shell`**

Starts a new shell (bash/zsh/...) and activates the Python virtual environment.

### **`pyshell`**

Starts an interactive Python interpreter with the InvenioRDM application loaded.

**Options**

`-d`, `--debug` / `--no-debug` Debug mode enables Flask development mode (default: disabled).

## Translations commands

Translations (i18n) message catalogs management.

| Command        | Description                          | Supported |
| :------------- | :----------------------------------- | :-------: |
| `extract`      | Extract strings from code and config |  v1.0.12  |
| `init`         | Initialize a specific locale catalog |  v1.0.12  |
| `update`       | Update message catalogs              |  v1.0.12  |
| `compile`      | Compile message catalogs             |  v1.0.12  |

### **`translations extract`**

Extract strings from code (generate `.pot` files).

**Options**

- `-b`, `--babel-ini` Relative path to babel.ini (including filename).


### **`translations init`**

Initialize a specific locale catalog (generate `.po` files).

**Options**

-  `-l`, `--locale` Locale to initialize.

### **`translations update`**

Update message catalogs.

### **`translations compile`**

Compile message catalogs (generate `.mo` files).

**Options**

-  `-f`, `--fuzzy` Allow fuzzy translations (not revised).

## Upgrade command

### **`upgrade`**

!!! error "Not yet supported"

## Invenio RDM commands

### **`rdm`**

Invenio app rdm commands.

### **`rdm pages`**

see [Static pages](../customize/static_pages.md).

### **`rdm pages create`**

**Options**

- `-f`, `--force` Creates static pages.

### **`rdm fixtures`**

Create the fixtures.

### **`rdm rebuild-all-indices`**

Reindex all services with optional selecting and ordering.

**Options**

- `-o`, `--order` Comma-separated list of services to reindex in the specified order. If not provided, all services will be reindexed.
e.g.:

```bash
invenio rdm rebuild-all-indices -o users,communities,records,requests,request_events
```

if you don't specify services, The following services will be reindexed:

`users, groups, domains, communities, members, records, record-media-files, affiliations, awards, funders, names, subjects, vocabularies, requests, request_events, oaipmh-server`

Note that the users, groups, and members use bulk indexing and rely on celery running. They will not be reindexed if celery is not running.

This command does not impact usage statistics indexes. You need to manually restore statistics indexes [from a backup](../develop/howtos/backup_search_indices.md).

# InvenioCLI reference

## Main commands

| Command | Description | Supported |
|:--------|:------------|:---------:|
| assets  | Statics and assets management commands. | v0.19.0 |
| check-requirements | Checks the system fulfills the pre-requirements. | v0.19.0 |
| containers         | Containers management commands. | v0.19.0 |
| destroy            | Removes all associated resources (containers, images, virtual environment, etc.) | v0.19.0 |
| init               | Initializes the application according to the chosen flavour (Currently only RDM is available) | v0.19.0 |
| install            | Installs the project locally. | v0.19.0 |
| packages           | Commands for package management. | v0.19.0 |
| pyshell            | Python shell command. | v0.19.0 |
| run                | Starts the local development server. | v0.19.0 |
| services           | Commands for services management. | v0.19.0 |
| shell              | Shell command. | v0.19.0 |
| upgrade            | Upgrades the current application to the specified specified InvenioRDM version | - |

### Assets command

Statics and assets management commands.

| Command | Description | Supported |
|:--------|:------------|:---------:|
| install | Install and link a React module. | v0.19.0 |
| build   | Build the current application static/assets files. | v0.19.0 |
| watch   | Statics and assets watch commands. | v0.19.0 |

#### Install

Install and link the React module specified by the path. For example:

```bash
invenio-cli assets install ../my-react-module/
```

#### Build

Build the current application static/assets files.

**Options**
- `-n`, `--no-wipe` Force the full recreation the assets and statics. Removes existint assets and static files. By default assets will be removed.
- `-p`, `--production` / `-d`, `--development` Production mode copies files. Development mode creates symbolic links, this allows to have real-time changes of the files. Defaults to development.

#### Watch

Statics and assets watch commands.

| Command | Description | Supported |
|:--------|:------------|:---------:|
| assets |  Watch assets files for changes and rebuild | v0.19.0 |
| module  | Watch a React module. | v0.19.0 |

Use `assets` to watch changes on python modules' files. To avoid redundancy this is the default of `watch`. The two commands below are equivalent:

```bash
invenio-cli assets watch
invenio-cli assets watch assets
```

Use `module` to watch changes on a React module. Before watching a React module, it should be linked. This can be done with the `assets install` command mentioned above. Nonetheless, if already installed it can be linked using the `-l`/`--link` option. For example:

```bash
invenio-cli assets watch module /path/toreact-invenio-desposit
invenio-cli assets watch module --link /path/toreact-invenio-desposit
```

### Check requirements command

Checks the system fulfills the pre-requirements.

**Options**

- `-d`, `--development` Check development requirements.

### Containers command

Containers management commands.

| Command | Description | Supported |
|:--------|:------------|:---------:|
| build   | Build application and service images. | v0.19.0 |
| destroy | Destroy containerized services and application. | v0.19.0 |
| setup   | Setup containerized services. | v0.19.0 |
| start   | Start containerized services and application. | v0.19.0 |
| status   | Checks if the services are up and running. | v0.19.0 |
| stop    | Stop containerized services and application. | v0.19.0 |

#### Build

Build application and service images.

**Options**
- `--pull` / `--no-pull` Download newer versions of the images/ Defaults to pull.
- `--cache` / `--no-cache` Use or not use the cache when building images. Defaults to cache (use).

#### Destroy

Destroy containerized services and application.

#### Setup

Setup containerized services. If `--no-services` is not specified this command will boot up the dockerized services and will not stop them afterwards unless `--stop-services` is specified.

**Options**

- `-f`, `--force` Force recreation of db tables, ES indices, queues, etc.
- `-n`, `--no-demo-data` Disable the creation of demo data.
- `--stop-services` Stop containers after setup.
- `-s`, `--services` / `-n`, `--no-services` Boot up or not the dockerized services. Defaults to boot them up.

#### Start

Start containerized services and application.

**Options**

- `--lock` / `--skip-lock` Lock Python dependencies (default=False).
- `--build` / `--no-build` Build images (default=False).
- `--setup` / `--no-setup` Setup services (default=False). It will run with force=True.
- `--demo-data` / `--no-demo-data` Include demo records (default=True), requires --setup.
- `-s`, `--services` / `-n`, `--no-services` Boot up or not the dockerized services. Defaults to boot them up.

This command is intended to only start the containers needed to run a full dockerize instance, for example:

```bash
invenio-cli containers start
```

However, for demo/preview purposes it allows to perform the other commands as well. Note that the taken steps are exacly the same (e.g. adding `--setup` is equivalent to `invenio-cli containers setup --force`).

#### Status

Checks if the services are up and running.

!!! info "Supported services"
    currently only ES, DB (postgresql/mysql) and redis are supported.

**Options**

- `-v`, `--verbose` Verbose mode will show all logs in the console.


#### Stop

Stop containerized services and application.

### Destroy command

Removes all associated resources (containers, images, volumes).

### Init command

Initializes the application according to the chosen flavour. Currently only `RDM` flavour is supported and it is the default value.

**Options**

- `-t`, `--template` TEXT  Cookiecutter path or git url to template
- `-c`, `--checkout` TEXT  Branch, tag or commit to checkout if `--template` is a git url

### Install command

Installs the  project locally.

Installs dependencies, creates instance directory, links invenio.cfg + templates, copies images and other statics and finally builds front-end assets.

**Options**
- `--pre` If specified, allows the installation of alpha releases
- `-p`, `--production` / `-d`, `--development` Production mode (default) copies statics/assets. Development mode symlinks statics/assets.

### Packages command

Commands for package management.

| Command | Description | Supported |
|:--------|:------------|:---------:|
| install   | Install one or a list of Python packages in the local environment. | v0.19.0 |
| lock | Lock Python dependencies. | v0.19.0 |
| outdated   | Show outdated Python dependencies. | - |
| update   | Update a single Python python package. | - |

#### Install

Install one or a list of Python packages in the local environment.

**Options**

- `-s`, `--skip-build`  Do not rebuild the assets.

#### Lock

Lock Python dependencies.

**Options**

- `--pre` Allows the installation of alpha releases.
- `--dev` Include development devepencies.

#### Outdated

!!! error "Not supported yet"

#### Update

!!! error "Not supported yet"

### Pyshell command

Python shell command.

**Options**
`-d`, `--debug` / `--no-debug` Debug mode enables Flask development mode (default: disabled).

### Run command

Starts the local development server.

**Options**

- `-h`, `--host` TEXT The interface to bind to.
- `-p`, `--port` INTEGER The port to bind to.
- `-d`, `--debug` / `--no-debug` Debug mode enables Flask development mode, auto-reloading and more (default: enabled).
- `-s`, `--services` / `-n`, `--no-services` Run dockerized services along with the instance or not.

### Services command

Commands for services management.

| Command | Description | Supported |
|:--------|:------------|:---------:|
| destroy   | Destroy developement services. | v0.19.0 |
| setup | Setup local services. | v0.19.0 |
| start   | Start local services. | v0.19.0 |
| status | Checks if the services are up and running. | v0.19.0 |
| stop   | Stop local services. | v0.19.0 |

#### Destroy

Destroy developement services.

#### Setup

Setup containerized services. If `--no-services` is not specified this command will boot up the dockerized services and will not stop them afterwards unless `--stop-services` is specified.

**Options**

- `-f`, `--force` Force recreation of db tables, ES indices, queues, etc.
- `-n`, `--no-demo-data` Disable the creation of demo data.
- `--stop-services` Stop containers after setup.
- `-s`, `--services` / `-n`, `--no-services` Boot up or not the dockerized services. Defaults to boot them up.

#### Start

Start local dockerized services.

#### Status

Checks if the services are up and running.

!!! "Supported services"
    currently only ES, DB (postgresql/mysql) and redis are supported.

**Options**

- `-v`, `--verbose` Verbose mode will show all logs in the console.

#### Stop

Stop local dockerized services.

### Shell command

Creates a new shell using Pipenv, which means that it will activate a new virtual environment.

### Upgrade command

!!! error "Not supported yet"

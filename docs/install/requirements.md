# System requirements

### Tools

InvenioRDM depends on the following requirements to be installed on your local system:

- MacOS or Linux-based systems (Windows systems is not supported).
- [Python](https://www.python.org/) 3.7, 3.8 or 3.9 and [pip](https://pip.pypa.io/en/stable/)
    - Python development headers:
        - On Ubuntu: `sudo apt install python3-dev`.
        - On RHEL/Fedora: `yum install -y python3-devel.x86_64`.
    - MacOS 11 Big Sur introduces some changes that might break the installation of some packages (for example `PostgreSQL` binaries). If this happens, make sure that you prepend the installation command with `SYSTEM_VERSION_COMPAT=1` ([more information](https://github.com/psycopg/psycopg2/issues/1200)):

        ```
        SYSTEM_VERSION_COMPAT=1 invenio-cli install
        ```

    - In case that `invenio-cli` (and other commands installed via `pip`) cannot be found after installing, you may have to update your `$PATH` to include the install directory (e.g. `PATH="$PATH:$HOME/.local/bin"` on Linux).

- [Docker](https://docs.docker.com/) 1.13.0+
- [Docker-Compose](https://docs.docker.com/compose/) 1.17.0+

For running and building the application locally you will also need:

- [Git](https://git-scm.com/).
- [Node.js](https://nodejs.org) 14.0.0+ (needed for local installation). We recommend that you install node through [nvm](https://github.com/nvm-sh/nvm) (e.g. `nvm install --lts --default 14`).
- [npm](https://www.npmjs.com/get-npm) < 7.
- [Cairo](https://invenio-formatter.readthedocs.io/en/latest/installation.html) needed for badges to be properly displayed.
- [DejaVu Fonts](https://dejavu-fonts.github.io/Download.html) needed for badges rendering.
- [ImageMagick](https://imagemagick.org/script/download.php) needed for IIIF file rendering.

!!! warning "Supported Python distributions"
    InvenioRDM targets CPython 3.7, 3.8, and 3.9. Anaconda Python in particular is not currently supported and other Python distributions are not tested.

### Services

InvenioRDM depends on the following services. During the installation we start these services in containers, but you could as well use externally hosted services for them:

- Databases: PostgreSQL 10+
- Elasticsearch: v7.0 - v7.10 (due to the license change introduced in v7.11).
- Cache: Redis, memcached
- Message broker: RabbitMQ, Redis
- Storage systems: Network storage, S3, XRootD, and more

!!! note "Elasticsearch vs OpenSearch"

    InvenioRDM will be transitioning from Elasticsearch to OpenSearch due to license changes in Elasticsearch which means it is no longer an open source product. We are currently assessing if it is feasible from a technical and resource perspective to support both products.

### Hardware

We usually run InvenioRDM on machines that have at least 8GB of RAM and at least 4 cores.

### Python virtual environments

Because we want to avoid cluttering the Python packages of the system or user with InvenioRDM dependencies, `invenio-cli` uses virtual environments.
This is done by interacting with `pipenv` behind the scenes, which is listed as a requirement and can simply be installed via `pip`.
To enable the use of a different Python version in the virtual environment than the one installed globally, a Python version manager such as `pyenv` (or `asdf` with `asdf-python`) is required.

For simplicity, we recommend to go with `pyenv` here.
In some cases, it can be installed via the system's package manager (e.g. `pacman -S pyenv`).
Otherwise, you can find the installation instructions on the [project's GitHub page](https://github.com/pyenv/pyenv/#installation) or use their [automatic installer](https://github.com/pyenv/pyenv-installer) (note the required [dependencies for locally building Python](https://github.com/pyenv/pyenv/wiki#suggested-build-environment)).

### Docker

#### Permissions to run Docker (Linux)

Your user that will be executing the CLI tool MUST be able execute
the `docker` command (i.e. it is not only available for the root user):

```bash
sudo usermod --append --groups docker $USER
```

After logging out and back in (to refresh the user's group information), the `docker ps` command should work without errors.
If it still displays a permission error on `docker.sock`, we strongly recommend *against* making it world-writable as it is sometimes suggested!
Instead, you could change the group of the socket to `docker` and allow users in that group to read and write to it.

```bash
sudo chgrp docker /var/run/docker.sock

# if the group doesn't have RW access yet
sudo chmod g+rw /var/run/docker.sock
```

#### Available memory for Docker (macOS)

On the same topic, make sure that Docker itself has enough memory to run.

In Linux based systems Docker can use all available memory. In macOS,
by default, it gets 2GB of RAM which most likely won't be enough. Allocating
6-8GB to it is optimal. You can do that in `Docker --> preferences --> resources`
and adjust the `Memory` to the corresponding value. If you have a few cores
more to spare, it might be a good idea to give more than 2. Take into account
that you will run between 4 and 8 containers.

#### Elasticsearch and Docker (macOS and Linux)

Among the containers you will run is an Elasticsearch container which is quite demanding.
Per Elasticsearch's [Docker documentation](https://www.elastic.co/guide/en/elasticsearch/reference/7.9/docker.html#docker-prod-prerequisites),
you will want to apply the following kernel setting:

On Linux, add the following to ``/etc/sysctl.conf`` on your local machine (host machine):

```bash
# Maximum number of memory map areas a process (Elasticsearch) may have
vm.max_map_count=262144
```

On macOS, do the following:

```bash
screen ~/Library/Containers/com.docker.docker/Data/com.docker.driver.amd64-linux/tty
# and in the shell
sysctl -w vm.max_map_count=262144
```

#### Use same contexts (macOS and Linux)

Make sure to always use the same context when using both Docker from the terminal and Docker Desktop. For more information see
[Docker Contexts](https://docs.docker.com/engine/context/working-with-contexts/).

# System requirements

### Tools

InvenioRDM depends on the following requirements to be installed on your local system:

- macOS or Linux-based systems (Windows systems is not supported).
- [Python](https://www.python.org/) 3.6, 3.7, or 3.8
    - Python development headers:
    - On Ubuntu: `sudo apt install python3-dev`.
    - On RHEL/Fedora: `yum install -y python3-devel.x86_64`.
- [Docker](https://docs.docker.com/) 1.13.0+
- [Docker-Compose](https://docs.docker.com/compose/) 1.17.0+

For running and building the application locally your also need:

- [Node.js](https://nodejs.org) 14.0.0+ (needed for local installation). We recommend that you install node through [nvm](https://github.com/nvm-sh/nvm).
- [npm](https://www.npmjs.com/get-npm) < 7.
- [Cairo](https://invenio-formatter.readthedocs.io/en/latest/installation.html) needed for badges to be properly displayed.

!!! warning "Other Python distributions"
    InvenioRDM targets CPython 3.6, 3.7 and 3.8 (lowest 3.6.2). Anaconda Python in particular is not currently supported and other Python distributions are not tested.

### Services

InvenioRDM depends on the following services. During the installation we start these services in countainers, but you could as well use externally hosted services for them:

- Databases: PostgreSQL 9.6+, MySQL 5.6
- Elasticsearch: v6.8 - v7.10 (due to the license change in v7.11, we are currently evaluating the situation).
- Cache: Redis, memcached
- Message broker: RabbitMQ, Redis
- Storage systems: S3, XRootD, and more

### Hardware

We usually run InvenioRDM on machines that have at least 8GB of RAM and at least
4 cores.

### Docker

#### Permissions to run Docker (Linux)

Your user that will be executing the CLI tool MUST be able execute
the `docker` command (i.e. it is not only available for the root user):

```bash
sudo usermod --append --groups docker $USER
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

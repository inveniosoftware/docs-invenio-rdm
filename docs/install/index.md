# Installation

To get started with InvenioRDM, you need to install `invenio-cli`, our
command line tool for creating and updating your instance.

## Pre-Requirements

Some system requirements are needed beforehand:

- [Python](https://www.python.org/) 3.6.2+ (Docker images are available for Python 3.6, 3.7 and 3.8.
- Python development headers. On Ubuntu: `sudo apt install python3-dev`. On RHEL/Fedora: `yum install -y python3-devel.x86_64`.
  On macOS: install XCode and activate the command line utilities.
- [Node.js](https://nodejs.org) 14.0.0+ (not needed to preview, only needed to develop)
- [Docker](https://docs.docker.com/) 1.13.0+
- [Docker-Compose](https://docs.docker.com/compose/) 1.17.0+
- [Cairo](https://invenio-formatter.readthedocs.io/en/latest/installation.html) needed for badges to be properly displayed.

!!! warning "Other Python distributions"
    InvenioRDM targets CPython 3.6, 3.7 and 3.8 (lowest 3.6.2). Anaconda Python in particular is not currently supported and other Python distributions are not tested.

In addition, make sure the user that will be executing the CLI has access to
the `docker` command (i.e. it is not only available for the root user):

```bash
sudo usermod --append --groups docker $USER
```

#### Hardware and Docker requirements

We usually deploy the RDM on machines that have around 8GB of RAM and at least
4 cores.

On the same topic, make sure that Docker itself has enough memory to run.
In Linux based systems Docker can use all available memory. In OS X,
by default, it gets 2GB of RAM which most likely won't be enough. Allocating
6-8GB to it is optimal. You can do that in `Docker --> preferences --> resources`
and adjust the `Memory` to the corresponding value. If you have a few cores
more to spare, it might be a good idea to give more than 2. Take into account
that you will run between 4 and 8 containers.

Among the containers you will run is an Elasticsearch container which is quite demanding.
Per Elasticsearch's [Docker documentation](https://www.elastic.co/guide/en/elasticsearch/reference/7.9/docker.html#docker-prod-prerequisites),
you will want to apply the following kernel setting:

On Linux, add the following to ``/etc/sysctl.conf`` on your local machine (host machine):

```bash
# Maximum number of memory map areas a process (ElasticSearch) may have
vm.max_map_count=262144
```

On macOS, do the following:

```bash
screen ~/Library/Containers/com.docker.docker/Data/com.docker.driver.amd64-linux/tty
# and in the shell
sysctl -w vm.max_map_count=262144
```

## Install the CLI

Once you have installed these requirements, you can install the Invenio CLI package,
aptly named `invenio-cli`. The package is available on [PyPI](https://pypi.org/project/invenio-cli/).
Use your favorite way to install a Python package:

Via pip:

``` bash
pip install invenio-cli
```

Via pipenv:

``` bash
pipenv install invenio-cli
```

Via pipx:

``` bash
pipx install invenio-cli
```

To make sure you've installed successfully:

``` bash
invenio-cli --version
```
``` console
invenio-cli, version 0.x.0
```

!!! note "CLI version"
     The CLI is in pre 1.0 release. The latest released version is listed on [GitHub](https://github.com/inveniosoftware/invenio-cli/releases) and available via [PyPi](https://pypi.org/project/invenio-cli/)

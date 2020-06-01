# Installation

To get started with InvenioRDM, you need to install `invenio-cli`, our
command line tool for creating and updating your instance.

## Pre-Requirements

Some system requirements are needed beforehand:

- [Python](https://www.python.org/) 3.6.2+ (Python 3.7 has been tested successfully. However, there is still no docker image available and therefore is only available for development).
- [nodejs](https://nodejs.org) 13.0.0+ (not needed to preview, only needed to develop)
- [Docker](https://docs.docker.com/) 1.13.0+
- [Docker-Compose](https://docs.docker.com/compose/) 1.17.0+

!!! warning "Other Python distributions"
    InvenioRDM targets CPython 3.6 and 3.7 (lowest 3.6.2). Anaconda Python in particular is not currently supported and other Python distributions are not tested.

In addition, make sure the user that will be executing the CLI has access to
the docker command (i.e. it is not only available for the root user):

```bash
sudo usermod --append --groups docker $USER
```

!!! note "Hardware requirements"
    We usually deploy the RDM in machines that have around 8GB of RAM and at least 4 cores. InvenioRDM can certainly run (for demo purposes) with less, just take into account that you are going to be running between 4 and 8 containers (among them an Elasticsearch container, which is quite demanding).

Once you have installed these requirements, you can install the CLI.

## Install the CLI

You can install and manage your InvenioRDM instance using the Invenio CLI package,
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

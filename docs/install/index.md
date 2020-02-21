# Installation

To get started with InvenioRDM, you need to install `invenio-cli`, our
command line tool for creating and updating your instance.

## Pre-Requirements

Some system requirements are needed beforehand:

- [Python](https://www.python.org/) (3.6 only)
- [nodejs](https://nodejs.org) (8.0.0+) (not needed to preview, only needed to develop)
- [Docker](https://docs.docker.com/) (1.13.0+)
- [Docker-Compose](https://docs.docker.com/compose/) (1.17.0+)

In addition, make sure the user that will be executing the CLI has access to
the docker command (i.e. it is not only available for the root user):

```console
$ sudo usermod --append --groups docker $USER
```

Once you have installed these requirements, you can install the CLI.

## Install the CLI

You can install and manage your InvenioRDM instance using the Invenio CLI package,
aptly named `invenio-cli`. The package is available on [PyPI](https://pypi.org/project/invenio-cli/).
Use your favorite way to install a Python package:

Via pip:

``` console
$ pip install invenio-cli
```

Via pipenv:

``` console
$ pipenv install invenio-cli
```

Via pipx:

``` console
$ pipx install invenio-cli
```

To make sure you've installed successfully:

``` console
$ invenio-cli --version
invenio-cli, version 0.10.0
```

*Note: The CLI is in pre 1.0 release. The last release's version is **0.10.0**. Your version may be different than the above.*

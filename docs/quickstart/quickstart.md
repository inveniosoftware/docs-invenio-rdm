# Quickstart

## Pre-Requirements

In order to successfully use the CLI, two components are needed:

- Docker-Compose
- Docker

You can find details on how to install them HERE and HERE, respectively. In addition, make sure the user that will be executing the CLI has access to the docker command (i.e. it is not only available for the root user). For that you can see the following DOCKER documentation.

## Install the CLI

You can install and manage your InvenioRDM instance using the Invenio CLI, aptly named `invenio-cli`. The package is available on [PyPI](https://pypi.org/project/invenio-cli/) and you should install it using `pipenv` (Follow the [instructions here](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv) to install `pipenv` for your platform):

``` console
$ pipenv install --pre invenio-cli
```

*Note: The CLI is still in alpha release. This release's version is **v1.0.0a8**. Use `pipenv run pip list | grep invenio-cli` to make sure you have the right version.*

**Known Issue**: If you are installing `invenio-cli` globally (e.g., pipx), some of the commands below in `--local` mode will not be found because they are not in the same virtualenv. We are investigating how to best remedy this. However, for the purposes of this installation guide, we use the `--containers` mode which doesn't face this issue.

## Quick containerized installation

``` console
$ invenio-cli init --flavour=RDM
$ cd my-site
$ invenio-cli build --pre --containers
$ invenio-cli setup --containers
$ invenio-cli demo --containers
$ invenio-cli server --containers
$ curl -k -XGET https://localhost/api/records/ | python3 -m json.tool
```
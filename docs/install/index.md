# Installation

**Intended audience**

The guide is intended for system administrators and developers who want to try, customize or develop with InvenioRDM on their _local machine_.

**Scope**

This guide covers how to install InvenioRDM locally on your machine, how to set up and configure your system for InvenioRDM.

## Quick start

#### [1. Install CLI tool](cli.md)

Install the InvenioRDM CLI tool (see [reference](../reference/cli.md)), e.g. via [`pip`](https://pip.pypa.io/en/stable/):

```shell
pip install invenio-cli
```

#### [2. Check system requirements](requirements.md)

!!! info "Information on requirements"

    Please do read the [system requirements](requirements.md) section!
    There's important information related to supported versions.

You can check if the proper requirements are installed via `invenio-cli`:

```shell
invenio-cli check-requirements
```

#### [3. Scaffold project](scaffold.md)

Scaffold your InvenioRDM instance. Replace ``<version>`` with the version you want to install:

- LTS release (for production systems): ``v12.0``
- STS release (for feature previews): ``v11.0``

```shell
invenio-cli init rdm -c <version>
# e.g:
invenio-cli init rdm -c v12.0
```

You will be asked several questions. If in doubt, choose the default.


#### [4. Build, setup and run](build-setup-run.md)

Now that the scaffolding is complete, it is time to check the development requirements

```shell
cd my-site/
invenio-cli check-requirements --development
```


You can run the main InvenioRDM application in two modes (choose one):

- Containerized application and services (good for a quick preview).
- Local application with containerized services (good for developers or if you want to customize InvenioRDM).

**Containerized application**

```shell
invenio-cli containers start --lock --build --setup
```

**Local application**

```shell
invenio-cli install
invenio-cli services setup
invenio-cli run
```

!!! warning "Linux: Managing Docker as a non-root user & Context Errors"

    If you encounter Docker errors running `invenio-cli services setup`, see our section on [Docker pre-requisites](./requirements.md#docker).

#### [5. Explore InvenioRDM](run.md)

Go and explore your InvenioRDM instance on:

- Local: [https://127.0.0.1:5000](https://127.0.0.1:5000)
- Container: [https://127.0.0.1](https://127.0.0.1)

!!! warning "Self-signed SSL certificate"

    Your browser will display a big warning about an invalid SSL certificate. This is because InvenioRDM generates a self-signed SSL certificate when you scaffold a new instance and because InvenioRDM requires that all traffic is over a secure HTTPS connection.

    All major browsers allow you to bypass the warning (not easily though). In Chrome/Edge you have to click in the browser window and type ``thisisunsafe``.

To create a new administrator account:

Depending on whether you are in a local or containerized setup, take note of the variations immediately following before stepping through the subsequently outlined steps.

**Local application**

In a local application context, precede the `invenio` commands by `pipenv run` (e.g., `pipenv run invenio users create <EMAIL> --password <PASSWORD> --active --confirm`).

**Containerized application**
In a fully containerized context, connect to a container first e.g. the web-api container: `docker exec -it my-site-web-api-1 /bin/bash`. Then run the commands from within the container as-is.

**Steps**
The following command creates an activated and confirmed user (assuming you have email verification enabled as is the default).

```shell
invenio users create <EMAIL> --password <PASSWORD> --active --confirm
```

Then, allow the user to access the administration panel:

```shell
invenio access allow administration-access user <EMAIL>
```

#### [6. Stop it](destroy.md)

When you are done, you can stop your instance and optionally destroy the containers:

**Containerized application**

To just stop the containers:

```shell
invenio-cli containers stop
```

To destroy them:

```shell
invenio-cli containers destroy
```

**Local application**

```shell
^C [CTRL+C]
invenio-cli services stop
```

```shell
invenio-cli services destroy
```

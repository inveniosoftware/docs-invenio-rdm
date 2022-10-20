# Installation

**Intended audience**

The guide is intended for system administrators and developers who want to try, customize or develop with InvenioRDM on their _local machine_.

**Scope**

This guide covers how to install InvenioRDM locally on your machine, how to setup and configure your system for InvenioRDM.

## Quick start

#### [1. Install CLI tool](cli.md)

Install the InvenioRDM CLI tool (see [reference](../reference/cli.md)), e.g. via [`pip`](https://pip.pypa.io/en/stable/):

```console
pip install invenio-cli
```

#### [2. Check system requirements](requirements.md)

!!! info "Information on requirements"

    Please do read the [system requirements](requirements.md) section!
    There's important information related to supported versions.

You can check if the proper requirements are installed via `invenio-cli`:

```console
invenio-cli check-requirements --development
```

#### [3. Scaffold project](scaffold.md)

Scaffold your InvenioRDM instance. Replace ``<version>`` with the version you want to install:

- LTS release (for production systems): ``v9.1``
- STS release (for feature previews): ``v10.0``

```
invenio-cli init rdm -c <version>
# e.g:
invenio-cli init rdm -c v9.1
```

You will be asked several questions. If in doubt, choose the default.

#### [4. Build, setup and run](build-setup-run.md)

You can run the main InvenioRDM application in two modes (choose one):

- Containerized application and services (good for a quick preview).
- Local application with containerized services (good for developers or if you want to customize InvenioRDM).

**Containerized application**

```console
cd my-site/
invenio-cli containers start --lock --build --setup
```

**Local application**

```console
cd my-site/
invenio-cli install
invenio-cli services setup
invenio-cli run
```

#### [5. Explore InvenioRDM](run.md)

Go and explore your InvenioRDM instance on:

- Local: [https://127.0.0.1:5000](https://127.0.0.1:5000)
- Container: [https://127.0.0.1](https://127.0.0.1)

!!! warning "Self-signed SSL certificate"

    Your browser will display a big warning about an invalid SSL certificate. This is because InvenioRDM generates a self-signed SSL certificate when you scaffold a new instance and because InvenioRDM requires that all traffic is over a secure HTTPS connection.

    All major browsers allow you to bypass the warning (not easily though). In Chrome/Edge you have to click in the browser window and type ``thisisunsafe``.

#### [6. Stop it](destroy.md)

When you are done, you can stop your instance and optionally destroy the containers:

**Containerized application**

To just stop the containers:

```bash
invenio-cli containers stop
```

To destroy them:

```bash
invenio-cli containers destroy
```

**Local application**

```bash
^C [CTRL+C]
invenio-cli services stop
```

```bash
invenio-cli services destroy
```

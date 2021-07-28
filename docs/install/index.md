# Installation

**Intended audience**

The guide is intended for system administrators and developers who want to try, customize or develop with InvenioRDM on their _local machine_.

**Scope**

This guide covers how to install InvenioRDM locally on your machine, how to setup and configure your system for InvenioRDM.

Checkout the [Deploy Guide](../deployment/index.md) if you are looking for a guide on how to deploy InvenioRDM to a server infrastructure.

## Quick start

#### [1. Install CLI tool](cli.md)

Install the InvenioRDM CLI tool (see [reference](../reference/cli.md)):

```console
pip install invenio-cli
```

#### [2. Check system requirements](requirements.md)

Do read the [system requirements](requirements.md) section. There's important information related to supported versions.

```console
invenio-cli check-requirements --development
```

#### [3. Scaffold project](scaffold.md)

Scaffold your InvenioRDM instance. You will be asked several questions. If in doubt, choose the default:

```
invenio-cli init rdm
```

#### 4. [Build, setup and run](build-setup-run.md)

You can run the main InvenioRDM application in two modes (choose one):

- Containerized application and services (good for a quick preview)
- Local application with containerized services (good for developers or if want to customize InvenioRDM).

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

#### 5. Explore InvenioRDM

Go and explore your InvenioRDM instance at on:

- Local: [https://127.0.0.1:5000](https://127.0.0.1:5000)
- Container: [https://127.0.0.1](https://127.0.0.1)

!!! warning "Self-signed SSL certificate"

    Your browser will display a big warning about an invalid SSL certificate. This is because InvenioRDM generates a self-signed SSL certificate when you scaffold a new instance and because InvenioRDM requires that all traffic is over a secure HTTPS connection.

    All major browsers allow you to bypass the warning (not easily though). In Chrome/Edge you have to click in the browser window and type ``thisisunsafe``.

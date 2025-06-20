# Install

**Scope**

This guide covers how to set up an InvenioRDM instance locally on your development machine.
How to host it in a production environment is the topic of the [deployment section](../operate/ops/deploy.md).

## Overview

Getting started with a new piece of software is often challenging. Getting all the requirements in place and familiarizing oneself with the underlying technologies is a lot of work. With web applications there are multiple separate applications that need to be orchestrated together (web server, database, cache, ...) which adds to the challenge. And all this upfront effort is often expended before the software can even be assessed for appropriateness!

To help with this, InvenioRDM proposes multiple avenues to get you familiar with it in the most convenient way for you possible.

### Try out the demo site: [https://inveniordm.web.cern.ch/](https://inveniordm.web.cern.ch/)

This will give you a good sense of what InvenioRDM provides out of the box. It's the simplest way to see the software in action. You can even compare it to https://zenodo.org/ which also runs InvenioRDM. It will give you a sense for how it can be customized.

### Preview InvenioRDM via local containers

To run an InvenioRDM instance on your local machine without much of the ceremony involved in fulfilling requirements, you can try our *"preview"*, also known as *"containerized"*, installation. This "installation" containerizes the application itself and every service used by the instance (from the web server to the database) via Docker and combines them via Docker Compose in order to quickly give you a local setup to play with. It doubles as a preview of how you could setup InvenioRDM in a production environment. Note that the [deployment section](../operate/ops/deploy.md) provides more information about what to consider when that time comes. The shortcoming of this approach is that the isolation of Docker containers may prove to be cumbersome for customizations and local development.

### Install InvenioRDM locally

When you are ready to adopt InvenioRDM or want to truly customize and extend it to your needs, we recommend you follow the steps to install it locally. Often this installation is referred as the *"local development"* one. This approach will still containerize the services, but it will install the InvenioRDM application itself on your machine (in a virtual environment so most requirements will be isolated from your system). It is what most institutions go for once they need to work on their instance, and the command line tool we provide makes it straightforward to manage.

Both the *preview* and *local development* installations use the `invenio-cli` tool to get up and running. A common workflow/arrangement is to use the *local development* installation on your local machine for, well, development, and use an equivalent of the *containerized preview* set up in production.

## Quick start

Here is the most succinct outline of the steps to take to get started whether you take the *containerized preview* approach or the *local development* approach. The header of each section links to its expanded documentation. We highly recommend you take the scenic route and follow the expanded documentation as it covers common issues and their solutions, as well as variants and deeper explanations.

### [1. Install the CLI tool](cli.md)

Irrespective of *preview* or *development* installation, you will need this command line tool:

=== "pip"

    ```shell
    pip install invenio-cli
    ```

=== "uv"

    ```shell
    uv tool install invenio-cli
    ```

=== "pipx"

    ```shell
    pipx install invenio-cli
    ```

### [2. Check system requirements](requirements.md)

You can check if the proper requirements are installed via `invenio-cli`:

```shell
invenio-cli check-requirements
```

!!! info "Information on requirements"

    Please do read the [system requirements](requirements.md) section!
    There's important information related to supported versions.


### [3. Initialize the instance's directory](initialize.md)

Scaffold your InvenioRDM instance. This is the same operation for *local development* as for *containerized preview*.

=== "Latest release (default)"

    ```shell
    invenio-cli init rdm
    ```

=== "Specific version"

    ```shell
    invenio-cli init rdm -c <version>
    # e.g:
    invenio-cli init rdm -c v12.0
    # for pre-release (InvenioRDM development branch)
    invenio-cli init rdm -c master
    ```

You will be asked several questions and given default options. If in doubt, accept the default.

Once the initialization is complete, navigate into your new instance directory:

```shell
cd my-site/
```

!!! tip
    Replace `my-site/` with the directory name you chose during `invenio-cli init`.


If you're preparing for local development, you can now check all development requirements:

```shell
invenio-cli check-requirements --development
```
> See the [system requirements](requirements.md) section if you haven’t already.


### [4. Build, setup and run](build-setup-run.md)

=== "Local development"

    ```shell
    # Install Python and Javascript packages
    invenio-cli install
    # Set up containerized database, cache, OpenSearch, etc.
    invenio-cli services setup
    # Serve the application locally through a development server
    invenio-cli run
    ```

=== "Containerized preview"

    ```shell
    invenio-cli containers start --lock --build --setup
    ```

!!! warning "Linux: Managing Docker as a non-root user & Context Errors"

    If you encounter Docker errors running `invenio-cli services setup`, see our section on [Docker pre-requisites](./requirements.md#docker).

### [5. Explore InvenioRDM](explore.md)

Go and explore your InvenioRDM instance!


=== "Local development"

    Visit [https://127.0.0.1:5000](https://127.0.0.1:5000)

=== "Containerized preview"

    Visit [https://127.0.0.1](https://127.0.0.1)

!!! warning "Self-signed SSL certificate"

    Your browser will display a big warning about an invalid SSL certificate. This is because InvenioRDM generates a self-signed SSL certificate when you scaffold a new instance and because InvenioRDM requires that all traffic is over a secure HTTPS connection.

    All major browsers allow you to bypass the warning (not easily though). In Chrome/Edge you have to click in the browser window and type ``thisisunsafe``.

### [6. Stop it](stop.md)

When you are done, you can stop your instance and optionally destroy the containers:

=== "Local development"

    ```shell
    # To stop the application server:
    # in terminal running invenio-cli run
    ^C [CTRL+C]
    # ---
    # To stop the service containers:
    invenio-cli services stop
    # ---
    # To destroy the service containers
    # (this will lose ALL data):
    invenio-cli services destroy
    ```

=== "Containerized preview"


    ```shell
    # To stop all containers:
    invenio-cli containers stop
    # ---
    # To destroy all containers:
    # (this will lose ALL data):
    invenio-cli containers destroy
    ```

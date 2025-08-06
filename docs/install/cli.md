# Install the command line tool

InvenioRDM is set up with a command line management tool, `invenio-cli`, which is used to manage and work with your local installation.

## Installation

`invenio-cli` is available on [PyPI](https://pypi.org/project/invenio-cli/). Use your favorite way to install it:

=== "pip"

    ```shell
    pip install invenio-cli
    ```

    !!! warning "Create a virtual environment"
        When installing on Debian 12 with Python 3.11, one has to create the virtual environment first with the `venv` module. For example: ```python -m venv venv --prompt invenioDRM.```

=== "uv"

    ```shell
    uv tool install invenio-cli
    ```

=== "pipx"

    ```shell
    pipx install invenio-cli
    ```

To make sure you've installed it successfully:

```bash
invenio-cli --version
```

You'll find the latest released version number on [PyPi](https://pypi.org/project/invenio-cli/). Each new version of InvenioRDM is accompanied by a new version of `invenio-cli` if only to have it select the new version as the default when initializing a project.

## Commands reference

For a full reference of available commands, see the [CLI reference](../reference/cli.md)


!!! tip "Shell tab completion"
     `invenio-cli` has support for shell tab completion of commands. See [shell completion](../reference/cli.md#shell-completion).

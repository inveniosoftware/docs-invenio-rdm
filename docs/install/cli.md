# Install CLI

InvenioRDM comes with a CLI management tool called Invenio-CLI which is used to manage and work with your local installation.

You can install the Invenio CLI package named `invenio-cli`. The package is available on [PyPI](https://pypi.org/project/invenio-cli/). Use your favorite way to install a Python package:

Via pip:

```bash
pip install invenio-cli
```

Via pipenv:

```bash
pipenv install invenio-cli
```

Via pipx:

```bash
pipx install invenio-cli
```

To make sure you've installed successfully:

```bash
invenio-cli --version
```
```console
invenio-cli, version 0.x.0
```

!!! note "CLI version"
     The CLI is in pre 1.0 release. The latest released version is listed on [GitHub](https://github.com/inveniosoftware/invenio-cli/releases) and available via [PyPi](https://pypi.org/project/invenio-cli/)


### Commands reference

For a full reference of available commands, see the [CLI reference](/reference/cli/)


!!! tip
     Invenio-CLI has support for Shell tab completion of commands. See [Shell completion](/reference/cli/#shell-completion).

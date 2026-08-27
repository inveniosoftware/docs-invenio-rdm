# Python package development

Python package development happens when you work on a single Python package (e.g. ``invenio-communities``). Either you are building a completely new package or
you are adding/modifying an existing package.

### Prerequisites

Make sure you have already [checked out the source code](source-code.md) of the
module(s) you want to work on.

### Install

Once you got the source code, create a Python virtual environment and make an
editable install of the Python package. We recommend using ``uv``, but you can
also use ``pip``:

To install optional dependency sets, add each extra declared by the
package separately. For example:

=== "uv"

    ```bash
    cd ~/src/invenio-app-rdm
    # opensearch2 only needed for certain modules
    uv sync --extra tests --extra opensearch2
    # or, if you are used to the pip way:
    uv pip install -e ".[tests,opensearch2]"
    ```

=== "pip"

    ```bash
    cd ~/src/invenio-app-rdm
    mkvirtualenv app-rdm
    # opensearch2 only needed for certain modules
    pip install -e ".[tests,opensearch2]"
    ```

    See [Python virtual environments](../../reference/virtualenvs.md) for more
    information about virtual environments.

For each package, check which extras it declares and install only those you
need. For example, ``tests`` is commonly needed for testing, while
``opensearch2`` is needed only by packages that support OpenSearch 2. An extra
that is not declared by a package cannot be passed to ``uv sync``.

### Run tests

Running the test is normally as simple as:

```bash
./run-tests.sh
```

The ``run-tests.sh`` under the hood uses [pytest](https://docs.pytest.org/) to run
the tests. If the module needs services such as a database, cache or search index,
the script usually uses ``docker-services-cli`` to automatically boot up
the required services

!!! note

    ``docker-services-cli`` may fail if you already have the services running.
    Most notably, if have a InvenioRDM development instance running, the you
    have to shut it down first before running tests.


### Multiple packages

If you need to work on multiple packages at the same time - for instance
you could be adding a cross-cutting feature to ``invenio-communities`` and
``invenio-requests`` at the same time, the installation is almost identical
to a single module:

First make sure you have the source code of both modules. Next, create one
virtual environment and install both packages in editable mode:

For independent packages, use ``uv pip`` to install them into one environment.
``uv sync`` is scoped to its current project (or a configured uv workspace).

=== "uv"

    ```bash
    uv pip install -e "~/src/invenio-communities[tests,opensearch2]" \
        -e "~/src/invenio-requests[tests,elasticsearch7]"
    ```

=== "pip"

    ```bash
    mkvirtualenv communities
    pip install -e "~/src/invenio-communities[tests,opensearch2]" \
        -e "~/src/invenio-requests[tests,elasticsearch7]"
    ```

### Application integration

See the section on [pre-release instance development](prerelease-instance-development.md) for how to
integrate your development version(s) in a development InvenioRDM application for integration testing.

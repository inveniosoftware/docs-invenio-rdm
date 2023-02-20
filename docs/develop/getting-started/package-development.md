# Python package development

Python package development happens when you work on a single Python package (e.g. ``invenio-communities``). Either you are building a completely new package or
you are adding/modifying an existing package.

### Prerequisites

Make sure you have already [checked out the source code](source-code.md) of the
module(s) you want to work on.

### Install

Once you got the source code, create a Python virtual environment and make an
editable install of the Python package:

!!! note

    ``mkvirtualenv`` is a tool provided by virtualenv-wrapper to manage Python
    virtualenvs. See [Python virtual environments](virtualenvs.md)

```
cd ~/src/invenio-app-rdm
mkvirtualenv app-rdm
# opensearch2 only needed for certain modules
pip install -e ".[tests,opensearch2]"
```

For each module, you'll have to check what is the precise list of extras
you need to add (the ``tests,opensearch2``). If you don't add them,
you won't have all the tools needed for testing.

### Run tests

Running the test is normally as simple as:

```
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

First make sure you have the source code of both modules. Next, simply do
editable installs of both:

```
mkvirtualenv communities
pip install -e "~/src/invenio-communities[tests,opensearch2]" \
    -e "~/src/invenio-requests[tests,elasticsearch7]"
```

### Application integration

See the section [instance development](instance-development.md) for how to
integrate your development versions in the InvenioRDM application.


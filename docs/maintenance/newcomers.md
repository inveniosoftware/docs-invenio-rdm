# Newcomers Guide

**Intended audience**

The guide is intended as a crash course fpr new core developers of InvenioRDM with prior experience in running and installing InvenioRDM.

**Scope**

The guide covers how we collaborate, the essential communication channels and key tools we use.

## Overview

Following is a quick overview over what you need to know in order to participate in the InvenioRDM development.

### Join communication channels

- Join Discord [``#rdm-internal``](https://discord.gg/8qatqBC)
- Member of GitHub [inveniosoftware organisation](https://github.com/inveniosoftware/opensource/blob/master/repositories.yml) and the ``inveniordm`` and ``developers`` teams (ask`` @lnielsen``)
- Mailing list project-inveniordm@cern.ch (ask ``@lnielsen``).

### Development iterations

We run **iterations ranging from 3-5 weeks** which are usually aligned with calendar months. Each iteration produces are new release. We use a sprint board to keep track of the current iteration. The current board is linked from https://inveniosoftware.org/products/rdm/#status.

We use a [product roadmap](https://github.com/inveniosoftware/product-rdm/milestones?direction=asc&sort=due_date&state=open) in GitHub to keep track of high-level features.

### Board workflow

See [board workflow](board-workflow.md)

### Iteration schedule

The high-level sprint schedule usually looks like this:

- 1st week:
    - Monday: Kick-off
    - Tuesday: Roadmap update
- last week:
    - Tuesday: Feature locking.
    - Thursday: Release, deployment and announcement.
    - Friday: Review, retrospective & triaging of stale issues.

### Daily tasks/meetings

You daily schedule looks like this:

- *Sprint notes:* daily before the standup, please post your sprint notes into #rdm-sprint-notes channel.
    - Focus on blockers, tasks completed.
    - The sprint notes are very important for cross timezone collaborations.
- *Standup:* daily at 15:15 UTC on Discord #rdm-internal voice channel (cancelled during bi-weekly telecons every second Tuesday, or move to after the telecon).

## Developing with InvenioRDM

### Setup your system

See [Setting up your system](https://invenio.readthedocs.io/en/latest/getting-started/development-environment.html)

### Tools

Invenio-CLI is the primary tool you'll use for development. See the [CLI reference documentation](https://inveniordm.docs.cern.ch/reference/cli/). In particular, you'll need the following commands to install development versions of libraries in your InvenioRDM instance:

```
invenio-cli install ...
invenio-cli assets build
invenio-cli assets watch
invenio-cli assets install
invenio-cli assets watch-module
```

Above commands, works when you install development versions of modules into InvenioRDM (i.e. integration testing). Often, you'll work on a specific Invenio modules, these modules you'll usually work on in the following way:

```
cd ~/src/invenio-<amodule>
mkvirtualenv <amodule>
# postgresql,elasticsearch7 only needed for certain modules
pip install -e ".[all,postgresql,elasticsearch7]"
./run-tests.sh
```

Run tests uses ``docker-services-cli`` to bootup needed services (like database, cache and search engine). To run tests individually, you can use:

```
# Copy/paste the following line fro ./run-tests.sh
eval "$(docker-services-cli up --db ${DB:-postgresql} --search ${ES:-elasticsearch} --mq ${CACHE:-redis} --env)"
# Run single test:
pytest tests/test_somemodule.py::test_sometestfunc -s
```

### Debugging tricks

**Python debugger**
For debugging use the Python debugger (PDB) or one of the variations (ipdb, pytest and wdb).

To set a breakpoint place the following code:

```python
import pdb
pdb.set_trace()
```

During tests, you may need to use pytest instead and run pytest with ``-s`` option:

```python
# pytest -s ...
import pytest
pytest.set_trace()
```

**Flask DebugToolbar**
You can also install [Flask-DebugToolbar](https://flask-debugtoolbar.readthedocs.io/en/latest/):

```
cd ~/src/my-site
pipenv run pip install Flask-Debugtoolbar
```

It has built-in:
- Profiler
- SQL queries logging
- View config/templates

**SQL queries**
Last, but not least you can print SQL queries to the console by setting the  variable in your ``config.py``:

```
# config.py
SQLALCHEMY_ECHO = True
```

### Coding style

InvenioRDM follows Invenio practices:

- Commits:
    - [Messages](https://invenio.readthedocs.io/en/latest/community/contributing/contribution-guide.html#commit-messages)
    - Logical: Commits should be logical chunks of works (git rebase is your friend). Do not make many small commits.
- Coding style: PEP8, isorting (checked by the ``./run-tests.sh`` script and ``.editorconfig`` helps you configure your editor)
- Follow existing style (look at the module you are working on):
    - Do not use type hints.
    - Support Python 3.6+


In doubt if something is allowed or not? Just ask :-)

## Design

### Architects

Invenio has four principal architects. All architects have:

1. previously designed and built at least one larger repository from scratch.
2. large knowledge of the existing codebase and vision of the project.

Architects are there to help you succeed in contributing, but also have a final say on all design choices made in Invenio (this is to ensure a coherent product and coherent decisions).

### RFCs

All larger design work is subject to an RFC. [Invenio RFCs](https://github.com/inveniosoftware/rfcs) are a communication tool, to:

- coordinate the design process
- document design decisions
- produce consensus among Invenio stakeholders

It's a collaborative process.

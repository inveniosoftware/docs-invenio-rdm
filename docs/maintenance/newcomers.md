# Newcomers Guide

**Intended audience**

The guide is intended as a crash course for new core developers of InvenioRDM with prior experience in running and installing InvenioRDM.

**Scope**

The guide covers how we collaborate, the essential communication channels and key tools we use.

## Overview

Following is a quick overview over what you need to know in order to participate in the InvenioRDM development.

### Join communication channels

- Join Discord [``inveniosoftware``](https://discord.gg/8qatqBC)
- Member of GitHub [inveniosoftware organisation](https://github.com/inveniosoftware/opensource/blob/master/repositories.yml) and the ``inveniordm`` and ``developers`` teams (ask`` @lnielsen``)
- Mailing list project-inveniordm@cern.ch (ask ``@lnielsen``).
- [ThisWeek](https://github.com/inveniosoftware/thisweek) digest is sent once a week on Discord #rdm-general channel.

### Development iterations

We run **iterations of 6-8 weeks** and each iteration produces a new release. We use one sprint board per team to keep track of the current iteration.

We use a [product roadmap](../contribute/roadmap.md) in GitHub to keep track of high-level features and plan the release.

### Board workflow

See [board workflow](board-workflow.md)

### Iteration schedule

The high-level sprint schedule usually looks like this:

- Week 1: Kick-off and design week.
- Week 2-5: Development
- Week 6: Integration, QA, testing
    - Feature lock
    - Thursday: Release, deployment and announcement.
    - Friday: Review, retrospective & triaging of stale issues.

### Daily meetings

You daily schedule looks like this:

- *Standup:* daily at 14:15 CET on Discord #rdm-internal voice channel.

## Developing with InvenioRDM

### Set up your system

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

Run tests uses ``docker-services-cli`` to boot up needed services (like database, cache and search engine). To run tests individually, you can use:

```
# Copy/paste the following line fro ./run-tests.sh
eval "$(docker-services-cli up --db ${DB:-postgresql} --search ${ES:-elasticsearch} --mq ${CACHE:-redis} --env)"
# Run single test:
pytest tests/test_somemodule.py::test_sometestfunc -s
```

## Design

### Architects

Invenio has four principal architects. All architects have:

1. Previously designed and built at least one larger repository from scratch.
2. Large knowledge of the existing codebase and vision of the project.

Architects are there to help you succeed in contributing, but also have a final say on all design choices made in Invenio (this is to ensure a coherent product and coherent decisions).

### RFCs

All larger design work is subject to an RFC. [Invenio RFCs](https://github.com/inveniosoftware/rfcs) are a communication tool, to:

- Coordinate the design process
- Document design decisions
- Produce consensus among Invenio stakeholders

It's a collaborative process.

# Maintainer Guide

**Intended audience**

This guide is intended for maintainers and developers of InvenioRDM itself.

**Scope**

The guide covers the development workflows

## Newcomers

First time you contribute to InvenioRDM core development? This section is for you.

Following is a quick overview over what you need to know in order to participate in the InvenioRDM development.

**Join communication channels**

- Join Discord [``#rdm-internal``](https://discord.gg/8qatqBC)
- Member of GitHub [inveniosoftware organisation](https://github.com/inveniosoftware/opensource/blob/master/repositories.yml) and the ``inveniordm`` and ``developers`` teams (ask`` @lnielsen``)
- Mailing list project-inveniordm@cern.ch (ask ``@lnielsen``).

**Development iterations**

We run **iterations ranging from 3-5 weeks** which are usually aligned with calendar months. Each iteration produces are new release. We use a sprintboard to keep track of the current iteration. The current board is linked from https://inveniosoftware.org/products/rdm/#status.

**Sprint schedule**

The high-level sprint schedule usually looks like this:

- 1st week:
    - Monday: Kick-off
    - Tuesday: Roadmap update
- last week:
    - Tuesday: Feature locking.
    - Thursday: Release, deployment and announcement.
    - Friday: Review, retrospective & triaging of stale issues.

**Daily tasks/meetings**

You daily schedule looks like this:

- *Sprint notes:* daily before the standup, please post your sprint notes into #rdm-sprint-notes channel.
    - Focus on blockers, tasks completed.
- *Standup:* daily at 15:15 UTC on Discord #rdm-internal voice channel (cancelled during bi-weekly telecons every second Tuesday).

**Sprintboard workflow**

See below.

**Developing with InvenioRDM**

Invenio-CLI is the primary tool you'll use for development. See the [CLI reference documentation](https://inveniordm.docs.cern.ch/reference/cli/). In particular, you'll need the following commands to install development versions of libraries in your InvenioRDM instance:

```
invenio-cli packages install ...
invenio-cli assets build
invenio-cli assets watch
invenio-cli assets install
invenio-cli assets watch-module
```

Above commands, works when you install development versions  of modules into InvenioRDM (i.e. integration testing). Often, you'll work on a specific Invenio modules, these modules you'll usually work on in the following way:

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


**Coding style**

InvenioRDM follows Invenio practices:

- Commits:
    - [Messages](https://invenio.readthedocs.io/en/latest/community/contributing/contribution-guide.html#commit-messages)
    - Logical: Commits should be logical chunks of works (git rebase is your friend). Do not make many small commits.
- Coding style: PEP8, isorting (checked by the ``./run-tests.sh`` script and ``.editorconfig`` helps you configure your editor)
- Follow existing style (look at the module you are working on):
    - Do not use type hints.
    - Support Python 3.6+


In doubt if something is allowed or not, please ask :-)

**Architects**

Invenio has four principal architects. All architects have:

1. previously designed and built at least one larger repository from scratch.
2. large knowledge of the existing codebase and vision of the project.

Architects are there to help you succeed in contributing, but also have a final say on all design choices made in Invenio (this is to ensure a coherent product and coherent decisions).

**RFCs**

All larger design work is subject to an RFC. [Invenio RFCs](https://github.com/inveniosoftware/rfcs) are a communication tool, to:

- coordinate the design process
- document design decisions
- produce consensus among Invenio stakeholders

It's a collaborative process.


## Board workflow

The following

- New issue
    - Move issue to "Triage"

- Start task:
    - Assign yourself
    - Move issue to "In progress"

- Finish task:
    - Link PR to issue (don't put PR on board except for small PRs)
    - Move to "Pending review"
    - Unassign yourself from **issue** or PR (the item that's visible on the board)

- Start a review:
    - Assign yourself
    - Move to "In review"
    - Reviews guidelines:
        - Use emojis, be polite/considerate/respectful, focus on code, not people.
        - Prefix all comments with:
            - Comment/Doubt/Question
            - Shelved: Open issue to document it.
            - Minor: PR-merge not blocked. Up to developer to decide if review comment should be fixed or not.
            - Moderate/Normal (default): Merge blocked until reviewer confirms it's fixed.
            - Major: Merge blocked. Live discussion needed, and likely involvement of an Invenio architect.
        - Never use "Request changes", only "Comment" or "Approve".

- Finish review:
    - Comments?
        - Unassign yourself
        - Assign creator
        - Leave in "In review"
    - Approved with comments?
        - Same as above, but developer can merge after fixing.
    - Approved?
        - Approve PR
        - Merge PR and check closes statement

- Start implement review comments:

    - Assign yourself
    - Leave in "In review"

- Finish implement review comments:

    - Assign reivewer
    - Leave in "In review"

## Release checklist

### Pre-release

- Cookiecutter-Invenio-RDM:
    - Merge everything to master..
    - Create new version branch from master.

### Release

The final step to release the new modules and source code is to release Invenio-CLI. Releasing Invenio-CLI, will make all new installation use the latest released packages.

- Invenio-CLI:
    - Update Cookiecutter-Invenio-RDM branch version in source code.
    - Bump version of Invenio-CLI

### Post-release

- Deploy InvenioRDM to QA and PROD (demo website and docs)
- Blog post (including adding a link under https://inveniosoftware.org/products/rdm/#status)
- Website update
    - Update [public roadmap](https://inveniosoftware.org/products/rdm/roadmap/).
    - Review project information
- Project tracking:
    - GitHub: Update [internal product roadmap](https://github.com/inveniosoftware/product-rdm/milestones?direction=asc&sort=due_date&state=open)

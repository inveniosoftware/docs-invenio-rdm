# Code style

InvenioRDM follows Invenio practices:

- Commits:
    - [Messages](https://invenio.readthedocs.io/en/latest/community/contributing/contribution-guide.html#commit-messages)
    - Logical: Commits should be logical chunks of works (git rebase is your friend). Do not make many small commits.
- Coding style: PEP8, isorting (checked by the ``./run-tests.sh`` script and ``.editorconfig`` helps you configure your editor)
- Follow existing style (look at the module you are working on):
    - Do not use type hints.
    - Support Python 3.7+ (i.e. any supported Python version)

In doubt if something is allowed or not? Just ask on Discord

Please also refer to the [development process](../process.md) for standards on
UX and scalability.

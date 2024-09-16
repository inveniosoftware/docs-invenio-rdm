# Code style

InvenioRDM follows Invenio practices:

- Commits:
    - [Messages](https://invenio.readthedocs.io/en/latest/community/contributing/contribution-guide.html#commit-messages)
    - Logical: Commits should be logical chunks of works (git rebase is your friend). Do not make many small commits.
- Coding style: PEP8, isorting (checked by the ``./run-tests.sh`` script and ``.editorconfig`` helps you configure your editor)
- Follow existing style (look at the module you are working on):
    - Support Python 3.9+ (i.e. any officially supported Python version)
    - Do not use type hints.
      - **Why?** Primarily for consistency across the codebase. Having some modules with type hints and others without would make the code harder to read and maintain.
      - Before we introduce type hints, as a community we would need to decide on:
        - Where do we apply type hints, e.g., everywhere or only in public API functions/classes/methods
        - What rules we would enforce via type linters and how specific or generic the types should be, especially with complex inheritance patterns or dynamically computed classes
        - Ensuring all developers and reviewers are familiar with typing conventions and enforce them during PR reviews.
        - Minimum Python versions. Typing syntax has evolved, and newer features are not backward-compatible with older Python versions. For example, Python 3.10+ allows the use of the `|` operator for unions, while older versions require `typing.Optional` or `typing.Union`. Introducing type hints would also require decisions on the minimum Python version supported so that we can work with a compelling set of typing primitives.
      - We agree on and understand that Python typing annotations can be useful though, especially when it comes to showing autocompletions in your editor and linters catching bugs. We shouldn't sacrifice readability and simplicity though for typing, since Python is still a dynamically typed language and cannot take advantage of performance benefits or compilation correctness from its types.

In doubt if something is allowed or not? Just ask on Discord

Please also refer to the [development process](../process.md) for standards on
UX and scalability.

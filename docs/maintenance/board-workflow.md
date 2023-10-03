# Sprintboard Workflow

**Intended audience**

This guide is intended for maintainers and developers of InvenioRDM itself.

**Scope**

The guide covers how we use the GitHub sprint boards during development.

## Board

You'll find the latest board linked from [inveniosoftware.org](https://inveniosoftware.org/products/rdm/#status)

## Columns

- **Triage**: Issue/PR is not ready to be worked on.
- **Todo**: Issue/PR is ready to be worked on.
- **In progress**: Issue/PR is being worked on.
- **Blocked**: Issue/PR is blocked.
- **Pending review**: Issue/PR is ready to be reviewed.
- **In review**: Issue/PR is being reviewed, or in progress of being updated from a review.
- **Done**: All closed issues and PR.
- **Milestone**: Hold the product milestone issue as reference for the goals we are working towards.

## Workflow

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

    - Assign reviewer
    - Leave in "In review"



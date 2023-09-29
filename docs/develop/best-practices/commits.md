# Commits, pull requests and reviews

## Commits

#### Logical commits

Please create logical separate commits. This is important to be able to track
changes over time and understand how a change relates to other parts of the
code.

Already made 20 step-by-step commits today? In a nutshell you can fix these
by using *rebasing*. Here are some helpful commands:

```console
# Rebase your commits - squash/fixup/reword/edit/reorder etc.
git rebase --interactive <sha>

# Reset your commit index, but leave the files unchanged
git reset <sha>

# Interactive add parts of files to a commit
git add --patch
```

####  Linear history

Our branches follow a linear commit history, meaning that
we use *rebasing* instead of e.g. *merge commits*. In a nutshell this
translates into:

```console
git fetch <remote>
git rebase --interactive <remote>/master
```

#### Commit message

!!! tip  "It's about content"

    Commit message is first and foremost about the content. You are communicating
    with fellow developers:

    - Be clear and brief - it's a summary.
    - Focus on **what** and especially **why**.

#### Message format

Inspired by [How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/):

1. [Separate subject from body with a blank line](https://chris.beams.io/posts/git-commit/#separate)
2. [Limit the subject line to 50 characters](https://chris.beams.io/posts/git-commit/#limit-50)
3. Indicate the component follow by a short description
4. [Do not end the subject line with a period](https://chris.beams.io/posts/git-commit/#end)
5. [Use the imperative mood in the subject line](https://chris.beams.io/posts/git-commit/#imperative)
6. [Wrap the body at 72 characters](https://chris.beams.io/posts/git-commit/#wrap-72)
7. [Use the body to explain what and why vs. how, using bullet points](https://chris.beams.io/posts/git-commit/#why-not-how)

**Git signatures**

The only signature we use is ``Co-authored-by`` (see above)
to provide credit to co-authors.

#### Message example

```
component: summarize changes in 50 char or less

* More detailed explanatory text, if necessary. Formatted using
  bullet points, preferably `*`. Wrapped to 72 characters.

* Explain the problem that this commit is solving. Focus on why you
  are making this change as opposed to how (the code explains that).
  Are there side effects or other unintuitive consequences of this
  change? Here's the place to explain them.

* The blank line separating the summary from the body is critical
  (unless you omit the body entirely); various tools like `log`,
  `shortlog` and `rebase` can get confused if you run the two
  together.

* Use words like "Adds", "Fixes" or "Breaks" in the listed bullets to help
  others understand what you did.

* If your commit closes or addresses an issue, you can mention
  it in any of the bullets after the dot. (closes #XXX) (addresses
  #YYY)

Co-authored-by: John Doe <john.doe@example.com>
```

## Pull requests

!!! tip "Discuss first, code later"

    See our [development process](../process.md). Please reach out to discuss
    your idea first and align on design with the community. This avoids
    duplicated and wasted  efforts.


When making your pull request, please keep the following in mind:

- Commits: Follow above guidelines.
- Add tests and don't decrease test coverage.
- Add documentation.
- Follow our best practices:
    - [Data migrations](../howtos/alembic.md)
    - [Translation strings](../howtos/i18n.md)
    - [CSS/JS](css-js.md) and [React](react.md)
    - [Web accessibility](accessibility.md)
    - [User interface](ui.md)
- Identify the [copyright holder(s)](../../contribute/copyright-policy.md) and update copyright headers for touched files (>15 lines contributions).
- New third-party code (copy/pasted source code or new dependencies) requires approval from architect or maintainer.
- 🟢 Green light on all GitHub status checks is required in order to merge your
  PR.

### Third-party code/dependencies

If you're adding third-party code, please reach out to an
[architect](https://github.com/orgs/inveniosoftware/teams/architects).

Third-party code must be licensed with a permissive open source license (MIT,
BSD, Apache, LGPL are accepted, while GPL and AGPL are not accepted) and the
license conditions must be respected (usually means you must maintain the
copyright notice).

InvenioRDM has 200+ Python dependencies and then we're not even counting the
NPM packages. Each dependency has the potential to break InvenioRDM. Therefore
a third-party dependency must be careful evaluated if before being added.

## Reviews

Reviews are a very important part of the development process, but also has the potential to lead to conflicts among developers.

Follow these guidelines to minimize the risk of conflicts:

#### Code of conduct

We expect everyone to comply with our [code of conduct](../../contribute/code-of-conduct.md) - be open, inclusive, considerate and respectful.

- *Reviewer*: Be respectful of the effort (often the labour was completed simply for the good of the community).
- *Creator*: Be receptive to constructive comments and criticism (the reviews are labour intensive and serves to produce a better product and development for the community).

#### Prefix your review comments

Prefix your review comments with one of the tags from the scale. This helps
the creator to understand the importance of your comment.

1. **Comment/Doubt/Question**: exactly that. A doubt, a question or a comment.

2. **Minor**: a change that the reviewer thinks might need change. However, it
  is not blocking, it is up to the developer to choose if and how to change
  it. It can be merged!

3. **Moderate/Normal (Default)**: a change that requires further discussion
  (e.g. breaking changes). It cannot be merged, unless explicitly stated by
  the reviewer (e.g. choose a solution proposed by the reviewer and implement
  it). Depending on the nature of the change a new review might be needed,
  use common sense.

4. **Major**: a change that needs further discussion, probably a chat. Even the
  opinion of an architect. It has high implications. It cannot be merged. Use
  *major* with caution.

5. **Shelved**: a suggestion that will be treated later on as part of a
  different issue. It is a good practice to reference the issue. Note that
  any of the previous (comment, minor, moderate and major) can be shelved if
  agreed by the PR creator and the reviewer.

#### Use emojis

Be polite and use emojis in your comments. This helps add a tiny bit of the
nonverbal and paraverbal communication back into text-based messsage (the
nonverbal/paraverbal part of message accounts for as much as 90% of a message).

#### Approval

Absence of approval means a pull request has not yet approved.

**Request changes**

❌ DON'T USE

GitHub allows a reviewer to "request changes". We do not use this feature.
Instead a reviewer should use the review comment scale above.

The only accepted use of the request changes features is e.g. for an architect
to block the merge of a PR in case there's a risk another maintainer might
merge the PR (e.g. missing to see a recent comment). It's important to
understand this is only in case of emergencies and urgent timing issues.

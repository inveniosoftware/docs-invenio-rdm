# Contribute documentation

Learn how to write and contribute technical documentation.

## References

- [Diátaxis](https://diataxis.fr/): learn how to write *tutorials*, *how-to guides*, *reference guides*, *explanation*.

- Training of 2-3 hours: [Google Technical Writing Courses for Engineers](https://developers.google.com/tech-writing/overview).

## Guidelines

### Before starting

- Set up a spell checker in your IDE, even better a "writing assistant" (popular ones [LanguageTool](https://languagetool.org/), [Grammarly](https://www.grammarly.com/)).
- Determine what your audience needs to learn, fit documentation to your audience.

### When writing

- Write in the second person. Refer to your audience as “you” rather than “we”.
- Create great opening sentences that establish a paragraph's central point.
- Prefer active voice to passive voice: `The mat was sat on by the cat.` -> `The cat sat on the mat.`
- Prefer task-based headings.
- Prefer list to long sentences. Use a numbered list when ordering is important and a bulleted list when ordering is irrelevant.
- Explain and give information progressively.
- Usage sections should feel like tutorials that call the user to action - e.g. "create a mapping".
- In tutorials, reinforce concepts with examples, note problems that readers may encounter.

### When completed

- Read documents out loud (to yourself).
- Ask for review.
- When using MkDocs, run the live server and verify that the page renders correctly (e.g. code snippets).

## External locations to update

When updating the documentation, you may move content and pages around that some modules of the InvenioRDM project link to. You will need to update those links to point to the moved pages. In particular, verify if your changes affect the links listed in these locations:

- the [default InvenioRDM frontpage](https://github.com/inveniosoftware/invenio-app-rdm/blob/master/invenio_app_rdm/theme/templates/semantic-ui/invenio_app_rdm/intro_section.html) shown after a fresh install
- the [inveniosoftware.org site](https://github.com/inveniosoftware/inveniosoftware.org) that positions InvenioRDM within the wider Invenio universe

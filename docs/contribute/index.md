# Contribute to InvenioRDM

InvenioRDM is a vibrant open-source project with a community spanning the globe.
We cover almost all time zones during our major online workshops! Here we highlight
how you can contribute and how we work.

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

## Governance

How the project is governed is outlined [here](https://inveniosoftware.org/governance/).

## Release process

InvenioRDM's development is split into monthly releases with the occasional
help from Invenio (the underlying framework) sprints. For example, the
"November release" is worked on during the month of November and is released
during the first week of December.

A monthly board is setup on GitHub with high-level goals and lower-level tasks:
[https://github.com/orgs/inveniosoftware/projects](https://github.com/orgs/inveniosoftware/projects).
The monthly work starts with a planning and an initial release of the upcoming month's packages
except for `invenio-cli`. This typically includes new versions of:

- flask-resource
- invenio-records-resources
- invenio-drafts-resources
- invenio-rdm-records
- invenio-app-rdm
- react-invenio-deposit
- cookiecutter-invenio-rdm

Releasing new versions of the packages at the beginning of the monthly sprint rather
than at the end reduces coordination problems during typically busy last days, prevents
repeated ad-hoc version increases during the same month, isolates new changes from
the previously released modules and makes releasing for production a continuous process
throughout the month.

At the end of the month, only `invenio-cli` needs to be released. It shifts the window
of acceptable dependencies, and coordinates and exposes the already released modules widely.

For maintainers, releasing `<version X>` (release commit merged in `master` already) is simply:

``` bash
git checkout master
git tags -a <version X> -m "<version X>"
git push upstream --follow-tags
```

## Types of Contributions

### Report Bugs and ask for features

Submit an issue at [https://github.com/inveniosoftware/invenio-app-rdm/issues](https://github.com/inveniosoftware/invenio-app-rdm/issues).
Select bug or feature and you will have a prepopulated GitHub issue created for you.
Fill it out!

InvenioRDM is made up of a collection of modules. As you become more familiar with them,
you may want to submit your ticket to their respective repositories.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

Follow the module's `CONTRIBUTING.md` file to ensure you are adhering to our process.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "good first issue"
is a good place to start. Otherwise, reach out on the [chat](https://discord.gg/8qatqBC) and ask.

Just as for fixing bugs, follow the module's `CONTRIBUTING.md` for the practical details.

### Write Documentation

InvenioRDM could always use more documentation, whether as part of these
official docs, in docstrings, or even on the web in blog posts,
articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at
[https://github.com/inveniosoftware/invenio-app-rdm/issues](https://github.com/inveniosoftware/invenio-app-rdm/issues)
or reply to the month's release on our [Discourse forum](https://invenio-talk.web.cern.ch/c/projects/invenio-rdm/).

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

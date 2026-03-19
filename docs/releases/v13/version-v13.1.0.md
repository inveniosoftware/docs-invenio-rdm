# InvenioRDM v13.1

*2026-03-27*

We are happy to announce the release of InvenioRDM v13.1. This is a minor release which will become the maintained tip of v13.
Future patches for v13 will land on this minor version only.


## What's new?

InvenioRDM v13.1 primarily backports the [request reviewers feature](../../maintenance/architecture/requests.md#reviewers-in-requests) to InvenioRDM v13.

This feature allows the selection of users (or groups) as "reviewers" for requests.
The selected reviewers will gain access to the request and its timeline (i.e. associated events and comments), and be able to comment on the request too.

!!! warning "Enabling the feature requires reindexing the requests"
    The information about the set of reviewers is stored in a new field in the request itself, so the schema has changed.
    Enabling the feature will require the search mappings to be updated, and the requests to be reindexed.
    For more details, see the [upgrade section below](#upgrading-from-v130-to-v131).


### Selecting reviewers for requests

The new request reviewers feature is (currently) opt-in, so you'll have to enable the `REQUESTS_REVIEWERS_ENABLED` feature flag via the configuration.
Additionally, the behavior can be tweaked with a few more configuration items:

```python
REQUESTS_REVIEWERS_ENABLED = True
"""Enable the request reviewers feature."""

REQUESTS_REVIEWERS_MAX_NUMBER = 15
"""Maximum number of reviewers allowed for a request."""

USERS_RESOURCES_GROUPS_ENABLED = True
"""Config to enable features related to existence of groups.

Makes groups available for selection as request reviewers, in addition to users.
"""
```

**Note** that the feature flag currently enables the request reviewers feature for *all kinds of requests*.


### Other notable changes

Even though the upgrade pulls in a number of major version bumps, there are actually only relatively few large changes.
Most of the major releases there just bump their own dependencies (to better isolate from breaking changes) rather than introducing breaking changes themselves.

Here are the most noteworthy changes:

* [`Invenio-Users-Resources` v9.0.0](https://pypi.org/project/invenio-users-resources/9.0.3/): Tightened permissions for users endpoints in the REST API, and change of HTTP status code from `403` to `404` on permission errors for increased privacy
* [`Invenio-RDM-Records` v20.2.0](https://pypi.org/project/invenio-rdm-records/20.2.0/): Renaming of several `React-Overridable` IDs; the full list of changed IDs is available in the [changelog for v20.2.0](https://github.com/inveniosoftware/invenio-rdm-records/blob/v20.2.0/CHANGES.rst?plain=1)



## Upgrading from v13.0 to v13.1


The first step of the upgrade process is of course to **install the new packages**.  
To do so, make sure that the version specifiers for the Invenio-App-RDM dependency in your project definition (`pyproject.toml`, `Pipfile`, ...) allow for the `13.1.x` range of releases, e.g. `invenio-app-rdm[opensearch2]~=13.1.0`.

The new packages should be found and installed via `invenio-cli install`.  
If the v13.1 release of Invenio-App-RDM still doesn't get pulled in, remove your lock file (`uv.lock`, `Pipfile.lock`, ...) and try again.

After installing the new packages, you'll need to **rebuild your frontend assets**, and **update the search mappings for the requests index and reindex all requests**.

For *local development setups*, the frontend assets have been built as part of `invenio-cli install` already.  
For *containerized setups*, this typically just requires rebuilding your container images; the frontend build is part of the default [`Dockerfile`](https://github.com/inveniosoftware/cookiecutter-invenio-rdm/blob/v13.0/%7B%7Bcookiecutter.project_shortname%7D%7D/Dockerfile).
If the frontend assets seem stale after spinning up the newly built containers, the culprit is often an outdated `static_data` volume.
Removing it and restarting the containers usually fixes this issue.
Just make sure not to delete the wrong volumes!

The search mappings and indexed requests can be updated with the following commands:

```bash
# update the search mappings for requests to include reviewers
invenio index update requests-request-v1.0.0 --no-check

# start bulk reindexing for all requests
invenio rdm rebuild-all-indices --order requests
```

That's it.
Other search indices like request events aren't affected and don't need to be updated.

!!! info "No action needed if you don't want to use the feature"
    If you *do not* intend to enable the request reviewers feature, no further action is necessary after upgrading the installed packages.
    But updating the mappings won't hurt either.

Enjoy v13.1! 😎

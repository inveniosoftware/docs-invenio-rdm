# InvenioRDM v14.1

*2026-12-01*

We are happy to announce the release of InvenioRDM v14.1. This is a minor
release which will become the maintained tip of v14.
Future patches for v14 will land on this minor version only.


## What's new?

InvenioRDM v14.1 includes updates to the default deposit form configuration,
including removing sub-fields that had a confusing red star. There is a 
new configuration option that lets you collapse the optional fields in the
deposit form. If you want to try this new option, set the following in
invenio.cfg

```python
APP_RDM_DEPOSIT_FORM_COLLAPSE_EMPTY_SECTIONS = True
``` 

You can [find more accordion configuration details here](../../../operate/customize/look-and-feel/override_components/#deposit-accordion-defaults).

## What's fixed?

There were bugs in the administration panel faceting, which have now been fixed
with a new API endpoint for admin moderation requests.


## Upgrading from v13.0 to v13.1


The first step of the upgrade process is of course to **install the new packages**.  
To do so, make sure that the version specifiers for the Invenio-App-RDM dependency 
in your project definition (`pyproject.toml`, `Pipfile`, ...) allow for the `14.1.x` 
range of releases, e.g. `invenio-app-rdm[opensearch2]~=14.1.0`.

The new packages should be found and installed via `invenio-cli install`.  
If the v14.1 release of Invenio-App-RDM still doesn't get pulled in, remove your lock file (`uv.lock`, `Pipfile.lock`, ...) and try again.

After installing the new packages, you'll need to **rebuild your frontend
assets**.

For *local development setups*, the frontend assets have been built as part of `invenio-cli install` already.  
For *containerized setups*, this typically just requires rebuilding your container images; the frontend build is part of the default [`Dockerfile`](https://github.com/inveniosoftware/cookiecutter-invenio-rdm/blob/v13.0/%7B%7Bcookiecutter.project_shortname%7D%7D/Dockerfile).
If the frontend assets seem stale after spinning up the newly built containers, the culprit is often an outdated `static_data` volume.
Removing it and restarting the containers usually fixes this issue.
Just make sure not to delete the wrong volumes!

Enjoy v14.1! 😎

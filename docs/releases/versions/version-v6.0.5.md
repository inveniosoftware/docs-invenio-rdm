# InvenioRDM v6.0.5

*2021-12-06*

InvenioRDM v6.0.5 is a bug fix releases that fixes a moderate severity vulnerability in earlier versions of InvenioRDM.

## Vulnerability fix

### Permissions not properly checked when a record is published

**Impact**

Invenio-Drafts-Resources does not properly check permissions when a record is published. The vulnerability is exploitable in a default installation of InvenioRDM. An authenticated  user is able via REST API calls to publish draft records of other users if they know the record identifier and the draft validates (e.g. all require fields filled out). An attacker is not able to modify the data in the record, and thus e.g. *cannot* change a record from restricted to public.

**Details**

The service's ``publish()`` method contains the following permission check:

```python
def publish(..):
    self.require_permission(identity, "publish")
```
However, the record should have been passed into the permission check so that the need generators have access to e.g. the record owner.

```python
def publish(..):
    self.require_permission(identity, "publish", record=record)
```
The bug is activated in Invenio-RDM-Records which has a need generator called ``RecordOwners()``, which when no record is passed in defaults to allow any authenticated user:

```python
class RecordOwners(Generator):
    def needs(self, record=None, **kwargs):
        if record is None:
            return [authenticated_user]
    # ...
```

**Patches**

The problem is patched in Invenio-Drafts-Resources v0.13.7 and 0.14.6+, which is part of InvenioRDM v6.0.1 and InvenioRDM v7.0 respectively.

You can verify the version installed of Invenio-Drafts-Resources via PIP:

```console
$ cd ~/src/my-site
$ pipenv run pip freeze | grep invenio-drafts-resources
invenio-drafts-resources==0.13.7
```

**References**

- [Security policy](https://inveniordm.docs.cern.ch/releases/security-policy/)
- [Security Advisory on GitHub](https://github.com/inveniosoftware/invenio-drafts-resources/security/advisories/GHSA-xr38-w74q-r8jv)

**CVE ID**

[CVE-2021-43781](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-43781)

**CVSS Score**

6.4 Moderate
CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:N


## Upgrading to v6.0.5

First make sure that you have upgraded to v6.0.x. See [upgrading to v6.0](../upgrading/upgrade-v6.0.md).

Next, all that is needed is an upgrade of the PyPI packages. After executing below command, your ``Pipfile`` and ``Pipfile.lock`` should have been updated:
```
$ cd my-site
$ invenio-cli packages update 6.0.5

Updating invenio-app-rdm[postgresql,elasticsearch7]~= to version 6.0.5...
Installing invenio-app-rdm[postgresql,elasticsearch7]~=6.0.5...
Adding invenio-app-rdm to Pipfile's [packages]...
✔ Installation Succeeded
Pipfile.lock (28dc29) out of date, updating to (a18515)...
Locking [dev-packages] dependencies...
Building requirements...
Resolving dependencies...
✔ Success!
Locking [packages] dependencies...
Building requirements...
Resolving dependencies...
✔ Success!
Updated Pipfile.lock (a18515)!
Installing dependencies from Pipfile.lock (a18515)...
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 0/0 — 00:00:00
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
Version 6.0.5 installed successfully.
```

See full instructions on [upgrading to v6.0.5](../upgrading/upgrade-v6.0.5.md).

## Maintenance policy

InvenioRDM v6.0 is a long-term support release which is supported until minimum 2022-08-05 and maximum until the next LTS release + 6 months. See our [Maintenance Policy](../maintenance-policy.md).

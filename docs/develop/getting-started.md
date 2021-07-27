# Getting started

### Development instance

The installation of the latest development version of InvenioRDM is very
similar to the normal installation guide. The primary difference is you should
use another instance template (by adding ``-c master`` to the scaffolding
command):

```
cd ~/src
invenio-cli init rdm -c master
```

Then install the instance as usual:

```
cd my-site
invenio-cli install
invenio-cli services setup
invenio-cli run
```

Above will install the latest **development releases** from PyPI and NPM. Each
module may have further changes on their latest master branch that has not yet
been released (see below).

### Development modules

**Source code checkout**

If you want to install the latest master branch of a dependent module, first
you have to checkout the source code repository:;//

The easiest is to use the [GitHub CLI tool](https://cli.github.com):

```
gh repo fork inveniosoftware/invenio-app-rdm
cd invenio-app-rdm
```

Above, we made a checkout of [Invenio-App-RDM](https://github.com/inveniosoftware/invenio-app-rdm) module. You'll have to adapt the command to checkout other modules.

Without the GitHub CLI tool, you'll first have to [fork the repository](https://docs.github.com/en/get-started/quickstart/fork-a-repo) on GitHub. Then, once you have a fork you can clone the repository and add the
upstream repository remote:

```
# without GitHub CLI:
git clone https://github.com/<your username>/invenio-app-rdm
cd invenio-app-rdm
git remote add upstream https://github.com/inveniosoftware/invenio-app-rdm
```

**Install module in instance**

Once you have a source code checkout, you can install the module in the
development instance:

```
cd ~/src/my-site
invenio-cli packages install ~/src/invenio-app-rdm
invenio-cli run
```

!!! warning

    Note, your development package must fit your InvenioRDM instance. If you
    for instance install the latest master branch of a module on a
    non-development instance of InvenioRDM it's not likely to work.

!!! warning

    A development package may have database, index and schema changes that
    needs to be added to the database. In this case, it's often the easiest to
    wipe and recreate the database/indexes:

        invenio-cli services destroy
        invenio-cli services setup

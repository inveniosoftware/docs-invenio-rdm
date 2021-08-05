# Getting started

### Development instance

The installation of the latest development version of InvenioRDM is very
similar to the normal installation guide. The primary difference is you should
that use another instance template (by adding ``-c master`` to the scaffolding
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

The commands above will install the latest **development releases** from PyPI
and NPM. In addition, each module may have further changes on their latest
*master* branch that has not yet been released (see below).

### Python development modules

**Source code checkout**

If you want to install the latest master branch of a dependent module, first
you have to checkout the source code repository:

The easiest is to use the [GitHub CLI tool](https://cli.github.com):

```
gh repo fork inveniosoftware/invenio-app-rdm
cd invenio-app-rdm
```

With the previous command, we made a checkout of [Invenio-App-RDM](https://github.com/inveniosoftware/invenio-app-rdm)
module. You'll have to adapt the command to checkout the module you want to work on.

Without the GitHub CLI tool, you'll first have to [fork the repository](https://docs.github.com/en/get-started/quickstart/fork-a-repo)
on GitHub. Then, once you have a fork you can clone the repository and add the
upstream repository remote:

```
# without GitHub CLI:
git clone https://github.com/<your username>/invenio-app-rdm
cd invenio-app-rdm
git remote add upstream https://github.com/inveniosoftware/invenio-app-rdm
```

**Install a module in an instance**

Once you have a source code checkout, you can install the module in the
development instance:

```
cd ~/src/my-site
invenio-cli packages install ~/src/invenio-app-rdm
invenio-cli run
```

!!! warning

    Note, your development package must fit your InvenioRDM instance. If you,
    for instance, install the latest master branch of a module on a
    non-development instance of InvenioRDM it's not likely to work.

!!! warning

    A development package may have database, index and schema changes that
    needs to be added to the database. In this case, it's often the easiest to
    wipe and recreate the database/indexes:

        invenio-cli services destroy
        invenio-cli services setup

**Edit CSS and JavaScript included in Python modules**

Some Python modules includes CSS/JavaScript which is usually located in
``assets/`` folders in the project.

By default, assets are not rebuilt when you edit the files, however you can
watch the files for changes and automatically rebuild the assets using the
following watch command.

```
cd ~/src/my-site
invenio-cli assets watch
```

!!! info

    Above only works for JS/CSS files distributed in the Python modules. In
    particular it doesn't work for React modules like React-Invenio-Deposit
    (see below).

!!! warning "No hot reloading"
    There is no hot reloading available. This means that even if the assets
    are watched and rebuilt, you need to refresh your browser to see the
    changes. In addition, **be aware of the cache**, it might be a good idea
    to disable your cache or use an incognito window when developing web UI.

### React development modules

InvenioRDM depends on a number of React modules published on NPM, namely
React-SearchKit, React-Invenio-Deposit and React-Invenio-Forms. If you need
to develop on these modules, there's a couple of extra steps.

- First, install the React module:

```
invenio-cli assets install ~/src/react-invenio-deposit
```

- Next, watch the modules for changes:

```
invenio-cli assets watch-module --link ~/src/react-invenio-deposit
```

- Last, in another terminal start the instance's assets watch (thus running
two watch commands):

```
invenio-cli assets watch
```

### Troubleshooting

**UnfinishedManifest error**

Rebuilding the webpack bundles is not a speed-of-light operation. It might
take a few seconds. If you see an `UnfinishedManifest` error in your
browser when you refresh, check the terminal to see whether the assets are
simply still building or if an actual build error (e.g. syntax error) occurred.

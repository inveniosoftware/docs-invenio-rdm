# [inveniordm.docs.cern.ch](https://inveniordm.docs.cern.ch)

[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/inveniosoftware/InvenioRDM?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge) [![License](https://img.shields.io/github/license/inveniosoftware/InvenioRDM.svg)](https://github.com/inveniosoftware/docs-invenio-rdm/blob/master/LICENSE)

## About

InvenioRDM user documentation web site.

## Run the docs locally

```console
$ mkvirtualenv docs-invenio-rdm
$ pip install -r requirements.txt
$ mkdocs serve # mike serve if you are using mike for versioning
$ firefox http://127.0.0.1:8000
```

## Set up versioning

This means having `/x.y.z/` at the end of the url to point to a specific release
version. You can also set up aliases to have `latest` or any desire string tag.

### Initial setup, onte time operations

#### Create the documentation branch

Create and orphan branch called `gh-pages`. This name is mandatory to avoid
extra configuration in mike and GitHub.

``` console
$ git checkout master
$ git checkout --orphan gh-pages
$ rm -rf ./*
$ git rm -r ./*
$ git commit -m "initial commit: index redirect"
$ git push origin gh-pages
```

Why an orphan branch? In order to separate the build documentation from the
source of it.

#### Create a latest redirection

By default GitHub pages serve the `index.html` file from the root directory.
Mike does not build one by default, and we would like the documentation site
to point to `/latest`. We can use the `set-default` command:

``` console
$ mike set-default latest -p
```

#### Install [mike](https://github.com/jimporter/mike)

Create a new branch (to do a PR from) and install mike's extras:

``` console
$ git checkout master
$ git checkout -b versioning
$ mike install-extras
```

Add and commit the changes. This will include formating of the `mkdocs.yaml`
plus some additions. As well as the css and js files needed for mike.

``` console
$ git add -p
$ git add docs/css/
$ git add docs/js/
$ git commit -m "versioning: add mikes extras"
$ git push origin versioning
```

**Note**: You might want to add `mike` to the requiresments.txt although it is
not necesary for the build itself.

### Operations

#### Deploy!

First of all fetch all branches to help mike sync. It does a great job on
this, but is better to be sure.

``` console
$ git fetch --all
```

Then you need to build the new documentation. It is recommended to
**not use** `-p` first. That way you can check the deployment (gh-pages
branch) locally and then push upstream.

``` console
$ mike deploy 0.7.0 latest
$ mike serve
```

Then deploy it (push it to gh-pages), if you want to update the aliases, for
example to release a new latest. Use the `-u` option when deploying.

``` console
$ mike deploy 0.7.0 latest -p -u
```

**Warning**: after deploying you will get the `site/` folder. There is
no need to commit it since it will be created each time you deploy.

Finally, you should tag it and push it to github so it stays versioned.
Note that you have pushed built documentation, but if you wish to be able
to edit it in the future you need to save its source files.

``` console
$ git tag v0.7.0
$ git push origin v0.7.0
```

#### Editing previous versions of the documentation

As mentioned above, when deploying we do not store the source files. Those
are stored in the git tags. Therefore, to edit previous documentation we
should edit those.

Then delete the old version of the docs and re-deploy:

```console
$ git checkout 0.6.3
$ mike delete 0.6.3 -p
$ # Perform edits, add and commit
$ git tag 0.6.4 # Or delete the old tag to keep it consistent with the InvenioRDM versions
$ mike deploy 0.6.3 -p
```

More docs [here](https://github.com/jimporter/mike).

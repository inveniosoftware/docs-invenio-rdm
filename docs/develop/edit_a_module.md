# Develop or edit a module

Customization might not be enough for you if you are implementing a feature or
fixing a bug. The point is that you need to install a module from a local path
and see the changes reflected on your instance.

If it is a backend change, simply installing the module from the local path
should be enough. In some corner cases, you might have to re-start the
instance (for that run `stop` and `run` again). For frontend (e.g. templates,
css, etc.) you need to symlink and re-build the assets. This can be a complex
process when using webpack, but Invenio-CLI has you covered.

## Templates and CSS

First, you have to install the module you want to edit:

```
invenio-cli ext module-install /path/to/new-module
```

Then you have to clean the assets (`--force` or `-f`), and create symbolic links
(`--development` or `-d`):

```
invenio-cli assets update --development --force
```

Cleaning the assets is required for two reasons, first the
module might have already been installed from upstream and therefore some
links already exist, or these files already exist (as hard copies) if the
installation was not done using the `--development` flag. As you can see, many
things can go wrong, so cleaning the assets is the wise thing to do.

In addition, if you want to modify CSS and see it when reloading the page you
need to *watch* the assets. This will automatically rebuild the webpack bundles
when you change the CSS (`.less`) files. In order to watch them, open another
terminal (still in your instance path i.e. `development-instance/`)
and activate the same virtual environment. Then run:

```
invenio-cli assets watch
```

!!! warning "No hot reloading"
    There is no hot reloading available. This means that even if the assets
    are watched and rebuilt, you need to refresh your browser to see the
    changes. In addition, **be aware of the cache**, it might be a good idea
    to disable your cache or use an incognito window when developing web UI.

This is a continually running operation, so do not close the terminal. You
will be able to see the rebuilding progress there -usually a percentage in the last
line- and the errors in case there were any.

!!! warning "You might see an UnfinishedManifest error"
    Rebuilding the webpack bundles is not a speed-of-light operation, it might
    take a few seconds. If you see an `UnfinishedManifest` error in your
    browser when you refresh, check the terminal to see if the assets are simply still
    building or if build errors (e.g. syntax errors) occurred.

## React modules

In a similar fashion than in the previous section, to develop on a react
module you have to install and watch it. Invenio-CLI has commands for that
too. To install a module run:

```
invenio-cli assets install-module /path/to/react-module
```

Then you have to watch it. Open another terminal in your instance path
(`development-instance/` as before) and activate the same
virtual environment. Note that if you are already watching some python
module, this action is independent (and per module):

```
invenio-cli assets watch-module  /path/to/react-module
```

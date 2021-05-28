# Develop or edit a module

## Backend-only module

If you are working on a backend only module or making a backend only change,
simply installing the module from the local path without building assets should be enough.

```
invenio-cli packages install --skip-build /path/to/module
```

and then re-start the instance.

## Frontend module

For frontend (e.g. templates, css, etc.) you need to symlink and re-build the assets. This can be a complex
process when using webpack, but Invenio-CLI has you covered.

### Templates and CSS

First, you have to install the module you want to edit:

```
invenio-cli packages install /path/to/module
```

and then re-start the instance.

The command takes care of cleaning the assets for you. This is convenient for
two reasons, first the module might have already been installed from upstream and
therefore some links already exist, or these files already exist (as hard copies) if the
installation was not done using the `--development` flag. As you can see, many
things can go wrong, so the added time is worth it.

The command also makes sure that changes to your Jinja templates will automatically be picked up.
That's just Flask auto-reloading feature at work. Make sure you reload your page to see the changes.

If you want to modify CSS and see it when reloading the page you
need to *watch* the assets. This will automatically rebuild the webpack bundles
when you change the CSS (`.less`) files. In order to watch them, open another
terminal (still in your instance path i.e. `development-instance/`). Then run:

```
invenio-cli assets watch
```

!!! warning "No hot reloading"
    There is no hot reloading available. This means that even if the assets
    are watched and rebuilt, you need to refresh your browser to see the
    changes. In addition, **be aware of the cache**, it might be a good idea
    to disable your cache or use an incognito window when developing web UI.

This is a continually running operation, so do not close the terminal. You
will be able to see the rebuilding progress there -usually a percentage on the last
line- and the errors in case there were any.

!!! warning "You might see an UnfinishedManifest error"
    Rebuilding the webpack bundles is not a speed-of-light operation. It might
    take a few seconds. If you see an `UnfinishedManifest` error in your
    browser when you refresh, check the terminal to see whether the assets are
    simply still building or if an actual build error (e.g. syntax error) occurred.

### React modules

In a similar fashion as in the previous section, to develop on a react
module you have to install and watch it. Invenio-CLI has commands for that
too. To install a module run:

```
invenio-cli assets install /path/to/react-module
```

Then you have to watch it. Open another terminal in your instance path
(`development-instance/` as before). Note that if you are already watching some python
module, this action is independent (and per module):

```
invenio-cli assets watch-module --link /path/to/react-module
```

You may have to restart `invenio-cli assets watch`.

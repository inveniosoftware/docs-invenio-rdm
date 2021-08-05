# Change the logo

Having your instance represent your institution starts with using your
institution's logo. We are going to change InvenioRDM's default logo to your logo.

Take an *svg* file and copy it to your **local** static files.
We'll use the [invenio white logo](https://github.com/inveniosoftware/cookiecutter-invenio-rdm/blob/master/%7B%7Bcookiecutter.project_shortname%7D%7D/static/images/logo-invenio-white.svg) as an example:

``` bash
cp static/images/logo-invenio-white.svg static/images/invenio-rdm.svg
```

Then, use the `assets build` command:

``` bash
invenio-cli assets build
```
``` console
# Summarized output
Collecting statics and assets...
Collect static from blueprints.
Created webpack project.
Copying project statics and assets...
Symlinking assets/...
Building assets...
Built webpack project.
```

This command makes sure files you have in `static/`, `assets/`, `templates/` and so on are placed in the right location with other similar files for the application. The files are by default symlinked to ensure future modifications to those files translate directly. No need to run `invenio-cli assets build` again for them.

In the browser, go to [https://127.0.0.1:5000/](https://127.0.0.1:5000) or refresh the page. And voilà! The logo has changed!

!!! warning "That evil cache"
    If you do not see it changing, check in an incognito window; the browser might have cached the logo.

If your logo isn't an svg, you still copy it to `static/images/`, but you need to edit the `invenio.cfg` file appropriately:

```diff
- THEME_LOGO="images/logo.svg"
+ THEME_LOGO="images/my-logo.png"
```

Then, run `assets build` as above and additionally restart the server:

```bash
^C
Stopping server and worker...
Server and worker stopped...
```
```bash
invenio-cli assets build -d
invenio-cli run
```

!!! info "Re-run when invenio.cfg changes"
    All changes to `invenio.cfg` **MUST** be accompanied by a restart like the above to be picked up. This only restarts the server; it does not destroy any data.

This workflow stands for all `static/` files:

- If you add a new file, run `invenio-cli assets build -d`.
- If you modify `invenio.cfg`, re-run `invenio-cli run` (because `invenio.cfg` has been symlinked above, you don't need to run `assets build`).
- If you modify a previously symlinked file, you don't need to do anything.

